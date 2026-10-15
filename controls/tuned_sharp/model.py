"""Borda-pilot block-sieve variant; not manuscript Algorithm 2.1."""
import math
import time
from pathlib import Path

import numpy as np

from src.manuscript_estimators import score_order, extract_pairs
from src.predictive_models import sm_fit
from src.resource_sieve import SieveResourceError
from src.sieve_budget_retry import retry_sieve_order

ROOT = Path(__file__).resolve().parents[2]
SEED = 202610150
SECONDS = 120.
MEMORY = 4 << 30
CACHE = ROOT / 'results/private/tuned_block_sieve/packing'


def block_grid(n):
    """Pre-data grid, including finer partitions for large catalogues."""
    return sorted({2, 3, 4, math.ceil(n / 10), math.ceil(n / 8)} - {0, 1})


def pilot_partition(units, seed):
    units = np.asarray(units)
    unique = np.unique(units)
    if len(unique) < 2:
        raise ValueError('At least two allocation units are required')
    order = np.random.default_rng(seed).permutation(unique)
    first = np.isin(units, order[:len(unique)//2])
    return np.flatnonzero(first), np.flatnonzero(~first)


def pilot_order(y, n, units, seed):
    pilot, terminal = pilot_partition(units, seed)
    priority = np.random.default_rng(SEED).permutation(n)
    order = score_order(y[pilot], np.arange(n), n, y.shape[1], priority)
    return order, pilot, terminal


def block_center(y, n, units, blocks, seed, *, cache=CACHE,
                 seconds=SECONDS, memory_bytes=MEMORY):
    """Independent pilot/sieve pools, unpadded contiguous equal-size blocks.

    Canonical source labels define sieve enumeration, as in the exact engine.
    Every eligible terminal report supplies one orientation-blind sampled pair
    per block. Cross-block center order remains fixed by the Borda pilot.
    """
    started = time.perf_counter()
    if not 2 <= blocks <= n:
        raise ValueError('Invalid number of blocks')
    pilot, pilot_ids, terminal_ids = pilot_order(y, n, units, seed)
    chunks = np.array_split(pilot, blocks)
    output, details = [], []
    for index, labels in enumerate(chunks):
        rng = np.random.default_rng(np.random.SeedSequence([seed, blocks, index, 173]))
        pairs = extract_pairs(y[terminal_ids], labels, rng)
        m, k = len(labels), len(pairs)
        detail = dict(index=index, labels=labels.tolist(), m=m, pairs=k,
                      integer_radius=m*(m*(m-1)//2)//k if k else None)
        try:
            order, meta = retry_sieve_order(pairs, labels, cache=cache,
                                            seconds=seconds, memory_bytes=memory_bytes)
        except SieveResourceError as exc:
            raise SieveResourceError(dict(exc.metadata, failed_block=detail,
                completed_blocks=details, requested_blocks=blocks,
                pilot_reports=len(pilot_ids), terminal_reports=len(terminal_ids))) from exc
        details.append(dict(detail, order=order.tolist(), solver=meta))
        output.extend(map(int, order))
    assert sorted(output) == list(range(n))
    return np.asarray(output), dict(variant='borda_block_sieve', requested_blocks=blocks,
        padding=0, pilot_order=pilot.tolist(), pilot_reports=len(pilot_ids),
        terminal_reports=len(terminal_ids), blocks=details, seed=seed,
        exact_within_blocks=True, seconds=time.perf_counter()-started)


def fit_block(y, n, units, blocks, seed, **options):
    try:
        order, metadata = block_center(y, n, units, blocks, seed, **options)
        return sm_fit('borda_block_sieve', y, order, metadata)
    except SieveResourceError as exc:
        return sm_fit('borda_block_sieve', y, None,
                      dict(exc.metadata, status='sieve_resource_budget'))


def validation_order(candidates):
    """No test argument: lower validation NLL, then fewer blocks."""
    eligible = [c for c in candidates if c['status'] == 'ok'
                and np.isfinite(c['validation_nll'])]
    return sorted(eligible, key=lambda c: (c['validation_nll'], c['blocks']))
