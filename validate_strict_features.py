"""Replay consequential invariants and compare with recorded pre-disconnect results."""
import hashlib
import importlib.metadata
import json
import platform
import runpy
import numpy as np
import pandas as pd
from run_strict_real import ROOT, OUT, load_tasks, split_task
from src.strict_models import StrictFit, pl_mm_step
from src.models import distances, pair_counts, kemeny_cost, logz_mean


def run():
    checks = {}
    for name, subdir in [('strict_feature_sources.json', ''), ('strict_tricot_sources.json', 'tricot')]:
        manifest = json.loads((ROOT/'data'/name).read_text())
        for row in manifest:
            data = (ROOT/'data/raw/strict_features'/subdir/row['file']).read_bytes()
            assert hashlib.sha256(data).hexdigest() == row['sha256'], row['file']
        checks[name] = len(manifest)
    suite = runpy.run_path(str(ROOT/'tests/test_strict_features.py'))
    passed = []
    for name, fn in suite.items():
        if name.startswith('test_'):
            fn(); passed.append(name)
    checks['independent_algorithm_checks'] = passed
    fitted = json.loads((OUT/'real_parameters.json').read_text())
    recorded_splits = pd.read_csv(OUT/'real_splits.csv')
    saved_predictions = pd.read_csv(OUT/'real_predictions.csv')
    models_checked = 0
    for index, task in enumerate(load_tasks()):
        name = task['name']; y = task['y']; fit, disc, test = split_task(task, index)
        assert len(set(fit) | set(disc) | set(test)) == len(y)
        for a, b in [(fit, disc), (fit, test), (disc, test)]:
            assert not (set(task['group'][a]) & set(task['group'][b]))
        for split, indices in [('fit', fit), ('discovery', disc), ('confirmation', test)]:
            s = recorded_splits[(recorded_splits.dataset == name) & (recorded_splits.split == split)]
            assert np.array_equal(s.record.to_numpy(), indices)
        for method, saved in fitted[name].items():
            model = StrictFit(method, None if saved['order'] is None else np.array(saved['order']),
                beta=float(saved['beta']), theta=None if saved['theta'] is None else np.array(saved['theta']),
                status=saved['status'], metadata=saved['metadata'])
            p = saved_predictions[(saved_predictions.dataset == name) & (saved_predictions.method == method)]
            assert np.array_equal(p.record.to_numpy(), test)
            assert np.allclose(model.nll(y[test]), p.nll, equal_nan=True, atol=1e-12)
            if model.status == 'ok':
                if method == 'pl':
                    worth = np.exp(model.theta); worth /= worth.sum()
                    wins = np.bincount(y[fit, :-1].ravel(), minlength=task['n'])
                    _, denom = pl_mm_step(y[fit], worth, wins)
                    assert np.max(np.abs(wins-worth*denom))/len(fit) < 1e-8
                else:
                    d = distances(y[fit], model.order).sum()
                    assert d == model.metadata['training_distance']
                    if 0 < model.beta < np.inf:
                        assert abs(logz_mean(task['r'], model.beta)[1]-d/len(fit)) < 1e-10
                    if method == 'mle':
                        assert model.metadata['certified']
                        assert kemeny_cost(pair_counts(y[fit], task['n']), model.order) == d
                        if 'lower_bound' in model.metadata:
                            assert model.metadata['lower_bound'] == d == model.metadata['upper_bound']
            models_checked += 1
    checks.update(real_tasks=len(fitted), real_fit_rows=models_checked,
                  source_reports=sum(len(t['y']) for t in load_tasks()), reports_dropped=0)
    total = 0
    for part, expected in [('bridge', 3200), ('shell', 1200), ('coverage', 360)]:
        s = pd.read_csv(OUT/f'{part}_selection_replicates.csv')
        fits = pd.read_csv(OUT/f'{part}_replicates.csv')
        assert len(s) == expected and not s.duplicated(['cell', 'rep']).any()
        assert fits.groupby(['cell', 'rep']).size().eq(3 if part == 'coverage' else 5).all()
        admitted = fits[(fits.method == 'efficient') & (fits.status == 'ok')]
        assert admitted.lambda_.le(1).all() and admitted.depth.eq(0).all()
        total += len(s)
    checks['independent_synthetic_training_datasets'] = total
    budget = pd.read_csv(OUT/'followup_budget_replicates.csv')
    assert len(budget) == 200*4*2
    checks['reused_training_datasets_in_budget_followup'] = 200
    audit = pd.read_csv(OUT/'tricot_eligibility.csv')
    assert len(audit) == 9 and not audit.eligible.any()
    checks['agricultural_candidates_all_reported'] = len(audit)
    checks['agricultural_fits'] = 0
    # These rounded numbers were recorded in the conversation before the
    # original workspace disconnected. They are validation targets, not inputs.
    expected = {
      '00024-00000001':-.026219, '00024-00000002':-.005448,
      '00024-00000003':-.034527, '00024-00000004':-.049548,
      '00025-00000001':.015911, '00025-00000002':-.077022,
      '00025-00000003':-.040099, '00025-00000004':-.010547,
      'dots2024_A_r3':.055920, 'dots2024_A_r5':.203438, 'dots2024_A_r6':.349638,
      'dots2024_B_r2':.088686, 'dots2024_B_r3':.289975,
      'dots2024_B_r5':.153208, 'dots2024_B_r6':-.126071}
    rr = pd.read_csv(OUT/'real_results.csv')
    rr = rr[rr.method == 'mle'].set_index('dataset')
    checks['pre_disconnect_real_deltas'] = {k: {
        'recorded_rounded': v, 'reproduced': float(rr.loc[k, 'delta']),
        'matches_to_rounding': bool(abs(rr.loc[k, 'delta']-v) < 1e-6)} for k, v in expected.items()}
    for part, targets in [('bridge', [-.054769, -.029927, -.003498, .028333, .064658]),
                          ('shell', [-.055495, -.027025, -.002569, .038823, .070849])]:
        s = pd.read_csv(OUT/f'{part}_summary.csv')
        s = s[(s.method == 'mle') & (s.n == 8) & (s.r == 3) &
              (s.N == 448) & (s['shape'] == 'equal')].sort_values('value')
        assert np.allclose(s.delta, targets, atol=1e-6, rtol=0)
    checks['pre_disconnect_primary_simulation_deltas_match'] = True
    accuracy = budget[budget.selector == 'pair'].groupby('budget').correct.mean()
    assert np.allclose(accuracy, [.685, .74, .825, .955])
    checks['pre_disconnect_budget_accuracies_match'] = True
    checks['runtime'] = {'python': platform.python_version(), **{x: importlib.metadata.version(x)
                        for x in ['numpy', 'scipy', 'pandas', 'matplotlib']}}
    checks['protocol_hashes'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in (ROOT/'docs/protocols').glob('STRICT*.md')}
    checks['status'] = 'passed'
    (OUT/'validation.json').write_text(json.dumps(checks, indent=2)+'\n')
    print(json.dumps(checks, indent=2))


if __name__ == '__main__':
    run()
