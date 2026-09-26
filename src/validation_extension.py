"""Declared validation laws and lossless source decoding; no new estimators."""
import hashlib
import json
from pathlib import Path
import urllib.request

import numpy as np
import rdata
from scipy.special import expit
from scipy.stats import norm

from .models import pl_nll, validate_rankings
from .strict_features import report_space

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT/'data/raw/validation_extension'
SEED = 202609260


def download_sources():
    sources = json.loads((ROOT/'data/validation_extension_sources.json').read_text())
    RAW.mkdir(parents=True, exist_ok=True)
    for entry in sources:
        path = RAW/entry['file']
        if not path.exists():
            payload = urllib.request.urlopen(entry['url'], timeout=60).read()
            if hashlib.sha256(payload).hexdigest() != entry['sha256']:
                raise ValueError('Source changed: '+entry['file'])
            path.write_bytes(payload)
        payload = path.read_bytes()
        if len(payload) != entry['bytes'] or hashlib.sha256(payload).hexdigest() != entry['sha256']:
            raise ValueError('Source checksum mismatch: '+entry['file'])
    return sources


def real_tasks():
    download_sources()
    tasks = []
    for name, n in [('beach_preferences', 15), ('sounds', 12)]:
        table = rdata.read_rda(RAW/(name+'.rda'))[name]
        a = table[['top_item', 'bottom_item']].to_numpy(dtype=float)
        assert np.isfinite(a).all() and np.equal(a, np.floor(a)).all()
        y = validate_rankings(a.astype(int)-1, n)
        groups = table.assessor.to_numpy()
        assert len(groups) == len(y) and not np.any(np.asarray(table.assessor.isna()))
        tasks.append(dict(name=name, n=n, r=2, y=y, groups=groups,
                          truth=None, unit='source_assessor_id',
                          source_index=0 if name == 'beach_preferences' else 1,
                          eligible=name != 'beach_preferences'))
    for k, name, n in [(1, 'patras_cost', 36), (2, 'patras_population', 48)]:
        text = (RAW/f'00034-0000000{k}.soi').read_text()
        records = []
        for line in text.splitlines():
            if not line or line.startswith('#'):
                continue
            multiplicity, order = line.split(':')
            report = [int(x.strip())-1 for x in order.split(',')]
            assert len(report) == 6
            records.extend([report]*int(multiplicity))
        y = validate_rankings(records, n)
        assert len(y) == 392 and f'# NUMBER ALTERNATIVES: {n}' in text
        tasks.append(dict(name=name, n=n, r=6, y=y, groups=np.arange(len(y)),
                          truth=np.arange(n), unit='documented_one_report_per_volunteer',
                          source_index=k+1, eligible=True))
    return tasks


def split_units(task, index):
    units = np.unique(task['groups'])
    rng = np.random.default_rng(np.random.SeedSequence([SEED, 1, index]))
    shuffled = rng.permutation(units)
    a, b = int(.6*len(units)), int(.8*len(units))
    return {name: np.flatnonzero(np.isin(task['groups'], chosen))
            for name, chosen in [('fit', shuffled[:a]), ('discovery', shuffled[a:b]),
                                 ('confirmation', shuffled[b:])]}


def unit_interval(values, groups, seed, resamples=2000, denominator=None):
    """Paired whole-assessor ratio bootstrap, retaining zero-contribution units.

    Point target is mean per original report, not a new reweighted training fit.
    denominator optionally defines an outcome-independent diagnostic bin.
    """
    values, groups = np.asarray(values, float), np.asarray(groups)
    if not np.isfinite(values).all():
        return dict(lo=np.nan, hi=np.nan, valid_bootstraps=0)
    denominator = np.ones(len(values)) if denominator is None else np.asarray(denominator, float)
    _, group = np.unique(groups, return_inverse=True)
    numerator = np.bincount(group, weights=values)
    count = np.bincount(group, weights=denominator)
    rng = np.random.default_rng(seed)
    sampled = rng.integers(len(numerator), size=(resamples, len(numerator)))
    total = count[sampled].sum(axis=1)
    numer = numerator[sampled].sum(axis=1)
    draws = numer[total > 0]/total[total > 0]
    lo, hi = np.quantile(draws, [.025, .975]) if len(draws) else (np.nan, np.nan)
    return dict(lo=float(lo), hi=float(hi), valid_bootstraps=len(draws))


def confounded_law(rho, truth=None):
    """Finite-state two-group PL law, including displayed set and group labels."""
    truth = np.arange(4) if truth is None else np.asarray(truth)
    sets, _, reports, _ = report_space(4, 3)
    chosen = np.array_equal(sets[0], [0, 1, 2])
    assert chosen
    rows, weights, groups, contexts = [], [], [], []
    for context, shown in enumerate([[0, 1, 2], [0, 2, 3]]):
        rows_here = reports[np.all(np.sort(reports, axis=1) == shown, axis=1)]
        high_share = (1+rho)/2 if context == 0 else (1-rho)/2
        for g, scale in enumerate([.2, .8]):
            probability = np.exp(-pl_nll(rows_here, -scale*np.arange(4)))
            group_share = high_share if g else 1-high_share
            rows.extend(truth[rows_here])
            weights.extend(.5*group_share*probability)
            groups.extend([g]*len(rows_here))
            contexts.extend([context]*len(rows_here))
    rows, weights, groups, contexts = map(np.asarray, [rows, weights, groups, contexts])
    assert np.isclose(weights.sum(), 1)
    return rows, weights, groups, contexts


def confounded_focal_contrast(rho):
    return float(rho*(expit(1.6)-expit(.4)))


def wilson(successes, total):
    if total == 0:
        return np.nan, np.nan
    z = norm.ppf(.975)
    rate = successes/total
    center = (rate+z*z/(2*total))/(1+z*z/total)
    half = z*np.sqrt(rate*(1-rate)/total+z*z/(4*total*total))/(1+z*z/total)
    return float(center-half), float(center+half)
