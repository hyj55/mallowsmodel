"""Published estimators without statistical stabilization.

SM: manuscript Algorithms 2.1/3.1, (3.4), Propositions 4.1/4.2.
PL: Hunter (2004), Section 5, simultaneous MM update (30).
Numerical failures and nonexistent finite estimates are outcomes, not repaired.
"""
from dataclasses import dataclass
import math
import numpy as np
from scipy.optimize import Bounds, brentq, milp
from scipy.sparse.csgraph import connected_components
from .models import (validate_rankings, pair_counts, exact_dp, distances,
                     logz_mean, kemeny_cost, _linear_order_constraints, pl_nll)
from .manuscript_estimators import efficient_center, sharp_center, score_order

TIE_SEED = 93847


@dataclass
class StrictFit:
    method: str
    order: object
    beta: float = math.nan
    theta: object = None
    status: str = 'ok'
    metadata: object = None

    def nll(self, y):
        if self.status != 'ok':
            return np.full(len(y), np.nan)
        if self.theta is not None:
            return pl_nll(y, self.theta)
        d = distances(y, self.order)
        if np.isinf(self.beta):
            return np.where(d == 0, 0., np.inf)
        return self.beta*d + logz_mean(y.shape[1], self.beta)[0]


def profile_beta_unbounded(total, count, r):
    """Proposition 4.2 including its two exact boundary cases."""
    d = total / count
    if d == 0:
        return np.inf
    if d >= r*(r-1)/4:
        return 0.
    upper = 1.
    while logz_mean(r, upper)[1] > d:
        upper *= 2
    return float(brentq(lambda b: logz_mean(r, b)[1]-d, 0., upper, xtol=1e-12))


def exact_integer_center(w, seconds=120.):
    """Conitzer et al. (2006) integral linear-order formulation.

    Antisymmetric variables are eliminated algebraically. No uncertified
    incumbent or insertion heuristic is returned as an exact center.
    """
    n = len(w)
    ii, jj, constraints = _linear_order_constraints(n)
    constant = int(w[ii, jj].sum())
    res = milp((w[jj, ii]-w[ii, jj]).astype(float),
               integrality=np.ones(len(ii)), bounds=Bounds(0, 1),
               constraints=constraints,
               options={'time_limit': seconds, 'mip_rel_gap': 0.})
    meta = {'solver_status': int(res.status), 'solver_message': str(res.message),
            'certified': False, 'time_limit': seconds}
    if res.x is None:
        return None, meta
    bits = np.rint(res.x).astype(int)
    wins = np.zeros(n, int)
    np.add.at(wins, ii, bits)
    np.add.at(wins, jj, 1-bits)
    if len(np.unique(wins)) != n:
        raise ArithmeticError('Nontransitive integer solution')
    order = np.argsort(-wins)
    upper = kemeny_cost(w, order)
    lower = math.ceil(float(res.mip_dual_bound)+constant-1e-6)
    if lower > upper or abs(float(res.fun)+constant-upper) > 1e-5:
        raise ArithmeticError('Invalid integer certificate')
    meta.update(lower_bound=lower, upper_bound=upper, certified=lower == upper)
    return (order if meta['certified'] else None), meta


def fit_sm_strict(y, n, method='mle', beta0=.8, pair_seed=0, milp_seconds=120.):
    y = validate_rankings(y, n)
    N, r = y.shape
    lam = N*r*(r-1)/(n*(n-1))
    meta = {'lambda': lam, 'beta0': beta0, 'tie_seed': TIE_SEED}
    if method == 'mle':
        w = pair_counts(y, n)
        if n <= 18:
            order = exact_dp(w, TIE_SEED)
            meta.update(branch='exact_subset_dp', certified=True)
        else:
            order, info = exact_integer_center(w, milp_seconds)
            meta.update(info, branch='exact_integer_formulation')
            if order is None:
                return StrictFit(method, None, status='optimum_not_certified', metadata=meta)
    elif method == 'sharp':
        try:
            order, info = sharp_center(y, n, pair_seed, beta0)
        except ValueError as e:
            if 'Exact sieve limited' not in str(e):
                raise
            return StrictFit(method, None, status='exact_sieve_unavailable', metadata=meta)
        meta.update(info)
    elif method == 'efficient':
        if lam > 1:
            return StrictFit(method, None, status='outside_schedule_domain', metadata=meta)
        # The legacy min(lambda,1) is identically lambda on this admitted domain.
        order, info = efficient_center(y, n, TIE_SEED, beta0)
        meta.update(info)
    elif method == 'borda':
        priority = np.random.default_rng(TIE_SEED).permutation(n)
        order = score_order(y, np.arange(n), n, r, priority)
        meta.update(branch='published_global_clipped_borda', depth=0)
    else:
        raise ValueError(method)
    total = int(distances(y, order).sum())
    beta = profile_beta_unbounded(total, N, r)
    meta.update(training_distance=total, beta_boundary='infinite' if np.isinf(beta)
                else ('zero' if beta == 0 else 'interior'))
    return StrictFit(method, order, beta=beta, metadata=meta)


def pl_mm_step(y, worth, nonlast_counts):
    """Exactly Hunter (30); exclude the trivial final choice of each ranking."""
    risk_sums = np.cumsum(worth[y][:, ::-1], axis=1)[:, ::-1]
    inv = 1/risk_sums
    inv[:, -1] = 0.
    exposure = np.bincount(y.ravel(), weights=np.cumsum(inv, axis=1).ravel(),
                           minlength=len(worth))
    update = nonlast_counts/exposure
    update /= update.sum()  # unidentifiable scale only
    return update, exposure


def fit_pl_mm(y, n, tolerance=1e-10, max_iterations=100000):
    y = validate_rankings(y, n)
    w = pair_counts(y, n)
    components, labels = connected_components(w > 0, directed=True, connection='strong')
    meta = {'algorithm': 'Hunter_2004_equation_30', 'components': int(components),
            'tolerance': tolerance, 'max_iterations': max_iterations,
            'penalty': 0., 'pseudo_comparisons': 0}
    if components != 1:
        return StrictFit('pl', None, status='no_unique_finite_mle', metadata=meta)
    wins = np.bincount(y[:, :-1].ravel(), minlength=n)
    worth = np.full(n, 1/n)
    initial_loss = float(pl_nll(y, np.log(worth)).sum())
    old_loss = initial_loss
    monotonic_error = 0.
    for iteration in range(1, max_iterations+1):
        new, exposure = pl_mm_step(y, worth, wins)
        if not np.all(np.isfinite(new)) or np.any(new <= 0):
            return StrictFit('pl', None, status='numerical_failure', metadata=meta)
        change = float(np.max(np.abs(np.log(new)-np.log(worth))))
        worth = new
        if iteration % 25 == 0 or change < tolerance:
            loss = float(pl_nll(y, np.log(worth)).sum())
            monotonic_error = max(monotonic_error, loss-old_loss)
            if loss > old_loss + 1e-8*max(1., abs(old_loss)):
                raise ArithmeticError('MM decreased the likelihood')
            old_loss = loss
        if change < tolerance:
            break
    _, exposure = pl_mm_step(y, worth, wins)
    gradient = wins-worth*exposure
    theta = np.log(worth); theta -= theta.mean()
    residual = float(np.max(np.abs(gradient))/len(y))
    meta.update(iterations=iteration, max_log_change=change,
                gradient_per_report=residual, monotonic_error=monotonic_error,
                training_nll=float(pl_nll(y, theta).mean()))
    if change >= tolerance or residual > 1e-8:
        return StrictFit('pl', None, status='not_converged', metadata=meta)
    priority = np.random.default_rng(TIE_SEED).permutation(n)
    order = np.lexsort((priority, -theta))
    return StrictFit('pl', order, theta=theta, metadata=meta)
