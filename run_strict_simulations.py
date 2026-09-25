"""Run STRICT_FEATURE_PROTOCOL.md; unsuccessful estimates remain recorded."""
import argparse
import hashlib
import json
from pathlib import Path
import time
import numpy as np
import pandas as pd
from scipy.stats import t as student_t
from src.strict_models import fit_sm_strict, fit_pl_mm
from src.strict_features import (small_law, draw_small, draw_large,
                                 population_features, discovery_choices)
from src.models import kendall

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'results/strict_features'
SEED = 202609251


def grid(part):
    if part == 'bridge':
        return [(8, r, N, 'bridge', a, shape) for r in [2, 3]
                for shape in ['equal', 'alternating'] for a in [0., .25, .5, .75, 1.]
                for N in [8, 28, 112, 448]]
    if part == 'shell':
        return [(8, 3, N, 'shell', h, shape) for shape in ['equal', 'alternating']
                for h in [0., .5, 1., 2., 4.] for N in [28, 112, 448]]
    if part == 'coverage':
        return [(32, 3, N, 'bridge', a, 'equal') for a in [0., .5, 1.]
                for N in [40, 160, 640]]
    raise ValueError(part)


def finite_summary(v, prefix):
    v = np.asarray(v, float)
    finite = v[np.isfinite(v)]
    row = {prefix+'_defined': int((~np.isnan(v)).sum()),
           prefix+'_infinite': int(np.isinf(v).sum()), prefix+'_finite': len(finite)}
    row[prefix] = float(v.mean()) if not np.isnan(v).any() else np.nan
    if len(finite):
        mean = finite.mean()
        half = student_t.ppf(.975, len(finite)-1)*finite.std(ddof=1)/np.sqrt(len(finite)) if len(finite)>1 else np.nan
        row.update({prefix+'_finite_conditional': mean,
                    prefix+'_finite_conditional_lo': mean-half,
                    prefix+'_finite_conditional_hi': mean+half})
        if len(finite) == len(v):
            row.update({prefix+'_lo': mean-half, prefix+'_hi': mean+half})
    return row


def summarize(part):
    df = pd.read_csv(OUT/f'{part}_replicates.csv')
    keys = ['family', 'n', 'r', 'N', 'value', 'shape', 'method']
    rows = []
    for key, g in df.groupby(keys):
        row = dict(zip(keys, key)); row['repetitions'] = len(g)
        row.update(lambda_=g.lambda_.iloc[0], mu=g.mu.iloc[0],
                   ok=int((g.status == 'ok').sum()), statuses=json.dumps(g.status.value_counts().to_dict()))
        for metric in ['risk', 'nll', 'delta', 'seconds']:
            row.update(finite_summary(g[metric], metric))
        rows.append(row)
    pd.DataFrame(rows).to_csv(OUT/f'{part}_summary.csv', index=False)
    selections = pd.read_csv(OUT/f'{part}_selection_replicates.csv')
    keys = keys[:-1]
    rows = []
    for key, g in selections.groupby(keys):
        for selector in ['pair', 'context']:
            row = dict(zip(keys, key)); row.update(selector=selector, repetitions=len(g))
            row['abstentions'] = int((g[selector+'_choice'] == 'abstain').sum())
            row['selected_sm'] = int((g[selector+'_choice'] == 'sm').sum())
            for metric in [selector+'_selected_nll', selector+'_regret', selector+'_correct']:
                row.update(finite_summary(g[metric], metric))
            rows.append(row)
    pd.DataFrame(rows).to_csv(OUT/f'{part}_selection_summary.csv', index=False)


def run(part, repetitions=40):
    OUT.mkdir(parents=True, exist_ok=True)
    rows, selection_rows, features = [], [], []
    start = time.time()
    part_id = {'bridge': 0, 'shell': 1, 'coverage': 2}[part]
    for cell, (n, r, N, family, value, shape) in enumerate(grid(part)):
        print(part, cell+1, '/', len(grid(part)), n, r, N, family, value, shape, flush=True)
        feature = population_features(n, r, family, value, shape)
        features.append(dict(n=n, r=r, N=N, family=family, value=value, shape=shape, **feature))
        for rep in range(repetitions):
            seed = np.random.SeedSequence([SEED, part_id, cell, rep])
            trng, drng, erng, arng = [np.random.default_rng(x) for x in seed.spawn(4)]
            truth = trng.permutation(n)
            def generate(rng, count):
                if n == 8:
                    return draw_small(rng, count, truth, family, value, shape, r)
                return draw_large(rng, count, truth, r, value, shape)
            train, discovery = generate(trng, N), generate(drng, 1000)
            if n == 8:
                canonical, probability, _ = small_law(n, r, family, value, shape)
                test = truth[canonical]
            else:
                test = generate(erng, 2000)
                probability = np.full(len(test), 1/len(test))
            info = dict(part=part, cell=cell, rep=rep, family=family, value=value,
                        shape=shape, n=n, r=r, N=N, lambda_=N*r*(r-1)/(n*(n-1)),
                        mu=N*r/n, unseen_items=n-len(np.unique(train)))
            models, runtime = {}, {}
            t0 = time.perf_counter(); models['pl'] = fit_pl_mm(train, n)
            runtime['pl'] = time.perf_counter()-t0
            methods = ['mle', 'sharp', 'efficient', 'borda'] if n == 8 else ['efficient', 'borda']
            for method in methods:
                t0 = time.perf_counter()
                models[method] = fit_sm_strict(train, n, method, pair_seed=int(arng.integers(2**31)))
                runtime[method] = time.perf_counter()-t0
            losses = {name: float(probability@model.nll(test)) for name, model in models.items()}
            for method, model in models.items():
                risk = kendall(model.order, truth) if model.status == 'ok' else np.nan
                rows.append(dict(**info, method=method, status=model.status,
                    risk=risk, nll=losses[method], delta=losses[method]-losses['pl'],
                    beta=model.beta, seconds=runtime[method],
                    branch=model.metadata.get('branch', 'hunter_mm' if method == 'pl' else 'unavailable'),
                    depth=model.metadata.get('depth', np.nan),
                    iterations=model.metadata.get('iterations', np.nan),
                    gradient=model.metadata.get('gradient_per_report', np.nan)))
            primary = 'mle' if n == 8 else 'borda'
            choices = discovery_choices(discovery, models[primary], models['pl'])
            selection = dict(**info, primary_sm=primary, sm_nll=losses[primary],
                             pl_nll=losses['pl'], **choices)
            for name in ['pair', 'context']:
                choice = choices[name+'_choice']
                loss = losses[primary] if choice == 'sm' else (losses['pl'] if choice == 'pl' else np.nan)
                both = np.isfinite([losses[primary], losses['pl']]).all()
                selection[name+'_selected_nll'] = loss
                selection[name+'_regret'] = loss-min(losses[primary], losses['pl']) if both else np.nan
                selection[name+'_correct'] = float(loss <= min(losses[primary], losses['pl'])+1e-12) if both and choice != 'abstain' else np.nan
            selection_rows.append(selection)
        pd.DataFrame(rows).to_csv(OUT/f'{part}_replicates.csv', index=False)
        pd.DataFrame(selection_rows).to_csv(OUT/f'{part}_selection_replicates.csv', index=False)
        pd.DataFrame(features).to_csv(OUT/f'{part}_population_features.csv', index=False)
    summarize(part)
    manifest = dict(part=part, seed=SEED, repetitions=repetitions,
                    independent_datasets=len(selection_rows), seconds=time.time()-start,
                    protocol_sha256=hashlib.sha256((ROOT/'docs/protocols/STRICT_FEATURE_PROTOCOL.md').read_bytes()).hexdigest())
    (OUT/f'{part}_manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print('DONE', manifest, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--part', choices=['bridge', 'shell', 'coverage'], required=True)
    parser.add_argument('--reps', type=int, default=40)
    args = parser.parse_args()
    run(args.part, args.reps)
