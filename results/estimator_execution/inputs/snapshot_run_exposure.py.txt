"""Exposure-regime experiments; recovered after the local workspace disconnected."""
import argparse
import hashlib
import json
from pathlib import Path
import time
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.special import expit
from scipy.stats import t as student_t
from src.data import ROOT,load_beans,load_sushi
from src.manuscript_estimators import efficient_center,exposure,schedule,sharp_center
from src.models import SMFit,distances,exact_dp,fit_beta,fit_pl,insertion_search,kendall,kemeny_cost,logz_mean,pair_counts,tune_pl
from src.tennis import chronological_year,download_tennis
from run_experiments import outer_split

SEED=20260925
OUT=ROOT/'results/exposure'
FACTORS=[0.,.25,.5,.75,1.]

def estimator_seed(data_seed):
    return int(np.random.SeedSequence([data_seed,73471]).generate_state(1)[0])

def js(path,value):
    Path(path).write_text(json.dumps(value,indent=2,default=lambda x:x.item() if hasattr(x,'item') else str(x))+'\n')

def draw(rng,count,n,r,truth,dgp,beta,theta):
    subset=np.argsort(rng.random((count,n)),axis=1)[:,:r]
    if dgp=='PL':
        order=np.argsort(-(theta[subset]+rng.gumbel(size=subset.shape)),axis=1)
        return np.take_along_axis(subset,order,axis=1)
    rank=np.argsort(truth)
    s=np.take_along_axis(subset,np.argsort(rank[subset],axis=1),axis=1)
    out=np.empty_like(s);out[:,0]=s[:,0]
    for j in range(1,r):
        p=np.exp(-beta*np.arange(j+1));p/=p.sum()
        where=j-rng.choice(j+1,size=count,p=p);cols=np.arange(j+1)[None,:]
        source=np.clip(cols-(cols>=where[:,None]),0,j-1)
        old=np.take_along_axis(out[:,:j],source,axis=1)
        out[:,:j+1]=np.where(cols==where[:,None],s[:,j,None],old)
    return out

def matched_theta(n,r,beta,truth):
    gap=np.arange(1,n)/(n-1);multiplicity=n-np.arange(1,n)
    target=logz_mean(r,beta)[1];rate=r*(r-1)/(n*(n-1))
    span=brentq(lambda x:rate*np.dot(multiplicity,expit(-x*gap))-target,0,1000)
    theta=np.empty(n);theta[truth]=np.linspace(span/2,-span/2,n)
    return theta

def center_fit(y,n,method,seed):
    t0=time.perf_counter()
    if method=='sharp':order,info=sharp_center(y,n,seed)
    elif method=='efficient':order,info=efficient_center(y,n,seed)
    elif method=='mle':
        w=pair_counts(y,n);order=exact_dp(w,seed)
        info=dict(certified=True,branch='exact_dp',depth=0)
    elif method=='insertion':
        w=pair_counts(y,n);initial,_=efficient_center(y,n,seed);order=insertion_search(w,initial)
        bound=np.minimum(w,w.T)[np.triu_indices(n,1)].sum();gap=kemeny_cost(w,order)-bound
        info=dict(certified=gap==0,gap_to_pair_bound=int(gap),branch='insertion',depth=0)
    else:raise ValueError(method)
    value=int(distances(y,order).sum());beta=fit_beta(value,len(y),y.shape[1])
    info.update(seconds=time.perf_counter()-t0,beta_cap_hit=beta>9.999)
    return SMFit(order,beta,value,info)

def compare(train,test,n,seed,methods,inner=None):
    t0=time.perf_counter()
    if inner is None and len(train)>=5:
        cut=int(.8*len(train));inner=train[:cut],train[cut:]
    tau=1. if inner is None else tune_pl(*inner,n,grid=(.1,1.,10.))[0]
    pl=fit_pl(train,n,tau);pl.metadata['full_pipeline_seconds']=time.perf_counter()-t0
    models={'pl':pl};losses={'pl':pl.nll(test)};factors={}
    for method in methods:
        t0=time.perf_counter()
        if inner is None:factor=.5
        else:
            sm_inner=center_fit(inner[0],n,method,seed)
            factor=FACTORS[int(np.argmin([sm_inner.nll(inner[1],f).mean() for f in FACTORS]))]
        model=center_fit(train,n,method,seed)
        model.metadata['full_pipeline_seconds']=time.perf_counter()-t0
        models[method]=model;factors[method]=factor;losses[method]=model.nll(test)
        losses[method+'_shrunk']=model.nll(test,factor)
    return models,losses,factors

def actual_exposure(y,n):
    w=pair_counts(y,n);counts=np.bincount(y.ravel(),minlength=n)
    pairs=(w+w.T)[np.triu_indices(n,1)]
    return dict(unseen_items=int((counts==0).sum()),unseen_pairs=int((pairs==0).sum()),
        item_min=int(counts.min()),item_max=int(counts.max()),pair_max=int(pairs.max()))

def mean_ci(values):
    v=np.asarray(values,float);mean=v.mean()
    half=student_t.ppf(.975,len(v)-1)*v.std(ddof=1)/np.sqrt(len(v)) if len(v)>1 else np.nan
    return mean,mean-half,mean+half

def simulate(part,reps=30):
    if part=='small':
        grid=[(8,r,N) for r,ns in [(2,[2,4,8,16,28,56,112]),(4,[1,2,4,8,16,64]),(8,[1,2,8,32])] for N in ns]
    else:grid=[(64,r,max(1,round(lam*64*63/(r*(r-1))))) for r in [2,8,32] for lam in [.03,.3,1,3]]
    methods=['sharp','efficient','mle'] if part=='small' else ['efficient'];rows=[]
    for cell,(n,r,N) in enumerate(grid):
        for di,dgp in enumerate(['SM','PL']):
            print(f'{part} n={n} r={r} N={N} DGP={dgp}',flush=True)
            for rep in range(reps):
                seed=SEED+100000*(part=='coverage')+cell*1000+di*100+rep
                rng=np.random.default_rng(seed);truth=rng.permutation(n)
                theta=matched_theta(n,r,.8,truth)
                train=draw(rng,N,n,r,truth,dgp,.8,theta)
                test=draw(rng,2000 if n==8 else 1000,n,r,truth,dgp,.8,theta)
                fit_seed=estimator_seed(seed)
                models,losses,factors=compare(train,test,n,fit_seed,methods)
                info=dict(part=part,dgp=dgp,rep=rep,seed=seed,estimator_seed=fit_seed,
                          **exposure(n,r,N),**actual_exposure(train,n))
                for method,model in models.items():
                    loss=losses[method];risk=kendall(model.order,truth);shrunk=losses.get(method+'_shrunk',loss)
                    rows.append(dict(**info,method=method,risk=risk,risk_normalized=risk/(n*(n-1)/2),
                        risk_over_shape=risk/info['reference_shape'],nll=loss.mean(),
                        delta_nll=(loss-losses['pl']).mean(),nll_shrunk=shrunk.mean(),
                        delta_shrunk=(shrunk-losses['pl']).mean(),beta=getattr(model,'beta',np.nan),
                        beta_factor=factors.get(method,np.nan),tau=getattr(model,'tau',np.nan),
                        depth=model.metadata.get('depth',0),branch=model.metadata.get('branch','ridge'),
                        sieve_size=model.metadata.get('sieve_size',np.nan),seconds=model.metadata['full_pipeline_seconds'],
                        beta_cap_hit=model.metadata.get('beta_cap_hit',False)))
            pd.DataFrame(rows).to_csv(OUT/f'{part}_replicates.csv',index=False)
    df=pd.DataFrame(rows);summaries=[]
    for keys,group in df.groupby(['part','dgp','n','r','N','method']):
        row=dict(zip(['part','dgp','n','r','N','method'],keys))
        row.update(exposure(int(row['n']),int(row['r']),int(row['N'])))
        for metric in ['risk','risk_normalized','risk_over_shape','nll','delta_nll','nll_shrunk','delta_shrunk','unseen_items','seconds']:
            mean,lo,hi=mean_ci(group[metric]);row.update({metric:mean,metric+'_lo':lo,metric+'_hi':hi})
        row.update(repetitions=len(group),depth_max=int(group.depth.max()),sieve_size=group.sieve_size.mean())
        summaries.append(row)
    pd.DataFrame(summaries).to_csv(OUT/f'{part}_summary.csv',index=False)

def group_ci(values,groups,seed,resamples=2000):
    frame=pd.DataFrame({'value':values,'group':groups})
    stats=frame.groupby('group').value.agg(['sum','count']);rng=np.random.default_rng(seed)
    idx=rng.integers(len(stats),size=(resamples,len(stats)))
    boot=stats['sum'].to_numpy()[idx].sum(axis=1)/stats['count'].to_numpy()[idx].sum(axis=1)
    return np.quantile(boot,[.025,.975])

def real_data():
    rows=[];audit_rows=[];params={};test_rows=[]
    for data,budgets in [(load_beans(),[2,5,10,14,30,100]),(load_sushi('b'),[5,10,25,50,100,300])]:
        pool,test_idx=outer_split(data)
        for rep in range(5):
            indices=np.random.default_rng(SEED+rep).permutation(pool)
            for N in budgets:
                print(f'real {data.name} N={N} rep={rep}',flush=True)
                train,test=data.y[indices[:N]],data.y[test_idx]
                methods=['efficient','mle' if data.n<=18 else 'insertion']
                models,losses,factors=compare(train,test,data.n,SEED+rep,methods)
                base=dict(dataset=data.name,rep=rep,**exposure(data.n,train.shape[1],N),**actual_exposure(train,data.n))
                audit_rows.append(base)
                for method,loss in losses.items():
                    rows.append(dict(**base,method=method,nll=loss.mean(),delta=(loss-losses['pl']).mean()))
                    test_rows.extend(dict(dataset=data.name,N=N,rep=rep,method=method,test_index=int(i),loss=float(v)) for i,v in zip(test_idx,loss))
                params[f'{data.name}_{rep}_{N}']=dict(train_indices=indices[:N].tolist(),test_indices=test_idx.tolist(),
                    pl_theta=models['pl'].theta.tolist(),tau=models['pl'].tau,
                    sm={m:dict(order=models[m].order.tolist(),beta=models[m].beta,factor=factors[m],metadata=models[m].metadata) for m in factors})
        pd.DataFrame(rows).to_csv(OUT/'real_replicates.csv',index=False)
    pd.DataFrame(audit_rows).to_csv(OUT/'real_exposure.csv',index=False);js(OUT/'real_parameters.json',params)
    testdf=pd.DataFrame(test_rows);summary=[]
    for keys,group in testdf.groupby(['dataset','N']):
        means=group.groupby(['method','test_index']).loss.mean().unstack(0)
        for method in means:
            delta=means[method]-means.pl;lo,hi=group_ci(delta.to_numpy(),means.index.to_numpy(),SEED)
            summary.append(dict(dataset=keys[0],N=keys[1],method=method,nll=means[method].mean(),delta=delta.mean(),lo=lo,hi=hi))
    pd.DataFrame(summary).to_csv(OUT/'real_summary.csv',index=False)

def tennis():
    folder=download_tennis();rows=[];audits=[];params={};pred_rows=[]
    for year in range(2010,2020):
        d=chronological_year(year,folder);n,train,test=d['n'],d['train'],d['test']
        print(f'tennis {year}: n={n} N={len(train)} test={len(test)}',flush=True)
        models,losses,factors=compare(train,test,n,SEED+year,['efficient','insertion'],inner=(d['inner_train'],d['inner_valid']))
        info=dict(year=year,**exposure(n,2,len(train)),**actual_exposure(train,n))
        audits.append(dict(**d['audit'],exposure=info))
        for target,mask in [('seen',d['test_seen']),('all_catalog',np.ones(len(test),bool))]:
            for method,loss in losses.items():
                delta=(loss-losses['pl'])[mask];lo,hi=group_ci(delta,d['groups'][mask],SEED+year)
                rows.append(dict(**info,target=target,method=method,test_matches=int(mask.sum()),
                    nll=loss[mask].mean(),brier=np.mean((1-np.exp(-loss[mask]))**2),delta=delta.mean(),lo=lo,hi=hi))
        outcome=(test[:,0]<test[:,1]).astype(int)
        for method,loss in losses.items():
            pwin=np.exp(-loss);prob=np.where(outcome==1,pwin,1-pwin)
            pred_rows.extend(dict(year=year,method=method,test_index=i,group=g,surface=s,seen=bool(seen),
                outcome=int(a),probability=float(p),nll=float(v),
                abs_pl_log_odds=float(abs(models['pl'].theta[y[0]]-models['pl'].theta[y[1]])))
                for i,(g,s,seen,a,p,v,y) in enumerate(zip(d['groups'],d['surface'],d['test_seen'],outcome,prob,loss,test)))
        params[str(year)]=dict(pl_theta=models['pl'].theta.tolist(),tau=models['pl'].tau,
            sm={m:dict(order=models[m].order.tolist(),beta=models[m].beta,factor=factors[m],metadata=models[m].metadata) for m in factors})
        pd.DataFrame(rows).to_csv(OUT/'tennis_by_year.csv',index=False)
        js(OUT/'tennis_audit.json',audits);js(OUT/'tennis_parameters.json',params)
    pd.DataFrame(pred_rows).to_csv(OUT/'tennis_predictions.csv',index=False)
    summary=[]
    for keys,group in pd.DataFrame(rows).groupby(['target','method']):
        mean,lo,hi=mean_ci(group.delta)
        summary.append(dict(target=keys[0],method=keys[1],years=len(group),delta=mean,lo=lo,hi=hi,
            nll=group.nll.mean(),brier=group.brier.mean(),test_matches=int(group.test_matches.sum())))
    pd.DataFrame(summary).to_csv(OUT/'tennis_summary.csv',index=False)

def feasibility():
    rows=[]
    for n in [8,64,512,4096]:
        for r in [2,min(8,n),min(32,n)]:
            for lam in [.03,.3,1,3]:
                N=max(1,round(lam*n*(n-1)/(r*(r-1))))
                stages=schedule(n,r,N,min(N*r*(r-1)/(n*(n-1)),1))
                rows.append(dict(**exposure(n,r,N),initial_depth=len(stages),
                    required_pilot_reports=sum(s['batch'] for s in stages),half_sample=N//2,
                    initial_schedule_fits=sum(s['batch'] for s in stages)<=N//2,exact_sieve_available=n<=8))
    pd.DataFrame(rows).drop_duplicates().to_csv(OUT/'schedule_feasibility.csv',index=False)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--part',choices=['small','coverage','real','tennis','all'],default='all')
    ap.add_argument('--reps',type=int,default=30);args=ap.parse_args();OUT.mkdir(parents=True,exist_ok=True)
    protocol=ROOT/'docs/protocols/EXPOSURE_PROTOCOL.md'
    js(OUT/f'run_{args.part}.json',dict(seed=SEED,part=args.part,repetitions=args.reps,
        protocol_sha256=hashlib.sha256(protocol.read_bytes()).hexdigest(),recovered_runner=True))
    feasibility()
    for part in (['small','coverage','real','tennis'] if args.part=='all' else [args.part]):
        if part in ['small','coverage']:simulate(part,args.reps)
        elif part=='real':real_data()
        else:tennis()
