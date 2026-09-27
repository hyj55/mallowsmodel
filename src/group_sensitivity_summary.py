"""Descriptive repeated-partition summaries; no independent-replicate confidence intervals."""
import hashlib
import json
import platform
from pathlib import Path
import numpy as np
import pandas as pd
import scipy

from .group_sensitivity import ROOT, SEED, SPLIT_PLAN


def divide(a, b):
    return float(a / b) if b else np.nan


def spread(values, prefix):
    values = np.asarray(values, dtype=float)
    finite = values[np.isfinite(values)]
    result = {prefix + '_finite_repeats': len(finite)}
    for suffix, value in [('mean', np.mean(finite) if len(finite) else np.nan),
                          ('median', np.median(finite) if len(finite) else np.nan),
                          ('p05', np.quantile(finite, .05) if len(finite) else np.nan),
                          ('p95', np.quantile(finite, .95) if len(finite) else np.nan),
                          ('negative_fraction', np.mean(finite < 0) if len(finite) else np.nan)]:
        result[prefix + '_' + suffix] = float(value)
    return result


def score_repeats(scores):
    rows = []
    keys = ['dataset', 'design', 'percent', 'repeat', 'scheme', 'method']
    for labels, frame in scores.groupby(keys, sort=True):
        test = int(frame.n_test.sum())
        finite = int(frame.n_finite.sum())
        available = int(frame.n_available.sum())
        infinite = int(frame.n_infinite.sum())
        paired = int(frame.n_paired.sum())
        macro_loss = frame.loc[frame.n_finite > 0, 'finite_sum'] / frame.loc[frame.n_finite > 0, 'n_finite']
        macro_delta = frame.loc[frame.n_paired > 0, 'delta_sum'] / frame.loc[frame.n_paired > 0, 'n_paired']
        row = dict(zip(keys, labels))
        row.update(n_test=test, n_finite=finite, n_available=available, n_infinite=infinite,
            evaluated_groups=len(frame), available_groups=int((frame.status == 'ok').sum()),
            paired_groups=int((frame.n_paired > 0).sum()),
            available_coverage=available/test, finite_coverage=finite/test,
            finite_nll=divide(frame.finite_sum.sum(), finite),
            macro_finite_nll=float(macro_loss.mean()),
            nll_all=(np.nan if available != test else np.inf if infinite else frame.finite_sum.sum()/test),
            n_paired=paired, paired_coverage=paired/test,
            delta=divide(frame.delta_sum.sum(), paired), macro_delta=float(macro_delta.mean()))
        rows.append(row)
    return pd.DataFrame(rows)


def summarize_scores(repeats):
    rows = []
    keys = ['dataset', 'design', 'percent', 'scheme', 'method']
    for labels, frame in repeats.groupby(keys, sort=True):
        row = dict(zip(keys, labels))
        row.update(repeats=len(frame), min_test_reports=int(frame.n_test.min()),
                   max_test_reports=int(frame.n_test.max()),
                   fully_available_repeats=int((frame.n_available == frame.n_test).sum()),
                   complete_finite_repeats=int(np.isfinite(frame.nll_all).sum()),
                   infinite_nll_repeats=int(np.isinf(frame.nll_all).sum()),
                   any_infinite_repeats=int((frame.n_infinite > 0).sum()),
                   unavailable_repeats=int(frame.nll_all.isna().sum()))
        for column in ['finite_nll', 'macro_finite_nll', 'delta', 'macro_delta',
                       'available_coverage', 'finite_coverage', 'paired_coverage']:
            row.update(spread(frame[column], column))
        rows.append(row)
    return pd.DataFrame(rows)


def contrast_repeats(contrasts):
    rows = []
    keys = ['dataset', 'design', 'percent', 'repeat', 'sm_method', 'reference']
    for labels, frame in contrasts.groupby(keys, sort=True):
        common = int(frame.n_common.sum())
        row = dict(zip(keys, labels))
        row.update(n_common=common, n_test=int(frame.n_test.sum()), common_coverage=divide(common, frame.n_test.sum()),
                   groups=int((frame.n_common > 0).sum()))
        for name in ['sm_change', 'pl_change', 'interaction']:
            row[name] = divide(frame[name + '_sum'].sum(), common)
            selected = frame.n_common > 0
            row['macro_' + name] = float((frame.loc[selected, name + '_sum'] / frame.loc[selected, 'n_common']).mean())
        rows.append(row)
    return pd.DataFrame(rows)


def summarize_contrasts(repeats):
    rows = []
    keys = ['dataset', 'design', 'percent', 'sm_method', 'reference']
    for labels, frame in repeats.groupby(keys, sort=True):
        row = dict(zip(keys, labels)); row['repeats'] = len(frame)
        for column in ['sm_change', 'pl_change', 'interaction', 'macro_sm_change',
                       'macro_pl_change', 'macro_interaction', 'common_coverage']:
            row.update(spread(frame[column], column))
        rows.append(row)
    return pd.DataFrame(rows)


def summarize_groups(scores):
    rows = []
    keys = ['dataset', 'design', 'percent', 'group', 'group_name', 'scheme', 'method']
    for labels, frame in scores.groupby(keys, sort=True):
        row = dict(zip(keys, labels))
        row.update(repeats=len(frame), available_repeats=int((frame.status == 'ok').sum()),
            complete_finite_repeats=int((frame.n_finite == frame.n_test).sum()),
            any_infinite_repeats=int((frame.n_infinite > 0).sum()),
            min_train_reports=int(frame.n_train.min()), max_train_reports=int(frame.n_train.max()),
            nll_finite_mean=float((frame.finite_sum / frame.n_finite.replace(0, np.nan)).mean()),
            finite_coverage_mean=float((frame.n_finite / frame.n_test).mean()),
            delta_mean=float((frame.delta_sum / frame.n_paired.replace(0, np.nan)).mean()),
            paired_coverage_mean=float((frame.n_paired / frame.n_test).mean()))
        rows.append(row)
    return pd.DataFrame(rows)


def summarize_fit_audit(audit):
    keys = ['dataset', 'design', 'percent', 'scheme', 'method', 'status']
    return audit.groupby(keys, dropna=False, sort=True).agg(
        fit_contexts=('status', 'size'), min_training_reports=('n_train', 'min'),
        max_training_reports=('n_train', 'max'), min_item_count=('item_min', 'min'),
        min_pair_count=('pair_min', 'min'), max_pair_count=('pair_min', 'max'),
        min_lambda=('lambda_', 'min'), max_lambda=('lambda_', 'max'),
        min_mu=('mu', 'min'), max_mu=('mu', 'max'),
        max_hierarchy_depth=('depth', 'max')).reset_index()


def build_tables(private):
    bundles = [p for p in sorted(private.iterdir()) if (p / 'manifest.json').exists()]
    score_parts, contrast_parts, group_parts, audit_parts, manifests = [], [], [], [], []
    for directory in bundles:
        manifest = json.loads((directory / 'manifest.json').read_text())
        if manifest['quick']:
            raise ValueError('Development runs cannot enter published summaries')
        manifests.append(manifest)
        scores = pd.read_csv(directory / 'group_scores.csv.gz')
        contrast = pd.read_csv(directory / 'contrasts.csv.gz')
        audit = pd.read_csv(directory / 'fit_audit.csv.gz')
        score_parts.append(score_repeats(scores))
        contrast_parts.append(contrast_repeats(contrast))
        group_parts.append(summarize_groups(scores))
        audit_parts.append(summarize_fit_audit(audit))
    if not bundles:
        raise ValueError('No completed datasets')
    repeat_scores = pd.concat(score_parts, ignore_index=True)
    repeat_contrasts = pd.concat(contrast_parts, ignore_index=True)
    return dict(scores=summarize_scores(repeat_scores), contrasts=summarize_contrasts(repeat_contrasts),
                group_scores=pd.concat(group_parts, ignore_index=True),
                eligibility=pd.concat(audit_parts, ignore_index=True),
                repeat_scores=repeat_scores, repeat_contrasts=repeat_contrasts), manifests


def publish_summaries(private, public):
    tables, datasets = build_tables(private)
    if len(datasets) != 9:
        raise ValueError('All nine frozen datasets must finish before publishing')
    public.mkdir(parents=True, exist_ok=True)
    hashes = {}
    for name, table in tables.items():
        suffix = '.csv.gz' if name.startswith('repeat_') or name == 'group_scores' else '.csv'
        path = public / (name + suffix)
        compression = {'method': 'gzip', 'mtime': 0} if suffix.endswith('.gz') else None
        table.to_csv(path, index=False, float_format='%.12g', compression=compression)
        hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    code_paths = ['src/group_sensitivity.py', 'src/group_sensitivity_summary.py', 'run_group_sensitivity.py',
                  'src/strict_models.py', 'src/manuscript_estimators.py', 'src/models.py',
                  'docs/protocols/GROUP_SENSITIVITY_20260927.md', 'data/group_sensitivity_sources.json']
    manifest = dict(protocol_commit='69541057711c08ff1508f25676bb6abfdd12c27d', seed=SEED,
        plan=SPLIT_PLAN, holdout_repetitions=100, datasets=datasets,
        interpretation='5th–95th percentiles describe split sensitivity; not population confidence intervals.',
        versions=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__, pandas=pd.__version__),
        code_sha256={p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in code_paths},
        published_sha256=hashes)
    (public / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('PUBLISHED', len(datasets), 'datasets', len(tables['repeat_scores']), 'repeat score summaries', flush=True)
