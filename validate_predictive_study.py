"""Read-only predictor, split, numerical and aggregate validation; never refits."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.predictive_study import (PUBLIC,PRIVATE,code_hashes,signature,read_records,
    load_tasks,empirical_context,synthetic_context,array_hash,evaluate,PROTOCOL_COMMIT)
from src.repeated_holdout import restore_fit
from src.models import pair_counts,kemeny_cost,distances
from src.predictive_models import bounded_beta,pl_objective,RIDGE_GRID
from summarize_predictive_study import summarize
from run_sieve_budget_retry import apply_saved_retries,retry_hashes,BASE_COMMIT
from src.manuscript_estimators import extract_pairs


def frames_equal(a,b):
    pd.testing.assert_frame_equal(a.reset_index(drop=True),b.reset_index(drop=True),
        check_dtype=False,rtol=2e-9,atol=2e-9)


def validate_public():
    manifest=json.loads((PUBLIC/'manifest.json').read_text())
    assert manifest['protocol_commit']==PROTOCOL_COMMIT
    assert manifest['code_sha256']==code_hashes()
    assert manifest['code_signature']==signature()
    assert manifest['summary_code_sha256']==hashlib.sha256((PUBLIC.parents[1]/'summarize_predictive_study.py').read_bytes()).hexdigest()
    assert manifest['resource_retry']['code_sha256']==retry_hashes()
    assert manifest['resource_retry']['base_commit']==BASE_COMMIT
    for name,digest in manifest['published_sha256'].items():
        assert hashlib.sha256((PUBLIC/name).read_bytes()).hexdigest()==digest,name
    if (PUBLIC/'packing_crosscheck.json').exists():
        check=json.loads((PUBLIC/'packing_crosscheck.json').read_text())
        assert check['orders']==29086 and check['complete_ordered_arrays_equal']
        assert check['original_orders_sha256']==check['completion_orders_sha256']
        assert check['verifier_sha256']==hashlib.sha256((PUBLIC.parents[1]/'verify_sieve_packing.py').read_bytes()).hexdigest()
    frame=pd.read_csv(PUBLIC/'repeat_scores.csv.gz')
    with gzip.open(PUBLIC/'predictors.jsonl.gz','rt') as stream:
        records=[json.loads(line) for line in stream]
    assert len(records)==1290 and len(frame)==7740
    retried=[r for r in records if 'resource_retry' in r]
    assert len(retried)==manifest['resource_retry']['attempts']==630
    assert sum(r['models']['sm_sharp']['status']=='ok' for r in retried)==manifest['resource_retry']['recovered']==100
    for record in retried:
        assert record['resource_retry']['code_sha256']==retry_hashes()
        assert record['resource_retry']['original_sharp']['status']=='sieve_resource_budget'
        assert not record['resource_retry']['statistical_definition_changed']
        assert record['models']['sm_sharp']['metadata']['retry_seconds']==1800
        assert record['models']['sm_sharp']['metadata']['retry_memory']==4<<30
    assert set(frame.r)<=set(range(2,11)) and (frame.R_bound==10).all()
    assert not frame.duplicated(['study','dataset','n','N','repeat','method']).any()
    assert frame.loc[frame.method.isin(['pl','sm_likelihood']),'status'].eq('ok').all()
    assert np.isfinite(frame.loc[frame.status.eq('ok'),'nll']).all()
    assert frame.loc[frame.status.ne('ok'),'nll'].isna().all()
    key=['study','dataset','n','N','repeat']
    pl=frame[frame.method.eq('pl')][key+['nll']]
    joined=frame.merge(pl,on=key,suffixes=('','_pl'),validate='many_to_one')
    np.testing.assert_allclose(joined.delta,joined.nll-joined.nll_pl,rtol=2e-9,atol=2e-9,equal_nan=True)
    aliases=frame[frame.alias_of.eq('sm_sharp')].merge(frame[frame.method.eq('sm_sharp')],on=key,suffixes=('','_sharp'))
    assert len(aliases)==1290
    np.testing.assert_allclose(aliases.nll,aliases.nll_sharp,equal_nan=True)
    assert aliases.status.eq(aliases.status_sharp).all()
    assert frame.loc[frame.study.eq('S0'),'r'].eq(3).all()
    assert frame.loc[frame.study.eq('L0'),'r'].eq(10).all()
    assert frame.loc[frame.dataset.str.startswith(('00024','00025'))|frame.dataset.isin(['beans','wheat']),'ci_kind'].eq('unavailable').all()
    summary=summarize(frame)
    for name,expected in [('primary.csv',summary[summary.study=='P0']),
            ('learning.csv',summary[(summary.study=='L0')|((summary.study=='P0')&summary.dataset.isin(['sushi_a','sushi_b']))]),
            ('synthetic.csv',summary[summary.study=='S0'])]:
        frames_equal(pd.read_csv(PUBLIC/name),expected)
    for record in records:
        assert record['code_signature']==signature()
        models=record['models']; n=record['n']
        for method,saved in models.items():
            fit=restore_fit(saved)
            if fit.status!='ok':
                assert fit.order is None
                continue
            np.testing.assert_array_equal(np.sort(fit.order),np.arange(n))
            if method=='pl':
                assert fit.metadata['tau'] in RIDGE_GRID
                assert abs(fit.theta.sum())<1e-7
                scores=fit.metadata['inner_nll']
                assert fit.metadata['tau']==RIDGE_GRID[int(np.argmin(scores))]
                assert fit.metadata['gradient_per_report']<=1e-7
            else:
                assert 0<=fit.beta<=10
            if method=='sm_likelihood':
                meta=fit.metadata
                assert meta['upper_bound']>=meta['lower_bound']
                assert meta['certified']==(meta['upper_bound']==meta['lower_bound'])
            if method=='sm_sharp':
                assert fit.metadata['A']==256
                assert fit.metadata['W_star']==int(np.ceil(2048*(n-1)/(record['r']-1)))
    print('PUBLIC: 1,290 parameter records; 7,740 scores; hashes, aliases, finite fits and aggregates verified',flush=True)
    return frame


def validate_features():
    root=PUBLIC.parents[1]; directory=root/'data/features'
    manifest=json.loads((directory/'predictive_comparison_manifest.json').read_text())
    for path,digest in manifest['inputs'].items():
        assert hashlib.sha256((root/path).read_bytes()).hexdigest()==digest
    for path,digest in manifest['outputs'].items():
        assert hashlib.sha256((directory/path).read_bytes()).hexdigest()==digest
    joined=pd.read_csv(directory/'predictive_comparison.csv').set_index('dataset')
    original=pd.read_csv(directory/'all_features.csv').set_index('dataset')
    primary=pd.read_csv(PUBLIC/'primary.csv')
    primary=primary[primary.method.eq('sm_likelihood')].set_index('dataset')
    assert len(joined)==33 and set(joined.index)==set(original.index)
    for name,row in primary.iterrows():
        assert np.isclose(joined.loc[name,'primary_delta'],row.delta_mean)
        assert joined.loc[name,'primary_available']==30
    for column in ('heterogeneity_sd','shell_tv','shell_excess_tv','context_display_sd','context_gap_slope','swap_gap_effect'):
        np.testing.assert_allclose(joined[column],original.loc[joined.index,column],equal_nan=True,rtol=2e-9,atol=2e-9)
    print('FEATURES: all three full-data characteristics unchanged; primary NLL join verified',flush=True)


def validate_full():
    tasks={t.name:t for t in load_tasks()}; records=apply_saved_retries(read_records()); aligned={}; replay=[]
    for index,record in enumerate(records,1):
        if record['study']=='S0':
            c=synthetic_context(record['generator'],record['n'],record['N'],record['repeat'])
        else:
            budget=None if record['study']=='P0' else record['N']
            c=empirical_context(tasks[record['dataset']],record['repeat'],budget)
            task=tasks[record['dataset']]
            for key,ids in c['parts'].items():
                np.testing.assert_array_equal(ids,record['parts'][key])
                align_key=(c['study'],task.split_key,c['repeat'],budget,key)
                # Within a dots arm task sizes share unit IDs, not source report rows.
                units=np.unique(task.units[ids])
                if align_key in aligned:
                    np.testing.assert_array_equal(units,aligned[align_key])
                aligned[align_key]=units
            assert not np.intersect1d(task.units[c['parts']['development']],task.units[c['parts']['test']]).size
            assert not np.intersect1d(task.units[c['parts']['inner']],task.units[c['parts']['validation']]).size
        assert {k:array_hash(v) for k,v in c['data'].items()}==record['data_sha256']
        models={m:restore_fit(f) for m,f in record['models'].items()}
        y=c['data']['development']; w=pair_counts(y,c['n'])
        for method,fit in models.items():
            if fit.status!='ok':
                continue
            if method=='pl':
                gradient=np.max(np.abs(pl_objective(fit.theta,y,fit.metadata['tau'])[1]))/len(y)
                assert gradient<=1e-7
            else:
                total=int(distances(y,fit.order).sum())
                assert total==fit.metadata['training_distance']
                assert abs(bounded_beta(total,len(y),y.shape[1])-fit.beta)<1e-10
                if method=='sm_likelihood':
                    assert kemeny_cost(w,fit.order)==fit.metadata['upper_bound']
                if method=='sm_sharp' and 'resource_retry' in record:
                    pairs=extract_pairs(y,np.arange(c['n']),np.random.default_rng(c['estimator_seed']+173))
                    pair_w=pair_counts(pairs,c['n'])
                    assert kemeny_cost(pair_w,fit.order)==fit.metadata['blocks'][0]['objective']
        fresh,losses=evaluate(c,models)
        for a,b in zip(fresh,record['scores']):
            for key,value in a.items():
                old=b[key]
                if isinstance(value,str):
                    assert value==old,(key,value,old)
                else:
                    assert np.isclose(value,old,equal_nan=True,rtol=2e-9,atol=2e-9),(key,value,old)
        for method,loss in losses.items():
            np.testing.assert_allclose(loss,np.asarray(record['losses'][method],float),rtol=2e-10,atol=2e-10,equal_nan=True)
        replay.append(dict(study=c['study'],dataset=c['dataset'],n=c['n'],N=c['N'],repeat=c['repeat']))
        if index%100==0:
            print('REPLAYED',index,'/',len(records),flush=True)
    print('FULL: sources, memberships, grouped bootstrap and all saved test losses replayed; no refits',flush=True)
    return len(replay)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repository-only',action='store_true');args=p.parse_args()
    validate_public()
    validate_features()
    if not args.repository_only:
        validate_full()
