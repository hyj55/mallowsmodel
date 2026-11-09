"""Derive held-out Kendall distances from the exact NLL evaluation objects.

No scientific refit, test selection, new split or changed center is introduced.
Source adapters assert agreement with recorded NLL before exporting new scores.
"""
import argparse
from collections import defaultdict
import csv
import gzip
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np
import pandas as pd
from src.heldout_kendall import report_loss, beta_audit, mean_nll
from src.models import distances
from src.repeated_holdout import load_tasks, split_task
from src.predictive_study import empirical_context, synthetic_context, array_hash

sys.set_int_max_str_digits(0)
ROOT = Path(__file__).resolve().parent
OUT = ROOT/'results/heldout_kendall'
ROWS = []
SOURCES = set()


def read(path):
    p = Path(path)
    if not p.is_absolute(): p = ROOT/p
    SOURCES.add(str(p.relative_to(ROOT)))
    return gzip.open(p, 'rt') if p.suffix == '.gz' else p.open()


def js(path):
    with read(path) as f: return json.load(f)


def lines(path):
    with read(path) as f:
        for s in f: yield json.loads(s)


def frame(path):
    with read(path) as f: return pd.read_csv(f)


def add(base, method, saved, y, expected=None, mass=None, beta0=None, beta_true=None, config=None):
    status = saved.get('status', 'ok')
    # Failed fit orders, if present, are not silently admitted.
    order = saved.get('order') if status == 'ok' else None
    value = mean_nll(y, saved, mass)
    if expected is not None:
        np.testing.assert_allclose(value, float(expected), rtol=2e-8, atol=2e-8, equal_nan=True,
                                   err_msg=str((base, method)))
    row = dict(base, method=method, status=status, nll=value, r=y.shape[1],
               **report_loss(y, order, mass),
               **beta_audit(saved.get('beta'), beta0, beta_true, config))
    ROWS.append(row)
    return row


def predictive():
    tasks = {t.name:t for t in load_tasks()}
    for path in ('results/predictive/predictors.jsonl.gz','results/estimator_comparison/predictors.jsonl.gz'):
        for a in lines(path):
            if a['study'] == 'S0':
                c = synthetic_context(a['dataset'].removeprefix('synthetic_'), a['n'], a['N'], a['repeat'])
            else:
                c = empirical_context(tasks[a['dataset']], a['repeat'], a['N'] if a['study']=='L0' else None)
            assert {k:array_hash(v) for k,v in c['data'].items()} == a['data_sha256']
            for m,fit in a['models'].items():
                study = a['study']
                if study == 'P0':
                    if m in ('pl','sm_likelihood'): study='P0'
                    elif m=='sm_global_sieve': study='B0'
                    else: continue  # independently admitted E0 records below
                base = dict(study=study,dataset=a['dataset'],setting=f"n{a['n']}-N{a['N']}",
                            repeat=a['repeat'],split='test',N=a['N'],n=a['n'],source=path)
                add(base,m,fit,c['data']['test'], beta0=.1 if 'sharp' in m or 'efficient' in m or 'global_sieve' in m else None,
                    beta_true=.8 if a['dataset']=='synthetic_sm' else None)
    # Scores are replayed against the saved numeric tables, independently of parameter logs.
    old = pd.concat([frame('results/predictive/repeat_scores.csv.gz'),frame('results/estimator_comparison/repeat_scores.csv.gz')])
    for row in ROWS:
        raw = 'P0' if row['study'] in ('P0','B0') else row['study']
        s = old[(old.study==raw)&(old.dataset==row['dataset'])&(old['repeat']==row['repeat'])&
                (old.N==row['N'])&(old.n==row['n'])&(old.method==row['method'])]
        assert len(s)==1, (row,len(s))
        np.testing.assert_allclose(row['nll'],s.nll.iloc[0],rtol=2e-8,atol=2e-8,equal_nan=True)


def repeated():
    tasks={t.name:t for t in load_tasks()}
    path='results/heldout_kendall/inputs/p1_predictors.jsonl.gz'
    for a in lines(path):
        if a['repeat'] not in range(5): continue
        task=tasks[a['dataset']]
        parts=split_task(task,a['repeat'])
        scores={(s['split'],s['method']):s for s in a['scores']}
        for split in ('discovery','confirmation'):
            base=dict(study='P1',dataset=task.name,setting='',repeat=a['repeat'],split=split,
                      N=len(parts['fit']),n=task.n,source=path)
            for m,f in a['models'].items():
                add(base,m,f,task.y[parts[split]],scores[split,m]['nll'],beta0=.1 if m in ('sharp','efficient') else None)


def fixed_real():
    tasks={t.name:t for t in load_tasks()}
    for folder,paramname,splitname,dscol,idcol in [
        ('baseline_replacement','parameters.json','splits.csv','dataset','row'),
        ('strict_features','real_parameters.json','real_splits.csv','dataset','record'),
        ('context_followup','parameters.json','splits.csv',None,'row')]:
        prefix='results/'+folder+'/'
        params=js(prefix+paramname);splits=frame(prefix+splitname)
        if folder=='context_followup': params={'wheat':params['models']}
        for ds,models in params.items():
            task=tasks[ds];s=splits if dscol is None else splits[splits[dscol]==ds]
            for split in ('discovery','confirmation'):
                held=task.y[s.loc[s['split']==split,idcol].to_numpy(int)]
                base=dict(study='P2',dataset=ds,setting='',repeat=0,split=split,
                          N=int((s['split']=='fit').sum()),n=task.n,source=prefix+paramname)
                for m,f in models.items():
                    add(base,m,f,held,beta0=f.get('metadata',{}).get('beta0',.1) if m in ('sharp','efficient') else None)
    from src.validation_extension import real_tasks, split_units
    params=js('results/validation_extension/real_parameters.json')
    for task in real_tasks():
        if not task['eligible']:continue
        parts=split_units(task,task['source_index'])
        for split in ('discovery','confirmation'):
            for m,f in params[task['name']].items():
                add(dict(study='P2',dataset=task['name'],setting='',repeat=0,split=split,
                         N=len(parts['fit']),n=task['n'],source='results/validation_extension/real_parameters.json'),
                    m,f,task['y'][parts[split]],beta0=f.get('metadata',{}).get('beta0',.1) if m in ('sharp','efficient') else None)


def groups():
    from src.group_sensitivity import load_group_tasks,within_split,holdout_split
    tasks={t.name:t for t in load_group_tasks()}
    path='results/heldout_kendall/inputs/g1_predictors.jsonl.gz'
    for a in lines(path):
            task=tasks[a['dataset']]
            if a['repeat'] not in range(5):continue
            train,test=(within_split(task.groups,task.index,a['percent'],a['repeat']) if a['design']=='within'
                        else holdout_split(task.groups,task.index,a['repeat']))
            if a['group'] >= 0: test=test[task.groups[test]==a['group']]
            base=dict(study='G1',dataset=task.name,setting=f"{a['design']}-p{a['percent']}-{a['scheme']}",
                      repeat=a['repeat'],split='test',N=a['N'],n=task.n,
                      group=a['group'],scheme=a['scheme'],design=a['design'],percent=a['percent'],source=path)
            for m,f in a['fits'].items():
                add(base,m,f,task.y[test],beta0=.1 if m in ('sm_sharp','sm_efficient') else None)


def learning():
    from src.data import load_all
    tasks={t.name:t for t in load_all()}
    scores=frame('results/regularized_learning/real_replicates.csv')
    params=js('results/regularized_learning/fitted_parameters.json')
    for row in scores.itertuples():
        ds=tasks[row.dataset];key=f'{row.dataset}_N{row.N}_rep{row.replicate}';p=params[key]
        ids=np.random.default_rng(20260920).permutation(len(ds.y))[:int(np.ceil(.2*len(ds.y)))]
        held=ds.y[ids]
        base=dict(study='L1',dataset=ds.name,setting=f'N{row.N}',N=row.N,n=ds.n,repeat=row.replicate,
                  split='test',source='results/regularized_learning/fitted_parameters.json')
        for m,theta,b,expected in [('SM',None,p['beta'],row.SM_nll),
                ('SM_calibrated',None,p['beta']*p['beta_factor'],row.SM_calibrated_nll),
                ('PL',p['pl_theta'],math.nan,row.PL_nll),('PL_near_mle',p['pl_near_theta'],math.nan,row.PL_near_mle_nll)]:
            order=p['sm_order'] if theta is None else np.argsort(-np.asarray(theta),kind='stable')
            add(base,m,dict(order=order,beta=b,theta=theta),held,expected)


def tuned_blocks():
    tasks={t.name:t for t in load_tasks()}
    from controls.tuned_sharp.run import selected_sources,case_id,get_context
    sources={case_id(a):a for a in selected_sources()}
    for rec in lines('results/tuned_block_sieve/models.jsonl.gz'):
        c,_=get_context(sources[rec['case']],tasks)
        scores={s['method']:s for s in rec['scores']}
        base=dict(study='Tuned_blocks',dataset=rec['dataset'],setting=rec['case'],repeat=0,split='test',
                  N=rec['N'],n=rec['n'],source='results/tuned_block_sieve/models.jsonl.gz')
        for m,f in rec['models'].items():
            add(base,m,f,c['data']['test'],scores[m]['nll'],beta0=.1 if m=='sm_efficient_fallback' else None)
        for a in rec['candidates']:
            add(dict(base,split='validation',N=len(c['data']['inner']),setting=rec['case']+f"-blocks{a['blocks']}"),
                'borda_block_sieve',a['model'],c['data']['validation'],a['validation_nll'])


def validation_simulations():
    from src.strict_features import small_law
    from src.validation_extension import confounded_law
    scores=frame('results/validation_extension/synthetic_fits.csv').set_index(['cell','rep','method'])
    for a in lines('results/validation_extension/synthetic_parameters.jsonl'):
        truth=np.asarray(a['truth']);n=len(truth)
        if a['family']=='calibration':
            support,mass,_=small_law(n,3,'bridge',a['setting'],'equal');support=truth[support]
        else: support,mass,_,_=confounded_law(a['setting'],truth)
        base=dict(study='D2',dataset=a['family'],setting=f"cell{a['cell']}-signal{a['setting']}-N{a['N']}",
                  N=a['N'],n=n,repeat=a['rep'],split='population',source='results/validation_extension/synthetic_parameters.jsonl')
        for m,f in a['models'].items(): add(base,m,f,support,scores.loc[(a['cell'],a['rep'],m),'nll'],mass)


def s4t():
    from experiments.section44_per_setting.verify import records
    from experiments.section44_per_setting.engine import normalizer
    for phase in ('calibration','confirmation'):
        for rec in records(phase):
            c=rec['cell']
            for m,info in rec['models'].items():
                f=rec['fits'][info['fit_key']];ok=f['status']=='ok'
                b=float(f['beta']) if ok else math.nan
                d=f.get('holdout_distance_sum');Ntest=rec['holdout_count']
                if ok:
                    assert d is not None and int(d)==d
                    np.testing.assert_allclose(b*d/Ntest+normalizer(c['r'],b)[0],f['holdout_nll'],rtol=1e-10,atol=1e-9)
                ROWS.append(dict(study='S4-T',dataset=c['id'],setting=rec['group'],repeat=rec['repeat'],
                    split='validation' if phase=='calibration' else 'test',N=c['N'],n=c['n'],r=c['r'],
                    method=m,status=f['status'],nll=f.get('holdout_nll',math.nan),
                    test_kendall_sum=d if ok else math.nan,test_kendall_mean=d/Ntest if ok else math.nan,
                    evaluation_count=Ntest,evaluation_target='test_reports',true_center_kendall=f.get('kendall'),
                    source='experiments/section44_per_setting/results/draws/'+phase,
                    **beta_audit(b,c['beta0'] if info['family']!='borda' else None,c['beta'],info['config'])))


def output(name):
    OUT.mkdir(exist_ok=True)
    df=pd.DataFrame(ROWS)
    raw=df.to_csv(index=False,float_format='%.15g').encode()
    (OUT/(name+'_fits.csv.gz')).write_bytes(gzip.compress(raw,mtime=0))
    (OUT/(name+'_sources.json')).write_text(json.dumps(sorted(SOURCES),indent=2)+'\n')
    print(name,len(df),'rows;',df.test_kendall_mean.notna().sum(),'defined distances',flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('part',choices=['predictive','repeated','fixed_real','s4t','groups','learning','tuned_blocks','validation_simulations'])
    a=p.parse_args();globals()[a.part]();output(a.part)
