"""Missing sampling identities must not silently generate inferential intervals."""
import itertools
import numpy as np
from run_strict_real import ci
from src.diagnostics import context_slope, pair_arrays
from src.manuscript_estimators import efficient_center
import pytest


def test_point_only_context_preserves_statistic_without_bootstrap():
    y = np.array([p for s in itertools.combinations(range(4), 3)
                  for p in itertools.permutations(s)] * 2)
    arrays = pair_arrays(y, np.arange(4), .8, np.array([.6, .2, -.2, -.6]))
    point = context_slope(arrays, resamples=0)
    reference = context_slope(arrays, resamples=20, seed=513)
    for key in ['observed', 'sm_predicted', 'pl_predicted', 'residual_vs_sm']:
        np.testing.assert_allclose(point[key], reference[key], atol=1e-12)
    assert point['valid_bootstraps'] == 0
    assert np.isnan(point['observed_lo']) and np.isnan(point['observed_hi'])


def test_unknown_independent_units_have_no_interval():
    values = np.array([.1, .2, -.3, .5])
    assert np.isnan(ci(values, 17, unit_identified=False)).all()
    assert np.isfinite(ci(values, 17, unit_identified=True)).all()


def test_direct_efficient_entry_point_cannot_cap_lambda():
    with pytest.raises(ValueError, match='lambda <= 1'):
        efficient_center(np.tile(np.arange(3), (10, 1)), 3)
