"""Read-only checks of saved estimator/theory comparisons; no experimental fits."""
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.group_sensitivity import fotakis_center
from src.models import pair_counts

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'results/theory_alignment'


def same(actual, expected):
    np.testing.assert_allclose(actual, expected, rtol=1e-11, atol=1e-11, equal_nan=True)


def mean(values, complete=True):
    values = np.asarray(values, dtype=float)
    valid = np.isfinite(values)
    if not valid.any() or (complete and not valid.all()):
        return np.nan
    return values[valid].sum() / valid.sum()


def validate_dimensions(frame):
    n, r, count = (frame[c].to_numpy(float) for c in ('n', 'r', 'N'))
    lam = count * r * (r - 1) / (n * (n - 1))
    nu = n * lam
    with np.errstate(divide='ignore'):
        v = -count * np.log1p(-r / n)
    expected = dict(lambda_=lam, mu=count*r/n, nu=nu, Q=n/lam, Vcov=v,
                    Bcov=n*n*np.exp(-v), coverage_ratio=(count*r/n)/np.log(np.e*r))
    for field, values in expected.items():
        same(frame[field], values)
    flags = dict(lambda_le_one=lam<=1+1e-12, nu_le_one=nu<=1+1e-12,
                 full_ranking=r==n, one_report=count==1,
                 coverage_dominated=(nu>=1)&(v<=np.log(nu)/2))
    for field, values in flags.items():
        assert np.array_equal(frame[field], values), field


def main():
    sources = json.loads((OUT/'sources.json').read_text())
    for entry in sources['saved_inputs']:
        data = (ROOT/entry['destination']).read_bytes()
        assert hashlib.sha256(data).hexdigest() == entry['sha256']
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == entry['git_sha']
    manifest = json.loads((OUT/'manifest.json').read_text())
    for path, expected in {**manifest['outputs'], **manifest['code']}.items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == expected, path
    tables = {name: pd.read_csv(OUT/(name+'.csv')) for name in manifest['rows']}
    for name, frame in tables.items():
        assert len(frame) == manifest['rows'][name]
    for name in ('p1_regimes', 'pure_sm_results', 'c1_sm_centers'):
        validate_dimensions(tables[name])

    p1 = pd.read_csv(ROOT/'results/repeated_holdout/repeat_scores.csv.gz')
    p1 = p1.loc[p1.split.eq('confirmation')]
    assert len(p1) == 575 and not p1.duplicated(['dataset','repeat','method']).any()
    for row in tables['p1_regimes'].itertuples():
        raw = p1.loc[p1.dataset.eq(row.dataset)&p1.method.eq('mle')]
        assert len(raw) == 5
        same(raw[['n','r','n_train']].to_numpy(), np.tile([row.n,row.r,row.N], (5,1)))
        assert row.pair_min_across_partitions == raw.min_pair_count.min()
        assert row.max_unseen_items == raw.unseen_items.max()
        assert row.all_pairs_observed_every_partition == raw.min_pair_count.gt(0).all()
    for row in tables['p1_methods'].itertuples():
        raw = p1.loc[p1.dataset.eq(row.dataset)&p1.method.eq(row.method)]
        assert row.partitions == len(raw) == 5
        assert row.successful_fits == raw.status.eq('ok').sum()
        assert json.loads(row.status_counts) == dict(Counter(raw.status))
        assert json.loads(row.branch_counts) == dict(Counter(raw.branch.dropna()))
        same(row.maximum_recorded_depth, raw.depth.max())
        assert row.finite_nll_partitions == np.isfinite(raw.nll).sum()
        same(row.nll_mean, mean(raw.nll))
        same(row.finite_conditional_nll, mean(raw.nll, False))
        same(row.objective_reference_kendall, mean(raw.objective_kendall))
    for row in tables['p1_estimator_contrasts'].itertuples():
        raw = p1.loc[p1.dataset.eq(row.dataset)]
        paired = raw.loc[raw.method.eq(row.method_a)].merge(
            raw.loc[raw.method.eq(row.method_b)], on='repeat', validate='one_to_one')
        diff = paired.nll_x.to_numpy()-paired.nll_y.to_numpy()
        assert len(diff) == row.partitions == 5
        assert np.isfinite(diff).sum() == row.finite_paired_partitions
        same(row.mean_nll_difference, mean(diff))
        same(row.finite_conditional_nll_difference, mean(diff, False))
        assert row.equal_nll_partitions == (np.isfinite(diff)&(np.abs(diff)<=1e-12)).sum()
    assert tables['p1_regimes'].lambda_le_one.sum() == 2
    assert tables['p1_regimes'].full_ranking.sum() == 9
    efficient = tables['p1_methods'].query('method == "efficient"')
    assert efficient.successful_fits.sum() == 10
    assert efficient.maximum_recorded_depth.dropna().eq(0).all()

    synthetic = tables['pure_sm_results']
    assert len(synthetic) == 209
    source_cache = {}
    for row in synthetic.itertuples():
        if row.source not in source_cache:
            source_cache[row.source] = pd.read_csv(ROOT/row.source)
        raw = source_cache[row.source]
        mask = raw.n.eq(row.n)&raw.r.eq(row.r)&raw.N.eq(row.N)&raw.method.eq(row.method)
        if row.component == 'S1_S2':
            mask &= raw.value.eq(0)&raw['shape'].eq(row.shape)
        else:
            mask &= raw.dgp.eq('SM')
        match = raw.loc[mask]
        assert len(match) == 1, (row.source, row.n, row.r, row.N, row.method)
        match = match.iloc[0]
        for field in ('risk','risk_lo','risk_hi','repetitions','nll'):
            same(getattr(row, field), match[field])
        same(row.successful_fits, match['ok'] if row.component=='S1_S2' else match.repetitions)
        expected = row.n / np.sqrt(row.N+1) / np.cosh(.4)**row.N if row.r==row.n else np.nan
        same(row.full_rank_shape, expected)
    for path, raw in source_cache.items():
        expected = raw.value.eq(0).sum() if 'value' in raw else raw.dgp.eq('SM').sum()
        assert synthetic.source.eq(path).sum() == expected

    g1 = pd.read_csv(ROOT/'results/group_sensitivity/repeat_scores.csv.gz')
    keys = ['dataset','design','percent','scheme']
    assert len(g1[keys].drop_duplicates()) == len(tables['g1_fotakis_vs_exact']) == 90
    for row in tables['g1_fotakis_vs_exact'].itertuples():
        mask = np.ones(len(g1), bool)
        for field in keys:
            mask &= g1[field].eq(getattr(row, field))
        raw = g1.loc[mask]
        paired = raw.loc[raw.method.eq('sm_fotakis')].merge(
            raw.loc[raw.method.eq('sm_mle')], on='repeat', validate='one_to_one')
        diff = paired.nll_all_x.to_numpy()-paired.nll_all_y.to_numpy()
        finite = np.isfinite(diff)
        assert row.repetitions == len(diff)
        assert row.complete_finite_pairs == finite.sum()
        same(row.fotakis_minus_exact, mean(diff))
        same(row.finite_conditional_difference, mean(diff, False))
        assert row.identical_nll_repetitions == (finite&(np.abs(diff)<=1e-12)).sum()
        same(row.max_absolute_difference, np.abs(diff[finite]).max() if finite.any() else np.nan)
    c1 = pd.read_csv(OUT/'inputs/c1_synthetic_algorithms.csv').query('dgp == "SM"')
    for row in tables['c1_sm_centers'].itertuples():
        raw = c1.loc[c1.N.eq(row.N)&c1.algorithm.eq(row.method)]
        assert len(raw) == row.repetitions == 30
        same(row.risk, mean(raw.central_kendall))
        same(row.mean_training_objective_gap, mean(raw.objective_gap))
        same(row.max_training_objective_gap, raw.objective_gap.max())
        assert row.zero_objective_gap_repetitions == raw.objective_gap.eq(0).sum()

    # A mathematical toy profile, not a new experimental sample or model fit.
    w = pair_counts(np.array([[0,1,2],[1,2,0]]), 3)
    for seed in range(10):
        assert fotakis_center(w, seed)[0] == 1
    tournament = (w>w.T) | ((w==w.T)&np.triu(np.ones((3,3),bool),1))
    assert list(np.argsort(-tournament.sum(axis=1), kind='stable')) == [0,1,2]
    # On every three-report profile of three items, no pair ties exist and
    # predecessor scores are n-1 minus tournament wins.
    for reports in itertools.product(itertools.permutations(range(3)), repeat=3):
        w = pair_counts(np.array(reports), 3)
        predecessors = w.T >= w
        np.fill_diagonal(predecessors, False)
        same(predecessors.sum(axis=1), 2-(w>w.T).sum(axis=1))
    print('Verified source bytes, all derived rows, regime identities, finite denominators, and majority tie distinctions.')


if __name__ == '__main__':
    main()
