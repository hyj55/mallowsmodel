"""Whole-report mechanism diagnostics for the direct subset ranking laws.

The shell DP and decomposition are algebraic diagnostics developed for this
project; they are not proposed as estimators from the supplied manuscript.
"""
from functools import lru_cache
from itertools import combinations

import numpy as np
from scipy.special import expit

from .models import distances, logz_mean, pl_nll, positions


@lru_cache(None)
def shell_counts(r):
    counts = np.array([1], dtype=np.int64)
    for j in range(2, r + 1):
        counts = np.convolve(counts, np.ones(j, dtype=np.int64))
    return counts


def sm_pair_probability(h, beta):
    """Manuscript Lemma 2.3, stable finite sums also at beta=0."""
    h = np.asarray(h, dtype=int)
    lookup = np.zeros(int(h.max()) + 1)
    for gap in np.unique(h):
        s = np.arange(1, gap + 1)
        t = np.arange(1, gap + 2)
        pr = np.exp(-beta * (s - 1)); pr /= pr.sum()
        pt = np.exp(-beta * (gap + 1 - t)); pt /= pt.sum()
        lookup[gap] = (pr[:, None] * pt[None, :] * (t[None, :] > s[:, None])).sum()
    return lookup[h]


def pl_shell_distribution(sets_in_center_order, theta, batch_size=96):
    """Exact distribution of inversions about a fixed center under subset PL.

    H_A(z) = sum_{i in A} w_i/sum_{j in A}w_j * z^{#{j in A:j<i}} H_{A-i}(z).
    Items are indexed in center order. All rows may have different displayed sets.
    Batch working storage is O(batch * 2^r * r^2), not O(r!).
    """
    sets = np.asarray(sets_in_center_order, dtype=int)
    r = sets.shape[1]
    length = r * (r - 1) // 2 + 1
    result = np.empty((len(sets), length))
    for start in range(0, len(sets), batch_size):
        chosen = sets[start:start + batch_size]
        z = np.asarray(theta)[chosen]
        w = np.exp(z - z.max(axis=1, keepdims=True))
        dp = np.zeros((len(chosen), 1 << r, length))
        mass = np.zeros((len(chosen), 1 << r))
        dp[:, 0, 0] = 1
        for mask in range(1, 1 << r):
            bit = mask & -mask
            mass[:, mask] = mass[:, mask ^ bit] + w[:, bit.bit_length() - 1]
            k = mask.bit_count()
            prev_length = (k - 1) * (k - 2) // 2 + 1
            for i in range(r):
                if not (mask & (1 << i)):
                    continue
                shift = (mask & ((1 << i) - 1)).bit_count()
                dp[:, mask, shift:shift + prev_length] += (
                    (w[:, i] / mass[:, mask])[:, None]
                    * dp[:, mask ^ (1 << i), :prev_length]
                )
        result[start:start + len(chosen)] = dp[:, -1]
    if not np.allclose(result.sum(axis=1), 1, atol=1e-12):
        raise ArithmeticError("PL shell probabilities do not sum to one")
    return result


def shell_decomposition(y, center, beta, theta):
    y = np.asarray(y)
    r = y.shape[1]
    sorted_sets = np.take_along_axis(y, np.argsort(positions(center)[y], axis=1), axis=1)
    unique, inverse = np.unique(sorted_sets, axis=0, return_inverse=True)
    distribution = pl_shell_distribution(unique, theta)
    d = distances(y, center)
    log_count = np.log(shell_counts(r)[d])
    pl_shell_nll = -np.log(distribution[inverse, d])
    sm_nll = beta * d + logz_mean(r, beta)[0]
    full_pl_nll = pl_nll(y, theta)
    sym_nll = pl_shell_nll + log_count
    radial, within = sm_nll - sym_nll, sym_nll - full_pl_nll
    if not np.allclose(radial + within, sm_nll - full_pl_nll, atol=1e-11):
        raise ArithmeticError("Shell decomposition identity failed")
    return {"total": sm_nll - full_pl_nll, "shell_mass": radial,
            "within_shell": within, "sm_nll": sm_nll,
            "pl_nll": full_pl_nll, "sym_nll": sym_nll}


def pair_arrays(y, center, beta, theta):
    """Columns enumerate center-position pairs, rows remain independent reports."""
    order_indices = np.argsort(positions(center)[y], axis=1)
    ordered = np.take_along_axis(y, order_indices, axis=1)
    a, b = np.array(list(combinations(range(y.shape[1]), 2))).T
    first, second = ordered[:, a], ordered[:, b]
    gap = np.broadcast_to(b - a, first.shape)
    z = (order_indices[:, a] < order_indices[:, b]).astype(float)
    sm = sm_pair_probability(gap, beta)
    worth_gap = np.asarray(theta)[first] - np.asarray(theta)[second]
    pl = expit(worth_gap)
    return {"z": z, "gap": gap, "sm": sm, "pl": pl,
            "pair": first * len(center) + second, "worth_gap": worth_gap}


def binary_nll(z, p):
    p = np.clip(p, 1e-12, 1 - 1e-12)
    return -(z * np.log(p) + (1-z) * np.log1p(-p))


def context_slope(arrays, strata=None, resamples=2000, seed=20260925, return_draws=False):
    """Pair fixed effects (or pair x stratum), report-cluster percentile bootstrap.

    The slope is descriptive and linear, not an extra fitted preference model.
    All regressors and eligibility use the displayed sets and frozen center only.
    """
    m, npairs = arrays["z"].shape
    pair = arrays["pair"].ravel()
    if strata is None:
        strata = np.zeros(m, dtype=int)
    _, strata_id = np.unique(strata, return_inverse=True)
    keys = np.column_stack([pair, np.repeat(strata_id, npairs)])
    _, cells = np.unique(keys, axis=0, return_inverse=True)
    h = arrays["gap"].ravel().astype(float)
    maxgap = int(h.max()) + 1
    frequency = np.bincount(cells * maxgap + h.astype(int),
                           minlength=(cells.max()+1) * maxgap).reshape(-1, maxgap)
    eligible = (frequency >= 2).sum(axis=1) >= 2
    keep = eligible[cells]
    info = {"eligible_cells": int(eligible.sum()),
            "eligible_pairs": int(len(np.unique(pair[keep]))),
            "pair_observations": int(keep.sum()),
            "reports": int(len(np.unique(np.repeat(np.arange(m), npairs)[keep])))}
    if not np.any(keep):
        return {**info, "status": "insufficient_within_cell_context_variation"}
    c = cells[keep]; _, c = np.unique(c, return_inverse=True)
    x = h[keep]
    report = np.repeat(np.arange(m), npairs)[keep]
    z = np.column_stack([arrays[name].ravel()[keep] for name in ["z", "sm", "pl"]])

    def slope(report_weights):
        weights = report_weights[report]
        sw = np.bincount(c, weights=weights)
        sx = np.bincount(c, weights=weights*x, minlength=len(sw))
        meanx = np.divide(sx, sw, out=np.zeros_like(sx), where=sw > 0)
        residual = x - meanx[c]
        denom = np.sum(weights * residual**2)
        if denom <= 1e-12:
            return np.full(3, np.nan)
        return ((weights*residual)[:, None] * z).sum(axis=0) / denom

    estimate = slope(np.ones(m))
    rng = np.random.default_rng(seed)
    sims = np.array([slope(np.bincount(rng.integers(m, size=m), minlength=m))
                     for _ in range(resamples)])
    raw_sims = sims
    sims = sims[np.isfinite(sims).all(axis=1)]
    answer = {**info, "status": "ok", "valid_bootstraps": len(sims)}
    for j, name in enumerate(["observed", "sm_predicted", "pl_predicted"]):
        answer[name] = float(estimate[j])
        answer[name+"_lo"], answer[name+"_hi"] = map(float, np.quantile(sims[:,j], [.025,.975]))
    for j, name in [(1,"residual_vs_sm"),(2,"residual_vs_pl")]:
        answer[name] = float(estimate[0]-estimate[j])
        answer[name+"_lo"], answer[name+"_hi"] = map(float, np.quantile(sims[:,0]-sims[:,j], [.025,.975]))
    if return_draws:
        answer["_draws"] = raw_sims
    return answer
