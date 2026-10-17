"""E0 score estimators on the unchanged five empirical allocations."""
import gzip
import hashlib
import io
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .manuscript_estimators import block_scores, efficient_center, score_order
from .models import kendall
from .predictive_models import sm_fit
from .predictive_study import array_hash, empirical_context, paired_bootstrap, BOOTSTRAP_SEED
from .repeated_holdout import ROOT, json_value, restore_fit, save_fit
from .strict_models import TIE_SEED

PUBLIC = ROOT / 'results/estimator_comparison'
PRIVATE = ROOT / 'results/private/estimator_comparison'
METHODS = ('pl', 'sm_likelihood', 'sm_sharp', 'sm_fotakis',
           'sm_efficient', 'sm_global_borda')
SCORE_METHODS = ('sm_efficient', 'sm_global_borda')
SOURCES = ('results/predictive/predictors.jsonl.gz',
           'results/predictive/repeat_scores.csv.gz')
CODE = ('src/estimator_comparison.py', 'run_estimator_comparison.py',
        'src/manuscript_estimators.py', 'src/predictive_models.py',
        'src/predictive_study.py', 'src/repeated_holdout.py',
        'src/models.py', 'src/strict_models.py')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def code_hashes():
    return {p: digest(ROOT/p) for p in CODE}


def compressed(data):
    out = io.BytesIO()
    with gzip.GzipFile(filename='', mode='wb', fileobj=out, mtime=0) as stream:
        stream.write(data)
    return out.getvalue()


def source_records():
    with gzip.open(ROOT/SOURCES[0], 'rt') as stream:
        records = [json.loads(line) for line in stream]
    records = sorted((r for r in records if r['study'] == 'P0'),
                     key=lambda r: (r['dataset'], r['repeat']))
    assert len(records) == 115
    assert len({(r['dataset'], r['repeat']) for r in records}) == 115
    return records


def fit_score_estimators(y, n):
    """Training-only construction; admission never depends on Sharp or test loss."""
    N, r = y.shape
    lam = N*r*(r-1)/(n*(n-1))
    priority = np.random.default_rng(TIE_SEED).permutation(n)
    scores = block_scores(y, np.arange(n), n, r)
    order = score_order(y, np.arange(n), n, r, priority)
    meta = dict(path='global_clipped_normalized_borda', tie_seed=TIE_SEED,
                lambda_=lam, score_ties=n-len(np.unique(scores)),
                center_reports=N, reference='M Proposition 2.14 and equation (3.4)')
    borda = sm_fit('sm_global_borda', y, order, meta)
    if N*r*(r-1) > n*(n-1):
        efficient = sm_fit('sm_efficient', y, None,
            dict(status='outside_schedule_domain', lambda_=lam, depth=None,
                 tie_seed=TIE_SEED, beta0=.1,
                 reason='Equation (3.23) requires lambda <= 1; no capped-resolution extension'))
    else:
        order, meta = efficient_center(y, n, seed=TIE_SEED, beta0=.1)
        meta.update(lambda_=lam, tie_seed=TIE_SEED, beta0=.1,
                    reference='M Algorithms 3.1/3.2 and equation (3.23)')
        efficient = sm_fit('sm_efficient', y, order, meta)
        if meta['depth'] == 0:
            np.testing.assert_array_equal(efficient.order, borda.order)
            assert efficient.beta == borda.beta
            assert efficient.metadata['training_distance'] == borda.metadata['training_distance']
            efficient.metadata['alias_of'] = 'sm_global_borda'
    return dict(sm_efficient=efficient, sm_global_borda=borda)


def execute(source, task, source_scores):
    key = f"{source['dataset']}-repeat{source['repeat']}"
    path = PRIVATE/(key+'.json.gz')
    fingerprint = dict(code=code_hashes(), sources={p:digest(ROOT/p) for p in SOURCES})
    if path.exists():
        with gzip.open(path, 'rt') as stream:
            record = json.load(stream)
        assert record['fingerprint'] == fingerprint, 'Changed E0 producer: use a fresh cache'
        return record
    context = empirical_context(task, source['repeat'])
    hashes = {k:array_hash(v) for k,v in context['data'].items()}
    assert hashes == source['data_sha256']
    train, test = context['data']['development'], context['data']['test']
    train_units = task.units[context['parts']['development']]
    assert not np.intersect1d(train_units, context['units']).size
    fits = {m:restore_fit(source['models'][m]) for m in METHODS[:4]}
    fits.update(fit_score_estimators(train, task.n))
    losses = {m:fit.nll(test) for m,fit in fits.items()}
    for method in METHODS[:4]:
        old = source_scores[(source_scores.dataset == task.name)
                            & (source_scores['repeat'] == source['repeat'])
                            & (source_scores.method == method)].iloc[0]
        np.testing.assert_allclose(losses[method].mean(), old.nll, atol=2e-9, rtol=2e-9,
                                   equal_nan=True)
    intervals = {}
    if context['identified_units']:
        seed = np.random.SeedSequence([BOOTSTRAP_SEED, context['split_key'],
                                      context['repeat'], context['N']])
        intervals = paired_bootstrap(losses, context['units'], seed)
    scores = []
    template = source_scores[(source_scores.dataset == task.name)
                            & (source_scores['repeat'] == source['repeat'])
                            & (source_scores.method == 'pl')].iloc[0].to_dict()
    for method in METHODS:
        fit = fits[method]
        if method in METHODS[:4]:
            row = source_scores[(source_scores.dataset == task.name)
                                & (source_scores['repeat'] == source['repeat'])
                                & (source_scores.method == method)].iloc[0].to_dict()
        else:
            row = dict(template, method=method, status=fit.status,
                nll=float(losses[method].mean()), delta=float((losses[method]-losses['pl']).mean()),
                beta=fit.beta, tau=np.nan, certified=False, objective_gap=np.nan,
                branch=fit.metadata.get('branch', fit.metadata.get('path', '')),
                alias_of=fit.metadata.get('alias_of', ''),
                kendall=kendall(fit.order, context['truth']) if fit.status == 'ok'
                        and context['truth'] is not None else np.nan,
                ci_kind='conditional_test_unit_percentile' if method in intervals else 'unavailable',
                bootstrap_units=len(np.unique(context['units'])) if method in intervals else 0)
            row.update(intervals.get(method, dict(nll_ci_low=np.nan, nll_ci_high=np.nan,
                                                  delta_ci_low=np.nan, delta_ci_high=np.nan)))
        row.update(study='E0', raw_study='P0', depth=fit.metadata.get('depth', np.nan))
        scores.append(row)
    # Existing successful Efficient fallback fits must replay exactly under the
    # ungated candidate with the same training data, constants and tie priority.
    previous = restore_fit(source['models']['sm_efficient_fallback'])
    if previous.status == 'ok':
        np.testing.assert_array_equal(previous.order, fits['sm_efficient'].order)
        assert previous.beta == fits['sm_efficient'].beta
        np.testing.assert_array_equal(previous.nll(test), losses['sm_efficient'])
    record = dict(dataset=task.name, repeat=source['repeat'], study='E0', raw_study='P0',
        n=task.n, r=context['r'], N=context['N'], split_key=context['split_key'],
        identified_units=context['identified_units'], unit_description=context['unit_description'],
        data_sha256=hashes, fingerprint=fingerprint,
        models={m:save_fit(f) for m,f in fits.items()}, scores=scores,
        parts=context['parts'], losses=losses, test_units=context['units'])
    PRIVATE.mkdir(parents=True, exist_ok=True)
    path.write_bytes(compressed(json.dumps(json_value(record), sort_keys=True,
                                         allow_nan=False).encode()))
    return record


def score_frame(records):
    frame = pd.DataFrame([r for record in records for r in record['scores']])
    for column in ('nll','delta','beta','tau','objective_gap','kendall','depth',
                   'nll_ci_low','nll_ci_high','delta_ci_low','delta_ci_high'):
        frame[column] = pd.to_numeric(frame[column], errors='coerce')
    frame['alias_of'] = frame.alias_of.fillna('')
    return frame.sort_values(['dataset','repeat','method']).reset_index(drop=True)


def borda_comparisons(frame):
    """Paired differences across the same five allocations, never unpaired SEs."""
    rows = []
    for dataset, group in frame.groupby('dataset', sort=True):
        borda = group[group.method == 'sm_global_borda'].set_index('repeat')
        for method in METHODS[:-1]:
            other = group[group.method == method].set_index('repeat')
            ids = sorted(set(borda.index[borda.status == 'ok'])
                         & set(other.index[other.status == 'ok']))
            values = borda.loc[ids, 'nll'].to_numpy()-other.loc[ids, 'nll'].to_numpy()
            count = len(values)
            complete = count == 5
            rows.append(dict(dataset=dataset, reference=method, planned=5, available=count,
                delta_mean=float(values.mean()) if complete else np.nan,
                delta_mcse=float(values.std(ddof=1)/np.sqrt(5)) if complete else np.nan,
                delta_min=float(values.min()) if complete else np.nan,
                delta_max=float(values.max()) if complete else np.nan,
                delta_conditional_mean=float(values.mean()) if count else np.nan,
                lower_splits=int((values < -1e-12).sum()),
                equal_splits=int((np.abs(values) <= 1e-12).sum()),
                interval_target='fixed_data_partition_precision'))
    return pd.DataFrame(rows)


def export(records):
    assert len(records) == 115
    frame = score_frame(records)
    assert len(frame) == 690 and frame.groupby(['dataset','method']).size().eq(5).all()
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC/'repeat_scores.csv.gz').write_bytes(compressed(
        frame.to_csv(index=False, float_format='%.12g').encode()))
    public = [{k:v for k,v in r.items() if k not in ('parts','losses','test_units','scores')}
              for r in records]
    content = '\n'.join(json.dumps(json_value(r), sort_keys=True, allow_nan=False) for r in public)+'\n'
    (PUBLIC/'predictors.jsonl.gz').write_bytes(compressed(content.encode()))
    manifest = dict(study='E0', allocations=115, repetitions=5, tasks=23, score_rows=690,
        methods=list(METHODS), code_sha256=code_hashes(),
        source_sha256={p:digest(ROOT/p) for p in SOURCES},
        fitting='Fit global Borda and independently admitted Efficient on unchanged development reports; reuse saved comparators.',
        efficient_admission='lambda <= 1; independent of Sharp status; no domain extension',
        tie_seed=TIE_SEED, beta0=.1, beta_interval=[0,10],
        uncertainty='Five-allocation means and paired MCSE; 2000 conditional test-unit bootstrap draws per identified split.',
        published_sha256={p:digest(PUBLIC/p) for p in ('repeat_scores.csv.gz','predictors.jsonl.gz')})
    (PUBLIC/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    return frame
