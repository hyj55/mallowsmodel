"""Fixed S4 design, candidate grids and independent stream namespaces."""
from dataclasses import asdict
import math

from .core import Calibration, PROOF

ROOT_SEED = 202610230
BASE_COMMIT = 'aa31e0f9786f5eacbb49f567d08903e33c852037'
PAPER_SHA256 = '400563b1789acbeea985e4b4c551162b64c87295ee3a7bf91037c8d4cc49e676'
CALIBRATION_REPEATS = 20
CONFIRMATION_REPEATS = 100


def cell(n, r, N, panel, beta=.8, beta0=None):
    beta0 = beta if beta0 is None else beta0
    return dict(id=f'n{n}-r{r}-N{N}-b{beta:g}-lo{beta0:g}', n=n, r=r, N=N,
                beta=beta, beta0=beta0, panel=panel)


def at_lambda(n, r, lam, panel, beta=.8, beta0=None):
    N = max(1, math.floor(lam*n*(n-1)/(r*(r-1))+1e-10))
    return cell(n, r, N, panel, beta, beta0)


def calibration_cells():
    return [at_lambda(n, r, lam, 'calibration') for n,r,lam in
            [(64,16,.5), (128,8,1), (128,32,.5), (512,32,1)]]


def confirmation_cells():
    cells = []
    for n in (8,12,16):
        for r in (2,3,4):
            for lam in (.05,.2,1):
                cells.append(at_lambda(n,r,lam,'small_exact'))
    for n in (128,512):
        for r in (4,16,n//4):
            for lam in (.05,.2,1):
                cells.append(at_lambda(n,r,lam,'information_coverage'))
    for n in (512,2048):
        for r in (8,32,n//4):
            for lam in (.05,.2,1):
                cells.append(at_lambda(n,r,lam,'hierarchy'))
    for n in (32,128,512):
        for r in (3,8):
            for lam in (.05,.2,1):
                cells.append(at_lambda(n,r,lam,'bounded_r_R10'))
    # Matched coverage near the nonappearance transition, same n, different r.
    for v in (1.,3.,6.):
        for r in (2,8,16):
            N = max(1, round(v/-math.log1p(-r/128)))
            cells.append(cell(128,r,N,'matched_coverage'))
    for n in (8,32,128):
        for N in (1,2,4,8,16,32,64):
            cells.append(cell(n,n,N,'full_ranking'))
    # Supplied beta0 equals beta here; fixed-lower-bound controls isolate beta0.
    for beta, beta0 in ((.4,.4),(1.6,1.6),(.8,.4),(1.6,.4)):
        for n,r,lam in ((128,8,.2),(512,32,1)):
            cells.append(at_lambda(n,r,lam,'signal_and_bound',beta,beta0))
    unique = {}
    for c in cells:
        if c['id'] in unique:
            unique[c['id']]['panels'].append(c['panel'])
        else:
            unique[c['id']] = dict(c,panels=[c['panel']])
    return list(unique.values())


def candidate_grid():
    # Anchored one-factor sweeps isolate effects; no full Cartesian search.
    candidates = {}
    def add(name, cfg, families=('efficient','sharp'), comparison='anchor'):
        candidates[name] = dict(config=asdict(cfg), families=list(families), comparison=comparison)
    add('proof', PROOF, comparison='manuscript')
    for A in (128,64,32,16,8):
        add(f'proof_A{A}',Calibration(A=A),comparison='A_only_from_proof')
    # Empirical anchor: all four calibrations are predeclared, not outcome edits.
    anchor = dict(A=4., c_width=1/16, K=.01, c_terminal=1/512)
    add('anchor',Calibration(**anchor))
    for A in (1.,2.,8.,16.,64.,128.,256.):
        add(f'anchor_A{A:g}',Calibration(**dict(anchor,A=A)),comparison='A_with_formula_terminal')
    for c in (1/32,1/8,1/4,1/2,1.):
        add(f'anchor_width{c:g}',Calibration(**dict(anchor,c_width=c)),comparison='stage_width')
    for k in (.003,.03,.1,.3,1.,None):
        add('anchor_K'+str(k),Calibration(**dict(anchor,K=k)),comparison='batch_coefficient')
    for c in (8.,1.,1/8,1/64,1/4096):
        add(f'anchor_terminal{c:g}',Calibration(**dict(anchor,c_terminal=c)),('sharp',),'terminal_coefficient')
    for c in (8.,1/8,1/64,1/512,1/4096):
        add(f'wide_anchor_terminal{c:g}',Calibration(A=16,c_width=1/8,K=.03,c_terminal=c),
            ('sharp',),'A_terminal_interaction')
    return candidates


def protocol():
    return dict(experiment='S4', title='Section 4.4: risk, hierarchy and calibration',
        base_commit=BASE_COMMIT, manuscript_sha256=PAPER_SHA256,
        root_seed=ROOT_SEED, calibration_repeats=CALIBRATION_REPEATS,
        confirmation_repeats=CONFIRMATION_REPEATS,
        calibration_cells=calibration_cells(), confirmation_cells=confirmation_cells(),
        candidates=candidate_grid(), subset_generator='Floyd uniform subset + truncated-geometric insertions',
        generation_chunk=2048, stream_key=['root_seed','phase(0 calibration / 1 confirmation)','cell_index','repeat'],
        child_streams=['true_center','reports','estimator_seed'],
        selection='Equal-cell mean normalized Kendall risk among candidates complete on every calibration draw, '
                  'with positive depth on at least half of draws; Sharp additionally requires exact-sieve branch '
                  'on every draw. Ties break by candidate ID. One fixed winner per family.',
        beta_policy='beta0 equals beta except explicit fixed-beta0=.4 controls; no adaptation to unknown beta',
        inference='100 independent draws per confirmation cell; paired differences; pointwise t intervals and '
                  '2000 paired-bootstrap intervals; no full-risk estimate if any planned fit is unavailable',
        sieve_budget=dict(seconds_per_packing=30, working_bytes=512<<20, total_terminal_seconds=120),
        geometry=dict(core_multiple=2, padding_each_side_multiple=3, block_cap_multiple=8),
        terminal_rule='W_star=ceil(c_terminal*A*(n-1)/(r-1)); only coefficient and A change',
        outside_domain='Efficient/Sharp are not evaluated at lambda>1; full rankings use Borda, '
                       'the exact Theorem 2.17 tournament rule and small-n exact Kemeny',
        failure_policy='No reroll, no approximate sieve, no dropping incomplete draws from unconditional risk',
        resources='Fit wall time includes warm shared packing cache; separate fresh-process working-allocation '
                  'profiling on confirmation repetition zero; generator/input memory reported separately')
