"""Read-only replay of memberships, stored predictions and published aggregates; no refits."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

from src.group_sensitivity import (ROOT, METHODS, load_group_tasks, within_split,
    holdout_split, matched_training, group_score, paired_contrast)
from src.group_sensitivity_summary import build_tables, summarize_scores, summarize_contrasts
from src.strict_models import StrictFit


def equal(a, b):
    if isinstance(a, str) or isinstance(b, str):
        assert a == b, (a, b)
    else:
        assert np.isclose(a, b, rtol=2e-10, atol=2e-10, equal_nan=True), (a, b)


def restore_fit(method, record):
    return StrictFit(method,
        None if record['order'] is None else np.array(record['order'], dtype=int),
        beta=float(record['beta']),
        theta=None if record['theta'] is None else np.array(record['theta'], dtype=float),
        status=record['status'], metadata=record['metadata'])


def validate_dataset(task, directory):
    scores = pd.read_csv(directory / 'group_scores.csv.gz')
    contrasts = pd.read_csv(directory / 'contrasts.csv.gz')
    score_keys = ['design', 'percent', 'repeat', 'scheme', 'group', 'method']
    contrast_keys = ['design', 'percent', 'repeat', 'group', 'sm_method', 'reference']
    assert not scores.duplicated(score_keys).any()
    assert not contrasts.duplicated(contrast_keys).any()
    expected_scores = {tuple(row[k] for k in score_keys): row for row in scores.to_dict('records')}
    expected_contrasts = {tuple(row[k] for k in contrast_keys): row for row in contrasts.to_dict('records')}
    checked_scores, checked_contrasts = set(), set()
    contexts = 0
    previous = None
    predictions = {}
    splits = {}

    def flush(key):
        if key is None or key[0] != 'within':
            return
        design, percent, repeat = key
        for g in range(len(task.group_names)):
            for method in METHODS[:-1]:
                for reference in ('pooled', 'matched_pool'):
                    record_key = (design, percent, repeat, g, method, reference)
                    if record_key not in expected_contrasts:
                        continue
                    row = expected_contrasts[record_key]
                    result = paired_contrast(predictions['local', g, method], predictions['local', g, 'pl'],
                                             predictions[reference, g, method], predictions[reference, g, 'pl'])
                    for name, value in result.items():
                        equal(value, row[name])
                    checked_contrasts.add(record_key)

    with gzip.open(directory / 'fits.jsonl.gz', 'rt') as stream:
        for line in stream:
            record = json.loads(line)
            key = record['design'], record['percent'], record['repeat']
            if key != previous:
                flush(previous); predictions = {}; previous = key
            if key not in splits:
                splits[key] = (within_split(task.groups, task.index, key[1], key[2])
                               if key[0] == 'within' else holdout_split(task.groups, task.index, key[2]))
            train, test = splits[key]
            ids = np.asarray(record['train_ids'], dtype=int)
            assert len(np.unique(ids)) == len(ids) and np.isin(ids, train).all()
            assert not np.intersect1d(ids, test).size
            scheme, group = record['scheme'], record['group']
            if scheme == 'pooled':
                np.testing.assert_array_equal(ids, train)
            else:
                local = train[task.groups[train] == group]
                if scheme == 'local':
                    np.testing.assert_array_equal(ids, local)
                else:
                    np.testing.assert_array_equal(ids, matched_training(train, len(local), task.index, key[1], key[2], group))
            if key[0] == 'group_holdout':
                assert not np.intersect1d(task.groups[ids], task.groups[test]).size
            fitted = {m: restore_fit(m, record['fits'][m]) for m in METHODS}
            groups = np.unique(task.groups[test]) if group == -1 else [group]
            for g in groups:
                te = test[task.groups[test] == g]
                values = {m: fitted[m].nll(task.y[te]) for m in METHODS}
                for method in METHODS:
                    row_key = (*key, scheme, int(g), method)
                    row = expected_scores[row_key]
                    result = group_score(values[method], fitted[method], len(te))
                    for name, value in result.items():
                        equal(value, row[name])
                    equal(len(ids), row['n_train'])
                    mask = np.isfinite(values[method]) & np.isfinite(values['pl'])
                    equal(int(mask.sum()) if method != 'pl' else 0, row['n_paired'])
                    equal(float((values[method][mask] - values['pl'][mask]).sum()) if method != 'pl' else 0., row['delta_sum'])
                    if key[0] == 'within':
                        predictions[scheme, int(g), method] = values[method]
                    checked_scores.add(row_key)
            contexts += 1
    flush(previous)
    assert len(checked_scores) == len(expected_scores)
    assert len(checked_contrasts) == len(expected_contrasts)
    manifest = json.loads((directory / 'manifest.json').read_text())
    assert contexts == manifest['fit_contexts']
    assert manifest['candidate_fit_attempts'] == contexts * len(METHODS)
    return dict(dataset=task.name, training_contexts=contexts, candidate_fits=contexts*len(METHODS),
                group_score_rows=len(checked_scores), four_way_contrast_rows=len(checked_contrasts),
                source_reports=len(task.y), groups=len(task.group_names),
                source_verified=True, split_membership_verified=True, stored_likelihood_replayed=True)


def validate_public(public):
    """CI path: checksum and aggregate checks require no respondent-level downloads."""
    manifest = json.loads((public / 'manifest.json').read_text())
    assert len(manifest['datasets']) == 9
    assert sum(x['reports'] for x in manifest['datasets']) == 7743
    assert all(not x['quick'] and x['holdout_repetitions'] == 100 for x in manifest['datasets'])
    for name, digest in manifest['published_sha256'].items():
        assert hashlib.sha256((public / name).read_bytes()).hexdigest() == digest, name
    for name, digest in manifest['code_sha256'].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    scores = pd.read_csv(public / 'repeat_scores.csv.gz')
    contrasts = pd.read_csv(public / 'repeat_contrasts.csv.gz')
    assert len(scores) == 23400
    assert (scores.n_finite + scores.n_infinite == scores.n_available).all()
    assert (scores.n_available <= scores.n_test).all()
    for frame, expected, name in [(scores, summarize_scores(scores), 'scores.csv'),
                                  (contrasts, summarize_contrasts(contrasts), 'contrasts.csv')]:
        actual = pd.read_csv(public / name)
        pd.testing.assert_frame_equal(actual, expected, check_dtype=False, rtol=2e-9, atol=2e-9)
    print('PUBLIC CHECKSUMS, REPEAT COUNTS AND AGGREGATES VERIFIED', flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--quick', action='store_true')
    parser.add_argument('--datasets', nargs='*')
    parser.add_argument('--repository-only', action='store_true')
    args = parser.parse_args()
    private = ROOT / ('results/private/group_sensitivity_quick' if args.quick else 'results/private/group_sensitivity')
    public = ROOT / 'results/group_sensitivity'
    if args.repository_only:
        validate_public(public)
        return
    tasks = load_group_tasks()
    if args.datasets:
        tasks = [t for t in tasks if t.name in args.datasets]
    checks = []
    for task in tasks:
        result = validate_dataset(task, private / task.name)
        checks.append(result)
        print('VERIFIED', task.name, result['candidate_fits'], 'candidate fits', flush=True)
    if not args.quick and not args.datasets:
        manifest = json.loads((public / 'manifest.json').read_text())
        for name, digest in manifest['published_sha256'].items():
            assert hashlib.sha256((public / name).read_bytes()).hexdigest() == digest, name
        for name, digest in manifest['code_sha256'].items():
            assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
        tables, _ = build_tables(private)
        for name, expected in tables.items():
            suffix = '.csv.gz' if name.startswith('repeat_') or name == 'group_scores' else '.csv'
            actual = pd.read_csv(public / (name + suffix))
            pd.testing.assert_frame_equal(actual, expected, check_dtype=False, rtol=2e-10, atol=2e-10)
        report = dict(status='passed', refits=0, sources_and_predictions=checks,
                      aggregate_tables_recomputed=len(tables), checksums_verified=True,
                      split_ranges_are_confidence_intervals=False)
        (public / 'validation.json').write_text(json.dumps(report, indent=2) + '\n')
        print('ALL PUBLISHED AGGREGATES VERIFIED WITHOUT REFITTING', flush=True)


if __name__ == '__main__':
    main()
