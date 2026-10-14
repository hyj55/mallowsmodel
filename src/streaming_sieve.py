"""Exact, resumable prefix-pruned packing; no allocation proportional to n!.

The native helper sees only (n, integer radius), never observations. Observed
pairs are scored only after the complete ordered packing has been certified.
The original implementations remain byte-identical for result replay.
"""
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import threading

import numpy as np

from .models import pair_counts, validate_rankings
from .manuscript_estimators import extract_pairs, schedule
from .resource_sieve import SieveResourceError
from .sieve_budget_retry import retry_sieve_order

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / 'results/private/streaming_sieve'
SOURCE = Path(__file__).with_suffix('.cpp')
ENGINE = 'lexicographic_prefix_cover_v1'
SECONDS = 1800.
MEMORY = 4 << 30


def file_hash(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def native_binary(cache=CACHE):
    """Compile the checked-in helper locally; never download or install tools."""
    compiler = shutil.which(os.environ.get('CXX', 'c++'))
    if not compiler:
        raise RuntimeError('A C++17 compiler is needed for the exact streaming engine')
    version = subprocess.check_output([compiler, '--version'], text=True).splitlines()[0]
    flags = ['-O3', '-std=c++17', '-Wall', '-Wextra', '-Werror']
    build = dict(source_sha256=file_hash(SOURCE), compiler=compiler,
                 compiler_version=version, flags=flags)
    key = hashlib.sha256(json.dumps(build, sort_keys=True).encode()).hexdigest()[:24]
    folder = Path(cache) / 'bin'; folder.mkdir(parents=True, exist_ok=True)
    binary = folder / key
    if not binary.exists():
        temporary = binary.with_suffix(f'.{os.getpid()}.{threading.get_ident()}.tmp')
        subprocess.run([compiler, *flags, str(SOURCE), '-o', str(temporary)], check=True)
        temporary.replace(binary)
    return binary, build


def streamed_packing(n, radius, cache=CACHE, seconds=SECONDS,
                     memory_bytes=MEMORY, resume=False, joint_cover=None):
    """Return a memory-mapped *complete* packing, or raise with its checkpoint.

    resume=True adds the requested time budget to an existing verified prefix.
    Callers must serialize construction of the same (n,radius) cache entry.
    """
    if not (isinstance(n, int) and 2 <= n <= 65535 and isinstance(radius, int)
            and 0 <= radius <= n*(n-1)//2 and seconds >= 0 and memory_bytes > 0):
        raise ValueError('Invalid packing dimensions, radius, or resource budget')
    cache = Path(cache); cache.mkdir(parents=True, exist_ok=True)
    implementation = dict(native=file_hash(SOURCE), wrapper=file_hash(__file__))
    key = hashlib.sha256(json.dumps(implementation, sort_keys=True).encode()).hexdigest()[:16]
    prefix = cache / f'{ENGINE}-{key}-{n}-{radius}'
    receipt = prefix.with_suffix('.json')
    rows = prefix.with_suffix('.orders'); state = prefix.with_suffix('.state')
    previous = None
    if receipt.exists():
        previous = json.loads(receipt.read_text())
        assert previous['implementation_sha256'] == implementation
        assert rows.stat().st_size == 2*n*previous['packing_so_far']
        assert file_hash(rows) == previous['orders_sha256']
        assert file_hash(state) == previous['state_sha256']
        if previous['complete']:
            return np.memmap(rows, dtype='<u2', mode='r', shape=(previous['sieve_size'], n)), dict(
                previous, packing_cache_hit=True)
        if not resume:
            raise SieveResourceError(dict(previous, reused_resource_receipt=True))
    elif rows.exists() or state.exists():
        raise RuntimeError('Uncommitted checkpoint files exist; use a fresh cache directory')
    binary, build = native_binary(cache)
    # Union bounds are more expensive per visited leaf. Enable them for large
    # catalogues; either policy has exactly the same accepted sequence.
    joint_cover = n >= 24 if joint_cover is None else bool(joint_cover)
    result = subprocess.run([str(binary), str(n), str(radius), str(seconds),
        str(memory_bytes), str(prefix), str(int(previous is not None)), '1', str(int(joint_cover))],
        capture_output=True, text=True, check=True)
    meta = json.loads(result.stdout)
    assert rows.stat().st_size == 2*n*meta['packing_so_far']
    checkpoint=state.read_text().split()
    cursor=list(map(int,checkpoint[8:])); available=list(range(n)); resolved=0
    for i,x in enumerate(cursor):
        resolved+=available.index(x)*math.factorial(n-i-1); available.remove(x)
    meta.update(engine=ENGINE, path='streaming_prefix_cover', m=n, integer_radius=radius,
        resolved_permutations=math.factorial(n) if meta['complete'] else resolved,
        total_permutations=math.factorial(n),
        seconds_limit=seconds, memory_bytes=memory_bytes, implementation_sha256=implementation,
        build=build, orders_sha256=file_hash(rows), state_sha256=file_hash(state),
        total_elapsed_seconds=meta['elapsed_seconds']+(previous or {}).get('total_elapsed_seconds', 0),
        sessions=(previous or {}).get('sessions', [])+[dict(seconds_limit=seconds,
            memory_bytes=memory_bytes, elapsed_seconds=meta['elapsed_seconds'],
            joint_cover=joint_cover,
            retained_before=(previous or {}).get('packing_so_far', 0),
            retained_after=meta['packing_so_far'])])
    if meta['complete']:
        meta.update(sieve_size=meta['packing_so_far'], exact=True)
    temporary = receipt.with_suffix('.tmp')
    temporary.write_text(json.dumps(meta, indent=2)+'\n'); temporary.replace(receipt)
    if not meta['complete']:
        raise SieveResourceError(meta)
    return np.memmap(rows, dtype='<u2', mode='r', shape=(meta['sieve_size'], n)), meta


def streaming_sieve_order(pairs, labels, **options):
    labels = np.sort(np.asarray(labels)); n = len(labels); k = len(pairs)
    J = n*(n-1)//2; radius = n*J//k if k else J
    if n <= 1 or k == 0 or radius >= J:
        return labels, dict(path='singleton', complete=True, exact=True, sieve_size=1,
            pairs=k, objective=int(sum(a > b for a, b in pairs)))
    if radius <= 1:
        return retry_sieve_order(pairs, labels, **{k:v for k,v in options.items()
            if k not in ('resume','joint_cover')})
    orders, meta = streamed_packing(n, radius, **options)
    lookup = {int(v):i for i,v in enumerate(labels)}
    local = np.asarray([[lookup[int(a)], lookup[int(b)]] for a,b in pairs])
    w = pair_counts(local, n); i,j = np.triu_indices(n, 1)
    best_loss = math.inf; best = None
    # Bound scoring temporaries too; a completed disk-backed packing need not
    # fit as one array. Strict improvement preserves the first lexicographic tie.
    memory = options.get('memory_bytes', MEMORY)
    chunk = max(1, min(32768, memory//max(1, 8*(4*n+4*J))))
    for start in range(0, len(orders), chunk):
        block = orders[start:start+chunk]
        ranks = np.argsort(block, axis=1)
        costs = (ranks[:,i] > ranks[:,j]) @ (w[i,j]-w[j,i]) + w[j,i].sum()
        index = int(costs.argmin())
        if costs[index] < best_loss:
            best_loss = int(costs[index]); best = block[index].copy()
    return labels[best], dict(meta, objective=best_loss, pairs=k)


def streaming_sharp_center(y, n, seed, **options):
    """The same single-terminal-block Sharp branch as the 530 missing fits."""
    y = validate_rankings(y, n); N,r = y.shape
    width = math.ceil(2048*(n-1)/(r-1))
    if schedule(n,r,N,(r-1)/(n-1),.1) or width < n:
        raise ValueError('Use the full Sharp hierarchy for a multistage construction')
    pairs = extract_pairs(y, np.arange(n), np.random.default_rng(seed+173))
    base = dict(A=256, W_star=width, padded_block_cap=8*width, depth=0,
        pilot_reports=0, actual_block_items=n, global_sieve_identical=True)
    try:
        order, info = streaming_sieve_order(pairs, np.arange(n), **options)
    except SieveResourceError as exc:
        raise SieveResourceError(dict(exc.metadata, **base)) from exc
    return order, dict(base, branch='exact_sieve', blocks=[info], pairs=len(pairs),
        sieve_size=info['sieve_size'], exact=True)
