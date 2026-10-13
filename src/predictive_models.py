"""Prespecified finite predictors for Algorithm 4.1; no test-driven tuning."""
import math
import time
import numpy as np
from scipy.optimize import Bounds, brentq, milp, minimize

from .models import (validate_rankings, pair_counts, distances, kemeny_cost,
                     logz_mean, pl_nll, _linear_order_constraints)
from .strict_models import StrictFit, TIE_SEED
from .group_sensitivity import exact_dp_batched, fotakis_center
from .manuscript_estimators import efficient_center, score_order
from .resource_sieve import sharp_center, global_sieve_center, SieveResourceError

BETA_MAX = 10.
RIDGE_GRID = (.01, .1, 1., 10., 100.)
MILP_SECONDS = 30.
R_BOUND = 10
METHODS = ('pl', 'sm_likelihood', 'sm_sharp', 'sm_fotakis', 'sm_efficient_fallback', 'sm_global_sieve')


def bounded_beta(total, count, r):
    mean = total/count
    if mean >= r*(r-1)/4:
        return 0.
    if mean <= logz_mean(r, BETA_MAX)[1]:
        return BETA_MAX
    return float(brentq(lambda b: logz_mean(r, b)[1]-mean, 0., BETA_MAX, xtol=1e-12))


def pl_objective(theta, y, tau):
    z = theta[y]
    den = np.logaddexp.accumulate(z[:, ::-1], axis=1)[:, ::-1]
    grad = np.zeros_like(theta)
    for k in range(y.shape[1]-1):
        prob = np.exp(z[:, k:]-den[:, k, None])
        grad += np.bincount(y[:, k:].ravel(), weights=prob.ravel(), minlength=len(theta))
        grad -= np.bincount(y[:, k], minlength=len(theta))
    return float((den[:, :-1]-z[:, :-1]).sum()+.5*tau*(theta @ theta)), grad+tau*theta


def ridge_pl(y, n, tau):
    y = validate_rankings(y, n)
    if tau <= 0:
        raise ValueError('Strictly positive ridge is required')
    started = time.perf_counter()
    options = dict(maxiter=3000, ftol=1e-14, gtol=1e-8, maxls=50, maxcor=20)
    result = minimize(pl_objective, np.zeros(n), args=(y, tau), jac=True,
                      method='L-BFGS-B', options=options)
    theta = result.x-result.x.mean()
    grad = float(np.max(np.abs(pl_objective(theta, y, tau)[1])))
    refinements = 0
    # L-BFGS can stop on objective rounding before the gradient criterion.
    # Positive ridge gives a nonsingular Hessian, so refine that same objective.
    while grad/max(1,len(y)) > 1e-7 and refinements < 5:
        z = theta[y]
        den = np.logaddexp.accumulate(z[:, ::-1],axis=1)[:, ::-1]
        hessian = tau*np.eye(n)
        for k in range(y.shape[1]-1):
            ids = y[:, k:]; p = np.exp(z[:, k:]-den[:, k, None])
            hessian[np.diag_indices(n)] += np.bincount(ids.ravel(),weights=p.ravel(),minlength=n)
            np.add.at(hessian,(ids[:,:,None],ids[:,None,:]),-p[:,:,None]*p[:,None,:])
        gradient = pl_objective(theta,y,tau)[1]
        theta -= np.linalg.solve(hessian,gradient)
        theta -= theta.mean(); refinements += 1
        grad = float(np.max(np.abs(pl_objective(theta,y,tau)[1])))
    # The residual is independently checked even after an optimizer success flag.
    if grad/max(1, len(y)) > 1e-7:
        raise ArithmeticError(f'PL gradient check failed: {grad}, {result.message}')
    return StrictFit('pl', np.argsort(-theta, kind='stable'), theta=theta,
        metadata=dict(tau=tau, penalty='sum_nll_plus_half_tau_l2', gradient_max=grad,
                      gradient_per_report=grad/len(y), converged=True,
                      solver_message=str(result.message), newton_refinements=refinements,
                      seconds=time.perf_counter()-started))


def tune_and_refit_pl(inner, validation, development, n):
    scores = [float(ridge_pl(inner, n, tau).nll(validation).mean()) for tau in RIDGE_GRID]
    index = int(np.argmin(scores))
    fit = ridge_pl(development, n, RIDGE_GRID[index])
    fit.metadata.update(inner_grid=list(RIDGE_GRID), inner_nll=scores,
                        inner_count=len(inner), validation_count=len(validation),
                        refit_count=len(development))
    return fit


def insertion_search(w, initial):
    order = list(map(int, initial))
    while True:
        best_delta, best_order = 0, None
        for a,item in enumerate(order):
            rest = order[:a]+order[a+1:]
            costs = np.r_[0, np.cumsum(w[item, rest])] + np.r_[np.cumsum(w[rest, item][::-1])[::-1], 0]
            b = int(costs.argmin()); delta = int(costs[b]-costs[a])
            if delta < best_delta:
                best_delta = delta; best_order = rest[:b]+[item]+rest[b:]
        if best_order is None:
            return np.asarray(order)
        order = best_order


def likelihood_center(y, n, seconds=MILP_SECONDS):
    started = time.perf_counter(); w = pair_counts(y, n)
    if n <= 18:
        order = exact_dp_batched(w)
        value = kemeny_cost(w, order)
        return order, dict(path='exact_subset_dp', certified=True, lower_bound=value,
                          upper_bound=value, objective_gap=0, seconds=time.perf_counter()-started)
    priority = np.random.default_rng(TIE_SEED).permutation(n)
    starts = [score_order(y, np.arange(n), n, y.shape[1], priority),
              np.lexsort((priority, (w.T >= w).sum(axis=1)))]
    starts += [np.random.default_rng(TIE_SEED+i).permutation(n) for i in range(3)]
    candidates = [insertion_search(w, order) for order in starts]
    order = min(candidates, key=lambda order: (kemeny_cost(w, order), tuple(order)))
    upper = kemeny_cost(w, order)
    ii,jj,constraint = _linear_order_constraints(n)
    lower = int(np.minimum(w, w.T)[ii,jj].sum())
    solver_status = 'pairwise_lower_bound'
    if lower != upper:
        constant = int(w[ii,jj].sum())
        result = milp((w[jj,ii]-w[ii,jj]).astype(float), integrality=np.ones(len(ii)),
            bounds=Bounds(0,1), constraints=constraint,
            options=dict(time_limit=seconds, mip_rel_gap=0.))
        solver_status = str(result.message)
        if result.x is not None:
            if np.max(np.abs(result.x-np.rint(result.x))) > 1e-5:
                raise ArithmeticError('Nonintegral MILP incumbent')
            bits = np.rint(result.x).astype(int); wins = np.zeros(n, int)
            np.add.at(wins, ii, bits); np.add.at(wins, jj, 1-bits)
            if len(np.unique(wins)) != n:
                raise ArithmeticError('Nontransitive MILP incumbent')
            candidate = np.argsort(-wins); cost = kemeny_cost(w, candidate)
            if abs(cost-constant-result.fun) > 1e-4:
                raise ArithmeticError('MILP objective mismatch')
            if (cost,tuple(candidate)) < (upper,tuple(order)):
                order,upper = candidate,cost
        bound = getattr(result, 'mip_dual_bound', None)
        if bound is not None and np.isfinite(bound):
            lower = max(lower, math.ceil(float(bound)+constant-1e-5))
    if lower > upper:
        raise ArithmeticError('Invalid optimization certificate')
    return order, dict(path='integer_plus_multistart', certified=lower == upper,
        lower_bound=lower, upper_bound=upper, objective_gap=upper-lower,
        solver_message=solver_status, milp_seconds_limit=seconds,
        seconds=time.perf_counter()-started)


def sm_fit(method, y, order, metadata):
    if order is None:
        return StrictFit(method, None, status=metadata['status'], metadata=metadata)
    total = int(distances(y, order).sum()); beta = bounded_beta(total, len(y), y.shape[1])
    return StrictFit(method, order, beta=beta,
        metadata=dict(metadata, training_distance=total, beta_max=BETA_MAX,
                      beta_boundary='cap' if beta == BETA_MAX else 'zero' if beta == 0 else 'interior'))


def fit_candidates(inner, validation, development, n, seed):
    N,r = development.shape; lam = N*r*(r-1)/(n*(n-1))
    fits = {'pl':tune_and_refit_pl(inner, validation, development, n)}
    order,meta = likelihood_center(development, n)
    fits['sm_likelihood'] = sm_fit('sm_likelihood', development, order, meta)
    try:
        order,meta = sharp_center(development, n, seed=seed, beta0=.1)
        fits['sm_sharp'] = sm_fit('sm_sharp', development, order, meta)
    except SieveResourceError as exc:
        fits['sm_sharp'] = sm_fit('sm_sharp', development, None,
            dict(exc.metadata, status='sieve_resource_budget'))
    w = pair_counts(development, n); joint = w+w.T
    if (joint[np.triu_indices(n, 1)] == 0).any():
        fits['sm_fotakis'] = sm_fit('sm_fotakis', development, None, dict(status='not_p_frequent'))
    else:
        fits['sm_fotakis'] = sm_fit('sm_fotakis', development, fotakis_center(w),
                                  dict(path='Fotakis_2021_Algorithm_1', pair_min=int(joint[np.triu_indices(n,1)].min())))
    if fits['sm_sharp'].status != 'ok' and lam <= 1:
        order,meta = efficient_center(development, n, seed=TIE_SEED, beta0=.1)
        fits['sm_efficient_fallback'] = sm_fit('sm_efficient_fallback', development, order, meta)
    else:
        fits['sm_efficient_fallback'] = sm_fit('sm_efficient_fallback', development, None,
            dict(status='sharp_available' if fits['sm_sharp'].status == 'ok' else 'outside_schedule_domain'))
    sharp = fits['sm_sharp']
    if r > R_BOUND:
        fits['sm_global_sieve'] = sm_fit('sm_global_sieve', development, None, dict(status='outside_fixed_R'))
    elif sharp.metadata.get('global_sieve_identical'):
        fits['sm_global_sieve'] = StrictFit('sm_global_sieve', sharp.order, beta=sharp.beta,
            status=sharp.status, metadata=dict(sharp.metadata, alias_of='sm_sharp', R_bound=R_BOUND))
    else:
        try:
            order,meta = global_sieve_center(development, n, seed=seed)
            fits['sm_global_sieve'] = sm_fit('sm_global_sieve', development, order, dict(meta,R_bound=R_BOUND))
        except SieveResourceError as exc:
            fits['sm_global_sieve'] = sm_fit('sm_global_sieve', development, None,
                dict(exc.metadata, status='sieve_resource_budget', R_bound=R_BOUND))
    assert set(fits) == set(METHODS)
    return fits
