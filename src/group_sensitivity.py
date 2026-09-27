"""Recovered original groups, outcome-blind splits, and admitted original estimators."""
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
import ast
import hashlib
import json
from pathlib import Path
import tarfile
import urllib.request

import numpy as np
import rdata

from .models import pair_counts, validate_rankings, kemeny_cost
from .strict_models import StrictFit, TIE_SEED, fit_pl_mm, fit_sm_strict, profile_beta_unbounded

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw/group_sensitivity'
SEED = 202609270
METHODS = ('sm_mle', 'sm_fotakis', 'sm_sharp', 'sm_efficient', 'pl')
SCHEMES = ('pooled', 'local', 'matched_pool')
SPLIT_PLAN = ((70, 100), (50, 20), (80, 20))


@dataclass
class GroupTask:
    name: str
    index: int
    n: int
    y: np.ndarray
    groups: np.ndarray
    group_names: tuple
    unit: str
    source: dict


def verified_file(entry, directory):
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / entry['file']
    if not path.exists():
        payload = urllib.request.urlopen(entry['url'], timeout=60).read()
        if hashlib.sha256(payload).hexdigest() != entry['sha256']:
            raise ValueError('Source checksum mismatch: ' + entry['file'])
        path.write_bytes(payload)
    payload = path.read_bytes()
    if hashlib.sha256(payload).hexdigest() != entry['sha256'] or len(payload) != entry['bytes']:
        raise ValueError('Source checksum mismatch: ' + entry['file'])
    return path


def soc_counts(text):
    counts = Counter()
    for line in text.splitlines():
        if not line or line.startswith('#'):
            continue
        count, order = line.split(':')
        counts[tuple(int(v.strip()) - 1 for v in order.split(','))] += int(count)
    return counts


def parse_original_trials(archive, folder):
    """Read tar members without extracting paths or executing source content."""
    rows, groups, names, alphabet = [], [], [], None
    with tarfile.open(archive) as tar:
        members = sorted((m for m in tar.getmembers()
                          if m.isfile() and m.name.startswith(folder + '/')),
                         key=lambda m: m.name)
        if len(members) != 40 or len({m.name for m in members}) != 40:
            raise ValueError('Expected 40 uniquely named trials: ' + folder)
        for g, member in enumerate(members):
            if len(Path(member.name).parts) != 2 or not member.name.endswith('.txt'):
                raise ValueError('Unexpected trial member: ' + member.name)
            names.append(member.name)
            lines = tar.extractfile(member).read().decode('utf-8').splitlines()
            for line in lines:
                if not line.strip():
                    continue
                values = ast.literal_eval(line)
                if (not isinstance(values, list) or len(values) != 4
                        or any(type(v) is not int for v in values) or len(set(values)) != 4):
                    raise ValueError('Not an original strict four-item ranking')
                current = tuple(sorted(values))
                if alphabet is None:
                    alphabet = current
                if current != alphabet:
                    raise ValueError('Difficulty conditions must not be mixed')
                rows.append([alphabet.index(v) for v in values])
                groups.append(g)
    y = validate_rankings(np.array(rows, dtype=int), 4)
    return y, np.array(groups, dtype=int), tuple(names), alphabet


def load_group_tasks():
    manifest = json.loads((ROOT / 'data/group_sensitivity_sources.json').read_text())
    archive = verified_file(manifest['archive'], RAW)
    pinned = {e['file']: e for e in json.loads((ROOT / 'data/strict_feature_sources.json').read_text())}
    tasks = []
    for index, (folder, dataset) in enumerate(manifest['trials'].items()):
        path = verified_file(pinned[dataset + '.soc'], ROOT / 'data/raw/strict_features')
        y, groups, names, values = parse_original_trials(archive, folder)
        if Counter(map(tuple, y)) != soc_counts(path.read_text()):
            raise ValueError('Recovered trials do not match current PrefLib source: ' + dataset)
        tasks.append(GroupTask(folder.lower(), index, 4, y, groups, names, 'original_trial',
                     dict(preflib=dataset, values=values, reports=len(y), groups=len(names),
                          frequency_match=True, archive_sha256=manifest['archive']['sha256'],
                          assessor_ids_available=False, board_layouts_available=False)))
    entry = next(e for e in json.loads((ROOT / 'data/validation_extension_sources.json').read_text())
                 if e['file'] == 'sounds.rda')
    table = rdata.read_rda(verified_file(entry, RAW))['sounds']
    a = table[['top_item', 'bottom_item']].to_numpy(dtype=float)
    if not np.isfinite(a).all() or not np.equal(a, np.floor(a)).all() or table.assessor.isna().any():
        raise ValueError('Invalid Sounds source')
    y = validate_rankings(a.astype(int) - 1, 12)
    ids, groups = np.unique(table.assessor.to_numpy(), return_inverse=True)
    if len(ids) != 46 or not np.all(np.bincount(groups) == 30):
        raise ValueError('Unexpected Sounds assessor structure')
    # Reversible source mapping stays in ignored input; public summaries use stable ordinal codes.
    tasks.append(GroupTask('sounds', 8, 12, y, groups,
                 tuple(f'assessor_{i:03d}' for i in range(len(ids))), 'source_assessor',
                 dict(reports=len(y), groups=len(ids), reports_per_group=30,
                      sha256=entry['sha256'], assessor_ids_available=True)))
    return tasks


def rng_for(task_index, percent, repeat, stream, group=0):
    return np.random.default_rng(np.random.SeedSequence([SEED, task_index, percent, repeat, stream, group]))


def within_split(groups, task_index, percent, repeat):
    train, test = [], []
    for g in np.unique(groups):
        ids = np.flatnonzero(groups == g)
        shuffled = rng_for(task_index, percent, repeat, 1, int(g)).permutation(ids)
        cut = len(ids) * percent // 100
        if not 0 < cut < len(ids):
            raise ValueError('Both train and test must contain reports for every group')
        train.extend(shuffled[:cut]); test.extend(shuffled[cut:])
    return np.sort(train), np.sort(test)


def holdout_split(groups, task_index, repeat):
    units = rng_for(task_index, 70, repeat, 2).permutation(np.unique(groups))
    cut = len(units) * 70 // 100
    train = np.flatnonzero(np.isin(groups, units[:cut]))
    test = np.flatnonzero(np.isin(groups, units[cut:]))
    return train, test


def matched_training(train, count, task_index, percent, repeat, group):
    return np.sort(rng_for(task_index, percent, repeat, 3, int(group)).choice(train, count, replace=False))


@lru_cache(maxsize=8)
def dp_layout(n, seed):
    masks = np.arange(1 << n, dtype=np.int64)
    membership = ((masks[None, :] >> np.arange(n)[:, None]) & 1)
    labels = np.random.default_rng(seed).permutation(n)
    layers = []
    for size in range(1, n + 1):
        selected = masks[np.bitwise_count(masks.astype(np.uint64)) == size]
        valid = (selected[:, None] & (1 << labels)) != 0
        previous = selected[:, None] ^ (1 << labels)
        layers.append((selected, previous, valid))
    return membership, labels, layers


def exact_dp_batched(w, seed=TIE_SEED):
    """Same subset recurrence and tie order as models.exact_dp, batched by cardinality."""
    n = len(w)
    if n > 18:
        raise ValueError('Exact subset DP computational guard is n<=18')
    membership, labels, layers = dp_layout(n, seed)
    subset_sums = np.asarray(w, dtype=np.int64) @ membership
    infinity = np.iinfo(np.int64).max // 4
    f = np.full(1 << n, infinity, dtype=np.int64)
    last = np.full(1 << n, -1, dtype=np.int16)
    f[0] = 0
    for masks, previous, valid in layers:
        cost = f[previous] + subset_sums[labels[None, :], previous]
        cost[~valid] = infinity
        chosen = np.argmin(cost, axis=1)
        f[masks] = cost[np.arange(len(masks)), chosen]
        last[masks] = labels[chosen]
    order, mask = [], (1 << n) - 1
    while mask:
        item = int(last[mask]); order.append(item); mask ^= 1 << item
    order = np.asarray(order[::-1])
    if kemeny_cost(w, order) != f[-1]:
        raise ArithmeticError('DP certificate failed')
    return order


def fotakis_center(w, seed=TIE_SEED + 2021):
    counts = w + w.T
    i, j = np.triu_indices(len(w), 1)
    if np.any(counts[i, j] == 0):
        raise ValueError('Fotakis p-frequent admission requires every pair to appear')
    precedes = 2 * w.T >= counts
    np.fill_diagonal(precedes, False)
    scores = precedes.sum(axis=1)
    priority = np.random.default_rng(seed).permutation(len(w))
    return np.lexsort((priority, scores))


@lru_cache(maxsize=65536)
def cached_beta(total, count, r):
    return profile_beta_unbounded(total, count, r)


def coverage(y, n):
    w = pair_counts(y, n)
    joint = w + w.T
    pair = joint[np.triu_indices(n, 1)]
    counts = np.bincount(y.ravel(), minlength=n)
    N, r = y.shape
    return w, dict(n=n, r=r, N=N, unseen=int((counts == 0).sum()),
        item_min=int(counts.min()), pair_min=int(pair.min()), observed_pairs=int((pair > 0).sum()),
        p=float(pair.min() / N), lambda_=N*r*(r-1)/(n*(n-1)),
        mu=N*r/n, coverage_ratio=N*r/n/np.log(np.e*r))


def fit_candidates(y, n):
    y = validate_rankings(y, n)
    w, audit = coverage(y, n)
    result = {}
    for method in METHODS:
        status = None
        if method.startswith('sm_') and audit['unseen']:
            status = 'unseen_catalog_items'
        elif method == 'sm_fotakis' and audit['pair_min'] == 0:
            status = 'not_p_frequent'
        elif method in ('sm_sharp', 'sm_efficient') and audit['lambda_'] > 1:
            status = 'excluded_outside_theorem_regime'
        elif method == 'sm_sharp' and n > 8:
            status = 'exact_sieve_unavailable'
        elif method == 'sm_efficient' and n <= 8:
            status = 'sharp_available_no_fallback_needed'
        if status:
            result[method] = StrictFit(method, None, status=status, metadata=dict(audit))
            continue
        if method in ('sm_mle', 'sm_fotakis'):
            order = exact_dp_batched(w) if method == 'sm_mle' else fotakis_center(w)
            total = kemeny_cost(w, order)
            beta = cached_beta(total, len(y), y.shape[1])
            result[method] = StrictFit(method, order, beta=beta, metadata=dict(audit,
                algorithm='exact_subset_dp_batched' if method == 'sm_mle' else 'Fotakis_2021_Algorithm_1',
                certified=method == 'sm_mle', training_distance=total,
                beta_boundary='infinite' if np.isinf(beta) else ('zero' if beta == 0 else 'interior')))
        elif method == 'pl':
            result[method] = fit_pl_mm(y, n)
            result[method].metadata.update(audit)
        else:
            result[method] = fit_sm_strict(y, n, method.removeprefix('sm_'), beta0=.1, pair_seed=202609270)
            result[method].metadata.update(audit)
    return result


def group_score(loss, fit, n_test):
    finite = np.isfinite(loss)
    positive_inf = np.isposinf(loss)
    if np.any(np.isneginf(loss)) or np.any(loss[finite] < -1e-10):
        raise ArithmeticError('Invalid NLL')
    return dict(status=fit.status, n_test=n_test,
                n_available=n_test if fit.status == 'ok' else 0,
                n_finite=int(finite.sum()), n_infinite=int(positive_inf.sum()),
                finite_sum=float(loss[finite].sum()),
                all_sum=float(loss.sum()) if fit.status == 'ok' else np.nan)


def paired_contrast(sm_a, pl_a, sm_b, pl_b):
    """Identical report mask for both families and both fitting schemes."""
    mask = np.isfinite(np.stack([sm_a, pl_a, sm_b, pl_b])).all(axis=0)
    if not mask.any():
        return dict(n_common=0, sm_change_sum=0., pl_change_sum=0., interaction_sum=0.)
    sm = sm_a[mask] - sm_b[mask]
    pl = pl_a[mask] - pl_b[mask]
    return dict(n_common=int(mask.sum()), sm_change_sum=float(sm.sum()),
                pl_change_sum=float(pl.sum()), interaction_sum=float((sm-pl).sum()))
