"""Frozen finite-sample mechanism checks, with unchanged published estimators."""
import argparse
from concurrent.futures import ProcessPoolExecutor
import hashlib
import json
from pathlib import Path
import time

import numpy as np
import pandas as pd
from scipy.stats import t

from src.diagnostics import pair_arrays, context_slope
from src.models import kendall
from src.strict_features import small_law
from src.strict_models import fit_sm_strict, fit_pl_mm
from src.validation_extension import SEED, confounded_law, confounded_focal_contrast, wilson

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'results/validation_extension'
REPETITIONS = 200
BOOTSTRAPS = 499


def encode(x):
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, np.generic):
        return x.item()
    raise TypeError(type(x))


def job(args):
    family, setting, N, rep, cell = args
    start = time.perf_counter()
    stream = np.random.SeedSequence([SEED, 10, cell, rep])
    labels_rng, train_rng, diagnostic_rng = [np.random.default_rng(s) for s in stream.spawn(3)]
    n = 8 if family == 'calibration' else 4
    truth = labels_rng.permutation(n)
    if family == 'calibration':
        support, mass, _ = small_law(n, 3, 'bridge', setting, 'equal')
        support = truth[support]
        source_groups = np.zeros(len(support), int)
        name = 'sm' if setting == 0 else 'pl'
    else:
        support, mass, source_groups, _ = confounded_law(setting, truth)
        name = 'group_pl_mixture'
    train = support[train_rng.choice(len(support), N, p=mass)]
    indices = diagnostic_rng.choice(len(support), 1000, p=mass)
    reports, groups = support[indices], source_groups[indices]
    sm, pl = fit_sm_strict(train, n, 'mle'), fit_pl_mm(train, n)
    fits, parameters = [], {}
    for fit in [sm, pl]:
        loss = fit.nll(support)
        population_nll = float(mass@loss)
        fits.append(dict(family=family, generator=name, setting=setting, n=n, r=3,
                         N=N, lambda_=N*6/(n*(n-1)), mu=N*3/n, rep=rep, cell=cell,
                         method=fit.method, status=fit.status, nll=population_nll,
                         risk=kendall(fit.order, truth) if fit.status == 'ok' else np.nan))
        parameters[fit.method] = dict(order=fit.order, beta=fit.beta, theta=fit.theta,
                                     status=fit.status, metadata=fit.metadata)
    sm_loss, pl_loss = fits[0]['nll'], fits[1]['nll']
    winner = 'sm' if sm_loss < pl_loss else 'pl' if pl_loss < sm_loss else 'tie'
    if np.isnan(sm_loss) or np.isnan(pl_loss):
        winner = 'unavailable'
    diagnostics = []
    for M in [60, 200, 1000]:
        y, g = reports[:M], groups[:M]
        conditions = ['oracle', 'fitted'] if family == 'calibration' else ['pooled', 'group_adjusted']
        for condition in conditions:
            if condition == 'fitted':
                order, beta = sm.order, sm.beta
            else:
                order, beta = truth, .8
            base = dict(family=family, generator=name, setting=setting, N=N, M=M,
                        rep=rep, cell=cell, diagnostic=condition, population_winner=winner)
            if order is None or not np.isfinite(beta) or pl.status != 'ok':
                diagnostics.append({**base, 'status':'fit_unavailable'})
                continue
            arrays = pair_arrays(y, order, beta, pl.theta)
            result = context_slope(arrays, strata=g if condition == 'group_adjusted' else None,
                                   resamples=BOOTSTRAPS, seed=SEED+10000*cell+100*rep+M)
            choice, correct, regret = 'abstain', np.nan, np.nan
            reject_zero, positive, reject_sm = np.nan, np.nan, np.nan
            if result['status'] == 'ok' and np.isfinite(result['observed_lo']):
                positive = float(result['observed_lo'] > 0)
                reject_zero = float(result['observed_lo'] > 0 or result['observed_hi'] < 0)
                reject_sm = float(result['residual_vs_sm_lo'] > 0 or result['residual_vs_sm_hi'] < 0)
                if condition == 'fitted' and winner not in ['tie', 'unavailable']:
                    choice = 'sm' if abs(result['observed']-result['sm_predicted']) < abs(result['observed']) else 'pl'
                    correct = float(choice == winner)
                    selected = sm_loss if choice == 'sm' else pl_loss
                    regret = selected-min(sm_loss, pl_loss)
            diagnostics.append(dict(**base, **result, reject_zero=reject_zero, positive=positive,
                                    reject_sm=reject_sm, context_choice=choice,
                                    correct=correct, regret=regret))
    return dict(fits=fits, diagnostics=diagnostics,
                parameters=dict(family=family, setting=setting, N=N, rep=rep,
                                cell=cell, truth=truth, models=parameters),
                seconds=time.perf_counter()-start)


def summarize():
    d = pd.read_csv(OUT/'synthetic_diagnostics.csv')
    rows = []
    keys = ['family', 'generator', 'setting', 'N', 'M', 'diagnostic']
    for key, group in d.groupby(keys):
        row = dict(zip(keys, key))
        row.update(repetitions=len(group), available=int(group.observed.notna().sum()),
                   unavailable=int(group.observed.isna().sum()),
                   eligible_pairs_mean=group.eligible_pairs.mean(),
                   observed_mean=group.observed.mean(),
                   predicted_sm_mean=group.sm_predicted.mean(),
                   regret_mean=group.regret.mean())
        for metric in ['reject_zero', 'positive', 'reject_sm', 'correct']:
            values = group[metric].dropna()
            successes, count = int(values.sum()), len(values)
            lo, hi = wilson(successes, count)
            row.update({metric: successes/count if count else np.nan,
                        metric+'_lo':lo, metric+'_hi':hi, metric+'_available':count})
        rows.append(row)
    pd.DataFrame(rows).to_csv(OUT/'synthetic_diagnostic_summary.csv', index=False)
    f = pd.read_csv(OUT/'synthetic_fits.csv')
    paired = f.pivot(index=['family','generator','setting','N','rep','cell'], columns='method', values='nll').reset_index()
    paired['delta'] = paired.mle-paired.pl
    paired.to_csv(OUT/'synthetic_paired.csv', index=False)
    rows = []
    for key, group in paired.groupby(['family','generator','setting','N']):
        values = group.delta.to_numpy()
        finite = values[np.isfinite(values)]
        available = ~np.isnan(values)
        value = float(values.mean()) if available.all() else np.nan
        se = finite.std(ddof=1)/np.sqrt(len(finite)) if len(finite)>1 else np.nan
        half = t.ppf(.975,len(finite)-1)*se
        lo, hi = (value-half, value+half) if np.isfinite(values).all() else (np.nan,np.nan)
        rows.append(dict(zip(['family','generator','setting','N'],key)) |
                    dict(delta=value, delta_lo=lo, delta_hi=hi, finite_conditional_delta=finite.mean() if len(finite) else np.nan,
                         finite=len(finite), undefined=int((~available).sum()), infinite=int(np.isinf(values).sum()),
                         repetitions=len(values)))
    pd.DataFrame(rows).to_csv(OUT/'synthetic_prediction_summary.csv', index=False)
    controls = [dict(rho=rho, focal_pair_effect=confounded_focal_contrast(rho),
                     within_each_group_focal_effect=0.) for rho in [0,.45,.9]]
    pd.DataFrame(controls).to_csv(OUT/'confounding_population_controls.csv', index=False)


def save_draws():
    """Archive the exact frozen draws by replay, not an additional experiment."""
    train_rows, diagnostic_rows, group_rows, offsets, identifiers = [], [], [], [0], []
    records=[json.loads(line) for line in (OUT/'synthetic_parameters.jsonl').read_text().splitlines()]
    fits=pd.read_csv(OUT/'synthetic_fits.csv')
    expected=set(map(tuple,fits[['cell','rep']].drop_duplicates().to_numpy()))
    identifiers_in_log=[(item['cell'],item['rep']) for item in records]
    assert len(records)==len(expected)==1400
    assert len(set(identifiers_in_log))==len(records) and set(identifiers_in_log)==expected
    for item in records:
        family,setting,N,rep,cell=(item[k] for k in ['family','setting','N','rep','cell'])
        streams=np.random.SeedSequence([SEED,10,cell,rep]).spawn(3)
        labels_rng,train_rng,diagnostic_rng=[np.random.default_rng(s) for s in streams]
        n=8 if family=='calibration' else 4
        truth=labels_rng.permutation(n)
        if family=='calibration':
            support,mass,_=small_law(n,3,'bridge',setting,'equal')
            support=truth[support]; groups=np.zeros(len(support),int)
        else:
            support,mass,groups,_=confounded_law(setting,truth)
        train=support[train_rng.choice(len(support),N,p=mass)]
        indices=diagnostic_rng.choice(len(support),1000,p=mass)
        train_rows.append(train.astype(np.uint8))
        diagnostic_rows.append(support[indices].astype(np.uint8))
        group_rows.append(groups[indices].astype(np.uint8))
        offsets.append(offsets[-1]+N); identifiers.append([cell,rep])
    np.savez_compressed(OUT/'synthetic_draws.npz',train=np.concatenate(train_rows),
                        training_offsets=np.asarray(offsets),diagnostic=np.asarray(diagnostic_rows),
                        groups=np.asarray(group_rows),cell_rep=np.asarray(identifiers))


def run(workers):
    OUT.mkdir(parents=True, exist_ok=True)
    tasks, cell = [], 0
    for setting in [0., 1.]:
        for N in [28, 448]:
            tasks.extend(('calibration', setting, N, rep, cell) for rep in range(REPETITIONS))
            cell += 1
    for setting in [0., .45, .9]:
        tasks.extend(('confounding', setting, 448, rep, cell) for rep in range(REPETITIONS))
        cell += 1
    fits, diagnostics = [], []
    started = time.perf_counter()
    with (OUT/'synthetic_parameters.jsonl').open('w') as params:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            for done, answer in enumerate(executor.map(job, tasks), 1):
                fits.extend(answer['fits']); diagnostics.extend(answer['diagnostics'])
                params.write(json.dumps(answer['parameters'], default=encode)+'\n')
                if done % 100 == 0 or done == len(tasks):
                    params.flush()
                    pd.DataFrame(fits).to_csv(OUT/'synthetic_fits.csv', index=False)
                    pd.DataFrame(diagnostics).to_csv(OUT/'synthetic_diagnostics.csv', index=False)
                    print('SYNTHETIC',done,'/',len(tasks),'elapsed_seconds',round(time.perf_counter()-started,1),flush=True)
    summarize()
    save_draws()
    manifest = dict(seed=SEED, independent_training_datasets=len(tasks), repetitions=REPETITIONS,
                    bootstrap_draws=BOOTSTRAPS, diagnostic_rows=len(diagnostics),
                    nested_budgets=[60,200,1000], new_estimator_definitions=0,
                    seconds=time.perf_counter()-started,
                    protocol_sha256=hashlib.sha256((ROOT/'docs/protocols/VALIDATION_EXTENSION_20260926.md').read_bytes()).hexdigest())
    (OUT/'synthetic_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--workers',type=int,default=2)
    parser.add_argument('--summarize-only',action='store_true')
    parser.add_argument('--archive-only',action='store_true')
    args=parser.parse_args()
    if args.archive_only:
        save_draws()
    elif args.summarize_only:
        summarize()
    else:
        run(args.workers)
