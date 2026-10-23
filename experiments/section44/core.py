"""Direct-subset simulation and parameterized manuscript Algorithms 2.1/3.1.

Only numerical calibration changes: core length 2W, padding 3W, offsets,
orientation-independent pair extraction and the exact greedy sieve are retained.
"""
from dataclasses import asdict, dataclass
from functools import lru_cache
import hashlib
import math
from pathlib import Path
import time

import numpy as np

from src.manuscript_estimators import padded_blocks, proof_constants, extract_pairs
from src.models import pair_counts
from src.resource_sieve import SieveResourceError, lexicographic_dp
from src.sieve_budget_retry import retry_sieve_order


@dataclass(frozen=True)
class Calibration:
    A: float = 256.
    c_width: float = 1.
    K: float | None = None
    c_terminal: float = 8.

    def asdict(self):
        return asdict(self)


PROOF = Calibration()


def digest_array(x):
    x = np.asarray(x, dtype='<i4')
    return hashlib.sha256(str(x.shape).encode()+x.tobytes()).hexdigest()


def direct_sm(rng, N, n, r, center, beta, chunk=2048):
    """Floyd uniform subsets, followed by independent Mallows insertions.

    The vectorization changes sampling speed, not the distribution. Each chunk
    draws uniform subsets before drawing its inversion variables. No full-n
    Mallows ranking is sampled/restricted. Chunk size is part of stream replay.
    """
    rank = np.argsort(center)
    out = np.empty((N, r), np.int32)
    for first in range(0, N, chunk):
        count = min(chunk, N-first)
        subsets = np.empty((count, r), np.int32)
        for k, j in enumerate(range(n-r, n)):
            t = rng.integers(0, j+1, size=count)
            duplicate = (subsets[:, :k] == t[:, None]).any(axis=1)
            subsets[:, k] = np.where(duplicate, j, t)
        subsets = np.take_along_axis(subsets, np.argsort(rank[subsets], axis=1), axis=1)
        orders = np.empty_like(subsets)
        for j in range(1, r+1):
            # Inverse CDF of P(V=v) proportional to exp(-beta*v), 0<=v<j.
            u = rng.random(count)
            v = np.floor(-np.log1p(-u*(-np.expm1(-beta*j)))/beta).astype(int)
            v = np.clip(v, 0, j-1)
            position = j-1-v
            cols = np.arange(j)[None, :]
            if j > 1:
                src = np.clip(cols-(cols > position[:, None]), 0, j-2)
                shifted = np.take_along_axis(orders[:, :j-1], src, axis=1)
                orders[:, :j] = np.where(cols == position[:, None], subsets[:, j-1, None], shifted)
            else:
                orders[:, 0] = subsets[:, 0]
        out[first:first+count] = orders
    return out


def kendall_fast(order, truth):
    ranks = np.argsort(truth)[np.asarray(order)]
    tree = np.zeros(len(order)+1, np.int64)
    seen, inv = 0, 0
    for value in ranks:
        i = int(value)+1
        total, j = 0, i
        while j:
            total += int(tree[j]); j -= j & -j
        inv += seen-total
        while i < len(tree):
            tree[i] += 1; i += i & -i
        seen += 1
    return inv


def coordinates(n, r, N):
    lam = N*r*(r-1)/(n*(n-1))
    v = None if r == n else -N*math.log1p(-r/n)
    return dict(lambda_=lam, mu=N*r/n, Vcov=v, Vcov_infinite=r == n,
                expected_unseen=0. if r == n else n*math.exp(-v),
                coverage_shape=0. if r == n else n*n*math.exp(-v),
                information_shape=min(n*n, n/lam), Nr=N*r)


def make_schedule(n, r, N, eta, beta0, cfg):
    c = proof_constants(beta0)
    K = c['K'] if cfg.K is None else cfg.K
    lam = N*r*(r-1)/(n*(n-1))
    m, used, stages = n, 0, []
    while eta*m > cfg.A:
        width = max(1, math.ceil(cfg.c_width*(math.sqrt(m/eta)+1/eta)))
        cap = min(m, 8*width)
        if cap >= m:
            return dict(status='noncontracting', stages=stages, used=used,
                        eta=eta, next_width=width, terminal_cap=m)
        s = len(stages)+1
        ell = math.log(c['CT'])+s*math.log(8)+math.log1p(lam*m)
        batch = math.ceil(K*eta*ell*n*(n-1)/(r*(r-1)))
        stages.append(dict(width=width, cap=cap, batch=batch, ell=ell))
        used += batch
        m = cap
        if used > N//2:
            return dict(status='sample_budget', stages=stages, used=used,
                        eta=eta, terminal_cap=m)
    return dict(status='feasible', stages=stages, used=used, eta=eta, terminal_cap=m)


def plan(n, r, N, beta0, cfg, family):
    lam = N*r*(r-1)/(n*(n-1))
    low = (r-1)/(n-1)
    if lam > 1+1e-12:
        return dict(status='outside_lambda_domain', candidates=[], stages=[], used=0)
    if family == 'sharp':
        p = make_schedule(n, r, N, low, beta0, cfg)
        p['candidates'] = [{k:v for k,v in p.items() if k != 'stages'}]
        return p
    candidates, eta = [], lam
    while eta >= low:
        candidates.append(eta); eta /= 2
    if N*r/n >= 1 and (not candidates or candidates[-1] != low):
        candidates.append(low)
    attempts = []
    for eta in candidates:
        p = make_schedule(n, r, N, eta, beta0, cfg)
        attempts.append({k:v for k,v in p.items() if k != 'stages'})
        if p['status'] == 'feasible':
            return dict(p, candidates=attempts)
    return dict(status='no_feasible_resolution', candidates=attempts, stages=[], used=0)


def score_nodes(y, labels_list, n, r, priority, chunk=512):
    """Stream report memberships; never scan every node for every report.

    Counts use all appearances of an item in this fresh batch, as (3.4) does.
    At a depth, the same fresh batch supplies every overlapping node.
    """
    lengths = np.asarray([len(a) for a in labels_list])
    offsets = np.r_[0, np.cumsum(lengths)]
    all_labels = np.concatenate(labels_list)
    block_for_member = np.repeat(np.arange(len(labels_list)), lengths)
    memberships = [[] for _ in range(n)]
    for member, label in enumerate(all_labels):
        memberships[int(label)].append(member)
    degree = max(map(len, memberships))
    table = np.full((n, degree), -1, np.int32)
    for label, indices in enumerate(memberships):
        table[label, :len(indices)] = indices
    sums = np.zeros(len(all_labels), float)
    counts = np.zeros(n, np.int64)
    for first in range(0, len(y), chunk):
        reports = y[first:first+chunk]
        counts += np.bincount(reports.ravel(), minlength=n)
        member = table[reports].reshape(-1)
        valid = np.flatnonzero(member >= 0)
        member = member[valid]
        report_index = valid // (r*degree)
        key = report_index*len(labels_list)+block_for_member[member]
        order = np.argsort(key, kind='stable')
        key, member = key[order], member[order]
        if not len(key):
            continue
        starts = np.r_[0, np.flatnonzero(key[1:] != key[:-1])+1]
        sizes = np.diff(np.r_[starts, len(key)])
        ranks = np.arange(len(key))-np.repeat(starts, sizes)
        q = np.repeat(sizes-1, sizes)-2*ranks
        sums += np.bincount(member, weights=q, minlength=len(sums))
    values = np.divide((n-1)*sums, (r-1)*counts[all_labels],
                       out=np.zeros_like(sums), where=counts[all_labels] > 0)
    orders = []
    for i, labels in enumerate(labels_list):
        score = np.clip(values[offsets[i]:offsets[i+1]], -len(labels), len(labels))
        orders.append(labels[np.lexsort((priority[labels], -score))])
    zeros = int(np.count_nonzero(counts == 0))
    return orders, dict(zero_items=zeros, zero_memberships=int(np.count_nonzero(counts[all_labels] == 0)),
                       memberships=len(all_labels), max_membership=degree)


def global_borda(y, n, priority):
    orders, meta = score_nodes(y, [np.arange(n)], n, y.shape[1], priority)
    return orders[0], meta


def run_hierarchy(y, n, schedule, priority, terminal_scores):
    r = y.shape[1]
    nodes = [(np.arange(n), np.arange(n))]
    offsets = np.zeros(n, np.int64)
    used, trace = 0, []
    for stage in schedule['stages']:
        batch = y[used:used+stage['batch']]
        assert len(batch) == stage['batch']
        orders, meta = score_nodes(batch, [a for a,_ in nodes], n, r, priority)
        children = []
        for (labels, active), order in zip(nodes, orders):
            for child, core, left in padded_blocks(order, stage['width']):
                active_child = core[np.isin(core, active)]
                if len(active_child):
                    offsets[active_child] += left
                    children.append((child, active_child))
        trace.append(dict(stage, first_report=used, last_report_exclusive=used+len(batch),
                          nodes=len(nodes), children=len(children), **meta))
        used += len(batch)
        nodes = children
    if terminal_scores:
        orders, terminal_meta = score_nodes(y[used:], [a for a,_ in nodes], n, r, priority)
    else:
        orders = [labels[np.argsort(priority[labels])] for labels,_ in nodes]
        terminal_meta = dict(arbitrary_terminal_order=True)
    anchors = np.zeros(n, np.int64)
    for (labels, active), order in zip(nodes, orders):
        ranks = np.empty(n, np.int64)
        ranks[order] = np.arange(len(order))
        anchors[active] = offsets[active]+ranks[active]
    result = np.lexsort((priority, anchors))
    return result, dict(depth=len(trace), stages=trace, used=used,
                        terminal_nodes=len(nodes), terminal_max_items=max(len(a) for a,_ in nodes),
                        terminal_memberships=sum(len(a) for a,_ in nodes), terminal=terminal_meta)


def fit(y, n, family, cfg=PROOF, beta0=.8, seed=0, cache=None,
        sieve_seconds=30., sieve_memory=512 << 20):
    N, r = y.shape
    priority = np.random.default_rng(seed).permutation(n)
    if family == 'borda':
        order, meta = global_borda(y, n, priority)
        return order, dict(status='ok', branch='global_borda', depth=0, **meta)
    if family == 'exact':
        order, meta = lexicographic_dp(pair_counts(y, n), seconds=120., memory_bytes=512 << 20)
        return order, dict(status='ok', branch='exact_kemeny', depth=None, **meta)
    if family == 'majority':
        # Theorem 2.17: a tied vote is one oriented edge, not two predecessors.
        w = pair_counts(y, n)
        predecessor = np.zeros(n, int)
        for i in range(n):
            for j in range(i+1, n):
                winner = i if w[i,j] > w[j,i] else j if w[j,i] > w[i,j] else (i if priority[i] < priority[j] else j)
                predecessor[j if winner == i else i] += 1
        return np.lexsort((priority, predecessor)), dict(status='ok', branch='majority_tournament', depth=None)
    p = plan(n, r, N, beta0, cfg, family)
    base = dict(config=cfg.asdict(), beta0=beta0, schedule=p)
    if p['status'] == 'outside_lambda_domain':
        return None, dict(base, status='outside_lambda_domain', depth=None)
    if p['status'] != 'feasible':
        order, meta = global_borda(y, n, priority)
        return order, dict(base, status='ok', branch='borda_fallback', depth=0,
                           fallback_reason=p['status'], **meta)
    pilot, info = run_hierarchy(y, n, p, priority, terminal_scores=family == 'efficient')
    if family == 'efficient':
        return pilot, dict(base, status='ok', branch='hierarchy', **info)
    eta = (r-1)/(n-1)
    W = max(1, math.ceil(cfg.c_terminal*cfg.A/eta))
    anchors = np.zeros(n, np.int64)
    blocks = []
    rng = np.random.default_rng(seed+173)
    pilot_info = dict(pilot_order=pilot.tolist(), W_star=W, coefficient=cfg.c_terminal,
                      padded_cap=8*W, **info)
    total_started = time.perf_counter()
    remaining = y[info['used']:]
    by_item = np.argsort(remaining.ravel(), kind='stable')
    counts = np.bincount(remaining.ravel(), minlength=n)
    report_lists = np.split(by_item//r, np.cumsum(counts)[:-1])
    for labels, core, left in padded_blocks(pilot, W):
        # Skip reports that cannot supply a pair without scanning every report
        # for every block. Their omission consumes no random draws, so this is
        # exactly the same pair stream as extract_pairs(remaining, labels, rng).
        ids, multiplicity = np.unique(np.concatenate([report_lists[i] for i in labels]),
                                      return_counts=True)
        eligible = ids[multiplicity >= 2]
        pairs = extract_pairs(remaining[eligible], labels, rng)
        options = dict(seconds=sieve_seconds, memory_bytes=sieve_memory)
        if cache is not None:
            options['cache'] = cache
        try:
            order, meta = retry_sieve_order(pairs, labels, **options)
        except SieveResourceError as exc:
            return None, dict(base, **pilot_info, status='resource_limit', branch='exact_sieve',
                              failed_block=dict(items=len(labels), core_items=len(core), pairs=len(pairs),
                                                **exc.metadata), completed_blocks=blocks)
        ranks = np.empty(n, np.int64)
        ranks[order] = np.arange(len(order))
        anchors[core] = left+ranks[core]
        blocks.append(dict(items=len(labels), core_items=len(core), pairs=len(pairs),
                           radius=(len(labels)*(len(labels)*(len(labels)-1)//2)//len(pairs)) if len(pairs) else None,
                           sieve_size=meta.get('sieve_size', 1), path=meta.get('path'),
                           packing_cache_hit=meta.get('packing_cache_hit', False)))
        if time.perf_counter()-total_started > 120.:
            return None, dict(base, **pilot_info, status='resource_limit', branch='exact_sieve',
                              reason='total_sieve_120_seconds', completed_blocks=blocks)
    return np.lexsort((priority, anchors)), dict(base, **pilot_info, status='ok',
                branch='exact_sieve', blocks=blocks, exact=True)
