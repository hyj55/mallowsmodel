"""Explain saved Sharp/Efficient execution; replay schedules, never fit models.

Public outputs retain fit-level locators and separate recorded from reconstructed
depth. Full stage/candidate plans are deduplicated, not averaged.
"""
import argparse
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import sys

import numpy as np
from src.manuscript_estimators import proof_constants

sys.set_int_max_str_digits(0)
ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'results/estimator_execution'
SOURCES = set()
PLANS = {}
ROWS = []
SNAPSHOT = '89b21645d5f7eb463cc90c4e982c3a66ce805b41'


def digest(b):
    return hashlib.sha256(b).hexdigest()


def read(path):
    path = Path(path)
    if not path.is_absolute():
        path = ROOT / path
    SOURCES.add(str(path.relative_to(ROOT)))
    return gzip.open(path, 'rt') if path.suffix == '.gz' else path.open()


def js(path):
    with read(path) as f:
        return json.load(f)


def lines(path):
    with read(path) as f:
        for line in f:
            yield json.loads(line)


def csvs(path):
    with read(path) as f:
        yield from csv.DictReader(f)


def number(v):
    return None if v in (None, '', 'nan', 'NaN') else float(v)


def integer(v):
    x = number(v)
    return None if x is None else int(x)


def family(method):
    return 'sharp' if 'sharp' in method.lower() else 'efficient'


def first_stage(n, r, N, eta, beta0, cfg):
    c = proof_constants(beta0)
    K = c['K'] if cfg.get('K') is None else cfg['K']
    lam = N*r*(r-1)/(n*(n-1))
    w = max(1, math.ceil(cfg.get('c_width', 1)*(math.sqrt(n/eta)+1/eta)))
    ell = math.log(c['CT'])+math.log(8)+math.log1p(lam*n)
    M = math.ceil(K*eta*ell*n*(n-1)/(r*(r-1)))
    return dict(eta=eta, eta_m0=eta*n, w1=w, cap1=min(n, 8*w), eight_w1=8*w,
                M1=M, ell1=ell, contracts=8*w < n, K=float(K), CT=float(c['CT']))


def schedule(n, r, N, eta, beta0, cfg, early_budget):
    """Original complete schedule or S4's early budget-rejection schedule."""
    c = proof_constants(beta0)
    K = c['K'] if cfg.get('K') is None else cfg['K']
    lam = N*r*(r-1)/(n*(n-1)); m = n; used = 0; stages = []
    while eta*m > cfg['A']:
        w = max(1, math.ceil(cfg['c_width']*(math.sqrt(m/eta)+1/eta)))
        cap = min(m, 8*w)
        if cap >= m:
            return dict(status='noncontracting', eta=eta, used=used, stages=stages,
                        terminal_cap=m, next_width=w)
        ell = math.log(c['CT'])+(len(stages)+1)*math.log(8)+math.log1p(lam*m)
        M = math.ceil(K*eta*ell*n*(n-1)/(r*(r-1)))
        stages.append(dict(m=m, width=w, cap=cap, batch=M)); used += M; m = cap
        if early_budget and used > N//2:
            break
    return dict(status='sample_budget' if used > N//2 else 'feasible', eta=eta,
                used=used, stages=stages, terminal_cap=m)


def make_plan(n, r, N, beta0, cfg, fam, mode):
    key = json.dumps([n, r, N, beta0, cfg, fam, mode], sort_keys=True)
    pid = digest(key.encode())[:16]
    if pid in PLANS:
        return pid, PLANS[pid]
    low = (r-1)/(n-1); lam = N*r*(r-1)/(n*(n-1))
    initial = low if fam == 'sharp' else min(lam, 1.) if mode == 'capped' else lam
    candidates = []
    if fam == 'sharp':
        candidates = [low]
    else:
        eta = initial
        while eta >= low:
            candidates.append(eta); eta /= 2
        if N*r/n >= 1 and (not candidates or candidates[-1] != low):
            candidates.append(low)
    attempts = []
    for eta in candidates:
        p = schedule(n, r, N, eta, beta0, cfg, mode == 's4')
        attempts.append(p)
        if p['status'] == 'feasible':
            break
    chosen = attempts[-1] if attempts and attempts[-1]['status'] == 'feasible' else None
    plan = dict(n=n, r=r, N=N, beta0=beta0, config=cfg, family=fam, mode=mode,
                alpha=low, lambda_=lam, mu=N*r/n, first=first_stage(n,r,N,initial,beta0,cfg),
                attempts=attempts, chosen=chosen)
    PLANS[pid] = plan
    return pid, plan


GATES = {
    'outside_lambda_domain': 'Not run: S4 admission requires lambda <= 1.',
    'outside_schedule_domain': 'Not run: Efficient requires lambda <= 1.',
    'excluded_outside_theorem_regime': 'Not run: G1 admission requires lambda <= 1.',
    'unseen_catalog_items': 'Not run: G1 requires every catalogue item to appear in training.',
    'sharp_available': 'Not run: this curve invokes Efficient only when Sharp is unavailable.',
    'sharp_available_no_fallback_needed': 'Not run: G1 reserves Efficient for larger catalogues.',
    'excluded_upstream_response_filtering': 'Not fit: source screening excluded this task.',
}


def add(study, dataset, setting, rep, method, n, r, N, model, source,
        beta0=.1, cfg=None, mode='original', gate_sieve=False, depth_basis='saved',
        phase='final', locator='', extra=None):
    cfg = dict(A=256., c_width=1., K=None, c_terminal=8.) if cfg is None else cfg
    meta = model.get('metadata', model)
    status = model.get('status', 'ok'); branch = meta.get('branch', '')
    recorded_depth = integer(meta.get('depth'))
    row = dict(study=study, dataset=dataset, setting=setting, phase=phase, repeat=rep,
               method=method, n=n, r=r, N=N, source=source, locator=locator,
               status=status, branch=branch, recorded_depth=recorded_depth,
               beta0=beta0, A=cfg['A'], c_width=cfg['c_width'], c_terminal=cfg['c_terminal'])
    row['fit_id'] = digest(json.dumps([study,dataset,setting,phase,rep,method,n,r,N,source,locator],sort_keys=True).encode())[:16]
    if N is None:
        row.update(reason=GATES.get(status, status), actual_depth=None, depth_basis='not applicable',
                   attention=True, reason_code=status)
        ROWS.append(row); return
    n,r,N = int(n),int(r),int(N)
    pid,p = make_plan(n,r,N,beta0,cfg,family(method),mode)
    f=p['first']; chosen=p['chosen']; gate=status in GATES or gate_sieve
    reason=[]; code=[]
    row.update(plan_id=pid, m0=n, half_sample=N//2, lambda_=p['lambda_'], mu=p['mu'], alpha=p['alpha'],
               eta_initial=f['eta'], eta_selected=None if gate or chosen is None else chosen['eta'],
               eta_initial_m0=f['eta_m0'], w1=f['w1'], eight_w1=f['eight_w1'], cap1=f['cap1'],
               M1=f['M1'], K=f['K'], CT=f['CT'], initial_contracts=f['contracts'],
               candidate_count=len(p['attempts']), W_star=math.ceil(cfg['c_terminal']*cfg['A']/p['alpha'])
               if family(method)=='sharp' else None)
    if gate:
        actual=None; reason.append('Not run: G1 item-count guard requires n <= 8.' if gate_sieve else GATES[status])
        code.append('n8_admission_guard' if gate_sieve else status)
        basis='not attempted'; row['parameter_role']='counterfactual; admission gate prevented scheduling'
    else:
        actual=0 if chosen is None or branch=='borda_fallback' else len(chosen['stages'])
        basis=depth_basis if recorded_depth is not None or depth_basis!='saved' else 'reconstructed from producer schedule'
        if recorded_depth is not None:
            assert recorded_depth==actual,(study,dataset,method,recorded_depth,actual)
        if chosen is None:
            failures=sorted({a['status'] for a in p['attempts']})
            if not p['attempts']:
                code.append('no_admissible_eta');reason.append('Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution.')
            else:
                code.append('+'.join(failures));reason.append('Global Borda fallback: no feasible schedule; candidate failures: '+', '.join(failures)+'.')
        elif actual==0:
            code.append('root_A_stop')
            reason.append('Zero pilot stages: selected eta*m0 <= A; the root is terminal.')
            if len(p['attempts'])>1:
                code.append('earlier_candidates_rejected');reason.append('Higher resolutions rejected: '+', '.join(sorted({a['status'] for a in p['attempts'][:-1]}))+'.')
            reason.append('Terminal global Borda is still computed.' if family(method)=='efficient' else 'Terminal pair-sieve is still required.')
        else:
            code.append('positive_depth');reason.append('Hierarchy executed '+str(actual)+' stages.')
        if status=='exact_sieve_unavailable':
            code.append('n8_terminal_guard');reason.append('Terminal sieve unavailable: this producer limits exact blocks to 8 items; the root block has '+str(n)+'.')
        elif status!='ok':
            code.append(status);reason.append('Terminal result unavailable: '+status+'.')
        row['parameter_role']='initial candidate; schedule evaluated but no pilot reports consumed' if branch=='borda_fallback' else ('hypothetical first stage; root stopped before it' if actual==0 else 'initial candidate; see selected resolution and full schedule')
    if mode=='capped' and p['lambda_']>1:
        reason.append('Producer uses eta=min(lambda,1): an outside-domain extension, not the admitted Algorithm 3.1.')
        code.append('capped_lambda_extension')
    if chosen is not None and not gate:
        sf=first_stage(n,r,N,chosen['eta'],beta0,cfg)
        row.update(selected_w1=sf['w1'], selected_M1=sf['M1'], selected_eta_m0=sf['eta_m0'],
                   planned_depth=len(chosen['stages']), planned_pilot_reports=chosen['used'])
    else:
        row.update(planned_depth=None, planned_pilot_reports=None)
    row.update(actual_depth=actual, depth_basis=basis, reason=' '.join(reason), reason_code=';'.join(code),
               used_pilot_reports=meta.get('pilot_reports',meta.get('used',0 if actual==0 else None)),
               attention=actual in (None,0) or status!='ok')
    if 'schedule' in meta and not gate:
        saved=meta['schedule']
        assert [a['status'] for a in saved.get('candidates',[])]==[a['status'] for a in p['attempts']], (dataset,method)
        assert [a['used'] for a in saved.get('candidates',[])]==[a['used'] for a in p['attempts']], (dataset,method)
        if saved.get('stages'):
            expected=p['attempts'][-1]['stages']
            assert [(s['width'],s['cap'],s['batch']) for s in saved['stages']]==[(s['width'],s['cap'],s['batch']) for s in expected],(dataset,method)
    if meta.get('eta') is not None and not gate:
        assert chosen is not None and math.isclose(meta['eta'],chosen['eta'],rel_tol=1e-14),(dataset,method)
    if meta.get('W_star') is not None:
        assert row['W_star']==meta['W_star'],(dataset,method,'terminal width')
    resource=meta.get('failed_block',meta.get('resource',meta.get('failure',meta))) if status in ('resource_limit','sieve_resource_budget') else {}
    if not isinstance(resource,dict):resource=meta
    for k in ['reason','estimated_bytes','memory_bytes','seconds_limit','m','pairs','radius','path']:
        v=resource.get(k)
        if v is not None:row['resource_'+k]=v
    row['pilot_terminal_block_max']=meta.get('terminal_max_items') if family(method)=='sharp' else None
    sizes=[b.get('items',b.get('m')) for b in meta.get('blocks',[]) if isinstance(b,dict)]
    sizes=[s for s in sizes if s is not None]
    if family(method)=='sharp':
        row['terminal_block_items']=resource.get('items',resource.get('m',meta.get('actual_block_items',max(sizes) if sizes else None)))
    else:
        row['terminal_block_items']=meta.get('terminal_max_items',n if actual==0 and not gate else None)
    if status=='exact_sieve_unavailable':row['terminal_block_items']=n
    if family(method)=='sharp' and actual==0 and not gate and row['terminal_block_items'] is None and (branch=='borda_fallback' or row['W_star']>=n):
        row['terminal_block_items']=n
    if resource.get('reason'):
        row['reason']+=' Resource receipt: '+str(resource['reason'])+'.'
    if extra:row.update(extra)
    ROWS.append(row)


def current_predictors():
    for path in ['results/estimator_comparison/predictors.jsonl.gz','results/predictive/predictors.jsonl.gz']:
        for a in lines(path):
            if a['study']=='P0':continue # E0 above is the independent admission table.
            for m,fit in a['models'].items():
                if 'sharp' not in m and 'efficient' not in m:continue
                add(a['study'],a['dataset'],'',a['repeat'],m,a['n'],a['r'],a['N'],fit,path)


def strict_tables():
    path='results/repeated_holdout/repeat_scores.csv.gz'
    for a in csvs(path):
        if a['method'] not in ['sharp','efficient'] or a['split']!='confirmation':continue
        add('P1',a['dataset'],'',a['repeat'],a['method'],int(a['n']),int(a['r']),int(a['n_train']),a,path)
    dims={a['dataset']:a for a in csvs('results/strict_features/real_datasets.csv')}
    for ds,models in js('results/strict_features/real_parameters.json').items():
        d=dims[ds]
        for m in ['sharp','efficient']:
            add('P2',ds,'strict real',0,m,int(d['n']),int(d['r']),int(d['N']),models[m],'results/strict_features/real_parameters.json')
    dims={a['dataset']:a for a in js('results/baseline_replacement/datasets.json')}
    for ds,models in js('results/baseline_replacement/parameters.json').items():
        d=dims[ds]
        for m in ['sharp','efficient']:
            add('P2',ds,'baseline',0,m,d['items'],d['r'],d['N_train'],models[m],'results/baseline_replacement/parameters.json')
    d=js('results/context_followup/coverage.json');models=js('results/context_followup/parameters.json')['models']
    for m in ['sharp','efficient']:
        add('P2','wheat','context',0,m,d['n'],d['r'],d['N'],models[m],'results/context_followup/parameters.json')
    dims={a['dataset']:a for a in csvs('results/validation_extension/real_datasets.csv')}
    for ds,models in js('results/validation_extension/real_parameters.json').items():
        d=dims[ds]
        for m in ['sharp','efficient']:
            add('P2',ds,'validation real',0,m,integer(d['n']),integer(d['r']),integer(d['N']),models[m],'results/validation_extension/real_parameters.json')
    for m in ['sharp','efficient']:
        add('P2','beach_preferences','screening',0,m,15,2,None,dict(status='excluded_upstream_response_filtering'),'results/validation_extension/real_datasets.csv')
    for part in ['bridge','shell','coverage']:
        path=f'results/strict_features/{part}_replicates.csv'
        for a in csvs(path):
            if a['method'] not in ['sharp','efficient']:continue
            setting='; '.join(f'{k}={a[k]}' for k in ['family','value','shape'] if a.get(k) not in ('','nan',None))
            add('S1' if part=='bridge' else 'S2',part+' cell '+a['cell'],setting,a['rep'],a['method'],int(a['n']),int(a['r']),int(a['N']),a,path,beta0=.8)
    path='results/estimator_execution/inputs/group_fit_receipts.csv.gz'
    for a in csvs(path):
        n,r=(12,2) if a['dataset']=='sounds' else (4,4)
        setting=f"{a['design']}; {a['percent']}%; {a['scheme']}"
        add('G1',a['dataset'],setting,a['repeat'],a['method'],n,r,int(a['n_train']),a,path,
            gate_sieve=a['status']=='exact_sieve_unavailable',locator='group='+a['group'],extra={'group':a['group']})


def snapshot():
    prefix='results/estimator_execution/inputs/'
    for part in ['small','coverage']:
        path=prefix+'snapshot_'+part+'_replicates.csv.gz'
        for a in csvs(path):
            if a['method'] not in ['sharp','efficient']:continue
            n,r,N=map(int,[a['n'],a['r'],a['N']])
            add('S3',part+' '+a['dgp'],'',a['rep'],a['method'],n,r,N,a,path,beta0=.8,mode='capped',locator='seed='+a['seed'])
            if N>=5:
                add('S3',part+' '+a['dgp'],'',a['rep'],a['method'],n,r,int(.8*N),dict(status='ok'),path,
                    beta0=.8,mode='capped',phase='inner dispersion tuning',depth_basis='reconstructed; inner metadata not retained',locator='outer_N='+str(N)+'; seed='+a['seed'])
    params=js(prefix+'snapshot_real_parameters.json.gz')
    path=prefix+'snapshot_real_replicates.csv.gz'
    for a in csvs(path):
        if a['method']!='efficient':continue # Shrinkage shares the same center.
        n,r,N=map(int,[a['n'],a['r'],a['N']]);key=f"{a['dataset']}_{a['rep']}_{N}"
        fit=dict(status='ok',metadata=params[key]['efficient']['metadata'])
        add('L2',a['dataset'],'',a['rep'],'efficient',n,r,N,fit,path,beta0=.8,mode='capped')
        if N>=5:
            add('L2',a['dataset'],'',a['rep'],'efficient',n,r,int(.8*N),dict(status='ok'),path,
                beta0=.8,mode='capped',phase='inner dispersion tuning',depth_basis='reconstructed; inner metadata not retained',locator='outer_N='+str(N))
    params=js(prefix+'snapshot_tennis_parameters.json.gz')
    path=prefix+'snapshot_tennis_by_year.csv.gz'
    for a in csvs(path):
        if a['method']!='efficient' or a['target']!='all_catalog':continue
        n,r,N=map(int,[a['n'],a['r'],a['N']])
        add('T1','ATP '+a['year'],'chronological',0,'efficient',n,r,N,
            dict(status='ok',metadata=params[a['year']]['efficient']['metadata']),path,beta0=.8,mode='capped')


def section44():
    cells={}; configs={}
    for phase in ['calibration','confirmation']:
        for file in sorted((ROOT/f'experiments/section44/results/draws/{phase}').glob('*.jsonl.gz')):
            path=str(file.relative_to(ROOT))
            for a in lines(path):
                d=a['cell'];cells[d['id']]=d
                for method,fit in a['models'].items():
                    if not method.startswith(('sharp','efficient')):continue
                    configs[(d['id'],method)]=fit['config']
                    add('S4-'+phase,d['id'],'',a['repeat'],method,d['n'],d['r'],d['N'],fit,path,
                        beta0=d['beta0'],cfg=fit['config'],mode='s4')
    path='experiments/section44/results/resource_profiles.csv'
    for a in csvs(path):
        if not a['method'].startswith(('sharp','efficient')):continue
        d=cells[a['cell']]
        add('S4-resources',a['cell'],'fresh-process profile',a['repeat'],a['method'],d['n'],d['r'],d['N'],a,path,
            beta0=d['beta0'],cfg=configs[(d['id'],a['method'])],mode='s4',extra={'profile_resource_limits':a['resource_limits']})


def tuned():
    path='results/tuned_block_sieve/models.jsonl.gz'
    for a in lines(path):
        for phase,key,N in [('validation candidate','candidates',a['train_count']),('development refit','refits',a['N'])]:
            for j,c in enumerate(a[key]):
                meta=c['model']['metadata'];bad=meta.get('failed_block',{})
                row=dict(study='Tuned-block',dataset=a['dataset'],setting=a['case'],phase=phase,repeat=a['repeat'],method='borda_block_sieve',
                         n=a['n'],r=a['r'],N=N,m0=a['n'],requested_blocks=c['blocks'],
                         status=c['status'],source=path,locator=f'{key}[{j}]',actual_depth=None,recorded_depth=None,
                         depth_basis='not defined for this variant',attention=True,used_pilot_reports=meta.get('pilot_reports'),
                         terminal_reports=meta.get('terminal_reports'),terminal_block_items=bad.get('m',max((x['m'] for x in meta.get('blocks',[])),default=None)),
                         resource_reason=meta.get('reason'),resource_estimated_bytes=meta.get('estimated_bytes'),resource_memory_bytes=meta.get('memory_bytes'),
                         resource_seconds_limit=meta.get('seconds_limit'),resource_pairs=bad.get('pairs'),
                         reason_code='fixed_borda_pilot'+(';' + c['status'] if c['status']!='ok' else ''),
                         reason='This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. '+('Candidate/refit completed.' if c['status']=='ok' else 'Exact block sieve stopped: '+str(meta.get('reason',c['status']))+'.'))
                row['fit_id']=digest(json.dumps([a['case'],phase,j],sort_keys=True).encode())[:16];ROWS.append(row)
        m='sm_efficient_fallback';fit=a['models'][m]
        add('Tuned-reference',a['dataset'],a['case'],a['repeat'],m,a['n'],a['r'],a['N'],fit,path,phase='saved reference')


def compressed(b):
    f=io.BytesIO()
    with gzip.GzipFile(fileobj=f,mode='wb',filename='',mtime=0) as z:z.write(b)
    return f.getvalue()


def csv_bytes(rows):
    fields=list(dict.fromkeys(k for row in rows for k in row))
    f=io.StringIO();w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
    return f.getvalue().encode()


def fmt(x):
    if x is None or x=='':return 'NA'
    if isinstance(x,bool):return 'yes' if x else 'no'
    if isinstance(x,float):return str(int(x)) if x.is_integer() else f'{x:.7g}'
    if isinstance(x,int) and len(str(abs(x)))>16:
        s=str(x);return s[0]+'.'+s[1:5]+'e'+str(len(s)-1)
    return str(x).replace('|','/').replace('\n',' ')


def span(rows,k):
    vals={str(x[k]):x[k] for x in rows if x.get(k) not in ('',None)}
    if not vals:return None
    values=list(vals.values())
    if len(values)==1:return fmt(values[0])
    if all(isinstance(v,(int,float)) for v in values):return fmt(min(values))+' to '+fmt(max(values))
    return ', '.join(sorted(map(fmt,values)))


def table(rows,cols):
    return '\n'.join(['| '+' | '.join(t for k,t in cols)+' |','|'+'|'.join('---' for _ in cols)+'|']+
                     ['| '+' | '.join(fmt(row.get(k)) for k,t in cols)+' |' for row in rows])+'\n'


def outputs():
    ROWS.clear();PLANS.clear();SOURCES.clear()
    source_manifest=js('results/estimator_execution/inputs/sources.json')
    for a in source_manifest:
        assert digest((ROOT/a['input']).read_bytes())==a['sha256'],a['input']
    current_predictors();strict_tables();snapshot();section44();tuned()
    assert len({x['fit_id'] for x in ROWS})==len(ROWS),'Duplicate contexts'
    for study in ['E0','P1']:
        subset=[r for r in ROWS if r['study']==study]
        assert len(subset)==230 and len({r['dataset'] for r in subset})==23,study
    for phase in ['calibration','confirmation']:
        expected={(a['cell'],int(a['repeat']),a['method'],a['status'],integer(a['depth']))
                  for a in csvs(f'experiments/section44/results/{phase}_fits.csv.gz')
                  if a['method'].startswith(('sharp','efficient'))}
        actual={(a['dataset'],int(a['repeat']),a['method'],a['status'],a['recorded_depth'])
                for a in ROWS if a['study']=='S4-'+phase}
        assert expected==actual,('S4 receipt/export coverage',phase)
    group_keys=['dataset','design','percent','scheme','method','status']
    expected={tuple(a[k] for k in group_keys):int(a['fit_contexts'])
              for a in csvs('results/group_sensitivity/eligibility.csv')
              if a['method'] in ['sm_sharp','sm_efficient']}
    actual=Counter(tuple(a[k] for k in group_keys)
                   for a in csvs('results/estimator_execution/inputs/group_fit_receipts.csv.gz'))
    assert dict(actual)==expected,'G1 receipt/eligibility coverage'
    result={};out=lambda name,b:result.__setitem__('results/estimator_execution/'+name,b.encode() if isinstance(b,str) else b)
    out('fits.csv.gz',compressed(csv_bytes(ROWS)))
    out('plans.jsonl.gz',compressed((''.join(json.dumps(dict(plan_id=k,**v),sort_keys=True)+'\n' for k,v in sorted(PLANS.items()))).encode()))
    studies=sorted({r['study'] for r in ROWS});overview=[]
    for study in studies:
        allrows=[r for r in ROWS if r['study']==study];selected=[r for r in allrows if r['attention']]
        grouped=defaultdict(list)
        for r in selected:
            key=tuple(r.get(k) for k in ['dataset','setting','phase','method','n','r','N','plan_id','actual_depth','reason','requested_blocks'])
            grouped[key].append(r)
        groups=[]
        for i,(_,rr) in enumerate(sorted(grouped.items(),key=lambda a:str(a[0]))):
            row=dict(rr[0],group_id=f'{study}-{i+1}',contexts=len(rr))
            for k in ['terminal_block_items','resource_estimated_bytes','resource_memory_bytes','resource_seconds_limit','resource_reason','resource_pairs','used_pilot_reports']:
                row[k]=span(rr,k)
            row['context_label']=row['dataset']+(' / '+row['setting'] if row['setting'] else '')
            groups.append(row)
        overview.append(dict(study=study,contexts=len(allrows),attention=len(selected),groups=len(groups),
                             positive=sum(r.get('actual_depth',0) is not None and r['actual_depth']>0 and r['status']=='ok' for r in allrows)))
        text=f'# {study}: Sharp/Efficient execution audit\n\n[Definitions and coverage](README.md) · [Every fit receipt](fits.csv.gz) · [Complete candidate/stage schedules](plans.jsonl.gz)\n\n'
        text+=f'{len(allrows)} recorded or explicitly reconstructed contexts; {len(selected)} have zero pilot depth, an admission exclusion, a fallback, an unavailable result, or a variant without hierarchical depth. They form {len(groups)} rows below. Identical parameter/reason rows are grouped across repetitions and, for G1, across anonymous group keys; no parameters are averaged. Fit-level group/repetition/source locators remain in the CSV. Positive-depth successful contexts remain in the CSV as coverage controls.\n\n'
        text+='**Read the tables together by row ID.** `w1, M1` refer to the initial candidate at `m0=n`; they are formula diagnostics, **not** evidence that a stage ran. For a stopped or excluded fit they are counterfactual. `eta selected` can differ after rejected candidate schedules; its first-stage values and every failed candidate are in the CSV/plan archive. `M1` is reports required for that round, while `N` is the actual fitting sample, not total dataset size. Resource numbers are saved estimates/limits, not measured RAM usage. `NA` means not applicable or not recorded, never zero.\n\n'
        text+='## Why the fit stopped or did not run\n\n'
        text+=table(groups,[('group_id','ID'),('context_label','Dataset / setting'),('phase','Fit phase'),('method','Estimator / configuration'),('contexts','Contexts'),('actual_depth','Executed depth'),('depth_basis','Depth evidence'),('status','Saved status'),('reason','Explanation')])
        text+='\n## Initial geometry and sample requirement\n\n'
        text+=table(groups,[('group_id','ID'),('n','n = m0'),('r','r'),('N','N'),('lambda_','lambda'),('A','A'),('eta_initial','eta initial'),('eta_selected','eta selected'),('w1','w1'),('eight_w1','8w1'),('M1','M1'),('half_sample','floor(N/2)'),('W_star','W*')])
        text+='\n## Constants and selected-resolution checks\n\nThe first table uses the initial resolution. This table exposes the resolution ultimately selected and the constants used to calculate each budget. A selected-resolution first round remains hypothetical when the root stops.\n\n'
        text+=table(groups,[('group_id','ID'),('beta0','beta0'),('c_width','cW'),('c_terminal','c terminal'),('K','K'),('CT','CT'),('eta_initial_m0','Initial eta*m0'),('selected_eta_m0','Selected eta*m0'),('selected_w1','Selected w1'),('selected_M1','Selected M1'),('initial_contracts','Initial 8w1 < m0')])
        resources=[g for g in groups if g.get('terminal_block_items') is not None or g.get('resource_reason') is not None]
        if resources:
            text+='\n## Terminal blocks and resource receipts\n\nRanges show different saved repetitions in the same row; exact integers and individual receipts are in the CSV. Formula W* can exceed n; the actual terminal block is clipped by the available items. A large W* is not itself a memory-allocation count.\n\n'
            text+=table(resources,[('group_id','ID'),('used_pilot_reports','Consumed pilot reports'),('requested_blocks','Requested blocks (variant)'),('terminal_block_items','Actual terminal / failed block items'),('resource_reason','Resource reason'),('resource_pairs','Pairs in failed block'),('resource_estimated_bytes','Estimated bytes'),('resource_memory_bytes','Memory limit bytes'),('resource_seconds_limit','Time limit seconds')])
        out(study+'.md',text)
        counts=Counter(r['reason_code'] for r in allrows)
        short=f'## Sharp/Efficient execution and stopping\n\n[Per-setting reasons and first-round parameters](../{study}.md) distinguish actual depth from a missing or unattempted fit. Counts below are fit contexts, not independent datasets. No predictor is refitted for this audit.\n\n'
        short+=table([dict(reason=k,count=v) for k,v in sorted(counts.items())],[('reason','Execution category'),('count','Contexts')])
        out('snippets/'+study+'.md',short)
    out('overview.csv',csv_bytes(overview))
    intro=GUIDE+'\n'+table([dict(x,study=f"[{x['study']}]({x['study']}.md)") for x in overview],[('study','Result family'),('contexts','Contexts'),('attention','Audited zero/excluded/fallback/unavailable'),('groups','Parameter rows'),('positive','Successful positive-depth contexts')])
    out('README.md',intro)
    manifest=dict(producer='build_estimator_execution.py',producer_sha256=digest(Path(__file__).read_bytes()),
                  no_model_fits=True,no_new_splits=True,fit_contexts=len(ROWS),plans=len(PLANS),
                  inputs={p:digest((ROOT/p).read_bytes()) for p in sorted(SOURCES|{'src/manuscript_estimators.py'})},
                  outputs={p:digest(b) for p,b in result.items()})
    out('manifest.json',json.dumps(manifest,indent=2)+'\n')
    return result


GUIDE=r'''# Sharp and Efficient: execution, depth and stopping reasons

[Results map](../README.md) · [Estimator definitions](../../docs/algorithms.md) · [S4](../../experiments/section44/README.md)

This is an audit of the saved experiments, not a new experiment. It does not change an estimator, fit, train/test split, loss, confidence interval or computation budget. Every table separates **normal root stopping**, **global-Borda fallback**, **admission exclusions**, and **terminal-sieve failures**. Depth zero is not a failure by itself. An unattempted fit has depth NA, not zero.

## Reading a row

- `n`: full catalogue size; `r`: items in each report; `N`: reports supplied to this particular fit. Inner fits use their own smaller N. G1 fits use their own group training size.
- `m0=n`: initial schedule cap. Later `m` is a block-size cap, not the number of reports. `M1` is the first-round report budget; `floor(N/2)` is the producer's pilot budget limit.
- `alpha=(r-1)/(n-1)`, `lambda=N*r*(r-1)/(n*(n-1))`, `mu=N*r/n`. Sharp starts at eta=alpha. Efficient searches a decreasing sequence starting at lambda (the explicitly identified exposure producer starts at min(lambda,1)).
- The recorded depth is preserved separately from executed/reconstructed depth. Formula reconstruction is identified in `depth_basis`. A gated method never acquires an invented execution depth. Full-data feature computations and MLE/PL fits do not acquire Sharp/Efficient labels.
- When a root already satisfies eta*m0 <= A, **no first pilot round is executed**. Its w1 and M1 are counterfactual formula diagnostics. Efficient still scores the whole catalogue using global clipped Borda. Sharp still attempts its terminal pair-sieve; its pilot is not an additional global-Borda fit.
- If an Efficient resolution is rejected, a smaller resolution can be chosen. Initial and selected eta are both shown. The exact selected w1/M1 and every attempted stage (m, width, cap, batch) are in the CSV and plan archive. A failed complete schedule may exceed the budget in round two even when M1 alone fits.
- Resource limits and estimates come from receipts. Blank limits were not retained; they are not unlimited budgets. A fitted center with infinite unpenalized dispersion is not an algorithm execution failure; this audit uses center status rather than silently relabeling a nonfinite held-out loss.

## Formulas and meanings

With the configuration's width coefficient cW (normally 1), the first-round diagnostics are

```math
w_1=\left\lceil c_W\left(\sqrt{n/\eta}+1/\eta\right)\right\rceil,\qquad
m_1=\min(n,8w_1),\qquad
M_1=\left\lceil K\eta\{\log C_T+\log8+\log(1+\lambda n)\}\frac{n(n-1)}{r(r-1)}\right\rceil.
```

S4 clamps w1 to at least 1. With rho=tanh(beta0/2), c*=2+2048/beta0^2, t*=min(1/8,beta0/64), b0=min(1/(8c*),t*/8), the proof configuration uses K=max(8,4/(b0*rho^2)) and CT=12/rho. S4 can explicitly replace K, cW, A and the terminal coefficient. The exact constants used are stored per plan. Sharp's terminal width is W*=ceil(c_terminal*A/alpha), normally c_terminal=8; it is distinct from the pilot w1. Padding gives an upper cap 8W*, clipped by actual items. The tuned disjoint-block variant has neither this W* nor this hierarchical depth.

The A test is the producer's stopping rule, not a statement that A is the only possible obstruction. `8w1 >= m0` is a separate geometry check. `M1 > floor(N/2)` is an immediate budget obstruction only for a round the schedule actually proposes; a counterfactual large M1 cannot be called the cause of a root A-stop.

## Coverage and provenance

E0 includes the independently assessed Efficient result for every empirical allocation. P0 contains only the main likelihood-center SM/PL comparison and needs no Sharp/Efficient table. B0 is the global-sieve alias of E0 Sharp, and L0's N=4000 endpoint reuses E0; aliases do not add fits. L0/S0 retain their actual conditional Efficient-fallback policy. D1 reuses S1/S2 model fits. D2, L1 and the C1 center benchmark contain no literal Sharp/Efficient fits; a standalone Borda or insertion method is not renamed Efficient.

P2 covers all fixed-allocation sources, plus the explicit Beaches screening exclusion. G1's public receipt projection contains every Sharp/Efficient fit context at repetition IDs 0–4, including each group and equal-budget control, without report indices or participant identities. The inputs manifest identifies the originating receipts. G1's unseen-item, lambda and item-count gates are study-specific admission rules, not universal impossibility claims about the estimator.

S3 exposure, L2 and T1 retain their recorded producer from the [implementation snapshot](https://github.com/hyj55/mallowsmodel/tree/89b21645d5f7eb463cc90c4e982c3a66ce805b41). That producer caps Efficient's initial resolution at 1 even for lambda>1. Those executed extension fits are explicitly distinguished from the outside-domain exclusions in other studies. L2/S3 inner dispersion-selection schedules use the runner's documented floor(0.8N), and are reconstructed, not saved inner-fit receipts. Their shrunk predictions reuse the same center and are not counted again. Insertion's deterministic Efficient starting order reuses the same schedule; it is not an additional estimator comparison. T1's final yearly fit parameters are available, but its inner chronological sample counts and inner center metadata are not retained in the linked receipts; their exact first-round parameters are unavailable and are not guessed. The separate schedule-feasibility CSV in the snapshot is a theoretical preflight, not a fitted dataset or an observed depth.

S4 calibration, confirmation and fresh-process resource profiles have separate tables. Resource profiles rerun existing datasets and are not independent simulation repetitions. Proof and calibrated configurations remain separate. The Borda-pilot tuned block-sieve table includes every validation candidate and development refit, including unsuccessful candidates; its Efficient reference table identifies reused predictors.

The [CSV](fits.csv.gz) is the fit-level index with source locators and exact numeric values. [Plans](plans.jsonl.gz) contain all attempted resolutions and stages without storing ranks or losses. [Inputs](inputs/sources.json) identify immutable snapshot blobs and sanitized G1 receipts. Decimal display rounding and resource ranges apply only to Markdown; no averaging changes schedule parameters. Rebuild or verify with `python build_estimator_execution.py` or `python build_estimator_execution.py --check`. Neither runs a scientific fit. The verifier checks every published byte against its manifest; schedule replay allows relative/absolute tolerance 1e-14 only for floating-point fields (such as logarithms), while integer widths, report budgets, depths, branches and status decisions must agree exactly across platforms.

## Tables by result family
'''


def compare_plan_values(saved, replayed, path='plan'):
    """Keep integer decisions exact; libm logarithms may differ by an ulp."""
    assert type(saved) is type(replayed),(path,type(saved),type(replayed))
    if isinstance(saved,dict):
        assert saved.keys()==replayed.keys(),path
        for k in saved:compare_plan_values(saved[k],replayed[k],path+'.'+k)
    elif isinstance(saved,list):
        assert len(saved)==len(replayed),path
        for i,(a,b) in enumerate(zip(saved,replayed)):compare_plan_values(a,b,path+f'[{i}]')
    elif isinstance(saved,float):
        assert math.isclose(saved,replayed,rel_tol=1e-14,abs_tol=1e-14),(path,saved,replayed)
    else:
        assert saved==replayed,(path,saved,replayed)


def build(check=False):
    result=outputs()
    if check:
        stored=json.loads((OUT/'manifest.json').read_text())
        for p,h in stored['outputs'].items():assert digest((ROOT/p).read_bytes())==h,p
        plan_path='results/estimator_execution/plans.jsonl.gz'
        saved=[json.loads(line) for line in gzip.decompress((ROOT/plan_path).read_bytes()).splitlines()]
        replayed=[json.loads(line) for line in gzip.decompress(result[plan_path]).splitlines()]
        compare_plan_values(saved,replayed)
        # The archived bytes remain authoritative after a numerically equivalent replay.
        result[plan_path]=(ROOT/plan_path).read_bytes()
        manifest_path='results/estimator_execution/manifest.json'
        expected=json.loads(result[manifest_path]);expected['outputs'][plan_path]=stored['outputs'][plan_path]
        result[manifest_path]=(json.dumps(expected,indent=2)+'\n').encode()
    for p,b in result.items():
        file=ROOT/p
        if check:assert file.read_bytes()==b,p
        else:file.parent.mkdir(parents=True,exist_ok=True);file.write_bytes(b)
    print(('Verified' if check else 'Built')+f' {len(result)} artifacts; {len(ROWS)} contexts; {len(PLANS)} unique schedules')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true')
    build(parser.parse_args().check)
