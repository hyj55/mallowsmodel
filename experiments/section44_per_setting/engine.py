"""Exact reuse of S4 fits, train-only dispersion, and separate report streams."""
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

from experiments.section44.core import Calibration, direct_sm, fit, plan, kendall_fast
from src.models import logz_mean
from .design import ROOT_SEED, holdout_size


def stable_hash(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def report_distances(y, order):
    """Exact inversion counts; vectorize across reports and one suffix at a time."""
    z = np.argsort(order)[y]
    out = np.zeros(len(y), np.int64)
    for j in range(y.shape[1] - 1):
        out += (z[:, j, None] > z[:, j+1:]).sum(axis=1)
    return out


def normalizer(r, beta):
    if beta < 1e-5:
        return logz_mean(r, beta)
    j = np.arange(2, r+1, dtype=float)
    logz = float(np.sum(np.log(-np.expm1(-j*beta))) - (r-1)*np.log(-np.expm1(-beta)))
    with np.errstate(over='ignore'):
        mean = float((r-1)/np.expm1(beta) - np.sum(j/np.expm1(j*beta)))
    return logz, mean


def fit_beta(total, N, r):
    target = total/N
    if target >= r*(r-1)/4:
        return 0.
    if target <= normalizer(r, 10.)[1]:
        return 10.
    return float(brentq(lambda b: normalizer(r, b)[1] - target, 0., 10., xtol=1e-12))


def score(y_train, y_holdout, order):
    train_distance = int(report_distances(y_train, order).sum())
    holdout_distance = int(report_distances(y_holdout, order).sum())
    N, r = y_train.shape
    beta = fit_beta(train_distance, N, r)
    logz = normalizer(r, beta)[0]
    return dict(beta=beta, train_distance_sum=train_distance,
                holdout_distance_sum=holdout_distance,
                train_nll=beta*train_distance/N+logz,
                holdout_nll=beta*holdout_distance/len(y_holdout)+logz)


def generate(c, phase, index, repeat):
    # Independent roles; confirmation never draws from calibration streams.
    streams = np.random.SeedSequence([ROOT_SEED, phase, index, repeat]).spawn(4)
    truth = np.random.default_rng(streams[0]).permutation(c['n'])
    train = direct_sm(np.random.default_rng(streams[1]), c['N'], c['n'], c['r'], truth, c['beta'])
    holdout = direct_sm(np.random.default_rng(streams[2]), holdout_size(c['N']), c['n'], c['r'], truth, c['beta'])
    seed = int(streams[3].generate_state(1)[0])
    return truth, train, holdout, seed


def computational_plan(c, family, config):
    if family == 'borda':
        return dict(status='feasible', stages=[], used=0), 'borda', dict(branch='global_borda', depth=0)
    cfg = Calibration(**config)
    p = plan(c['n'], c['r'], c['N'], c['beta0'], cfg, family)
    if p['status'] == 'outside_lambda_domain':
        return p, 'outside', dict(branch='outside_lambda_domain', depth=None)
    if p['status'] != 'feasible':
        return p, 'borda', dict(branch='borda_fallback', depth=0, fallback_reason=p['status'])
    if family == 'efficient' and not p['stages']:
        return p, 'borda', dict(branch='hierarchy', depth=0)
    stages = [(s['width'], s['batch']) for s in p['stages']]
    W = max(1, math.ceil(cfg.c_terminal*cfg.A*(c['n']-1)/(c['r']-1))) if family == 'sharp' else None
    # Equal (width,batch) stages and equal actual terminal geometry induce the
    # same operations, fresh report allocations and random-pair stream.
    canonical_W = c['n'] if W is not None and 2*W >= c['n'] else W
    key = stable_hash([family, stages, canonical_W])[:24]
    return p, key, dict(branch='exact_sieve' if family == 'sharp' else 'hierarchy',
                        depth=len(stages), W_star=W, pilot_reports=p['used'])


def perform_fit(c, family, config, train, seed, cache):
    return fit(train, c['n'], family, Calibration(**config), c['beta0'], seed,
               Path(cache), sieve_seconds=30., sieve_memory=512 << 20)


def clean(x):
    if isinstance(x, dict):
        return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x, (list, tuple)):
        return [clean(v) for v in x]
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, np.generic):
        return x.item()
    return x
