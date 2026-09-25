"""Check the new cluster diagnostic against the existing report-level definition."""
import itertools
import numpy as np
from run_context_followup import context, village_weights
from src.diagnostics import pair_arrays, context_slope


def test_cluster_definition_reduces_to_report_bootstrap():
    y = np.array([p for s in itertools.combinations(range(4), 3)
                  for p in itertools.permutations(s)] * 2)
    arrays = pair_arrays(y, np.arange(4), .8, np.array([.6, .2, -.2, -.6]))
    groups = np.arange(len(y))
    weights = village_weights(groups, 513)
    actual = context(arrays, groups, weights)
    reference = context_slope(arrays, seed=513)
    for key in ['observed', 'observed_lo', 'observed_hi', 'sm_predicted',
                'residual_vs_sm_lo', 'residual_vs_sm_hi', 'valid_bootstraps']:
        np.testing.assert_allclose(actual[key], reference[key], atol=1e-12)


def test_whole_cluster_resampling():
    groups = np.array([2, 2, 4, 4, 4, 9])
    weights = village_weights(groups, 17)
    assert np.array_equal(weights[:, 0], weights[:, 1])
    assert np.array_equal(weights[:, 2], weights[:, 3])
    assert np.array_equal(weights[:, 3], weights[:, 4])
    assert np.all(weights[:, [0, 2, 5]].sum(axis=1) == 3)
