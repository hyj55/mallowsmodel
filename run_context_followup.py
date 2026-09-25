"""Original-source audit and frozen wheat experiment; no observation repair.

Requires requirements-lock.txt plus rdata==1.0.0. Run from the repository root.
Raw source files remain ignored; only anonymous indices and summaries are saved.
"""
import ast
from collections import defaultdict
import hashlib
import itertools
import json
from pathlib import Path
import urllib.request
import warnings

import numpy as np
import pandas as pd
import rdata
from src.strict_models import fit_sm_strict, fit_pl_mm
from src.diagnostics import pair_arrays

ROOT = Path(__file__).resolve().parent
RAW = ROOT/'data/raw/context_followup'
OUT = ROOT/'results/context_followup'
SEED = 202609252
SOURCES = {
    'breadwheat.rda': 'AgrDataSci/gosset/bb5eb75c08fe3ab0f28931c093dcb66dea7c4185/data/breadwheat.rda',
    'breadwheat.R': 'AgrDataSci/gosset/bb5eb75c08fe3ab0f28931c093dcb66dea7c4185/R/breadwheat.R',
    'SP_Rank_Dataset.csv': 'amrit19/SP-Rank-Dataset/d9ceab3386ac04aca7791fd83da8508851f87dc9/SP_Rank_Dataset.csv',
    'sp_README.md': 'amrit19/SP-Rank-Dataset/d9ceab3386ac04aca7791fd83da8508851f87dc9/README.md',
}


def download():
    RAW.mkdir(parents=True, exist_ok=True)
    manifest = []
    for name, path in SOURCES.items():
        url = 'https://raw.githubusercontent.com/'+path
        file = RAW/name
        if not file.exists():
            file.write_bytes(urllib.request.urlopen(url, timeout=60).read())
        manifest.append(dict(file=name, url=url, sha256=hashlib.sha256(file.read_bytes()).hexdigest()))
    dest = ROOT/'data/context_followup_sources.json'
    if dest.exists():
        assert json.loads(dest.read_text()) == manifest, 'Source hash mismatch'
    else:
        dest.write_text(json.dumps(manifest, indent=2)+'\n')


def audit_sp():
    source = pd.read_csv(RAW/'SP_Rank_Dataset.csv')
    source = source[source.treatment.isin([4, 5, 6])].copy()
    source['cohort'] = np.where(source.workerid <= 720, 'four', 'five')
    rows = []
    for (cohort, domain), task in source.groupby(['cohort', 'domain']):
        gaps, displays = defaultdict(set), set()
        invalid = 0
        for record in task.itertuples():
            options, votes = sorted(ast.literal_eval(record.options)), ast.literal_eval(record.votes)
            invalid += int(sorted(votes) != options or len(set(options)) != len(options))
            displays.add(tuple(options))
            for a, b in itertools.combinations(range(len(options)), 2):
                gaps[(options[a], options[b])].add(b-a)
        rows.append(dict(cohort=cohort, domain=int(domain), reports=len(task),
                         participants=task.workerid.nunique(), invalid=invalid,
                         displays=len(displays), seen_items=len(set(itertools.chain.from_iterable(displays))),
                         pairs=len(gaps), varying_objective_gap_pairs=sum(len(v)>1 for v in gaps.values()),
                         fits=0, decision='not_informative_for_objective_gap_context_contrast'))
    pd.DataFrame(rows).to_csv(OUT/'sprank_audit.csv', index=False)


def village_weights(groups, seed):
    _, inverse = np.unique(groups, return_inverse=True)
    count = inverse.max()+1
    rng = np.random.default_rng(seed)
    return np.array([np.bincount(rng.integers(count, size=count), minlength=count)[inverse]
                     for _ in range(2000)])


def context(arrays, groups, weights, stratified=False):
    """Descriptive fixed-effect slope, with frozen eligibility and village bootstrap.

    Changes only the uncertainty unit relative to the earlier report bootstrap;
    this diagnostic is not a center estimator or a new probability model.
    """
    m, k = arrays['z'].shape
    h = arrays['gap'].ravel().astype(float)
    keys = np.column_stack([arrays['pair'].ravel(),
                            np.repeat(groups if stratified else np.zeros(m, int), k)])
    _, cell = np.unique(keys, axis=0, return_inverse=True)
    width = int(h.max())+1
    freq = np.bincount(cell*width+h.astype(int), minlength=(cell.max()+1)*width).reshape(-1, width)
    eligible = (freq >= 2).sum(axis=1) >= 2
    keep = eligible[cell]
    result = dict(eligible_cells=int(eligible.sum()), pair_observations=int(keep.sum()),
                  eligible_pairs=int(len(np.unique(arrays['pair'].ravel()[keep]))))
    if not keep.any():
        return dict(result, status='insufficient_within_cell_context_variation')
    _, c = np.unique(cell[keep], return_inverse=True)
    x = h[keep]
    report = np.repeat(np.arange(m), k)[keep]
    result['contributing_metadata_blocks'] = int(len(np.unique(groups[report])))
    result['interval_warning'] = ('single_block_no_between_cluster_information'
                                  if result['contributing_metadata_blocks'] < 2 else
                                  'working_interval_missing_village_and_fixed_training')
    z = np.column_stack([arrays[name].ravel()[keep] for name in ['z', 'sm', 'pl']])

    def slope(w):
        w = w[report]
        sw = np.bincount(c, weights=w)
        sx = np.bincount(c, weights=w*x)
        mean = np.divide(sx, sw, out=np.zeros_like(sx), where=sw>0)
        residual = x-mean[c]
        denominator = (w*residual**2).sum()
        return ((w*residual)[:, None]*z).sum(axis=0)/denominator if denominator>1e-12 else np.full(3, np.nan)

    estimate = slope(np.ones(m))
    samples = np.array([slope(w) for w in weights])
    samples = samples[np.isfinite(samples).all(axis=1)]
    result.update(status='ok', valid_bootstraps=len(samples))
    for j, name in enumerate(['observed', 'sm_predicted', 'pl_predicted']):
        result[name] = float(estimate[j])
        result[name+'_lo'], result[name+'_hi'] = np.quantile(samples[:, j], [.025, .975]) if len(samples) else (np.nan, np.nan)
    for j, name in [(1, 'residual_vs_sm'), (2, 'residual_vs_pl')]:
        result[name] = float(estimate[0]-estimate[j])
        result[name+'_lo'], result[name+'_hi'] = np.quantile(samples[:, 0]-samples[:, j], [.025, .975]) if len(samples) else (np.nan, np.nan)
    return result


def run():
    OUT.mkdir(parents=True, exist_ok=True)
    download()
    audit_sp()
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', UserWarning)
        data = rdata.read_rda(RAW/'breadwheat.rda')['breadwheat']
    shown = data[['variety_a', 'variety_b', 'variety_c']].astype(str).to_numpy()
    names = sorted(set(shown.ravel()))
    labels = {name: i for i, name in enumerate(names)}
    assert data.shape[0] == 493 and len(names) == 16
    reports = []
    for items, best, worst in zip(shown, data.overall_best, data.overall_worst):
        assert len(set(items)) == 3 and best in 'ABC' and worst in 'ABC' and best != worst
        b, w = 'ABC'.index(best), 'ABC'.index(worst)
        reports.append([labels[items[i]] for i in [b, 3-b-w, w]])
    y = np.asarray(reports)
    missing_village = data.village.isna().to_numpy()
    recorded_village = data.village.astype(str).to_numpy()
    recorded_village[missing_village] = '__UNKNOWN_METADATA_BLOCK__'
    _, village = np.unique(recorded_village, return_inverse=True)
    order = np.random.default_rng(SEED).permutation(len(y))
    parts = dict(fit=order[:295], discovery=order[295:394], confirmation=order[394:])
    assert len(np.unique(np.concatenate(list(parts.values())))) == len(y)
    pd.DataFrame([dict(row=int(i), village=int(village[i]), split=s) for s, ix in parts.items() for i in ix]).to_csv(OUT/'splits.csv', index=False)
    train = y[parts['fit']]
    coverage = dict(reports=len(y), n=16, r=3, N=len(train), lambda_=7.375, mu=55.3125,
                    distinct_displays=len(np.unique(np.sort(y, axis=1), axis=0)),
                    known_villages=int(data.village.nunique()), bootstrap_blocks=len(np.unique(village)),
                    missing_village=int(missing_village.sum()), reports_dropped=0,
                    missing_village_per_split={s:int(missing_village[ix].sum()) for s,ix in parts.items()},
                    villages_per_split={s:len(np.unique(village[ix])) for s,ix in parts.items()},
                    unseen_training_items=int((np.bincount(train.ravel(), minlength=16)==0).sum()))
    (OUT/'coverage.json').write_text(json.dumps(coverage, indent=2)+'\n')
    models = {'pl': fit_pl_mm(train, 16)}
    for method in ['mle', 'sharp', 'efficient', 'borda']:
        print('FIT', method, flush=True)
        models[method] = fit_sm_strict(train, 16, method, beta0=.1, pair_seed=SEED)
    params = {}
    for name, fit in models.items():
        params[name] = dict(status=fit.status, order=fit.order, beta=fit.beta,
                            theta=fit.theta, metadata=fit.metadata)
    def encode(x):
        if isinstance(x, np.ndarray): return x.tolist()
        if isinstance(x, np.generic): return x.item()
        raise TypeError(type(x))
    (OUT/'parameters.json').write_text(json.dumps(dict(items=names, models=params), default=encode, indent=2)+'\n')
    scores, contexts = [], []
    for split in ['discovery', 'confirmation']:
        ix = parts[split]
        weights = village_weights(village[ix], SEED+(split=='confirmation'))
        plloss = models['pl'].nll(y[ix])
        for method, fit in models.items():
            loss = fit.nll(y[ix]); delta = loss-plloss
            low, high = (np.quantile(weights@delta/weights.sum(axis=1), [.025, .975])
                         if np.isfinite(delta).all() else (np.nan, np.nan))
            scores.append(dict(split=split, method=method, status=fit.status, nll=loss.mean(),
                               delta=delta.mean(), delta_lo=low, delta_hi=high))
        if models['mle'].status == models['pl'].status == 'ok':
            arrays = pair_arrays(y[ix], models['mle'].order, models['mle'].beta, models['pl'].theta)
            for stratified in [False, True]:
                contexts.append(dict(split=split, village_fixed_effects=stratified,
                                     **context(arrays, village[ix], weights, stratified)))
    pd.DataFrame(scores).to_csv(OUT/'scores.csv', index=False)
    pd.DataFrame(contexts).to_csv(OUT/'context.csv', index=False)
    print(pd.DataFrame(scores).to_string(index=False))
    print(pd.DataFrame(contexts).to_string(index=False))


if __name__ == '__main__':
    run()
