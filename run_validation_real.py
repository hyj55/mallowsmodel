"""Original Sounds/Patras reports; beach source exclusion is frozen before fits."""
import hashlib
import json
from pathlib import Path
import time

import numpy as np
import pandas as pd

from src.models import pair_counts, kendall
from src.strict_models import fit_sm_strict, fit_pl_mm
from src.diagnostics import pair_arrays, context_slope, shell_decomposition
from src.validation_extension import SEED, real_tasks, split_units, unit_interval
from run_validation_synthetic import encode

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results/validation_extension'


def run():
    OUT.mkdir(parents=True,exist_ok=True)
    scores, descriptions, splits, predictions, profiles, contexts, shells = ([] for _ in range(7))
    parameters={}
    for task in real_tasks():
        name,n,r=task['name'],task['n'],task['r']
        y,groups=task['y'],task['groups']
        print('REAL',name,flush=True)
        desc=dict(dataset=name,reports=len(y),assessors=len(np.unique(groups)),n=n,r=r,
                  distinct_displays=len(np.unique(np.sort(y,axis=1),axis=0)),
                  eligible=task['eligible'],unit=task['unit'],
                  objective_reference_available=task['truth'] is not None)
        if not task['eligible']:
            desc.update(status='excluded_upstream_response_filtering',fits=0)
            descriptions.append(desc)
            for method in ['pl','mle','sharp','efficient','borda']:
                scores.append(dict(dataset=name,method=method,status=desc['status'],
                                   nll=np.nan,delta=np.nan,delta_lo=np.nan,delta_hi=np.nan))
            continue
        parts=split_units(task,task['source_index'])
        for split,ids in parts.items():
            splits.extend(dict(dataset=name,record=int(i),unit=int(groups[i]),split=split) for i in ids)
        train,discovery,test=(y[parts[s]] for s in ['fit','discovery','confirmation'])
        w=pair_counts(train,n)
        observed=(w+w.T)[np.triu_indices(n,1)]
        desc.update(status='included',fits=5,N=len(train),N_discovery=len(discovery),N_confirmation=len(test),
                    confirmation_units=len(np.unique(groups[parts['confirmation']])),
                    lambda_=len(train)*r*(r-1)/(n*(n-1)),mu=len(train)*r/n,
                    observed_training_pairs=int((observed>0).sum()),
                    reports_dropped=0,unseen_training_items=int((np.bincount(train.ravel(),minlength=n)==0).sum()))
        descriptions.append(desc)
        models={};parameters[name]={}
        for method in ['pl','mle','sharp','efficient','borda']:
            started=time.perf_counter()
            fit=fit_pl_mm(train,n) if method=='pl' else fit_sm_strict(train,n,method,beta0=.1,pair_seed=SEED+task['source_index'])
            elapsed=time.perf_counter()-started
            models[method]=fit
            parameters[name][method]=dict(order=fit.order,theta=fit.theta,beta=fit.beta,status=fit.status,metadata=fit.metadata)
            loss=fit.nll(test);delta=loss-models['pl'].nll(test)
            ci=unit_interval(delta,groups[parts['confirmation']],SEED+task['source_index'])
            scores.append(dict(dataset=name,method=method,status=fit.status,
                               nll=float(loss.mean()),delta=float(delta.mean()),delta_lo=ci['lo'],delta_hi=ci['hi'],
                               valid_bootstraps=ci['valid_bootstraps'],seconds=elapsed,
                               objective_kendall=kendall(fit.order,task['truth']) if fit.status=='ok' and task['truth'] is not None else np.nan))
            predictions.extend(dict(dataset=name,method=method,record=int(i),unit=int(groups[i]),nll=float(x))
                               for i,x in zip(parts['confirmation'],loss))
            print(' ',method,fit.status,flush=True)
        sm,pl=models['mle'],models['pl']
        if sm.status==pl.status=='ok' and np.isfinite(sm.beta):
            for split in ['discovery','confirmation']:
                ids=parts[split];held=y[ids];held_groups=groups[ids]
                if r==2:
                    # Entire reports are pairs; no independence is asserted within an assessor.
                    training=pair_arrays(train,sm.order,sm.beta,pl.theta)
                    cuts=np.quantile(training['worth_gap'],[1/3,2/3])
                    arrays=pair_arrays(held,sm.order,sm.beta,pl.theta)
                    bins=np.searchsorted(cuts,arrays['worth_gap'][:,0],side='right')
                    for index in range(3):
                        mask=bins==index
                        ci=unit_interval(arrays['z'][:,0]*mask,held_groups,
                                         SEED+task['source_index']+index,denominator=mask)
                        profiles.append(dict(dataset=name,split=split,bin=index,reports=int(mask.sum()),
                                             assessors=int(len(np.unique(held_groups[mask]))),
                                             observed=float(arrays['z'][mask].mean()) if mask.any() else np.nan,
                                             observed_lo=ci['lo'],observed_hi=ci['hi'],
                                             sm=float(arrays['sm'][mask].mean()) if mask.any() else np.nan,
                                             pl=float(arrays['pl'][mask].mean()) if mask.any() else np.nan,
                                             lower_cut=cuts[0],upper_cut=cuts[1]))
                else:
                    comp=shell_decomposition(held,sm.order,sm.beta,pl.theta)
                    for component in ['total','shell_mass','within_shell']:
                        ci=unit_interval(comp[component],held_groups,SEED+task['source_index'])
                        shells.append(dict(dataset=name,split=split,component=component,
                                           value=comp[component].mean(),lo=ci['lo'],hi=ci['hi']))
                    for reference,order in [('fitted',sm.order),('objective',task['truth'])]:
                        arrays=pair_arrays(held,order,sm.beta,pl.theta)
                        result=context_slope(arrays,resamples=2000,seed=SEED+task['source_index'])
                        contexts.append(dict(dataset=name,split=split,reference=reference,**result))
        for filename,rows in [('real_scores',scores),('real_datasets',descriptions),('real_splits',splits),
                              ('real_predictions',predictions),('real_pair_profiles',profiles),
                              ('real_context',contexts),('real_shells',shells)]:
            pd.DataFrame(rows).to_csv(OUT/(filename+'.csv'),index=False)
        (OUT/'real_parameters.json').write_text(json.dumps(parameters,default=encode,indent=2)+'\n')
    manifest=dict(seed=SEED,included_tasks=3,source_exclusions=1,eligible_original_reports=2164,
                  deleted_eligible_reports=0,pre_fit_protocol_commit='ddad79788574374d3c31699c74a145ff75d9008f',
                  pre_fit_source_amendment_commit='6e3cef2e97978153f5c4c6911f5a62b94d905bd0',
                  protocol_sha256=hashlib.sha256((ROOT/'docs/protocols/VALIDATION_EXTENSION_20260926.md').read_bytes()).hexdigest())
    (OUT/'real_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(pd.DataFrame(scores).to_string(index=False),flush=True)


if __name__=='__main__':
    run()
