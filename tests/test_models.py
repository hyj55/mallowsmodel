from itertools import permutations
import numpy as np
import pytest
from src.models import (distances, exact_dp, kemeny_cost, logz_mean,
                        pair_counts, pl_nll, sample_sm, validate_rankings)
from src.strict_models import exact_integer_center, profile_beta_unbounded


def test_exact_dp_and_integer_program_match_exhaustive_search():
    rng = np.random.default_rng(81)
    for n in [3, 5, 7]:
        y = np.array([rng.choice(n, 3, replace=False) for _ in range(17)])
        w = pair_counts(y, n)
        optimum = min(kemeny_cost(w, p) for p in permutations(range(n)))
        dp = exact_dp(w, 3)
        mip, certificate = exact_integer_center(w, 10.)
        assert certificate['certified']
        assert kemeny_cost(w, dp) == kemeny_cost(w, mip) == optimum
        assert distances(y, dp).sum() == optimum


def test_distributions_normalize_and_profile_score():
    beta, r = .8, 5
    orders = np.array(list(permutations(range(r))))
    d = distances(orders, np.arange(r))
    logz, mean = logz_mean(r, beta)
    p = np.exp(-beta*d-logz)
    np.testing.assert_allclose(p.sum(), 1.)
    np.testing.assert_allclose(p@d, mean)
    np.testing.assert_allclose(profile_beta_unbounded(100*mean, 100, r), beta, atol=1e-10)
    np.testing.assert_allclose(np.exp(-pl_nll(orders, np.array([1., .3, .1, -.7, -.9]))).sum(), 1.)


def test_sampler_is_direct_subset_mallows():
    rng = np.random.default_rng(999)
    y = sample_sm(rng, 12000, 5, 2, np.arange(5), .8)
    select = np.all(np.sort(y, axis=1) == np.array([0, 4]), axis=1)
    reversal = np.mean(y[select, 0] == 4)
    p = 1/(1+np.exp(.8))
    assert abs(reversal-p) < 5*np.sqrt(p*(1-p)/select.sum())
    assert abs(distances(y, np.arange(5)).mean()-p) < .02


def test_no_silent_label_truncation_or_data_repair():
    for y in [[[0.1, 1.9]], [[0, 0]], [[0, 9]], [['0', '1']]]:
        with pytest.raises(ValueError):
            validate_rankings(y, 3)
