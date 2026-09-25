import itertools
import numpy as np
from scipy.optimize import minimize
from src.strict_models import (fit_pl_mm, pl_mm_step, profile_beta_unbounded,
                               fit_sm_strict, exact_integer_center)
from src.strict_features import (small_law, report_space, population_features,
                                 strict_pair_loss)
from src.models import pl_nll, logz_mean, pair_counts, kemeny_cost, exact_dp


def test_mm_matches_independent_likelihood_optimization():
    rng = np.random.default_rng(714)
    all_y, probabilities, _ = small_law(5, 3, 'bridge', .4, 'equal')
    y = all_y[rng.choice(len(all_y), 400, p=probabilities)]
    model = fit_pl_mm(y, 5)
    assert model.status == 'ok'
    def loss(x):
        theta = np.r_[x, -np.sum(x)]
        return pl_nll(y, theta).sum()
    result = minimize(loss, np.zeros(4), method='BFGS', options={'gtol': 1e-7})
    assert abs(loss(result.x)-pl_nll(y, model.theta).sum()) < 1e-6
    assert model.metadata['gradient_per_report'] < 1e-8
    worth = np.array([1., 2., 3., 4., 5.]); worth /= worth.sum()
    wins = np.bincount(y[:, :-1].ravel(), minlength=5)
    denom = np.zeros(5)
    for row in y:
        for k in range(len(row)-1):
            for item in row[k:]:
                denom[item] += 1/worth[row[k:]].sum()
    expected = wins/denom; expected /= expected.sum()
    assert np.allclose(pl_mm_step(y, worth, wins)[0], expected, atol=1e-13)


def test_boundary_and_domain_outcomes_are_not_repaired():
    y = np.tile(np.arange(3), (10, 1))
    assert fit_pl_mm(y, 3).status == 'no_unique_finite_mle'
    sm = fit_sm_strict(y, 3)
    assert np.isinf(sm.beta)
    assert sm.nll(y[:1])[0] == 0
    assert np.isinf(sm.nll(np.array([[1, 0, 2]]))[0])
    assert fit_sm_strict(y, 3, 'efficient').status == 'outside_schedule_domain'
    assert profile_beta_unbounded(30, 10, 3) == 0
    beta = profile_beta_unbounded(1, 1000000, 3)
    assert beta > 10
    assert abs(logz_mean(3, beta)[1]-1e-6) < 1e-12


def test_declared_noise_and_shell_controls():
    for shape in ['equal', 'alternating']:
        for value in [0., .25, .5, .75, 1.]:
            _, p, _ = small_law(8, 3, 'bridge', value, shape)
            assert abs(p.sum()-1) < 1e-12
        base = population_features(8, 3, 'bridge', 0., shape)
        half = population_features(8, 3, 'bridge', .5, shape)
        endpoint = population_features(8, 3, 'bridge', 1., shape)
        assert abs(endpoint['context_slope']) < 1e-12
        assert abs(half['context_slope']-.5*base['context_slope']) < 1e-12
        assert abs(base['within_shell_kl']) < 1e-12
        sets, local, reports, d = report_space(8, 3)
        _, p0, _ = small_law(8, 3, 'shell', 0., shape)
        _, p4, _ = small_law(8, 3, 'shell', 4., shape)
        for distance in np.unique(d):
            a = p0.reshape(len(sets), -1)[:, d == distance].sum(axis=1)
            b = p4.reshape(len(sets), -1)[:, d == distance].sum(axis=1)
            assert np.allclose(a, b, atol=1e-13)


def test_pair_marginals_and_integer_certificate():
    y = np.array(list(itertools.permutations(range(4))))
    sm = fit_sm_strict(y, 4)
    assert np.allclose(strict_pair_loss(y, sm), np.log(2))
    w = pair_counts(np.vstack([y, np.tile([3, 1, 0, 2], (5, 1))]), 4)
    order, info = exact_integer_center(w, 10.)
    assert info['certified']
    assert kemeny_cost(w, order) == kemeny_cost(w, exact_dp(w))
