"""Exploratory same-order sports and small-sample regularization checks."""
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.special import expit,gammaln
from src.data import ROOT,load_beans,load_sushi
from src.models import SMFit,distances,fit_beta,fit_pl,pl_nll
from src.tennis import chronological_year,download_tennis
from run_exposure import OUT,SEED,FACTORS,group_ci,js,mean_ci

def sm_given_order(y,order):
    D=int(distances(y,order).sum())
    return SMFit(order,fit_beta(D,len(y),y.shape[1]),D,{})

def sports():
    saved=json.loads((OUT/'tennis_parameters.json').read_text());folder=download_tennis()
    rows=[];matchrows=[]
    for year in range(2010,2020):
        d=chronological_year(year,folder);n=d['n'];param=saved[str(year)]
        theta=np.array(param['pl_theta']);order=np.argsort(-theta,kind='stable')
        inner_pl=fit_pl(d['inner_train'],n,param['tau'])
        inner=sm_given_order(d['inner_train'],inner_pl.order)
        factor=FACTORS[int(np.argmin([inner.nll(d['inner_valid'],f).mean() for f in FACTORS]))]
        sm=sm_given_order(d['train'],order);mask=d['test_seen']
        test=d['test'][mask];groups=d['groups'][mask];pl_loss=pl_nll(test,theta)
        for name,f in [('same_order',1.),('same_order_shrunk',factor)]:
            loss=sm.nll(test,f);delta=loss-pl_loss;lo,hi=group_ci(delta,groups,SEED+year)
            rows.append(dict(year=year,method=name,beta=sm.beta,factor=f,nll=loss.mean(),delta=delta.mean(),lo=lo,hi=hi))
        gap=theta[test[:,0]]-theta[test[:,1]]
        for i in range(len(test)):
            matchrows.append(dict(year=year,group=str(year)+'_'+str(groups[i]),gap=abs(gap[i]),
                favorite_win=int(gap[i]>0),tied=bool(gap[i]==0),pl_probability=expit(abs(gap[i])),
                sm_probability=expit(sm.beta*factor),delta=sm.nll(test[i:i+1],factor)[0]-pl_loss[i]))
    pd.DataFrame(rows).to_csv(OUT/'tennis_same_order_by_year.csv',index=False);summary=[]
    for method,g in pd.DataFrame(rows).groupby('method'):
        mean,lo,hi=mean_ci(g.delta);summary.append(dict(method=method,delta=mean,lo=lo,hi=hi,nll=g.nll.mean()))
    pd.DataFrame(summary).to_csv(OUT/'tennis_same_order_summary.csv',index=False)
    df=pd.DataFrame(matchrows)
    df['bin']=pd.cut(df.gap,[0,.5,1,1.5,np.inf],right=False,labels=['0–0.5','0.5–1','1–1.5','1.5+'])
    bins=[]
    for name,g in df.loc[~df.tied].groupby('bin',observed=True):
        lo,hi=group_ci(g.favorite_win,g.group,SEED)
        bins.append(dict(gap_bin=name,count=len(g),observed=g.favorite_win.mean(),lo=lo,hi=hi,
            PL=g.pl_probability.mean(),SM_same_order=g.sm_probability.mean(),delta=g.delta.mean(),tied_total=int(df.tied.sum())))
    pd.DataFrame(bins).to_csv(OUT/'tennis_strength_bins.csv',index=False)
    original=pd.read_csv(OUT/'tennis_predictions.csv');calibration=[]
    for method,g in original[original.seen].groupby('method'):
        g=g.sort_values('probability',kind='stable')
        for k,idx in enumerate(np.array_split(np.arange(len(g)),10)):
            b=g.iloc[idx];lo,hi=group_ci(b.outcome,b.year.astype(str)+'_'+b.group,SEED+k)
            calibration.append(dict(method=method,bin=k,count=len(b),predicted=b.probability.mean(),observed=b.outcome.mean(),lo=lo,hi=hi))
    pd.DataFrame(calibration).to_csv(OUT/'tennis_calibration.csv',index=False)

def real_penalties():
    saved=json.loads((OUT/'real_parameters.json').read_text())
    datasets={d.name:d for d in [load_beans(),load_sushi('b')]};rows=[]
    for key,param in saved.items():
        name,rep,N=key.rsplit('_',2);data=datasets[name]
        train=data.y[param['train_indices']];test=data.y[param['test_indices']]
        losses={'pl_tuned':pl_nll(test,np.array(param['pl_theta'])),
                'uniform':np.repeat(gammaln(test.shape[1]+1),len(test))}
        for tau in [1.,10.]:losses[f'pl_fixed_{int(tau)}']=fit_pl(train,data.n,tau).nll(test)
        for method,p in param['sm'].items():
            sm=SMFit(np.array(p['order']),p['beta'],0,{})
            losses[method+'_shrunk']=sm.nll(test,p['factor'])
        for method,loss in losses.items():
            rows.extend(dict(dataset=name,N=int(N),rep=int(rep),method=method,index=i,loss=float(v))
                        for i,v in zip(param['test_indices'],loss))
    summary=[]
    for keys,g in pd.DataFrame(rows).groupby(['dataset','N']):
        means=g.groupby(['index','method']).loss.mean().unstack(1)
        for method in means:
            row=dict(dataset=keys[0],N=keys[1],method=method,nll=means[method].mean())
            for comparator in ['pl_tuned','pl_fixed_1','pl_fixed_10','uniform']:
                delta=means[method]-means[comparator];lo,hi=group_ci(delta,means.index,SEED)
                row.update({comparator+'_delta':delta.mean(),comparator+'_lo':lo,comparator+'_hi':hi})
            summary.append(row)
    pd.DataFrame(summary).to_csv(OUT/'real_penalty_sensitivity.csv',index=False)

if __name__=='__main__':
    sports();real_penalties()
    protocol=ROOT/'docs/protocols/EXPOSURE_FOLLOWUP.md'
    js(OUT/'followup_manifest.json',dict(seed=SEED,exploratory=True,
        protocol_sha256=hashlib.sha256(protocol.read_bytes()).hexdigest()))
