"""Replay pinned regularized controls without replacing their published fits.

The isolated source directory is byte-verified against commit 89b21645. All
reconstructed predictors must match their recorded NLL before distances are used.
"""
import argparse
import gzip
import json
import math
from pathlib import Path
import sys
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results/heldout_kendall'
LEGACY=OUT/'inputs/legacy'
sys.path.insert(0,str(LEGACY))
from src import data
data.RAW=ROOT/'data/raw'
from src.models import distances,logz_mean,fit_pl,pl_nll,exact_dp,pair_counts,fit_beta
import run_experiments as old
import run_exposure as exposure

ROWS=[]
WITNESSES=[]


def emit(base,method,mean,nll,beta=math.nan,beta0=None,count=None,recovery='saved_center',order=None,theta=None):
    r=base['r']
    assert -1e-7<=mean<=r*(r-1)/2+1e-7,(base,method,mean)
    row=dict(base,method=method,status='ok',split='test',nll=float(nll),
             test_kendall_mean=float(mean),test_kendall_sum=int(round(mean*count)) if count is not None else math.nan,
             evaluation_count=count,evaluation_target='test_reports',beta_fit=beta,algorithm_beta0=beta0,
             beta_fit_below_beta0=None if beta0 is None or math.isnan(beta) else beta<beta0,
             constant_beta0_status='supplied_input_not_inferred' if beta0 is not None else 'not_an_input',recovery=recovery)
    ROWS.append(row)
    if order is not None:
        WITNESSES.append(dict(study=base['study'],dataset=base['dataset'],setting=base['setting'],repeat=base['repeat'],
                              method=method,order=np.asarray(order).tolist(),theta=None if theta is None else np.asarray(theta).tolist()))
    return row


def checked(base,method,test,order,nll,beta=math.nan,theta=None,beta0=None,recovery='saved_center'):
    d=distances(test,np.asarray(order));score=pl_nll(test,theta) if theta is not None else beta*d+logz_mean(test.shape[1],beta)[0]
    np.testing.assert_allclose(score.mean(),nll,atol=2e-7,rtol=2e-7,err_msg=str((base,method)))
    return emit(base,method,d.mean(),nll,beta,beta0,len(test),recovery,order,theta)


def algebra(base,method,test,nll,beta,beta0=None):
    assert beta>0 and np.isfinite(beta)
    mean=(nll-logz_mean(test.shape[1],beta)[0])/beta
    total=round(mean*len(test));np.testing.assert_allclose(total/len(test),mean,atol=2e-6)
    return emit(base,method,total/len(test),nll,beta,beta0,len(test),'SM_NLL_identity')


def save(part):
    (OUT/f'legacy_{part}_fits.csv.gz').write_bytes(gzip.compress(pd.DataFrame(ROWS).to_csv(index=False,float_format='%.15g').encode(),mtime=0))
    (OUT/f'legacy_{part}_witnesses.jsonl.gz').write_bytes(gzip.compress(('\n'.join(json.dumps(a) for a in WITNESSES)+'\n').encode(),mtime=0))
    print(part,len(ROWS),'scores',flush=True)


def small_coverage(part):
    df=pd.read_csv(LEGACY/f'results/exposure/{part}_replicates.csv')
    for index,((seed,dgp),g) in enumerate(df.groupby(['seed','dgp'],sort=True)):
        row=g.iloc[0];n,r,N=map(int,(row.n,row.r,row.N));rep=int(row.rep)
        rng=np.random.default_rng(int(seed));truth=rng.permutation(n)
        theta=exposure.matched_theta(n,r,.8,truth)
        train=exposure.draw(rng,N,n,r,truth,dgp,.8,theta)
        test=exposure.draw(rng,2000 if n==8 else 1000,n,r,truth,dgp,.8,theta)
        base=dict(study='S3',dataset=f'{part}_{dgp}',setting=f'n{n}-r{r}-N{N}',repeat=rep,n=n,r=r,N=N,
                  source=f'89b21645:results/exposure/{part}_replicates.csv',beta_true=.8 if dgp=='SM' else None)
        for row in g.itertuples():
            if row.method=='pl':
                f=fit_pl(train,n,row.tau)
                checked(base,'pl',test,f.order,row.nll,theta=f.theta,recovery='deterministic_fit_replay')
            else:
                beta0=.8 if row.method in ('sharp','efficient') else None
                if row.beta>0:
                    result=algebra(base,row.method,test,row.nll,row.beta,beta0)
                else:
                    f=exposure.center_fit(train,n,row.method,int(row.estimator_seed))
                    result=checked(base,row.method,test,f.order,row.nll,beta=f.beta,beta0=beta0,recovery='deterministic_fit_replay')
                b=row.beta*row.beta_factor
                np.testing.assert_allclose(b*result['test_kendall_mean']+logz_mean(r,b)[0],row.nll_shrunk,atol=2e-7)
                emit(base,row.method+'_shrunk',result['test_kendall_mean'],row.nll_shrunk,b,beta0,len(test),'same_saved_center_as_unshrunk')
        if index%30==29:save(part)
    save(part)


def synthetic():
    df=pd.read_csv(LEGACY/'results/synthetic_replicates.csv')
    for (dgp,rep),g in df.groupby(['dgp','replicate']):
        d=['SM','PL_equal','PL_unequal'].index(dgp);rng=np.random.default_rng(old.SEED+10000+1000*d+int(rep));n,r=10,3
        truth=rng.permutation(n)
        if dgp=='SM':
            development=old.sample_sm(rng,300,n,r,truth,.8);test=old.sample_sm(rng,2000,n,r,truth,.8)
            oracle=.8*distances(test,truth)+logz_mean(r,.8)[0]
        else:
            theta=np.empty(n);theta[truth]=old.matched_pl_theta(n,r,.8,dgp.split('_')[1])[0]
            development=old.sample_pl(rng,300,n,r,theta);test=old.sample_pl(rng,2000,n,r,theta);oracle=pl_nll(test,theta)
        for row in g.itertuples():
            base=dict(study='S3',dataset=dgp,setting=f'n10-r3-N{row.N}',repeat=int(rep),n=n,r=r,N=row.N,
                      source='89b21645:results/synthetic_replicates.csv',beta_true=.8 if dgp=='SM' else None)
            sm=algebra(base,'SM',test,row.SM_nll,row.beta)
            emit(base,'SM_calibrated',sm['test_kendall_mean'],row.SM_calibrated_nll,row.beta*row.sm_beta_factor,count=len(test),recovery='same_saved_center_as_unshrunk')
            for method,tau,expected in [('PL',row.tau,row.PL_nll),('PL_near_mle',1e-6,row.PL_near_mle_nll)]:
                f=fit_pl(development[:row.N],n,tau)
                checked(base,method,test,f.order,expected,theta=f.theta,recovery='deterministic_fit_replay')
            np.testing.assert_allclose(oracle.mean(),row.oracle_nll,atol=2e-8)
            emit(base,'oracle',distances(test,truth).mean(),row.oracle_nll,.8 if dgp=='SM' else math.nan,count=len(test),order=truth)
        save('synthetic')


def real():
    tasks={t.name:t for t in data.load_all()}
    params=json.loads((LEGACY/'results/exposure/real_parameters.json').read_text())
    scores=pd.read_csv(LEGACY/'results/exposure/real_replicates.csv').set_index(['dataset','rep','N','method'])
    for key,p in params.items():
        name,rep,N=key.rsplit('_',2);rep,N=int(rep),int(N);task=tasks[name]
        train=task.y[p['train_indices']];test=task.y[p['test_indices']]
        base=dict(study='L2',dataset=name,setting=f'N{N}',repeat=rep,n=task.n,r=test.shape[1],N=N,
                  source='89b21645:results/exposure/real_parameters.json')
        theta=np.asarray(p['pl_theta']);order=np.argsort(-theta,kind='stable')
        checked(base,'pl',test,order,scores.loc[(name,rep,N,'pl'),'nll'],theta=theta)
        for m,f in p['sm'].items():
            for suffix,factor in [('',1),('_shrunk',f['factor'])]:
                checked(base,m+suffix,test,f['order'],scores.loc[(name,rep,N,m+suffix),'nll'],
                        beta=f['beta']*factor,beta0=.8 if m=='efficient' else None)
        for tau in (1.,10.):
            f=fit_pl(train,task.n,tau)
            checked(dict(base,study='L2_penalty'),f'pl_fixed_{int(tau)}',test,f.order,float(f.nll(test).mean()),theta=f.theta,recovery='deterministic_fit_replay')
    save('real')


def tennis():
    from src.tennis import chronological_year
    params=json.loads((LEGACY/'results/exposure/tennis_parameters.json').read_text())
    scores=pd.read_csv(LEGACY/'results/exposure/tennis_by_year.csv').set_index(['year','target','method'])
    same=pd.read_csv(LEGACY/'results/exposure/tennis_same_order_by_year.csv')
    for year in range(2010,2020):
        d=chronological_year(year,ROOT/'data/raw/tennis');p=params[str(year)];theta=np.asarray(p['pl_theta']);order=np.argsort(-theta,kind='stable')
        for target,mask in [('seen',d['test_seen']),('all_catalog',np.ones(len(d['test']),bool))]:
            test=d['test'][mask]
            base=dict(study='T1_ATP',dataset='ATP',setting=f'{year}-{target}',repeat=0,n=d['n'],r=2,N=len(d['train']),
                      source='89b21645:results/exposure/tennis_parameters.json')
            checked(base,'pl',test,order,scores.loc[(year,target,'pl'),'nll'],theta=theta)
            for m,f in p['sm'].items():
                for suffix,factor in [('',1),('_shrunk',f['factor'])]:
                    checked(base,m+suffix,test,f['order'],scores.loc[(year,target,m+suffix),'nll'],
                            beta=f['beta']*factor,beta0=.8 if m=='efficient' else None)
        for row in same[same.year==year].itertuples():
            checked(dict(base,study='C1_ATP',setting=str(year)),row.method,d['test'][d['test_seen']],order,row.nll,beta=row.beta*row.factor)
    save('tennis')


def empirical_controls():
    tasks={t.name:t for t in data.load_all()}
    transfer=pd.read_csv(LEGACY/'results/beans_transfer_replicates.csv')
    outer=pd.read_csv(LEGACY/'results/outer_fold_replicates.csv')
    contexts=[]
    ds=tasks['beans'];mask=np.char.endswith(ds.groups.astype(str),'15')
    for row in transfer.itertuples():
        train=ds.y[mask];train=train[np.random.default_rng(old.SEED+110000+row.replicate).permutation(len(train))]
        contexts.append(('T1_Beans',row,train,ds.y[~mask],ds.n,row.replicate))
    for name,g in outer.groupby('dataset'):
        ds=tasks[name];rng=np.random.default_rng(old.SEED+220000);folds=np.array_split(rng.permutation(len(ds.y)),5)
        for row in g.sort_values('fold').itertuples():
            pool=np.concatenate([f for j,f in enumerate(folds) if j!=row.fold]);pool=rng.permutation(pool)[:min(3000,len(pool))]
            contexts.append(('C1_outer',row,ds.y[pool],ds.y[folds[row.fold]],ds.n,row.fold))
    for study,row,train,test,n,rep in contexts:
        base=dict(study=study,dataset=row.dataset,setting=f'N{len(train)}',repeat=rep,n=n,r=test.shape[1],N=len(train),source='89b21645:results/'+('beans_transfer_replicates.csv' if study=='T1_Beans' else 'outer_fold_replicates.csv'))
        sm=algebra(base,'SM',test,row.SM_nll,row.beta)
        emit(base,'SM_calibrated',sm['test_kendall_mean'],row.SM_calibrated_nll,row.beta*row.sm_beta_factor,count=len(test),recovery='same_saved_center_as_unshrunk')
        for m,tau,val in [('PL',row.tau,row.PL_nll),('PL_near_mle',1e-6,row.PL_near_mle_nll)]:
            f=fit_pl(train,n,tau);checked(base,m,test,f.order,val,theta=f.theta,recovery='deterministic_fit_replay')
    params=json.loads((LEGACY/'results/fitted_parameters.json').read_text())
    same=pd.read_csv(LEGACY/'results/same_order_replicates.csv')
    for row in same.itertuples():
        ds=tasks[row.dataset];_,idx=old.outer_split(ds);test=ds.y[idx];p=params[f'{row.dataset}_N{row.N}_rep{row.replicate}']
        base=dict(study='C1_same_order',dataset=row.dataset,setting=f'N{row.N}',repeat=row.replicate,n=ds.n,r=test.shape[1],N=row.N,source='89b21645:results/same_order_replicates.csv')
        for m,order,val in [('SM',p['sm_order'],row.SM_nll),('PL_same_SM_order',p['sm_order'],row.PL_same_SM_order_nll),
                            ('PL',np.argsort(-np.asarray(p['pl_theta'])),row.PL_nll),('SM_on_PL_order',np.argsort(-np.asarray(p['pl_theta'])),row.SM_on_PL_order_nll)]:
            emit(base,m,distances(test,order).mean(),val,count=len(test),order=order,recovery='saved_or_prespecified_common_order')
    ds=tasks['sushi_b'];_,idx=old.outer_split(ds);test=ds.y[idx]
    for p in json.loads((LEGACY/'results/cutting_plane_pilot.json').read_text()):
        base=dict(study='C1_cutting_plane',dataset='sushi_b',setting=f"N{p['N']}",repeat=0,n=ds.n,r=10,N=p['N'],source='89b21645:results/cutting_plane_pilot.json')
        checked(base,'SM',test,p['order'],p['test_nll'],beta=p['beta'])
    save('controls')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('part',choices=['small','coverage','synthetic','real','tennis','controls']);a=p.parse_args()
    if a.part in ('small','coverage'):small_coverage(a.part)
    elif a.part=='controls':empirical_controls()
    else:globals()[a.part]()
