"""Selective Mallows and direct Plackett--Luce, with whole-report likelihoods.

W[i,j] counts reports ranking i before j. No independence of pairs is assumed.
Exact Kemeny DP implements Proposition 4.1 of the supplied manuscript.
"""
from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
import time

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, brentq, milp, minimize
from scipy.sparse import coo_matrix
from scipy.special import logsumexp


def validate_rankings(y, n):
    y = np.asarray(y, dtype=np.int64)
    if y.ndim != 2 or not len(y) or y.shape[1] < 2:
        raise ValueError("Expected nonempty rectangular strict rankings, r >= 2")
    if np.any((y < 0) | (y >= n)) or np.any(np.diff(np.sort(y, axis=1), axis=1) == 0):
        raise ValueError("Invalid labels or repeated item within report")
    return y


def pair_counts(y, n):
    y = validate_rankings(y, n)
    w = np.zeros((n, n), dtype=np.int64)
    for a, b in combinations(range(y.shape[1]), 2):
        np.add.at(w, (y[:, a], y[:, b]), 1)
    return w


def positions(order):
    return np.argsort(order)


def distances(y, order):
    z = positions(order)[y]
    d = np.zeros(len(y), dtype=np.int64)
    for a, b in combinations(range(y.shape[1]), 2):
        d += z[:, a] > z[:, b]
    return d


def kemeny_cost(w, order):
    return int(np.tril(w[np.ix_(order, order)], -1).sum())


def kendall(order, truth):
    return int(distances(np.asarray(order)[None, :], truth)[0])


def _priority(n, seed):
    return np.random.default_rng(seed).permutation(n)


def _sort(score, priority, decreasing=False):
    return np.lexsort((priority, -score if decreasing else score))


def borda(w, seed=0):
    """Exposure-normalized signed Borda; paper's global score, without clipping.

    For fixed r, comparison exposure is (r-1) times item appearance count.
    Clipping to [-n,n] after multiplying by n-1 changes nothing here.
    Missing items have score zero.
    """
    exposure = (w + w.T).sum(axis=1)
    score = np.divide((w - w.T).sum(axis=1), exposure,
                      out=np.zeros(len(w)), where=exposure > 0)
    return _sort(score, _priority(len(w), seed), decreasing=True)


def posest(w, seed=0):
    """FKS (2021), Algorithm 1: count opponents with empirical majority >= 1/2.

    As in the published >= rule, a zero-exposure opponent counts as a tie/loss.
    This has no frequent-pair guarantee when pairs are missing. Ties in the
    final scores are broken by a seeded uniform random permutation.
    """
    loss = (w.T >= w).sum(axis=1) - 1
    return _sort(loss, _priority(len(w), seed))


def greedy(w, seed=0):
    """Equal-reliability specialization of Raman--Joachims (2014), Algorithm 2."""
    remaining = list(range(len(w)))
    priority = _priority(len(w), seed)
    order = []
    while remaining:
        sub = w[np.ix_(remaining, remaining)]
        score = (sub - sub.T).sum(axis=1)
        k = int(np.lexsort((priority[remaining], -score))[0])
        order.append(remaining.pop(k))
    return np.asarray(order)


def insertion_search(w, initial):
    """Best improving single-item insertion, repeated to a strict local optimum."""
    order = list(map(int, initial))
    while True:
        best_delta, best_order = 0, None
        for a, item in enumerate(order):
            rest = order[:a] + order[a+1:]
            # Cost involving item when inserted at each of n positions.
            before = np.r_[0, np.cumsum(w[item, rest])]
            after = np.r_[np.cumsum(w[rest, item][::-1])[::-1], 0]
            costs = before + after
            b = int(np.argmin(costs))
            delta = int(costs[b] - costs[a])
            if delta < best_delta:
                best_delta = delta
                best_order = rest[:b] + [item] + rest[b:]
        if best_order is None:
            return np.asarray(order)
        order = best_order


def multistart(w, seed=0, random_starts=5):
    rng = np.random.default_rng(seed)
    starts = [borda(w, seed), posest(w, seed), greedy(w, seed)]
    starts += [rng.permutation(len(w)) for _ in range(random_starts)]
    candidates = [insertion_search(w, x) for x in starts]
    return min(candidates, key=lambda x: kemeny_cost(w, x))


def exact_dp(w, seed=0):
    n = len(w)
    if n > 18:
        raise ValueError("Exponential DP is restricted to n <= 18")
    m = 1 << n
    subset_sums = np.zeros((n, m), dtype=np.int64)
    for mask in range(1, m):
        bit = mask & -mask
        j = bit.bit_length() - 1
        subset_sums[:, mask] = subset_sums[:, mask ^ bit] + w[:, j]
    f = np.full(m, np.iinfo(np.int64).max // 4, dtype=np.int64)
    last = np.full(m, -1, dtype=np.int16)
    f[0] = 0
    labels = _priority(n, seed)
    for mask in range(1, m):
        for i in labels:
            bit = 1 << int(i)
            if mask & bit:
                prev = mask ^ bit
                val = f[prev] + subset_sums[i, prev]
                if val < f[mask]:
                    f[mask], last[mask] = val, i
    order, mask = [], m - 1
    while mask:
        i = int(last[mask])
        order.append(i)
        mask ^= 1 << i
    order = np.asarray(order[::-1])
    assert kemeny_cost(w, order) == f[-1]
    return order


@lru_cache(maxsize=4)
def _linear_order_constraints(n):
    ii, jj = np.triu_indices(n, 1)
    index = np.full((n, n), -1, dtype=int)
    index[ii, jj] = np.arange(len(ii))
    triples = np.asarray(list(combinations(range(n), 3)), dtype=int)
    i, j, k = triples.T
    cols = np.stack([index[i, j], index[j, k], index[i, k]], axis=1)
    rows = np.repeat(np.arange(len(triples)), 3)
    values = np.tile([1., 1., -1.], len(triples))
    a = coo_matrix((values, (rows, cols.ravel())), shape=(len(triples), len(ii))).tocsc()
    return ii, jj, LinearConstraint(a, 0, 1)


def milp_center(w, seed=0, time_limit=10., initial=None):
    """Generic exact linear-order formulation; returns a certificate or a gap.

    x_ij=1 iff i is before j (i<j). 0<=x_ij+x_jk-x_ik<=1 forbids cycles.
    A timed-out incumbent is never labelled an exact MLE without a valid bound.
    """
    n = len(w)
    order = multistart(w, seed) if initial is None else np.asarray(initial)
    upper = kemeny_cost(w, order)
    lower = int(np.minimum(w, w.T)[np.triu_indices(n, 1)].sum())
    if upper == lower:
        return order, {"lower_bound": lower, "certified": True, "status": "pair_bound"}
    ii, jj, constraint = _linear_order_constraints(n)
    base = int(w[ii, jj].sum())
    res = milp((w[jj, ii] - w[ii, jj]).astype(float), integrality=np.ones(len(ii)),
               bounds=Bounds(0, 1), constraints=constraint,
               options={"time_limit": time_limit, "mip_rel_gap": 0.})
    if res.x is not None:
        x = (res.x > .5).astype(int)
        wins = np.zeros(n, dtype=int)
        np.add.at(wins, ii, x)
        np.add.at(wins, jj, 1-x)
        if len(np.unique(wins)) != n:
            raise RuntimeError("MILP returned nontransitive incumbent")
        candidate = np.argsort(-wins)
        value = kemeny_cost(w, candidate)
        if abs(value - (res.fun + base)) > 1e-4:
            raise RuntimeError("MILP objective mismatch")
        if value < upper:
            order, upper = candidate, value
    bound = getattr(res, "mip_dual_bound", None)
    if bound is not None and np.isfinite(bound):
        lower = max(lower, int(np.ceil(bound + base - 1e-5)))
    if lower > upper:
        raise RuntimeError("Invalid lower bound")
    return order, {"lower_bound": lower, "certified": lower == upper,
                   "status": str(res.message)}


def logz_mean(r, beta):
    """Stable exact log normalizer and expected inversions via finite sums."""
    logz, mean = 0., 0.
    for j in range(2, r+1):
        v = np.arange(j)
        a = -beta * v
        z = logsumexp(a)
        logz += z
        mean += float(np.dot(v, np.exp(a-z)))
    return logz, mean


def fit_beta(total_distance, count, r, beta_max=10.):
    d = total_distance / count
    if d >= r*(r-1)/4:
        return 0.
    if d <= logz_mean(r, beta_max)[1]:
        return beta_max
    return float(brentq(lambda b: logz_mean(r, b)[1]-d, 0., beta_max, xtol=1e-12))


@dataclass
class SMFit:
    order: np.ndarray
    beta: float
    objective: int
    metadata: dict

    def nll(self, y, beta_factor=1.):
        beta = self.beta * beta_factor
        return beta * distances(y, self.order) + logz_mean(y.shape[1], beta)[0]


def fit_sm(y, n, seed=0, solver="auto", time_limit=10.):
    t0 = time.perf_counter()
    w = pair_counts(y, n)
    solver = ("dp" if n <= 18 else "milp") if solver == "auto" else solver
    meta = {"solver": solver}
    if solver == "dp":
        order = exact_dp(w, seed)
        meta.update(certified=True, lower_bound=kemeny_cost(w, order))
    elif solver == "milp":
        order, extra = milp_center(w, seed, time_limit)
        meta.update(extra)
    else:
        functions = {"borda": borda, "posest": posest, "greedy": greedy, "multistart": multistart}
        order = functions[solver](w, seed)
        meta.update(certified=False, lower_bound=int(np.minimum(w, w.T)[np.triu_indices(n, 1)].sum()))
    obj = kemeny_cost(w, order)
    beta = fit_beta(obj, len(y), y.shape[1])
    meta.update(seconds=time.perf_counter()-t0, absolute_gap=obj-meta["lower_bound"])
    return SMFit(order, beta, obj, meta)


def pl_nll(y, theta):
    z = np.asarray(theta)[y]
    den = np.logaddexp.accumulate(z[:, ::-1], axis=1)[:, ::-1]
    return (den[:, :-1]-z[:, :-1]).sum(axis=1)


def pl_objective(theta, y, tau):
    z = theta[y]
    den = np.logaddexp.accumulate(z[:, ::-1], axis=1)[:, ::-1]
    grad = np.zeros_like(theta)
    for k in range(y.shape[1]-1):
        probs = np.exp(z[:, k:]-den[:, k, None])
        grad += np.bincount(y[:, k:].ravel(), weights=probs.ravel(), minlength=len(theta))
        grad -= np.bincount(y[:, k], minlength=len(theta))
    value = (den[:, :-1]-z[:, :-1]).sum() + .5*tau*np.dot(theta, theta)
    return float(value), grad+tau*theta


@dataclass
class PLFit:
    theta: np.ndarray
    tau: float
    metadata: dict

    def nll(self, y):
        return pl_nll(y, self.theta)

    @property
    def order(self):
        return np.argsort(-self.theta, kind="stable")


def fit_pl(y, n, tau=1., initial=None):
    if tau <= 0:
        raise ValueError("Use strictly positive ridge for a guaranteed finite fit")
    t0 = time.perf_counter()
    y = validate_rankings(y, n)
    x0 = np.zeros(n) if initial is None else initial
    # Translation invariance plus positive ridge forces the optimum to sum to zero.
    res = minimize(pl_objective, x0, args=(y, tau), jac=True, method="L-BFGS-B",
                   options={"maxiter": 1000, "ftol": 1e-12, "gtol": 1e-7, "maxls": 40})
    theta = res.x-res.x.mean()
    gradnorm = float(np.max(np.abs(pl_objective(theta, y, tau)[1])))
    if not res.success and gradnorm > 1e-4:
        raise RuntimeError(f"PL optimization failed: {res.message}; grad={gradnorm}")
    return PLFit(theta, tau, {"success": bool(res.success), "gradient_max": gradnorm,
                             "seconds": time.perf_counter()-t0})


def tune_pl(train, valid, n, grid=(.01, .1, 1., 10., 100.)):
    fits = [fit_pl(train, n, tau=t) for t in grid]
    losses = [float(f.nll(valid).mean()) for f in fits]
    k = int(np.argmin(losses))
    return grid[k], dict(zip(map(str, grid), losses))


def sample_sm(rng, count, n, r, center, beta):
    """Sample the subset FIRST, then directly draw its Mallows order by insertion."""
    rank = positions(center)
    rows = np.empty((count, r), dtype=int)
    probs = [np.exp(-beta*np.arange(j)) for j in range(1, r+1)]
    probs = [x/x.sum() for x in probs]
    for t in range(count):
        s = rng.choice(n, r, replace=False)
        s = s[np.argsort(rank[s])]
        out = []
        for j, item in enumerate(s, 1):
            inv = int(rng.choice(j, p=probs[j-1]))
            out.insert(j-1-inv, int(item))
        rows[t] = out
    return rows


def sample_pl(rng, count, n, r, theta):
    rows = np.empty((count, r), dtype=int)
    for t in range(count):
        s = rng.choice(n, r, replace=False)
        rows[t] = s[np.argsort(-(theta[s]+rng.gumbel(size=r)))]
    return rows
