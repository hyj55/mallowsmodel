"""Full-data, equal-displayed-gap pair frequencies; no predictive experiment."""
from itertools import combinations
import numpy as np
import pandas as pd

from .models import validate_rankings, pair_counts, exact_dp, kemeny_cost
from .strict_models import exact_integer_center, TIE_SEED


def insertion_order(w, initial):
    """Deterministic, strictly improving Kemeny insertions; no exactness claim."""
    order = list(map(int, initial))
    while True:
        best_delta, best_order = 0, None
        for a, item in enumerate(order):
            rest = order[:a] + order[a+1:]
            costs = (np.r_[0, np.cumsum(w[item, rest])]
                     + np.r_[np.cumsum(w[rest, item][::-1])[::-1], 0])
            b = int(np.argmin(costs))
            delta = int(costs[b] - costs[a])
            if delta < best_delta:
                best_delta, best_order = delta, rest[:b] + [item] + rest[b:]
        if best_order is None:
            return np.asarray(order)
        order = best_order


def reference_center(y, n, seconds=120.):
    """Use all reports for a descriptive center, never for a new test score."""
    w = pair_counts(y, n)
    lower = int(np.minimum(w, w.T)[np.triu_indices(n, 1)].sum())
    meta = dict(certified=False, pairwise_lower_bound=lower, tie_seed=TIE_SEED)
    if n <= 18:
        order = exact_dp(w, TIE_SEED)
        meta.update(method='exact_subset_dp', certified=True)
    else:
        order = None
        if n <= 100:
            order, solver = exact_integer_center(w, seconds)
            meta['integer_solver'] = solver
            if order is not None:
                meta.update(method='certified_integer_center', certified=True)
        if order is None:
            exposure = (w+w.T).sum(axis=1)
            win_rate = np.divide(w.sum(axis=1), exposure,
                                 out=np.full(n, .5), where=exposure > 0)
            priority = np.random.default_rng(TIE_SEED).permutation(n)
            starts = [np.lexsort((priority, -win_rate)),
                      np.lexsort((priority, -(w-w.T).sum(axis=1)))]
            candidates = [insertion_order(w, start) for start in starts]
            order = min(candidates, key=lambda x: (kemeny_cost(w, x), tuple(x)))
            meta.update(method='two_start_insertion_approximation',
                        candidate_objectives=[kemeny_cost(w, x) for x in candidates])
    meta['objective'] = kemeny_cost(w, order)
    meta['pairwise_bound_gap'] = meta['objective'] - lower
    return order, meta


def pair_frequencies(y, order):
    """Every observed pair x h cell, oriented by one declared reference order.

    h is the position difference in the restriction of order to this display,
    not in the global catalogue or the noisy reported ranking. Adjacent h=1.
    """
    order = np.asarray(order, dtype=int)
    if sorted(order.tolist()) != list(range(len(order))):
        raise ValueError('Reference must be a full catalogue permutation')
    y = validate_rankings(y, len(order))
    perm = np.argsort(np.argsort(order)[y], axis=1)
    shown = np.take_along_axis(y, perm, axis=1)
    parts = []
    for a, b in combinations(range(y.shape[1]), 2):
        parts.append(pd.DataFrame(dict(item_i=shown[:, a], item_j=shown[:, b],
            h=b-a, wins=(perm[:, a] < perm[:, b]).astype(int), count=1)))
    cells = pd.concat(parts, ignore_index=True).groupby(
        ['h', 'item_i', 'item_j'], as_index=False, sort=True)[['wins', 'count']].sum()
    cells['losses'] = cells['count'] - cells.wins
    cells['win_rate'] = cells.wins / cells['count']
    assert cells['count'].sum() == len(y)*y.shape[1]*(y.shape[1]-1)//2
    return cells


def summarize_frequencies(cells):
    """Observed dispersion only; no independence, CI or bias correction assumed."""
    rows = []
    for h, g in cells.groupby('h', sort=True):
        count = int(g['count'].sum())
        p = float(g.wins.sum()/count)
        variance = float(np.average((g.win_rate-p)**2, weights=g['count']))
        comparable = len(g) >= 2
        rows.append(dict(h=int(h), pairs=len(g), pair_occurrences=count,
            mean_win_rate=p, heterogeneity_sd=np.sqrt(variance) if comparable else np.nan,
            equal_pair_sd=float(g.win_rate.std(ddof=0)) if comparable else np.nan,
            min_win_rate=float(g.win_rate.min()), max_win_rate=float(g.win_rate.max()),
            count_min=int(g['count'].min()), count_median=float(g['count'].median()),
            count_max=int(g['count'].max()), singleton_cells=int(g['count'].eq(1).sum()),
            occurrence_share_count_ge5=float(g.loc[g['count'].ge(5), 'count'].sum()/count),
            comparable=comparable))
    gaps = pd.DataFrame(rows)
    comparable = gaps.loc[gaps.comparable]
    total = int(cells['count'].sum())
    comparable_total = int(comparable.pair_occurrences.sum())
    summary = dict(pair_gap_cells=len(cells), pair_occurrences=total,
        comparable_gaps=len(comparable), comparable_pair_occurrences=comparable_total,
        comparable_occurrence_share=comparable_total/total,
        heterogeneity_sd=float(np.sqrt(np.average(comparable.heterogeneity_sd**2,
            weights=comparable.pair_occurrences))) if comparable_total else np.nan,
        h1_heterogeneity_sd=float(gaps.loc[gaps.h.eq(1), 'heterogeneity_sd'].iloc[0]),
        count_min=int(cells['count'].min()), count_median=float(cells['count'].median()),
        count_max=int(cells['count'].max()), singleton_cells=int(cells['count'].eq(1).sum()),
        singleton_occurrence_share=float(cells['count'].eq(1).sum()/total),
        occurrence_share_count_ge5=float(cells.loc[cells['count'].ge(5), 'count'].sum()/total))
    return gaps, summary
