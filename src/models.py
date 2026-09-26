"""Likelihood mathematics, exact manuscript DP, and direct-subset samplers.

Statistical fitting is defined only in strict_models.py. Superseded capped,
penalized and heuristic fitting entry points are retained in Git history.
"""
from functools import lru_cache
from itertools import combinations
import numpy as np
from scipy.optimize import LinearConstraint
from scipy.sparse import coo_matrix
from scipy.special import logsumexp

def validate_rankings(y, n):
    raw = np.asarray(y)
    if raw.dtype.kind not in "iu":
        raise ValueError("Ranking labels must be integers; no truncation or imputation")
    y = raw.astype(np.int64, copy=False)
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


def pl_nll(y, theta):
    z = np.asarray(theta)[y]
    den = np.logaddexp.accumulate(z[:, ::-1], axis=1)[:, ::-1]
    return (den[:, :-1]-z[:, :-1]).sum(axis=1)


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
