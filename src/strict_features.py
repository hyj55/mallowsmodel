"""Declared synthetic interventions and diagnostics, not replacement estimators."""
from functools import lru_cache
from itertools import combinations, permutations
import math
import numpy as np
from scipy.optimize import brentq
from scipy.special import expit, logsumexp
from .models import distances, logz_mean, pl_nll, positions
from .diagnostics import sm_pair_probability, pair_arrays


def matched_worths(n, r, shape, beta=.8):
    gaps = np.ones(n-1)
    if shape == 'alternating':
        gaps[1::2] = 4.
    elif shape != 'equal':
        raise ValueError(shape)
    base = -np.r_[0., np.cumsum(gaps)]
    base -= base.mean()
    a, b = np.triu_indices(n, 1)
    target = logz_mean(r, beta)[1]
    inclusion = r*(r-1)/(n*(n-1))
    scale = brentq(lambda z: inclusion*expit(z*(base[b]-base[a])).sum()-target, 0., 1000.)
    return scale*base


@lru_cache(None)
def report_space(n, r):
    sets = np.array(list(combinations(range(n), r)), dtype=int)
    local = np.array(list(permutations(range(r))), dtype=int)
    reports = sets[:, local].reshape(-1, r)
    d = distances(local, np.arange(r))
    return sets, local, reports, d


@lru_cache(maxsize=128)
def small_law(n, r, family, value, shape, beta=.8):
    sets, local, reports, d = report_space(n, r)
    theta = matched_worths(n, r, shape, beta)
    sm = np.exp(-beta*d-logz_mean(r, beta)[0])
    pl = np.exp(-pl_nll(reports, theta)).reshape(len(sets), -1)
    if family == 'bridge':
        conditional = (1-value)*sm[None, :] + value*pl
    elif family == 'shell':
        conditional = np.empty_like(pl)
        for distance in np.unique(d):
            mask = d == distance
            logits = value*np.log(pl[:, mask])
            shell_mass = sm[mask].sum()
            conditional[:, mask] = shell_mass*np.exp(logits-logsumexp(logits, axis=1)[:, None])
    else:
        raise ValueError(family)
    if not np.allclose(conditional.sum(axis=1), 1., atol=2e-13):
        raise ArithmeticError('Unnormalized law')
    mean = float((conditional*d[None, :]).sum(axis=1).mean())
    if abs(mean-logz_mean(r, beta)[1]) > 1e-10:
        raise ArithmeticError('Average noise was not held fixed')
    if family == 'shell':
        for distance in np.unique(d):
            if not np.allclose(conditional[:, d == distance].sum(axis=1),
                               sm[d == distance].sum(), atol=2e-13):
                raise ArithmeticError('Shell intervention changed a shell mass')
    return reports, conditional.ravel()/len(sets), theta


def draw_small(rng, count, truth, family, value, shape, r):
    reports, probabilities, _ = small_law(len(truth), r, family, value, shape)
    return truth[reports[rng.choice(len(reports), count, p=probabilities)]]


def draw_large(rng, count, truth, r, value, shape='equal'):
    """Whole reports generated directly conditional on uniform subsets."""
    n = len(truth)
    subset = np.sort(np.argsort(rng.random((count, n)), axis=1)[:, :r], axis=1)
    theta = matched_worths(n, r, shape)
    choose_pl = rng.random(count) < value
    out = np.empty_like(subset)
    if choose_pl.any():
        s = subset[choose_pl]
        out[choose_pl] = np.take_along_axis(s, np.argsort(-(theta[s]+rng.gumbel(size=s.shape)), axis=1), axis=1)
    if (~choose_pl).any():
        s = subset[~choose_pl]
        y = np.empty_like(s); y[:, 0] = s[:, 0]
        for j in range(1, r):
            p = np.exp(-.8*np.arange(j+1)); p /= p.sum()
            where = j-rng.choice(j+1, size=len(s), p=p)
            cols = np.arange(j+1)[None, :]
            source = np.clip(cols-(cols >= where[:, None]), 0, j-1)
            old = np.take_along_axis(y[:, :j], source, axis=1)
            y[:, :j+1] = np.where(cols == where[:, None], s[:, j, None], old)
        out[~choose_pl] = y
    return truth[out]


def population_features(n, r, family, value, shape):
    sets, local, reports, d = report_space(n, r)
    _, joint, _ = small_law(n, r, family, value, shape)
    p = joint.reshape(len(sets), -1)*len(sets)
    ranks = np.argsort(local, axis=1)
    pairs, gaps, rates = [], [], []
    shell_kl = 0.
    for dist in np.unique(d):
        mask = d == dist
        mass = p[:, mask].sum(axis=1)
        shell_kl += float((p[:, mask]*np.log(p[:, mask]*mask.sum()/mass[:, None])).sum()/len(sets))
    for a, b in combinations(range(r), 2):
        pairs.extend((sets[:, a]*n+sets[:, b]).tolist())
        gaps.extend([b-a]*len(sets))
        rates.extend((p[:, ranks[:, a] < ranks[:, b]].sum(axis=1)).tolist())
    pairs, gaps, rates = map(np.asarray, (pairs, gaps, rates))
    within_gap = np.empty_like(rates)
    for h in np.unique(gaps):
        within_gap[gaps == h] = rates[gaps == h]-rates[gaps == h].mean()
    centered_h, centered_p = np.zeros(len(rates)), np.zeros(len(rates))
    for pair in np.unique(pairs):
        mask = pairs == pair
        centered_h[mask] = gaps[mask]-gaps[mask].mean()
        centered_p[mask] = rates[mask]-rates[mask].mean()
    denom = centered_h@centered_h
    return dict(mean_inversions=float(joint@distances(reports, np.arange(n))),
                equal_gap_probability_sd=float(np.sqrt(np.mean(within_gap**2))),
                within_shell_kl=shell_kl,
                context_probability_sd=float(np.sqrt(np.mean(centered_p**2))),
                context_slope=float(centered_h@centered_p/denom) if denom else np.nan)


def strict_pair_loss(y, model):
    """Average pair log loss within a whole report; no probability clipping."""
    if model.status != 'ok':
        return np.full(len(y), np.nan)
    a, b = np.triu_indices(y.shape[1], 1)
    if model.theta is not None:
        return np.logaddexp(0., model.theta[y[:, b]]-model.theta[y[:, a]]).mean(axis=1)
    z = np.argsort(np.argsort(positions(model.order)[y], axis=1), axis=1)
    h = np.abs(z[:, a]-z[:, b])
    p = np.ones_like(h, float) if np.isinf(model.beta) else sm_pair_probability(h, model.beta)
    outcome_probability = np.where(z[:, a] < z[:, b], p, 1-p)
    with np.errstate(divide='ignore'):
        return (-np.log(outcome_probability)).mean(axis=1)


def context_point(y, sm, pl):
    if sm.status != 'ok' or pl.status != 'ok' or not np.isfinite(sm.beta):
        return {'eligible_cells': 0, 'status': 'fit_unavailable'}
    a = pair_arrays(y, sm.order, sm.beta, pl.theta)
    pairs = a['pair'].ravel(); h = a['gap'].ravel().astype(float)
    z = a['z'].ravel(); ps = a['sm'].ravel()
    numer, expected, denominator, eligible = 0., 0., 0., 0
    for pair in np.unique(pairs):
        mask = pairs == pair
        _, count = np.unique(h[mask], return_counts=True)
        if (count >= 2).sum() < 2:
            continue
        x = h[mask]-h[mask].mean()
        numer += x@z[mask]; expected += x@ps[mask]
        denominator += x@x; eligible += 1
    if not denominator:
        return {'eligible_cells': eligible, 'status': 'insufficient_context_variation'}
    return {'eligible_cells': eligible, 'status': 'ok', 'observed': numer/denominator,
            'sm_predicted': expected/denominator, 'pl_predicted': 0.}


def discovery_choices(y, sm, pl):
    a, b = strict_pair_loss(y, sm).mean(), strict_pair_loss(y, pl).mean()
    choice = 'abstain'
    if not np.isnan(a) and not np.isnan(b) and not (np.isinf(a) and np.isinf(b)):
        choice = 'sm' if a < b else 'pl'
    context = context_point(y, sm, pl)
    c = 'abstain'
    if context['status'] == 'ok':
        c = 'sm' if abs(context['observed']-context['sm_predicted']) < abs(context['observed']) else 'pl'
    return dict(pair_choice=choice, discovery_pair_sm=a, discovery_pair_pl=b,
                context_choice=c, **{'context_'+k: v for k, v in context.items()})
