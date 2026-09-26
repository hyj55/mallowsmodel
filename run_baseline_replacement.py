"""Frozen, original-data replacement of historical Beans/Sushi fits."""
import json
from pathlib import Path
import time
import numpy as np
import pandas as pd
from src.data import load_all, audit, save_manifest
from src.strict_models import fit_sm_strict, fit_pl_mm
from run_strict_real import ci

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'results/baseline_replacement'
SEED = 202609253


def run():
    OUT.mkdir(parents=True, exist_ok=True)
    tasks = load_all()
    scores, splits, descriptions, parameters = [], [], [], {}
    for task in tasks:
        print('BASELINE', task.name, flush=True)
        N, r, n = len(task.y), task.y.shape[1], task.n
        seed = np.random.SeedSequence([SEED, 0 if task.name == 'beans' else 1])
        indices = np.random.default_rng(seed).permutation(N)
        a, b = int(.6*N), int(.8*N)
        parts = {'fit': indices[:a], 'discovery': indices[a:b], 'confirmation': indices[b:]}
        for split, rows in parts.items():
            splits.extend(dict(dataset=task.name, row=int(i), split=split) for i in rows)
        train, test = task.y[parts['fit']], task.y[parts['confirmation']]
        info = audit(task)
        info.update(N_train=len(train), N_discovery=b-a, N_test=N-b,
                    lambda_=len(train)*r*(r-1)/(n*(n-1)), mu=len(train)*r/n,
                    uncertainty_status='unavailable_assessor_ids' if task.name=='beans' else 'conditional_respondent_bootstrap')
        descriptions.append(info)
        parameters[task.name] = {}
        models = {}
        for method in ['pl', 'mle', 'sharp', 'efficient', 'borda']:
            start = time.perf_counter()
            fit = fit_pl_mm(train, n) if method == 'pl' else fit_sm_strict(
                train, n, method, beta0=.1, pair_seed=SEED, milp_seconds=120.)
            models[method] = fit
            parameters[task.name][method] = dict(status=fit.status, order=fit.order,
                beta=fit.beta, theta=fit.theta, metadata=fit.metadata)
            print(' ', method, fit.status, flush=True)
            loss, delta = fit.nll(test), fit.nll(test)-models['pl'].nll(test)
            low, high = ci(delta, SEED, unit_identified=task.name!='beans')
            scores.append(dict(dataset=task.name, method=method, status=fit.status,
                               nll=float(loss.mean()), delta=float(delta.mean()), delta_lo=low,
                               delta_hi=high, seconds=time.perf_counter()-start,
                               uncertainty_status=info['uncertainty_status']))
        # Save after every task, including nonconvergence and solver failures.
        pd.DataFrame(scores).to_csv(OUT/'scores.csv', index=False)
        pd.DataFrame(splits).to_csv(OUT/'splits.csv', index=False)
        (OUT/'datasets.json').write_text(json.dumps(descriptions, indent=2)+'\n')
        def convert(value):
            if isinstance(value, np.ndarray):return value.tolist()
            if isinstance(value, np.generic):return value.item()
            raise TypeError(type(value))
        (OUT/'parameters.json').write_text(json.dumps(parameters, default=convert, indent=2)+'\n')
    save_manifest(OUT)
    print(pd.DataFrame(scores).to_string(index=False))


if __name__ == '__main__':
    run()
