"""Run the independent S4 protocol with resumable, hash-locked draw receipts."""
import argparse
from dataclasses import asdict
import gzip
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import numpy as np

from experiments.section44.core import (Calibration, PROOF, coordinates, digest_array,
    direct_sm, fit, kendall_fast, plan)
from experiments.section44.design import (ROOT_SEED, CALIBRATION_REPEATS,
    CONFIRMATION_REPEATS, calibration_cells, confirmation_cells, candidate_grid, protocol)

HERE = Path(__file__).resolve().parent
OUTPUT = HERE/'results'
PRIVATE = ROOT/'results/private/section44'
CODE = ['experiments/section44/'+p for p in ('core.py','design.py','run.py')]+[
    'src/manuscript_estimators.py','src/models.py','src/resource_sieve.py','src/sieve_budget_retry.py']


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def code_hashes():
    return {p:sha(ROOT/p) for p in CODE}


def write_json(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+'\n')


def gzip_write(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_suffix('.tmp')
    with temporary.open('wb') as raw:
        with gzip.GzipFile(fileobj=raw,mode='wb',filename='',mtime=0) as stream:
            stream.write((json.dumps(value,separators=(',',':'),allow_nan=False)+'\n').encode())
    temporary.replace(path)


def clean(x):
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [clean(v) for v in x]
    if isinstance(x,np.ndarray):return x.tolist()
    if isinstance(x,np.generic):return x.item()
    return x


def initialize():
    p=protocol(); path=OUTPUT/'protocol.json'
    if path.exists():
        assert json.loads(path.read_text())==p,'Protocol changed after registration'
    else:write_json(path,p)
    signature=dict(code=code_hashes(),protocol=sha(path))
    stamp=OUTPUT/'producer.json'
    if stamp.exists():
        saved=json.loads(stamp.read_text()); assert saved['signature']==signature,'Producer changed; use a fresh run'
    else:
        write_json(stamp,dict(signature=signature,python=sys.version,platform=platform.platform(),
            numpy=np.__version__,cpu_count=os.cpu_count(),threads={k:os.getenv(k) for k in
            ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS')}))
    return signature


def data(c, phase, index, repeat):
    streams=np.random.SeedSequence([ROOT_SEED,phase,index,repeat]).spawn(3)
    center=np.random.default_rng(streams[0]).permutation(c['n'])
    y=direct_sm(np.random.default_rng(streams[1]),c['N'],c['n'],c['r'],center,c['beta'])
    seed=int(streams[2].generate_state(1)[0])
    return center,y,seed


def methods(c, phase, selected=None):
    rows=[('borda','borda',PROOF)]
    if c['n']<=16:rows.append(('exact_kemeny','exact',PROOF))
    if c['r']==c['n']:
        rows.append(('majority_2_17','majority',PROOF))
        return rows
    if coordinates(c['n'],c['r'],c['N'])['lambda_']>1+1e-12:
        return rows
    if phase==0:
        for name,candidate in candidate_grid().items():
            for family in candidate['families']:
                rows.append((family+'__'+name,family,Calibration(**candidate['config'])))
    else:
        for family in ('efficient','sharp'):
            rows.append((family+'_proof',family,PROOF))
            rows.append((family+'_calibrated',family,Calibration(**selected[family]['config'])))
    return rows


def execute(c,phase,index,repeat,signature,selected):
    path=PRIVATE/('calibration' if phase==0 else 'confirmation')/c['id']/f'{repeat:03}.json.gz'
    if path.exists():
        with gzip.open(path,'rt') as f:rec=json.load(f)
        assert rec['signature']==signature
        if phase:assert rec['selection_sha256']==sha(OUTPUT/'selection.json')
        return rec
    started=time.perf_counter()
    truth,y,seed=data(c,phase,index,repeat)
    generation=time.perf_counter()-started
    count=np.bincount(y.ravel(),minlength=c['n'])
    rec=dict(cell=c,phase=phase,index=index,repeat=repeat,signature=signature,
        selection_sha256=sha(OUTPUT/'selection.json') if phase else None,
        truth=truth.tolist(),truth_sha256=digest_array(truth),reports_sha256=digest_array(y),
        estimator_seed=seed,generation_seconds=generation,input_bytes=y.nbytes,
        coordinates=coordinates(c['n'],c['r'],c['N']),zero_items=int(np.count_nonzero(count==0)),
        min_item_count=int(count.min()),models={})
    for name,family,cfg in methods(c,phase,selected):
        before=time.perf_counter()
        cache=PRIVATE/('packing-'+os.getenv('S4_CACHE_NAMESPACE','default'))
        order,meta=fit(y,c['n'],family,cfg,c['beta0'],seed,cache)
        elapsed=time.perf_counter()-before
        result=dict(meta,seconds=elapsed,order=None if order is None else order.tolist(),
                    kendall=None if order is None else kendall_fast(order,truth))
        if 'pilot_order' in result:
            pilot=np.asarray(result['pilot_order']); delta=np.abs(np.argsort(pilot)-np.argsort(truth))
            W=result['W_star']
            result['pilot_diagnostics']=dict(kendall=kendall_fast(pilot,truth),
                mean_displacement=float(delta.mean()),max_displacement=int(delta.max()),
                fraction_displacement_gt_W=float(np.mean(delta>W)),
                displacement_tail_sum=int(delta[delta>W].sum()))
        rec['models'][name]=clean(result)
    gzip_write(path,rec)
    return rec


def read_records(phase):
    folder=PRIVATE/('calibration' if phase==0 else 'confirmation')
    for path in sorted(folder.glob('*/*.json.gz')):
        with gzip.open(path,'rt') as f:yield json.load(f)


def select():
    records=list(read_records(0))
    assert len(records)==len(calibration_cells())*CALIBRATION_REPEATS
    candidates=candidate_grid(); result={}; table=[]
    for family in ('efficient','sharp'):
        eligible=[]
        for name,c in candidates.items():
            if family not in c['families']:continue
            fits=[(r,r['models'][family+'__'+name]) for r in records]
            complete=sum(f['status']=='ok' for _,f in fits)
            active=sum(f.get('depth',0)>0 for _,f in fits)
            sieves=sum(f.get('branch')=='exact_sieve' and f['status']=='ok' for _,f in fits)
            admissible=complete==len(fits) and active>=len(fits)/2 and (family!='sharp' or sieves==len(fits))
            score=float(np.mean([f['kendall']/(r['cell']['n']*(r['cell']['n']-1)/2)
                       for r,f in fits])) if complete==len(fits) else None
            row=dict(family=family,candidate=name,config=c['config'],comparison=c['comparison'],
                expected=len(fits),complete=complete,active=active,exact_sieve=sieves,
                normalized_risk=score,eligible=admissible)
            table.append(row)
            if admissible:eligible.append(row)
        if not eligible:raise RuntimeError(f'No completed active {family} candidate; do not use confirmation to choose')
        best=min(eligible,key=lambda a:(a['normalized_risk'],a['candidate']))
        result[family]=best
    write_json(OUTPUT/'calibration_candidates.json',table)
    selection=dict(result,calibration_draws=len(records),protocol_sha256=sha(OUTPUT/'protocol.json'),
                   producer_sha256=sha(OUTPUT/'producer.json'))
    path=OUTPUT/'selection.json'
    if path.exists():assert json.loads(path.read_text())==selection
    else:write_json(path,selection)
    print('LOCKED SELECTION',json.dumps(result),flush=True)
    return selection


def preflight():
    rows=[]
    for c in calibration_cells()+confirmation_cells():
        if c['r']==c['n']:continue
        for name,candidate in candidate_grid().items():
            cfg=Calibration(**candidate['config'])
            for family in candidate['families']:
                p=plan(c['n'],c['r'],c['N'],c['beta0'],cfg,family)
                rows.append(dict(cell=c['id'],family=family,candidate=name,
                    status=p['status'],depth=len(p['stages']),pilot_reports=p['used'],
                    eta=p.get('eta'),terminal_cap=p.get('terminal_cap'),
                    W_star=math_ceil(cfg.c_terminal*cfg.A*(c['n']-1)/(c['r']-1))))
    write_json(OUTPUT/'schedule_preflight.json',rows)


def math_ceil(x):
    import math
    return math.ceil(x)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['preflight','calibrate','confirm','select'])
    parser.add_argument('--cell',default=None)
    parser.add_argument('--start',type=int,default=0)
    parser.add_argument('--stop',type=int,default=None)
    parser.add_argument('--shard',type=int,default=0)
    parser.add_argument('--shards',type=int,default=1)
    args=parser.parse_args()
    signature=initialize()
    if args.phase=='preflight':preflight();return
    if args.phase=='select':select();return
    phase=0 if args.phase=='calibrate' else 1
    selected=json.loads((OUTPUT/'selection.json').read_text()) if phase else None
    cells=confirmation_cells() if phase else calibration_cells()
    B=CONFIRMATION_REPEATS if phase else CALIBRATION_REPEATS
    for index,c in enumerate(cells):
        if index%args.shards!=args.shard:continue
        if args.cell and args.cell not in c['id']:continue
        for repeat in range(args.start,min(B,args.stop or B)):
            rec=execute(c,phase,index,repeat,signature,selected)
            if repeat%10==0 or repeat==B-1:
                status={k:v['status'] for k,v in rec['models'].items() if v['status']!='ok'}
                print(args.phase,c['id'],repeat+1,'/',B,'unavailable',status,flush=True)
    if not phase and args.cell is None and args.stop is None:select()


if __name__=='__main__':main()
