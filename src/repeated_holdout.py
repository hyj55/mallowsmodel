"""Repeated estimation of the existing real comparison; unchanged fitting laws."""
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import rdata

from .data import load_all
from .diagnostics import pair_arrays, context_slope, shell_decomposition
from .models import pair_counts, validate_rankings, distances, kendall
from .strict_models import StrictFit, fit_pl_mm, fit_sm_strict, profile_beta_unbounded
from .strict_features import discovery_choices
from .validation_extension import real_tasks

ROOT = Path(__file__).resolve().parents[1]
SEED = 202609280
REPETITIONS = 30
METHODS = ('pl', 'mle', 'sharp', 'efficient', 'borda')
PROTOCOL_COMMIT = '3da7e993c9ce2ae23a85a418cfa19ac2b138f01d'
CORE_FILES = ('src/repeated_holdout.py', 'src/repeated_holdout_summary.py',
              'run_repeated_real.py', 'src/data.py', 'src/models.py',
              'src/strict_models.py', 'src/manuscript_estimators.py',
              'src/diagnostics.py', 'src/strict_features.py',
              'src/validation_extension.py', 'run_strict_real.py',
              'docs/protocols/REPEATED_HOLDOUT_20260928.md')


@dataclass
class Task:
    name: str
    study: str
    y: np.ndarray
    n: int
    units: np.ndarray
    split_key: int
    estimator_seed: int
    unit_description: str
    truth: object = None


def source_inventory():
    entries = []
    for manifest, folder in [('data/sources.json', 'data/raw'),
            ('data/strict_feature_sources.json', 'data/raw/strict_features'),
            ('data/validation_extension_sources.json', 'data/raw/validation_extension'),
            ('data/context_followup_sources.json', 'data/raw/context_followup')]:
        for source in json.loads((ROOT / manifest).read_text()):
            if manifest.endswith('context_followup_sources.json') and source['file'] != 'breadwheat.rda':
                continue
            payload = (ROOT / folder / source['file']).read_bytes()
            assert hashlib.sha256(payload).hexdigest() == source['sha256'], source['file']
            assert 'bytes' not in source or len(payload) == source['bytes'], source['file']
            entries.append(dict(path=folder+'/'+source['file'], sha256=source['sha256'], bytes=len(payload)))
    return entries


def load_tasks():
    from run_strict_real import load_tasks as strict_tasks
    tasks = []
    for item in load_all():
        tasks.append(Task(item.name, 'baseline_replacement', item.y, item.n,
            np.arange(len(item.y)), 0 if item.name == 'beans' else 1, 202609253,
            'anonymous_report' if item.name == 'beans' else 'aligned_sushi_respondent'))
    for i, item in enumerate(strict_tasks()):
        key = 100 + ord(item['arm']) if item['family'] == 'dots2024' else 1000+i
        tasks.append(Task(item['name'], 'strict_features', item['y'], item['n'],
            item['group'], key, 202609251+i, item['grouping'], item['truth']))
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', UserWarning)
        wheat = rdata.read_rda(ROOT / 'data/raw/context_followup/breadwheat.rda')['breadwheat']
    shown = wheat[['variety_a', 'variety_b', 'variety_c']].astype(str).to_numpy()
    labels = {v:i for i,v in enumerate(sorted(set(shown.ravel())))}
    rows = []
    for items, best, worst in zip(shown, wheat.overall_best, wheat.overall_worst):
        assert len(set(items)) == 3 and best in 'ABC' and worst in 'ABC' and best != worst
        b, w = 'ABC'.index(best), 'ABC'.index(worst)
        rows.append([labels[items[i]] for i in (b, 3-b-w, w)])
    assert len(rows) == 493 and len(labels) == 16
    tasks.append(Task('wheat', 'context_followup', validate_rankings(rows, 16), 16,
                      np.arange(493), 2000, 202609252, 'anonymous_report_missing_cluster_ids'))
    for item in real_tasks():
        if item['eligible']:
            tasks.append(Task(item['name'], 'validation_extension', item['y'], item['n'],
                item['groups'], 3000+item['source_index'], 202609260+item['source_index'],
                item['unit'], item['truth']))
    assert len(tasks) == 23 and len({t.name for t in tasks}) == 23
    source_inventory()
    return tasks


def split_task(task, repeat):
    if not 0 <= repeat < REPETITIONS:
        raise ValueError('Repetition outside the frozen plan')
    units = np.unique(task.units)
    rng = np.random.default_rng(np.random.SeedSequence([SEED, task.split_key, repeat]))
    order = rng.permutation(units)
    a, b = int(.6*len(units)), int(.8*len(units))
    parts = {name:np.flatnonzero(np.isin(task.units, selected))
             for name,selected in [('fit',order[:a]), ('discovery',order[a:b]), ('confirmation',order[b:])]}
    assert all(len(v) for v in parts.values())
    np.testing.assert_array_equal(np.sort(np.concatenate(list(parts.values()))), np.arange(len(task.y)))
    return parts


def json_value(value):
    if isinstance(value, dict):
        return {str(k):json_value(v) for k,v in value.items()}
    if isinstance(value, (list, tuple, np.ndarray)):
        return [json_value(v) for v in value]
    if isinstance(value, (np.integer, np.bool_)):
        return value.item()
    if isinstance(value, (float, np.floating)):
        return float(value) if np.isfinite(value) else str(float(value))
    return value


def save_fit(fit):
    return json_value(dict(method=fit.method, order=fit.order, beta=fit.beta,
                           theta=fit.theta, status=fit.status, metadata=fit.metadata))


def restore_fit(saved):
    return StrictFit(saved['method'], None if saved['order'] is None else np.asarray(saved['order']),
        beta=float(saved['beta']), theta=None if saved['theta'] is None else np.asarray(saved['theta']),
        status=saved['status'], metadata=saved['metadata'])


def fit_all(task, train):
    result = {'pl':fit_pl_mm(train, task.n)}
    for method in METHODS[1:]:
        result[method] = fit_sm_strict(train, task.n, method, beta0=.1,
                                      pair_seed=task.estimator_seed, milp_seconds=120.)
    return result


def score_loss(loss, pl_loss, status, pl_status):
    loss, pl_loss = np.asarray(loss), np.asarray(pl_loss)
    assert len(loss) and len(loss) == len(pl_loss)
    assert not np.isneginf(loss).any()
    assert not (loss[np.isfinite(loss)] < -1e-10).any()
    finite = np.isfinite(loss)
    paired = finite & np.isfinite(pl_loss)
    difference = loss-pl_loss if status == pl_status == 'ok' else np.full(len(loss), np.nan)
    return dict(n_test=len(loss), n_finite=int(finite.sum()), n_infinite=int(np.isposinf(loss).sum()),
        n_available=len(loss) if status == 'ok' else 0,
        nll=float(loss.mean()),
        finite_report_nll=float(loss[finite].mean()) if finite.any() else np.nan,
        paired_delta=float(difference.mean()), n_paired_finite=int(paired.sum()),
        finite_report_delta=float((loss[paired]-pl_loss[paired]).mean()) if paired.any() else np.nan)


def coverage(train, n):
    w = pair_counts(train, n)
    item = np.bincount(train.ravel(), minlength=n)
    pairs = (w+w.T)[np.triu_indices(n, 1)]
    N, r = train.shape
    return dict(n_train=N, n=n, r=r, unseen_items=int((item == 0).sum()),
        min_item_count=int(item.min()), min_pair_count=int(pairs.min()),
        observed_pairs=int((pairs > 0).sum()), lambda_=N*r*(r-1)/(n*(n-1)), mu=N*r/n)


def diagnostic_rows(task, train, held, models, base):
    """Existing diagnostic point definitions; no new bootstrap significance test."""
    if task.study == 'baseline_replacement':
        return []
    sm, pl = models['mle'], models['pl']
    rows = []
    fitted_ok = sm.status == pl.status == 'ok' and np.isfinite(sm.beta)
    if task.name == 'sounds':
        if not fitted_ok:
            return [dict(base, kind='pair_profile', reference='fitted', component=str(i), status='fit_unavailable') for i in range(3)]
        tr = pair_arrays(train, sm.order, sm.beta, pl.theta)
        a = pair_arrays(held, sm.order, sm.beta, pl.theta)
        cuts = np.quantile(tr['worth_gap'], [1/3, 2/3])
        bins = np.searchsorted(cuts, a['worth_gap'][:, 0], side='right')
        for i in range(3):
            mask = bins == i
            rows.append(dict(base, kind='pair_profile', reference='fitted', component=str(i),
                status='ok' if mask.any() else 'empty_bin', reports=int(mask.sum()),
                observed=float(a['z'][mask].mean()) if mask.any() else np.nan,
                sm_predicted=float(a['sm'][mask].mean()) if mask.any() else np.nan,
                pl_predicted=float(a['pl'][mask].mean()) if mask.any() else np.nan,
                lower_cut=float(cuts[0]), upper_cut=float(cuts[1])))
        return rows
    references = ['fitted'] + (['objective'] if task.truth is not None else [])
    for reference in references:
        valid = fitted_ok
        order, beta = sm.order, sm.beta
        if reference == 'objective':
            order = task.truth
            if task.study == 'strict_features':
                # The original objective-order follow-up profiles its reference dispersion.
                beta = profile_beta_unbounded(distances(train, order).sum(), len(train), train.shape[1])
                valid = pl.status == 'ok' and np.isfinite(beta)
            # The original Patras objective diagnostic retains fitted SM dispersion.
        row = dict(base, kind='context', reference=reference, component='slope')
        row.update(context_slope(pair_arrays(held, order, beta, pl.theta), resamples=0)
                   if valid else dict(status='fit_unavailable'))
        rows.append(row)
    if task.study in ('strict_features', 'validation_extension'):
        shell = shell_decomposition(held, sm.order, sm.beta, pl.theta) if fitted_ok else None
        for component in ('total', 'shell_mass', 'within_shell'):
            rows.append(dict(base, kind='shell', reference='fitted', component=component,
                status='ok' if fitted_ok else 'fit_unavailable',
                value=float(shell[component].mean()) if fitted_ok else np.nan))
    if task.name == 'wheat':
        rows.append(dict(base, kind='context', reference='village_adjusted', component='slope',
                         status='unavailable_missing_village'))
    if task.study == 'strict_features' and fitted_ok:
        from run_strict_real import diagnostic_profiles
        for row in diagnostic_profiles(held, train, sm, pl, {'name':task.name}, base['split']):
            row.update(base, kind='pair_profile', reference='fitted',
                       component=f"gap{row['gap']}_bin{row['bin']}", status='ok')
            row['sm_predicted'], row['pl_predicted'] = row.pop('sm'), row.pop('pl')
            rows.append(row)
    return rows


def evaluate(task, repeat, parts, models):
    train = task.y[parts['fit']]
    base = dict(dataset=task.name, study=task.study, repeat=repeat)
    audit = coverage(train, task.n)
    scores, diagnostics, selections = [], [], []
    for split in ('discovery', 'confirmation'):
        held = task.y[parts[split]]
        losses = {m:models[m].nll(held) for m in METHODS}
        for method in METHODS:
            fit = models[method]
            scores.append(dict(base, split=split, method=method, status=fit.status, **audit,
                **score_loss(losses[method], losses['pl'], fit.status, models['pl'].status),
                beta=fit.beta, branch=fit.metadata.get('branch', 'hunter_mm' if method == 'pl' else 'unavailable'),
                depth=fit.metadata.get('depth', np.nan), certified=fit.metadata.get('certified', False),
                objective_kendall=kendall(fit.order, task.truth) if fit.status == 'ok' and task.truth is not None else np.nan))
        diagnostics.extend(diagnostic_rows(task, train, held, models, dict(base, split=split)))
    if task.study == 'strict_features':
        choices = discovery_choices(task.y[parts['discovery']], models['mle'], models['pl'])
        for selector in ('pair', 'context'):
            chosen = choices[selector+'_choice']
            model = models['mle'] if chosen == 'sm' else models['pl'] if chosen == 'pl' else None
            selections.append(dict(base, selector=selector, choice=chosen,
                confirmation_nll=float(model.nll(task.y[parts['confirmation']]).mean()) if model is not None else np.nan,
                context_eligible_cells=choices.get('context_eligible_cells', 0)))
    return dict(scores=scores, diagnostics=diagnostics, selections=selections)


def code_hashes():
    return {p:hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in CORE_FILES}
