"""Average separately trained predictive losses and conditional Monte Carlo precision."""
import hashlib
import json
import platform
import numpy as np
import pandas as pd
import scipy

from .repeated_holdout import ROOT, REPETITIONS, SEED, PROTOCOL_COMMIT, code_hashes


def mean_fields(values, prefix):
    a = np.asarray(values, dtype=float)
    finite = a[np.isfinite(a)]
    all_finite = len(finite) == len(a)
    mcse = float(finite.std(ddof=1)/np.sqrt(len(finite))) if len(finite) > 1 else np.nan
    with np.errstate(invalid='ignore'):
        average = float(a.mean()) if not np.isnan(a).any() else np.nan
    return {prefix+'_mean':average,
        prefix+'_defined_repeats':int((~np.isnan(a)).sum()),
        prefix+'_infinite_repeats':int(np.isinf(a).sum()),
        prefix+'_finite_repeats':len(finite),
        prefix+'_partition_mcse':mcse if all_finite else np.nan,
        prefix+'_finite_conditional_mean':float(finite.mean()) if len(finite) else np.nan,
        prefix+'_finite_conditional_partition_mcse':mcse}


def summarize_scores(frame):
    rows = []
    for key, g in frame.groupby(['dataset', 'study', 'split', 'method'], sort=True):
        row = dict(zip(['dataset', 'study', 'split', 'method'], key))
        row.update(repetitions=len(g), successful_fits=int(g.status.eq('ok').sum()),
            status_counts=json.dumps(g.status.value_counts().sort_index().to_dict(), sort_keys=True),
            n_train=int(g.n_train.iloc[0]), n_test=int(g.n_test.iloc[0]),
            n=int(g.n.iloc[0]), r=int(g.r.iloc[0]),
            finite_report_coverage=float((g.n_finite/g.n_test).mean()),
            paired_finite_report_coverage=float((g.n_paired_finite/g.n_test).mean()),
            unseen_training_item_repeats=int((g.unseen_items > 0).sum()))
        for name in ('nll', 'paired_delta', 'finite_report_nll', 'finite_report_delta', 'objective_kendall'):
            row.update(mean_fields(g[name], name))
        rows.append(row)
    return pd.DataFrame(rows)


def summarize_diagnostics(frame):
    rows = []
    keys = ['dataset', 'study', 'split', 'kind', 'reference', 'component']
    metrics = [m for m in ['value', 'observed', 'sm_predicted', 'pl_predicted',
               'residual_vs_sm', 'residual_vs_pl', 'eligible_pairs', 'pair_observations',
               'reports', 'contributing_reports', 'observations'] if m in frame]
    for key, g in frame.groupby(keys, sort=True):
        row = dict(zip(keys, key)); row.update(recorded_repetitions=len(g),
            successful_diagnostics=int(g.status.eq('ok').sum()),
            status_counts=json.dumps(g.status.value_counts().sort_index().to_dict(), sort_keys=True))
        for name in metrics:
            row.update(mean_fields(g[name], name))
        rows.append(row)
    return pd.DataFrame(rows)


def summarize_selections(frame):
    rows = []
    for key, g in frame.groupby(['dataset', 'study', 'selector'], sort=True):
        row = dict(zip(['dataset', 'study', 'selector'], key))
        row.update(repetitions=len(g), abstentions=int(g.choice.eq('abstain').sum()),
                   selected_sm=int(g.choice.eq('sm').sum()), selected_pl=int(g.choice.eq('pl').sum()))
        row.update(mean_fields(g.confirmation_nll, 'confirmation_nll'))
        rows.append(row)
    return pd.DataFrame(rows)


def tables_from_records(records):
    frames = {name:pd.DataFrame([row for record in records for row in record[name]])
              for name in ('scores', 'diagnostics', 'selections')}
    return dict(repeat_scores=frames['scores'], scores=summarize_scores(frames['scores']),
        repeat_diagnostics=frames['diagnostics'], diagnostics=summarize_diagnostics(frames['diagnostics']),
        repeat_selections=frames['selections'], selections=summarize_selections(frames['selections']))


def publish(records, tasks, sources, output):
    expected = {(task.name, rep) for task in tasks for rep in range(REPETITIONS)}
    actual = [(r['dataset'], r['repeat']) for r in records]
    assert len(tasks) == 23 and len(actual) == len(set(actual)) == len(expected) == 690
    assert set(actual) == expected
    output.mkdir(parents=True, exist_ok=True)
    frames = tables_from_records(records)
    digests = {}
    for name, frame in frames.items():
        suffix = '.csv.gz' if name.startswith('repeat_') else '.csv'
        path = output / (name + suffix)
        frame.to_csv(path, index=False, float_format='%.15g',
                     compression={'method':'gzip', 'mtime':0} if suffix.endswith('gz') else None)
        digests[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    descriptors = []
    for task in tasks:
        record = next(r for r in records if r['dataset'] == task.name)
        descriptors.append(dict(dataset=task.name, study=task.study, n=task.n, r=task.y.shape[1],
            reports=len(task.y), units=len(np.unique(task.units)), unit_description=task.unit_description,
            split_key=task.split_key, estimator_seed=task.estimator_seed,
            split_sizes={k:len(v) for k,v in record['parts'].items()}))
    manifest = dict(seed=SEED, repetitions=REPETITIONS, protocol_commit=PROTOCOL_COMMIT,
        baseline_main='551368d48a0b87e7f8573d0f28efa1ac66e4c625', training_contexts=len(records),
        candidate_fits=5*len(records), datasets=descriptors, sources=sources,
        code_sha256=code_hashes(), published_sha256=digests,
        versions=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__, pandas=pd.__version__),
        target='Mean confirmation loss over independently randomized original 60/20/20 partitions',
        precision='Partition Monte Carlo standard error conditional on fixed source observations; not population uncertainty')
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print('PUBLISHED', len(records), 'training contexts;',len(frames['repeat_scores']),'held-out score rows',flush=True)
