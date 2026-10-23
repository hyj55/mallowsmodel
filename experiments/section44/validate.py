"""Read-only verification of S4 provenance, independent draws and summaries."""
import argparse
import gzip
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import numpy as np
import pandas as pd
from experiments.section44.core import digest_array,kendall_fast
from experiments.section44.design import protocol,calibration_cells,confirmation_cells,candidate_grid
from experiments.section44.run import OUTPUT,HERE,sha,code_hashes,data,methods
from experiments.section44.report import interval


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--quick',action='store_true');args=parser.parse_args()
    assert json.loads((OUTPUT/'protocol.json').read_text())==protocol()
    producer=json.loads((OUTPUT/'producer.json').read_text())
    assert producer['signature']['code']==code_hashes()
    assert producer['signature']['protocol']==sha(OUTPUT/'protocol.json')
    selected=json.loads((OUTPUT/'selection.json').read_text())
    assert selected['protocol_sha256']==sha(OUTPUT/'protocol.json')
    assert selected['producer_sha256']==sha(OUTPUT/'producer.json')
    manifest=OUTPUT/'manifest.json'
    if manifest.exists():
        for p,h in json.loads(manifest.read_text())['files'].items():assert sha(HERE/p)==h,p
    scores={};cal={};draws=0
    for phase,cells,B in [(0,calibration_cells(),20),(1,confirmation_cells(),100)]:
        label='calibration' if phase==0 else 'confirmation'
        for index,c in enumerate(cells):
            path=OUTPUT/'draws'/label/(c['id']+'.jsonl.gz')
            with gzip.open(path,'rt') as f:records=[json.loads(line) for line in f]
            assert [r['repeat'] for r in records]==list(range(B))
            for rec in records:
                draws+=1
                assert rec['phase']==phase and rec['index']==index and rec['cell']==c
                assert rec['signature']==producer['signature']
                truth=np.asarray(rec['truth']);assert sorted(truth)==list(range(c['n']))
                assert digest_array(truth)==rec['truth_sha256']
                assert set(rec['models'])=={name for name,_,_ in methods(c,phase,selected)}
                if phase:assert rec['selection_sha256']==sha(OUTPUT/'selection.json')
                if rec['repeat']==0 and (not args.quick or index in (0,len(cells)//2,len(cells)-1)):
                    center,y,seed=data(c,phase,index,0)
                    assert digest_array(y)==rec['reports_sha256'] and np.array_equal(center,truth)
                    assert seed==rec['estimator_seed']
                for method,m in rec['models'].items():
                    if m['status']=='ok':
                        assert sorted(m['order'])==list(range(c['n']))
                        if (method.startswith('efficient') and m.get('depth')==0) or m.get('branch')=='borda_fallback':
                            assert m['order']==rec['models']['borda']['order']
                        if not args.quick or rec['repeat']==0:
                            assert kendall_fast(np.asarray(m['order']),truth)==m['kendall']
                        if m.get('stages'):
                            used=0
                            for stage in m['stages']:
                                assert stage['first_report']==used
                                used+=stage['batch'];assert stage['last_report_exclusive']==used
                            assert used==m['used']<=c['N']//2
                        if m.get('branch')=='exact_sieve':
                            assert m['exact']
                            cfg=m['config'];assert m['W_star']==math.ceil(cfg['c_terminal']*cfg['A']*(c['n']-1)/(c['r']-1))
                            assert all(b['items']<=8*m['W_star'] for b in m['blocks'])
                    else:assert m['order'] is None and m['kendall'] is None
                    if phase:
                        scores.setdefault((c['id'],method),[]).append(m['kendall'])
                    elif '__' in method:
                        family,name=method.split('__',1)
                        cal.setdefault((family,name),[]).append((c,m))
    # Reconstruct the locked selection from calibration receipts, never confirmation.
    for family in ('efficient','sharp'):
        choices=[]
        for (fam,name),fits in cal.items():
            if fam!=family:continue
            complete=all(m['status']=='ok' for c,m in fits)
            active=sum(m.get('depth',0)>0 for c,m in fits)
            sieves=all(m.get('branch')=='exact_sieve' for c,m in fits)
            if complete and active>=len(fits)/2 and (family!='sharp' or sieves):
                risk=float(np.mean([m['kendall']/(c['n']*(c['n']-1)/2) for c,m in fits]))
                choices.append((risk,name))
        risk,name=min(choices)
        assert selected[family]['candidate']==name
        assert abs(selected[family]['normalized_risk']-risk)<1e-14
    summary=pd.read_csv(OUTPUT/'summary.csv')
    for row in summary.itertuples():
        values=scores[(row.cell,row.method)];complete=[x for x in values if x is not None]
        assert len(values)==row.expected==100 and len(complete)==row.complete
        if len(complete)==100:
            stats=interval(complete)
            for field in ('mean','mcse','ci_low','ci_high'):
                assert np.isclose(getattr(row,'kendall_'+field),stats[field],rtol=1e-10,atol=1e-10)
        else:assert pd.isna(row.kendall_mean) and pd.isna(row.kendall_ci_low)
    for row in pd.read_csv(OUTPUT/'paired_comparisons.csv').itertuples():
        a,b=scores[(row.cell,row.method)],scores[(row.cell,row.reference)]
        d=[x-y for x,y in zip(a,b) if x is not None and y is not None]
        assert len(d)==row.complete_pairs
        if len(d)==100:
            stats=interval(d)
            for field in ('mean','mcse','ci_low','ci_high'):
                assert np.isclose(getattr(row,field),stats[field],rtol=1e-10,atol=1e-10)
        else:assert pd.isna(row.mean)
    resources=pd.read_csv(OUTPUT/'resource_profiles.csv')
    assert len(resources)==len(scores)
    assert not resources.duplicated(['cell','method']).any()
    print(f'PASS: {draws} independent draw receipts; {len(scores)} confirmation cells/methods; '
          'seed namespaces, selected constants, fitted orders, data hashes, intervals and resource receipts')


if __name__=='__main__':main()
