"""Validate current artifacts without fitting or changing an estimator.

--repository-only checks committed artifacts without downloaded source data and
does not write files. Full mode additionally reconstructs source reports and
recomputes saved predictions, then records the checks that actually passed.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import warnings

import numpy as np
import pandas as pd

from src.models import distances, pair_counts, kemeny_cost, logz_mean
from src.strict_models import StrictFit, pl_mm_step

ROOT = Path(__file__).resolve().parent
AUDIT = ROOT / 'results/audit'


def read_json(path):
    return json.loads((ROOT / path).read_text())


def write_json(path, value):
    (ROOT / path).write_text(json.dumps(value, indent=2) + '\n')


def current_files():
    ignored = {'.git', '__pycache__', '.pytest_cache', '.venv', 'audit_before'}
    return [p for p in ROOT.rglob('*') if p.is_file()
            and not any(x in ignored for x in p.relative_to(ROOT).parts)
            and not p.is_relative_to(ROOT/'data/raw')]


def repository_checks():
    files = current_files()
    link_count, python_count = 0, 0
    for path in files:
        if path.suffix not in {'.md', '.py', '.yml', '.json', '.csv', '.txt', '.bib'}:
            continue
        content = path.read_text()
        assert not re.search(r'^(?:<{7}|>{7}|={7})$', content, re.M), path
        assert not re.search(r'^(?:<{7}|>{7}) ', content, re.M), path
        assert not any(ord(c) < 32 and c not in '\n\r\t' for c in content), path
        if path.suffix == '.py':
            ast.parse(content, filename=str(path))
            python_count += 1
        if path.suffix == '.md':
            for target in re.findall(r'!?\[[^\]]*\]\(([^)\s]+)\)', content):
                if re.match(r'^[a-zA-Z]+:', target) or target.startswith('#'):
                    continue
                target = target.split('#')[0]
                assert (path.parent / target).exists(), (path.relative_to(ROOT), target)
                link_count += 1
    # Exact repeated prose files are usually an unintended second active copy.
    documents = [p for p in files if p.suffix == '.md' and p.stat().st_size > 300]
    seen = {}
    for path in documents:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest not in seen, (seen.get(digest), path)
        seen[digest] = path
    retired = read_json('results/audit/retired_paths.json')
    assert all(not (ROOT/p).exists() for p in retired)
    names = {node.name for node in ast.parse((ROOT/'src/models.py').read_text()).body
             if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
    assert not names.intersection({'fit_pl', 'fit_sm', 'fit_beta', 'fit_mallows'})
    workflow = (ROOT/'.github/workflows/strict_features.yml').read_text()
    assert 'contents: read' in workflow and 'contents: write' not in workflow
    assert 'git push' not in workflow
    strict = pd.read_csv(ROOT/'results/strict_features/real_results.csv')
    assert len(strict) == 80
    anonymous = ~strict.dataset.str.startswith('dots2024')
    assert strict.loc[anonymous, ['delta_lo', 'delta_hi']].isna().all().all()
    assert strict.loc[anonymous, 'uncertainty_status'].eq('unavailable_assessor_ids').all()
    wheat = pd.read_csv(ROOT/'results/context_followup/scores.csv')
    assert len(wheat) == 10 and wheat[['delta_lo', 'delta_hi']].isna().all().all()
    context = pd.read_csv(ROOT/'results/context_followup/context.csv')
    interval_columns = [c for c in context if c.endswith(('_lo', '_hi'))]
    assert context[interval_columns].isna().all().all()
    assert context.loc[context.village_fixed_effects, 'status'].eq('unavailable_missing_village').all()
    split = pd.read_csv(ROOT/'results/context_followup/splits.csv')
    assert len(split) == 493 and split.row.nunique() == 493 and split.village.eq(-1).sum() == 113
    baseline = pd.read_csv(ROOT/'results/baseline_replacement/scores.csv')
    assert len(baseline) == 15
    assert baseline.loc[baseline.dataset.eq('beans'), ['delta_lo', 'delta_hi']].isna().all().all()
    assert baseline.loc[baseline.method.eq('mle'), 'status'].eq('ok').all()
    assert baseline.loc[baseline.method.eq('sharp'), 'status'].eq('exact_sieve_unavailable').all()
    assert baseline.loc[baseline.method.eq('efficient'), 'status'].eq('outside_schedule_domain').all()
    parameters = read_json('results/baseline_replacement/parameters.json')
    certificate = parameters['sushi_b']['mle']['metadata']
    assert certificate['certified'] and certificate['lower_bound'] == certificate['upper_bound'] == 45149
    splits = pd.read_csv(ROOT/'results/baseline_replacement/splits.csv')
    a = splits[splits.dataset.eq('sushi_a')][['row', 'split']].reset_index(drop=True)
    b = splits[splits.dataset.eq('sushi_b')][['row', 'split']].reset_index(drop=True)
    pd.testing.assert_frame_equal(a, b)
    for name, N in [('beans', 842), ('sushi_a', 5000), ('sushi_b', 5000)]:
        group = splits[splits.dataset.eq(name)]
        assert len(group) == N and set(group.row) == set(range(N))
    return dict(status='passed', parsed_python_files=python_count,
                local_markdown_links=link_count, exact_duplicate_documents=0,
                conflict_markers=0, retired_paths_absent=len(retired),
                anonymous_intervals_withdrawn=True, missing_villages_not_used_as_clusters=True,
                baseline_source_rows_preserved=10842, sushi_respondent_folds_aligned=True,
                sushi_b_certified_integer_objective=45149,
                workflow_read_only=True)


def restore(method, saved):
    return StrictFit(method, None if saved['order'] is None else np.asarray(saved['order']),
                     beta=float(saved['beta']),
                     theta=None if saved['theta'] is None else np.asarray(saved['theta']),
                     status=saved['status'], metadata=saved['metadata'])


def check_fit(fit, train, n):
    if fit.status != 'ok':
        return
    if fit.method == 'pl':
        worth = np.exp(fit.theta)
        worth /= worth.sum()
        wins = np.bincount(train[:, :-1].ravel(), minlength=n)
        _, denominator = pl_mm_step(train, worth, wins)
        assert np.max(np.abs(wins - worth*denominator))/len(train) < 1e-8
    else:
        d = int(distances(train, fit.order).sum())
        assert d == fit.metadata['training_distance']
        if 0 < fit.beta < np.inf:
            assert abs(logz_mean(train.shape[1], fit.beta)[1] - d/len(train)) < 1e-10
        if fit.method == 'mle':
            assert fit.metadata['certified']
            assert kemeny_cost(pair_counts(train, n), fit.order) == d
            if 'lower_bound' in fit.metadata:
                assert fit.metadata['lower_bound'] == fit.metadata['upper_bound'] == d


def check_manifest(manifest, base):
    for entry in manifest:
        payload = (base/entry['file']).read_bytes()
        assert hashlib.sha256(payload).hexdigest() == entry['sha256'], entry['file']
        if 'bytes' in entry:
            assert len(payload) == entry['bytes']
    return len(manifest)


def baseline_checks():
    from src.data import load_all
    from run_strict_real import ci
    from run_baseline_replacement import SEED
    out = ROOT/'results/baseline_replacement'
    check_manifest(read_json('results/baseline_replacement/data_manifest.json'), ROOT/'data/raw')
    parameters = read_json('results/baseline_replacement/parameters.json')
    scores, splits = pd.read_csv(out/'scores.csv'), pd.read_csv(out/'splits.csv')
    count = 0
    for task in load_all():
        group = splits[splits.dataset.eq(task.name)]
        train = task.y[group.loc[group.split.eq('fit'), 'row']]
        test = task.y[group.loc[group.split.eq('confirmation'), 'row']]
        pl = restore('pl', parameters[task.name]['pl']).nll(test)
        for method, saved in parameters[task.name].items():
            fit = restore(method, saved)
            check_fit(fit, train, task.n)
            row = scores[(scores.dataset == task.name) & (scores.method == method)].iloc[0]
            losses, deltas = fit.nll(test), fit.nll(test)-pl
            assert row.status == fit.status
            assert np.allclose([row.nll, row.delta], [losses.mean(), deltas.mean()],
                               rtol=0, atol=1e-12, equal_nan=True)
            low, high = ci(deltas, SEED, unit_identified=task.name != 'beans')
            assert np.allclose([row.delta_lo, row.delta_hi], [low, high],
                               rtol=0, atol=1e-12, equal_nan=True)
            count += 1
    record = dict(status='passed', source_files_verified=2, source_reports=10842,
                  reports_dropped=0, saved_fit_rows_checked=count,
                  point_values_and_conditional_intervals_recomputed=True,
                  all_three_mle_objectives_certified=True,
                  prefit_protocol_commit='517990bb8cc7111513eeca9dac5dd3d97e25831b')
    write_json('results/baseline_replacement/validation.json', record)
    return record


def wheat_checks():
    import rdata
    from src.diagnostics import pair_arrays, context_slope
    source_count = check_manifest(read_json('data/context_followup_sources.json'),
                                  ROOT/'data/raw/context_followup')
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', UserWarning)
        frame = rdata.read_rda(ROOT/'data/raw/context_followup/breadwheat.rda')['breadwheat']
    saved = read_json('results/context_followup/parameters.json')
    labels = {x:i for i, x in enumerate(saved['items'])}
    # Independent decoding: remove the two named endpoints to find the middle.
    reports = []
    for _, row in frame.iterrows():
        items = {key: row['variety_'+key.lower()] for key in 'ABC'}
        middle, = set('ABC') - {row.overall_best, row.overall_worst}
        reports.append([labels[items[k]] for k in (row.overall_best, middle, row.overall_worst)])
    y = np.asarray(reports)
    splits = pd.read_csv(ROOT/'results/context_followup/splits.csv')
    assert np.array_equal(splits.village.eq(-1), frame.village.isna().iloc[splits.row])
    train = y[splits.loc[splits.split.eq('fit'), 'row']]
    scores = pd.read_csv(ROOT/'results/context_followup/scores.csv')
    contexts = pd.read_csv(ROOT/'results/context_followup/context.csv')
    fits = {name: restore(name, p) for name, p in saved['models'].items()}
    for fit in fits.values():
        check_fit(fit, train, 16)
    for split in ['discovery', 'confirmation']:
        test = y[splits.loc[splits.split.eq(split), 'row']]
        pl = fits['pl'].nll(test)
        for name, fit in fits.items():
            row = scores[(scores.split == split) & (scores.method == name)].iloc[0]
            assert np.allclose([row.nll, row.delta], [fit.nll(test).mean(), (fit.nll(test)-pl).mean()],
                               rtol=0, atol=1e-12, equal_nan=True)
        arrays = pair_arrays(test, fits['mle'].order, fits['mle'].beta, fits['pl'].theta)
        computed = context_slope(arrays, resamples=0)
        row = contexts[(contexts.split == split) & ~contexts.village_fixed_effects].iloc[0]
        for key in ['observed', 'sm_predicted', 'pl_predicted', 'eligible_pairs', 'pair_observations']:
            assert np.isclose(row[key], computed[key], rtol=0, atol=1e-12), key
    record = dict(status='passed', source_files_verified=source_count,
                  ranking_reports=493, ranking_reports_dropped=0,
                  saved_score_rows_checked=10, unadjusted_context_rows_checked=2,
                  missing_village_labels=113, inferential_intervals_available=False,
                  village_adjusted_diagnostic='unavailable_missing_village',
                  parameter_refit_comparison='../audit/refit_comparison.json')
    write_json('results/context_followup/validation.json', record)
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repository-only', action='store_true')
    args = parser.parse_args()
    result = {'repository': repository_checks()}
    if not args.repository_only:
        result['baseline_replacement'] = baseline_checks()
        result['context_followup'] = wheat_checks()
        result['strict_feature_validation'] = read_json('results/strict_features/validation.json')['status']
        assert result['strict_feature_validation'] == 'passed'
        result['implementation_hashes'] = {
            str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted((ROOT/'src').glob('*.py'))}
        result['status'] = 'passed'
        write_json('results/audit/validation.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
