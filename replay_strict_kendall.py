"""Recover S1/S2 distances, checking every reconstructed fit against saved NLL.

Positive finite SM beta permits exact algebraic recovery from its saved NLL.
PL and SM boundary fits instead replay the original deterministic estimator.
The original outputs are never overwritten; replayed parameter witnesses are saved.
"""
import argparse
import gzip
import json
import math
from pathlib import Path
import numpy as np
import pandas as pd
import build_heldout_kendall as audit
from run_strict_simulations import grid,SEED
from src.strict_features import small_law,draw_small,draw_large
from src.strict_models import fit_sm_strict,fit_pl_mm
from src.repeated_holdout import save_fit
from src.models import logz_mean,kendall
from src.heldout_kendall import beta_audit


def run(part):
    original=audit.frame(f'results/strict_features/{part}_replicates.csv')
    part_id={'bridge':0,'shell':1,'coverage':2}[part]
    witness=[]
    for (cell,rep),g in original.groupby(['cell','rep'],sort=True):
        n,r,N,family,value,shape=grid(part)[cell]
        streams=np.random.SeedSequence([SEED,part_id,int(cell),int(rep)]).spawn(4)
        trng,drng,erng,arng=[np.random.default_rng(s) for s in streams]
        truth=trng.permutation(n)
        train=draw_small(trng,N,truth,family,value,shape,r) if n==8 else draw_large(trng,N,truth,r,value,shape)
        if n==8:
            support,mass,_=small_law(n,r,family,value,shape);test=truth[support]
        else:
            test=draw_large(erng,2000,truth,r,value,shape);mass=None
        methods=['mle','sharp','efficient','borda'] if n==8 else ['efficient','borda']
        seeds={m:int(arng.integers(2**31)) for m in methods}
        base=dict(study='S1' if n==8 else 'S2',dataset=f'{part}-{shape}-{value:g}',
                  setting=f'cell{cell}-n{n}-r{r}-N{N}',cell=int(cell),part=part,repeat=int(rep),
                  split='population' if mass is not None else 'test',N=N,n=n,r=r,
                  source=f'results/strict_features/{part}_replicates.csv')
        for row in g.itertuples():
            beta0=.8 if row.method in ('sharp','efficient') else None
            truthbeta=.8 if family=='bridge' and value==0 else None
            if row.status=='ok' and row.method!='pl' and np.isfinite(row.beta) and row.beta>1e-8:
                mean=(row.nll-logz_mean(r,row.beta)[0])/row.beta
                assert -1e-6<=mean<=r*(r-1)/2+1e-6
                if mass is None:
                    total=int(round(mean*len(test)))
                    np.testing.assert_allclose(total/len(test),mean,atol=2e-7)
                    mean=total/len(test)
                else:total=math.nan
                audit.ROWS.append(dict(base,method=row.method,status='ok',nll=row.nll,
                    test_kendall_mean=mean,test_kendall_sum=total,evaluation_count=len(test),
                    evaluation_target='population' if mass is not None else 'test_reports',
                    recovery='SM_NLL_identity',true_center_kendall=row.risk,
                    **beta_audit(row.beta,beta0,truthbeta)))
            elif row.status!='ok':
                audit.add(base,row.method,dict(status=row.status,order=None,beta=row.beta),test,row.nll,mass,beta0,truthbeta)
            else:
                fit=fit_pl_mm(train,n) if row.method=='pl' else fit_sm_strict(train,n,row.method,pair_seed=seeds[row.method])
                assert fit.status=='ok',(part,cell,rep,row.method,fit.status)
                assert kendall(fit.order,truth)==row.risk,(part,cell,rep,row.method,'center mismatch')
                saved=save_fit(fit)
                rec=audit.add(base,row.method,saved,test,row.nll,mass,beta0,truthbeta)
                rec['recovery']='deterministic_fit_replay'
                witness.append(dict(cell=int(cell),repeat=int(rep),method=row.method,model=saved))
        if rep==39:
            print(part,'cell',cell+1,'/',len(grid(part)),flush=True)
            audit.output('strict_'+part)
            (audit.OUT/f'strict_{part}_witnesses.jsonl.gz').write_bytes(gzip.compress(
                ('\n'.join(json.dumps(a) for a in witness)+'\n').encode(),mtime=0))
    audit.output('strict_'+part)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('part',choices=['bridge','shell','coverage']);a=p.parse_args();run(a.part)
