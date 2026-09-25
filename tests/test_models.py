from itertools import permutations

import numpy as np
from scipy.optimize import check_grad

from src.models import (distances, exact_dp, fit_beta, fit_pl, insertion_search,
                        kemeny_cost, logz_mean, milp_center, pair_counts, pl_nll,
                        pl_objective, sample_sm)
from src.cutting_plane import cutting_plane_center


def test_exact_dp_and_milp_match_exhaustive_search():
    rng = np.random.default_rng(81)
    for n in [3, 5, 7]:
        y = np.array([rng.choice(n, 3, replace=False) for _ in range(17)])
        w = pair_counts(y, n)
        optimum = min(kemeny_cost(w, p) for p in permutations(range(n)))
        dp = exact_dp(w, 3)
        mip, certificate = milp_center(w, seed=3, time_limit=5)
        assert kemeny_cost(w, dp) == optimum
        assert kemeny_cost(w, mip) == optimum
        assert certificate["certified"]
        assert distances(y, dp).sum() == optimum
        cut, cut_certificate = cutting_plane_center(w, seed=3, time_limit=5)
        assert kemeny_cost(w, cut) == optimum
        assert cut_certificate["certified"]


def test_distributions_normalize_and_profile_score():
    beta, r = .8, 5
    orders = np.array(list(permutations(range(r))))
    d = distances(orders, np.arange(r))
    logz, mean = logz_mean(r, beta)
    p = np.exp(-beta*d-logz)
    np.testing.assert_allclose(p.sum(), 1.)
    np.testing.assert_allclose(p@d, mean)
    np.testing.assert_allclose(fit_beta(100*mean, 100, r), beta, atol=1e-10)
    np.testing.assert_allclose(np.exp(-pl_nll(orders, np.array([1., .3, .1, -.7, -.9]))).sum(), 1.)


def test_pl_gradient_and_finite_fit_on_disconnected_data():
    y = np.array([[0, 2, 1], [2, 0, 1], [0, 1, 2]])
    x = np.array([.5, -.2, .3, -.6])
    err = check_grad(lambda t: pl_objective(t, y, .7)[0],
                     lambda t: pl_objective(t, y, .7)[1], x)
    assert err < 1e-5
    fit = fit_pl(y, 4, tau=.1)
    assert np.isfinite(fit.nll(y)).all()
    assert abs(fit.theta.sum()) < 1e-10
    assert abs(fit.theta[3]) < 1e-5


def test_insertion_is_monotone_and_locally_optimal():
    rng = np.random.default_rng(62)
    w = rng.integers(0, 12, size=(8, 8))
    np.fill_diagonal(w, 0)
    start = rng.permutation(8)
    out = insertion_search(w, start)
    objective = kemeny_cost(w, out)
    assert objective <= kemeny_cost(w, start)
    for i in range(8):
        rest = list(out[:i])+list(out[i+1:])
        for j in range(8):
            alt = rest[:j]+[out[i]]+rest[j:]
            assert kemeny_cost(w, alt) >= objective


def test_sampler_is_direct_subset_mallows():
    rng = np.random.default_rng(999)
    y = sample_sm(rng, 12000, 5, 2, np.arange(5), .8)
    # Even globally far-apart items have the SAME reversal probability for r=2.
    select = np.all(np.sort(y, axis=1) == np.array([0, 4]), axis=1)
    reversal = np.mean(y[select, 0] == 4)
    p = 1/(1+np.exp(.8))
    assert abs(reversal-p) < 5*np.sqrt(p*(1-p)/select.sum())
    assert abs(distances(y, np.arange(5)).mean()-p) < .02
