"""Read-only checks of all repetitions, saved predictors and public averages."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.sparse.csgraph import connected_components

from run_repeated_real import read_records
from src.repeated_holdout import (ROOT, METHODS, REPETITIONS, load_tasks, split_task,
    restore_fit, evaluate, code_hashes, source_inventory, PROTOCOL_COMMIT)
from src.repeated_holdout_summary import (tables_from_records, summarize_scores,
    summarize_diagnostics, summarize_selections)
from src.models import distances, pair_counts, kemeny_cost
from src.strict_models import profile_beta_unbounded, pl_mm_step

PUBLIC = ROOT / 'results/repeated_holdout'


def equal(a, b):
    if isinstance(a, str) or isinstance(b, str):
        assert a == b, (a, b)
    else:
        assert np.isclose(a, b, rtol=2e-10, atol=2e-10, equal_nan=True), (a, b)


def frames_equal(actual, expected):
    pd.testing.assert_frame_equal(actual, expected, check_dtype=False,
                                  rtol=2e-9, atol=2e-9)


def validate_public():
    manifest = json.loads((PUBLIC / 'manifest.json').read_text())
    assert manifest['repetitions'] == REPETITIONS == 30
    assert manifest['training_contexts'] == 690 and manifest['candidate_fits'] == 3450
    assert manifest['protocol_commit'] == PROTOCOL_COMMIT
    assert manifest['code_sha256'] == code_hashes()
    for name, digest in manifest['published_sha256'].items():
        assert hashlib.sha256((PUBLIC / name).read_bytes()).hexdigest() == digest, name
    scores = pd.read_csv(PUBLIC / 'repeat_scores.csv.gz')
    diagnostics = pd.read_csv(PUBLIC / 'repeat_diagnostics.csv.gz')
    selections = pd.read_csv(PUBLIC / 'repeat_selections.csv.gz')
    keys = ['dataset', 'repeat', 'split', 'method']
    assert not scores.duplicated(keys).any() and len(scores) == 6900
    descriptors = {t['dataset']:t for t in manifest['datasets']}
    assert len(descriptors) == 23 and set(scores.dataset) == set(descriptors)
    assert set(scores.method) == set(METHODS)
    for (name, split, method), g in scores.groupby(['dataset', 'split', 'method']):
        assert set(g.repeat) == set(range(REPETITIONS))
        task = descriptors[name]
        assert (g.n_train == task['split_sizes']['fit']).all()
        assert (g.n_test == task['split_sizes'][split]).all()
        assert (g.n == task['n']).all() and (g.r == task['r']).all()
    assert (scores.n_finite + scores.n_infinite == scores.n_available).all()
    assert (scores.n_available <= scores.n_test).all()
    assert ((scores.n_available == scores.n_test) == scores.status.eq('ok')).all()
    assert ((scores.n_infinite > 0) == np.isposinf(scores.nll)).all()
    assert (scores.nll.isna() == scores.status.ne('ok')).all()
    assert (scores.n_paired_finite <= scores.n_finite).all()
    paired = scores.merge(scores[scores.method.eq('pl')][
        ['dataset', 'repeat', 'split', 'nll', 'status']], on=['dataset', 'repeat', 'split'],
        suffixes=('', '_pl'), validate='many_to_one')
    valid = paired.status.eq('ok') & paired.status_pl.eq('ok')
    np.testing.assert_allclose(paired.loc[valid, 'paired_delta'],
        paired.loc[valid, 'nll'] - paired.loc[valid, 'nll_pl'], rtol=2e-9, atol=2e-9)
    assert paired.loc[~valid, 'paired_delta'].isna().all()
    assert not diagnostics.duplicated(['dataset', 'repeat', 'split', 'kind', 'reference', 'component']).any()
    assert len(selections) == 16*30*2
    assert not selections.duplicated(['dataset', 'repeat', 'selector']).any()
    for name, expected in [('scores', summarize_scores(scores)),
            ('diagnostics', summarize_diagnostics(diagnostics)),
            ('selections', summarize_selections(selections))]:
        frames_equal(pd.read_csv(PUBLIC / (name+'.csv')), expected)
    print('PUBLIC HASHES, COMPLETE REPEAT COUNTS AND AVERAGES VERIFIED', flush=True)
    return manifest


def check_parameters(task, train, models):
    for method, model in models.items():
        if model.status != 'ok':
            assert model.order is None
            if method == 'pl' and model.status == 'no_unique_finite_mle':
                count, _ = connected_components(pair_counts(train, task.n) > 0,
                                                directed=True, connection='strong')
                assert count == model.metadata['components'] and count > 1
            if method == 'mle':
                assert model.status == 'optimum_not_certified' and not model.metadata['certified']
            continue
        np.testing.assert_array_equal(np.sort(model.order), np.arange(task.n))
        if method == 'pl':
            worth = np.exp(model.theta - model.theta.max()); worth /= worth.sum()
            wins = np.bincount(train[:, :-1].ravel(), minlength=task.n)
            _, exposure = pl_mm_step(train, worth, wins)
            residual = np.max(np.abs(wins-worth*exposure))/len(train)
            assert residual < 1e-8
            equal(residual, model.metadata['gradient_per_report'])
            equal(model.nll(train).mean(), model.metadata['training_nll'])
        else:
            total = int(distances(train, model.order).sum())
            equal(total, model.metadata['training_distance'])
            equal(model.beta, profile_beta_unbounded(total, len(train), train.shape[1]))
            if method == 'mle':
                assert model.metadata['certified']
                if task.n > 18:
                    value = kemeny_cost(pair_counts(train, task.n), model.order)
                    assert value == model.metadata['lower_bound'] == model.metadata['upper_bound']


def validate_records(tasks, records, expected_repetitions):
    signature = hashlib.sha256(json.dumps(code_hashes(), sort_keys=True).encode()).hexdigest()
    expected = {(t.name, r) for t in tasks for r in range(expected_repetitions)}
    assert {(r['dataset'], r['repeat']) for r in records} == expected
    assert len(records) == len(expected)
    by_name = {t.name:t for t in tasks}
    aligned = {}
    checked = []
    for record in records:
        task, rep = by_name[record['dataset']], record['repeat']
        assert record['code_signature'] == signature
        parts = split_task(task, rep)
        for split, ids in parts.items():
            np.testing.assert_array_equal(ids, record['parts'][split])
            for other, other_ids in parts.items():
                if split != other:
                    assert not np.intersect1d(task.units[ids], task.units[other_ids]).size
            key = task.split_key, rep, split
            units = np.unique(task.units[ids])
            if key in aligned:
                np.testing.assert_array_equal(aligned[key], units)
            aligned[key] = units
        fitted = {m:restore_fit(record['models'][m]) for m in METHODS}
        check_parameters(task, task.y[parts['fit']], fitted)
        fresh = evaluate(task, rep, parts, fitted)
        for table in ('scores', 'diagnostics', 'selections'):
            assert len(fresh[table]) == len(record[table])
            for a, b in zip(fresh[table], record[table]):
                assert set(a) == set(b)
                for field in a:
                    equal(a[field], b[field])
        checked.append(dict(dataset=task.name, repeat=rep, training_reports=len(parts['fit']),
                            heldout_score_rows=len(fresh['scores'])))
        if len(checked) % 30 == 0:
            print('REPLAYED', len(checked), '/', len(records), 'training contexts', flush=True)
    return checked


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repository-only', action='store_true')
    parser.add_argument('--quick', action='store_true')
    parser.add_argument('--datasets', nargs='*')
    args = parser.parse_args()
    if args.repository_only:
        validate_public()
        return
    tasks = load_tasks()
    if args.datasets:
        tasks = [t for t in tasks if t.name in args.datasets]
        assert len(tasks) == len(set(args.datasets))
    private = ROOT / ('results/private/repeated_holdout_quick' if args.quick else 'results/private/repeated_holdout')
    records = [r for r in read_records(private) if r['dataset'] in {t.name for t in tasks}]
    checks = validate_records(tasks, records, 2 if args.quick else REPETITIONS)
    if not args.quick and not args.datasets:
        manifest = validate_public()
        assert manifest['sources'] == source_inventory()
        for name, frame in tables_from_records(records).items():
            suffix = '.csv.gz' if name.startswith('repeat_') else '.csv'
            frames_equal(pd.read_csv(PUBLIC / (name+suffix)), frame)
        result = dict(training_contexts=len(checks), candidate_fits=len(checks)*len(METHODS),
            heldout_score_rows=sum(c['heldout_score_rows'] for c in checks),
            all_sources_verified=True, all_memberships_verified=True,
            aligned_tasks_verified=True, whole_unit_separation_verified=True,
            all_stored_parameters_checked=True, all_predictions_replayed=True,
            all_diagnostics_and_selectors_replayed=True, all_six_public_tables_recomputed=True,
            refits_performed=0, manifest_sha256=hashlib.sha256((PUBLIC/'manifest.json').read_bytes()).hexdigest(),
            validator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
        (PUBLIC / 'validation.json').write_text(json.dumps(result, indent=2)+'\n')
    print('ALL REQUESTED SAVED-PREDICTION CHECKS PASSED', len(checks), flush=True)


if __name__ == '__main__':
    main()
