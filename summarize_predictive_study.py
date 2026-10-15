"""Publish complete predictive-study aggregates without fitting any model."""
import gzip
import hashlib
import json
import math
import platform
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from scipy.stats import t as student_t

from src.predictive_study import (read_records,signature,code_hashes,source_inventory,
    load_tasks,PUBLIC,PROTOCOL_COMMIT,BUDGETS,SIMULATION_CELLS)
from src.repeated_holdout import json_value
from src.resource_sieve import CACHE
from src.sieve_budget_retry import CACHE as RETRY_CACHE,ball_size
from run_sieve_budget_retry import apply_saved_retries,retry_hashes,BASE_COMMIT


def task_label(name):
    if name.startswith('00024-'):
        return 'Dots 2013, gap '+str((3,5,7,9)[int(name[-1])-1])
    if name.startswith('00025-'):
        return 'Puzzle, minimum '+str((11,5,7,9)[int(name[-1])-1])+' steps'
    return {'beans':'Beans','wheat':'Wheat','sushi_a':'Sushi A','sushi_b':'Sushi B',
        'sounds':'Sounds','patras_cost':'PatrasIQ cost','patras_population':'PatrasIQ population'}.get(
        name,name.replace('dots2024_','Dots 2024 ').replace('_',' '))


def summarize(frame):
    rows=[]
    keys=['study','dataset','n','r','N','method']
    for key,g in frame.groupby(keys,sort=True):
        row=dict(zip(keys,key)); planned=20 if row['study']=='S0' else 30
        finite=g.status.eq('ok') & np.isfinite(g.nll) & np.isfinite(g.delta)
        good=g[finite]; count=len(good); complete=count==planned
        row.update(repetitions=len(g),planned_repetitions=planned,available=count,
            complete=complete,certified_centers=int(g.certified.sum()),
            aliases=int(g.alias_of.fillna('').ne('').sum()),
            n_test_min=int(g.n_test.min()),n_test_max=int(g.n_test.max()),
            lambda_min=float(g.lambda_.min()),lambda_max=float(g.lambda_.max()),
            statuses=json.dumps(g.status.value_counts().to_dict(),sort_keys=True),
            interval_target='independent_simulation_mean' if row['study']=='S0' else 'fixed_data_partition_precision')
        for measure in ('nll','delta','kendall'):
            values=good[measure].dropna().to_numpy()
            mean=float(values.mean()) if len(values) else np.nan
            se=float(values.std(ddof=1)/np.sqrt(len(values))) if len(values)>1 else np.nan
            row[measure+'_conditional_mean']=mean
            row[measure+'_mean']=mean if complete else np.nan
            row[measure+'_mcse']=se if complete else np.nan
            row[measure+'_split_q025']=float(np.quantile(values,.025)) if complete and len(values) else np.nan
            row[measure+'_split_q975']=float(np.quantile(values,.975)) if complete and len(values) else np.nan
            width=student_t.ppf(.975,len(values)-1)*se if len(values)>1 else np.nan
            row[measure+'_ci_low']=mean-width if complete and row['study']=='S0' else np.nan
            row[measure+'_ci_high']=mean+width if complete and row['study']=='S0' else np.nan
        rows.append(row)
    return pd.DataFrame(rows)


def markdown_table(frame,columns):
    rows=['| '+' | '.join(title for key,title in columns)+' |',
          '|'+'|'.join('---' for _ in columns)+'|']
    for _,r in frame.iterrows():
        cells=[]
        for key,_ in columns:
            v=r[key]
            cells.append('NA' if pd.isna(v) else f'{v:+.5f}' if isinstance(v,(float,np.floating)) and key.startswith('delta') else
                         f'{v:.5f}' if isinstance(v,(float,np.floating)) else str(v))
        rows.append('| '+' | '.join(cells)+' |')
    return '\n'.join(rows)


def write_tables(summary):
    # Keep the raw export stable; readers receive separate scientific reports.
    from build_study_reports import build
    build(update_manifest=False)


def publish():
    records=apply_saved_retries(read_records()); expected=signature()
    assert len(records)==1290, (len(records),'Expected 690 P0 + 360 L0 + 240 S0 fits')
    assert all(r['code_signature']==expected for r in records)
    frame=pd.DataFrame([s for r in records for s in r['scores']])
    assert len(frame)==7740
    keys=['study','dataset','repeat','n','N','method']
    assert not frame.duplicated(keys).any()
    assert (frame.groupby(['study','dataset','n','N','method']).size()==frame.groupby(['study','dataset','n','N','method']).size().index.get_level_values('study').map(lambda s:20 if s=='S0' else 30)).all()
    summary=summarize(frame)
    PUBLIC.mkdir(parents=True,exist_ok=True)
    outputs=[]
    if (PUBLIC/'packing_crosscheck.json').exists():outputs.append('packing_crosscheck.json')
    for name,data in [('primary.csv',summary[summary.study=='P0']),
                      ('learning.csv',summary[(summary.study=='L0')|((summary.study=='P0')&summary.dataset.isin(['sushi_a','sushi_b']))]),
                      ('synthetic.csv',summary[summary.study=='S0'])]:
        data.to_csv(PUBLIC/name,index=False,float_format='%.12g'); outputs.append(name)
    frame=frame.sort_values(keys).reset_index(drop=True)
    (PUBLIC/'repeat_scores.csv.gz').write_bytes(gzip.compress(frame.to_csv(index=False,float_format='%.12g').encode(),mtime=0))
    outputs.append('repeat_scores.csv.gz')
    public=[]
    for record in records:
        keep={k:v for k,v in record.items() if k not in ('parts','losses','scores')}
        public.append(json.dumps(json_value(keep),sort_keys=True,allow_nan=False))
    (PUBLIC/'predictors.jsonl.gz').write_bytes(gzip.compress(('\n'.join(public)+'\n').encode(),mtime=0))
    outputs.append('predictors.jsonl.gz')
    retry_rows=[]
    for record in records:
        if 'resource_retry' not in record:continue
        fit=record['models']['sm_sharp'];meta=fit['metadata']
        retry_rows.append(dict(study=record['study'],dataset=record['dataset'],n=record['n'],
            N=record['N'],repeat=record['repeat'],status=fit['status'],
            reason=meta.get('reason',''),seconds_limit=1800,memory_bytes=4<<30))
    retry_frame=pd.DataFrame(retry_rows)
    retry_frame.to_csv(PUBLIC/'resource_retries.csv',index=False)
    outputs.append('resource_retries.csv')
    bounds=[]
    cases=sorted({(r['n'],r['n']*(r['n']*(r['n']-1)//2)//r['N'])
        for r in records if 'resource_retry' in r and r['models']['sm_sharp']['status']!='ok'})
    for n,radius in cases:
        volume=ball_size(n,radius);orders=(math.factorial(n)+volume-1)//volume
        bounds.append(dict(n=n,integer_radius=radius,kendall_ball_size=volume,
            maximal_packing_order_lower_bound=orders,
            explicit_int16_order_storage_lower_bound_bytes=2*n*orders,
            interpretation='Covering-count lower bound for any maximal packing; not an implicit-solver memory lower bound'))
    (PUBLIC/'sieve_cover_bounds.json').write_text(json.dumps(bounds,indent=2)+'\n')
    outputs.append('sieve_cover_bounds.json')
    receipts=[]
    for path in sorted(list(CACHE.glob('*.json'))+list(RETRY_CACHE.glob('*.json'))):
        receipt=json.loads(path.read_text())
        # Pre-allocation failures precede radius-dependent construction; retain
        # the cache key as well as its receipt so the attempted radius is explicit.
        receipt['cache_file']=path.name
        receipt['attempt']='expanded_budget' if receipt.get('seconds_limit')==1800 else 'initial_budget'
        receipt['integer_radius_from_cache_key']=int(path.stem.split('-')[-3])
        receipts.append(receipt)
    (PUBLIC/'sieve_resources.json').write_text(json.dumps(receipts,indent=2)+'\n'); outputs.append('sieve_resources.json')
    write_tables(summary); outputs.append('tables.md')
    descriptors=[dict(dataset=t.name,n=t.n,r=t.y.shape[1],reports=len(t.y),
        allocation_unit=t.unit_description,units=len(np.unique(t.units)),split_key=t.split_key,
        estimator_seed=t.estimator_seed,source_report_sha256=hashlib.sha256(np.asarray(t.y,dtype='<i8').tobytes()).hexdigest()) for t in load_tasks()]
    manifest=dict(protocol_commit=PROTOCOL_COMMIT,code_signature=expected,code_sha256=code_hashes(),
        resource_retry=dict(base_commit=BASE_COMMIT,code_sha256=retry_hashes(),
            seconds_limit=1800,memory_bytes=4<<30,
            attempts=sum('resource_retry' in r for r in records),
            recovered=sum('resource_retry' in r and r['models']['sm_sharp']['status']=='ok' for r in records)),
        summary_code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        sources=source_inventory(),datasets=descriptors,training_contexts=1290,
        context_counts={'P0':690,'L0':360,'S0':240},score_rows=7740,
        runtime=dict(python=platform.python_version(),platform=platform.platform(),
                     numpy=np.__version__,scipy=scipy.__version__,pandas=pd.__version__),
        summed_context_seconds=sum(r['seconds'] for r in records),
        timing_note='Sum of worker elapsed fitting/scoring times, not parallel wall-clock duration; synthetic generation precedes this timer.',
        computational_alias='sm_global_sieve reuses sm_sharp when identity is proved',
        published_sha256={name:hashlib.sha256((PUBLIC/name).read_bytes()).hexdigest() for name in outputs})
    (PUBLIC/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Published',len(records),'contexts;',len(frame),'score rows;',len(summary),'summary rows')


if __name__=='__main__':
    publish()
