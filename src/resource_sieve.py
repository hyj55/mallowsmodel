"""Exact lexicographic pair-sieve with resource budgets, not an item-count limit.

The byte-locked manuscript_estimators module is retained for replaying its
supplementary fits. New predictive runs use this implementation instead.
"""
from functools import lru_cache
from itertools import islice, permutations
import json
import math
from pathlib import Path
import time

import numpy as np

from .models import pair_counts, kemeny_cost, validate_rankings
from .manuscript_estimators import (schedule, hierarchy, padded_blocks,
                                   extract_pairs, proof_constants, score_order)

MEMORY_BYTES = 1 << 30
PACKING_SECONDS = 120.
CACHE = Path(__file__).resolve().parents[1] / 'results/private/resource_sieve'
ENGINE = 'lexicographic_exact_v1'


class SieveResourceError(RuntimeError):
    def __init__(self, metadata):
        self.metadata = metadata
        super().__init__(metadata['reason'])


def check_budget(started, estimated_bytes, seconds, memory_bytes, **metadata):
    reason = ('working_array_memory_budget' if estimated_bytes > memory_bytes else
              'packing_wall_time_budget' if time.perf_counter()-started > seconds else None)
    if reason:
        raise SieveResourceError(dict(metadata, reason=reason,
            estimated_bytes=int(estimated_bytes), memory_bytes=memory_bytes,
            seconds_limit=seconds, elapsed_seconds=time.perf_counter()-started,
            engine=ENGINE, complete=False))


def lexicographic_dp(w, seconds=PACKING_SECONDS, memory_bytes=MEMORY_BYTES):
    """Exact Kemeny optimum, first lexicographic optimum among all permutations.

    F(A) minimizes the cost when the *first* item i is removed. Its contribution
    is the sum of W[j,i] over j in A except i. First-item ties yield lexicographic
    tie-breaking of the complete order, unlike last-item tie-breaking.
    """
    started = time.perf_counter()
    n = len(w)
    estimated = (1 << n)*(64*n+64)
    check_budget(started, estimated, seconds, memory_bytes, m=n, path='full_space_dp')
    masks = np.arange(1 << n, dtype=np.int64)
    labels = np.arange(n)
    membership = ((masks[None, :] >> labels[:, None]) & 1)
    sums = np.asarray(w, dtype=np.int64).T @ membership
    del membership
    infinity = np.iinfo(np.int64).max // 8
    f = np.full(1 << n, infinity, dtype=np.int64)
    first = np.full(1 << n, -1, dtype=np.int32)
    f[0] = 0
    sizes = np.bitwise_count(masks.astype(np.uint64))
    for size in range(1, n+1):
        selected = masks[sizes == size]
        previous = selected[:, None] ^ (1 << labels)
        valid = (selected[:, None] & (1 << labels)) != 0
        cost = f[previous] + sums[labels[None, :], previous]
        cost[~valid] = infinity
        chosen = cost.argmin(axis=1)
        f[selected] = cost[np.arange(len(selected)), chosen]
        first[selected] = chosen
        check_budget(started, estimated, seconds, memory_bytes, m=n, path='full_space_dp')
    mask = (1 << n)-1
    order = []
    while mask:
        item = int(first[mask]); order.append(item); mask ^= 1 << item
    order = np.asarray(order)
    assert kemeny_cost(w, order) == f[-1]
    return order, dict(path='full_space_dp', certified=True,
        objective=int(f[-1]), estimated_bytes=estimated,
        elapsed_seconds=time.perf_counter()-started)


def orientation_words(orders):
    """Packed inversion indicators; multiple words prevent overflow at m>=12."""
    ranks = np.argsort(orders, axis=1)
    i, j = np.triu_indices(orders.shape[1], 1)
    words = np.zeros((len(orders), (len(i)+63)//64), dtype=np.uint64)
    for bit, (a, b) in enumerate(zip(i, j)):
        words[:, bit//64] |= (ranks[:, a] > ranks[:, b]).astype(np.uint64) << np.uint64(bit % 64)
    return words


@lru_cache(maxsize=1)
def permutation_arrays(m, memory_bytes=MEMORY_BYTES, seconds=PACKING_SECONDS):
    started = time.perf_counter(); count = math.factorial(m); pairs = m*(m-1)//2
    dtype = np.uint8 if m <= 256 else np.uint32
    # Includes remaining-index, XOR/popcount/filter buffers and packing indices.
    estimated = count*(m*np.dtype(dtype).itemsize + 24*((pairs+63)//64)+24)
    check_budget(started, estimated, seconds, memory_bytes, m=m, path='greedy_packing',
                 permutations=count)
    orders = np.empty((count, m), dtype=dtype)
    words = np.empty((count, (pairs+63)//64), dtype=np.uint64)
    stream = permutations(range(m)); offset = 0
    while offset < count:
        block = np.array(list(islice(stream, 32768)), dtype=dtype)
        orders[offset:offset+len(block)] = block
        words[offset:offset+len(block)] = orientation_words(block)
        offset += len(block)
        check_budget(started, estimated, seconds, memory_bytes, m=m, path='greedy_packing',
                     permutations=count, enumerated=offset)
    return orders, words, estimated


def build_packing(m, radius, seconds=PACKING_SECONDS, memory_bytes=MEMORY_BYTES):
    started = time.perf_counter()
    orders, words, estimated = permutation_arrays(m, memory_bytes, seconds)
    remaining = np.arange(len(orders), dtype=np.int64)
    keep = []
    while len(remaining):
        first = int(remaining[0]); keep.append(first)
        distance = np.bitwise_count(words[remaining] ^ words[first]).sum(axis=1)
        remaining = remaining[distance > radius]
        check_budget(started, estimated, seconds, memory_bytes, m=m, radius=radius,
                     path='greedy_packing', packing_so_far=len(keep),
                     permutations=math.factorial(m), remaining=len(remaining))
    meta = dict(engine=ENGINE, m=m, radius=radius, path='greedy_packing',
        complete=True, sieve_size=len(keep), estimated_bytes=estimated,
        elapsed_seconds=time.perf_counter()-started, seconds_limit=seconds,
        memory_bytes=memory_bytes)
    return orders[keep], meta


def cached_packing(m, radius, cache=CACHE, seconds=PACKING_SECONDS, memory_bytes=MEMORY_BYTES):
    cache = Path(cache); cache.mkdir(parents=True, exist_ok=True)
    stem = f'{ENGINE}-{m}-{radius}-{memory_bytes}-{seconds:g}'
    receipt = cache / (stem+'.json'); output = cache / (stem+'.npz')
    if receipt.exists():
        meta = json.loads(receipt.read_text())
        if not meta['complete']:
            raise SieveResourceError(dict(meta, reused_resource_receipt=True))
        with np.load(output) as archive:
            return archive['orders'], dict(meta, packing_cache_hit=True)
    try:
        orders, meta = build_packing(m, radius, seconds, memory_bytes)
    except SieveResourceError as exc:
        receipt.write_text(json.dumps(exc.metadata, indent=2)+'\n')
        raise
    np.savez_compressed(output, orders=orders)
    receipt.write_text(json.dumps(meta, indent=2)+'\n')
    return orders, meta


def sieve_order(pairs, labels, cache=CACHE, seconds=PACKING_SECONDS, memory_bytes=MEMORY_BYTES):
    labels = np.sort(labels); m = len(labels); k = len(pairs)
    base = dict(engine=ENGINE, m=m, pairs=k, complete=True, exact=True)
    if m <= 1 or k == 0:
        return labels, dict(base, radius=None, sieve_size=1, path='empty_pair_set')
    J = m*(m-1)//2; phi = m*J/k; radius = (m*J)//k
    base.update(radius=phi, integer_radius=radius)
    if radius >= J:
        return labels, dict(base, sieve_size=1, path='singleton', objective=int(
            sum(int(a) > int(b) for a,b in pairs)))
    lookup = {int(item):i for i,item in enumerate(labels)}
    local = np.array([[lookup[int(a)], lookup[int(b)]] for a,b in pairs])
    w = pair_counts(local, m)
    if radius == 0:
        order, meta = lexicographic_dp(w, seconds, memory_bytes)
        return labels[order], dict(base, **meta, sieve_size=math.factorial(m))
    orders, meta = cached_packing(m, radius, cache, seconds, memory_bytes)
    # Score in chunks; do not allocate candidates x observations or dense m! x J.
    i,j = np.triu_indices(m, 1); best_loss = math.inf; best = None
    for start in range(0, len(orders), 32768):
        block = orders[start:start+32768]
        ranks = np.argsort(block, axis=1)
        cost = (ranks[:, i] > ranks[:, j]) @ (w[i,j]-w[j,i]) + w[j,i].sum()
        ix = int(cost.argmin())
        if cost[ix] < best_loss:
            best_loss = int(cost[ix]); best = block[ix]
    return labels[best], dict(meta, **base, packing_radius=radius, objective=best_loss)


def global_sieve_center(y, n, seed=0, **options):
    pairs = extract_pairs(y, np.arange(n), np.random.default_rng(seed+173))
    order, info = sieve_order(pairs, np.arange(n), **options)
    return order, dict(branch='global_pair_sieve', blocks=[info], pairs=len(pairs),
                       sieve_size=info['sieve_size'], exact=True)


def sharp_center(y, n, seed=0, beta0=.1, **options):
    y = validate_rankings(y, n); N,r = y.shape
    priority = np.random.default_rng(seed).permutation(n)
    stages = schedule(n, r, N, (r-1)/(n-1), beta0)
    A = proof_constants(beta0)['A']; width = math.ceil(8*A*(n-1)/(r-1))
    base = dict(A=A, W_star=width, padded_block_cap=8*width, depth=len(stages))
    if sum(s['batch'] for s in stages) > N//2:
        return score_order(y, np.arange(n), n, r, priority), dict(base,
            branch='borda_fallback', pilot_reports=0, global_sieve_identical=False)
    pilot, used, _ = hierarchy(y, n, stages, priority, terminal_scores=False)
    anchors = np.zeros(n, int); blocks = []; rng = np.random.default_rng(seed+173)
    for labels, core, left in padded_blocks(pilot, width):
        pairs = extract_pairs(y[used:], labels, rng)
        try:
            order, info = sieve_order(pairs, labels, **options)
        except SieveResourceError as exc:
            raise SieveResourceError(dict(exc.metadata, **base, pilot_reports=used,
                actual_block_items=len(labels), global_sieve_identical=(used == 0 and len(labels) == n)))
        rank = np.empty(n, int); rank[order] = np.arange(len(order)); anchors[core] = left+rank[core]
        blocks.append(info)
    return np.lexsort((priority, anchors)), dict(base, branch='exact_sieve', pilot_reports=used,
        blocks=blocks, sieve_size=sum(x['sieve_size'] for x in blocks),
        pairs=sum(x['pairs'] for x in blocks), global_sieve_identical=(used == 0 and len(blocks) == 1 and blocks[0]['m'] == n))
