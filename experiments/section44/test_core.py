"""Distributional and algorithm-equivalence checks for S4."""
from collections import Counter
from itertools import combinations, permutations
import math
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import numpy as np

from experiments.section44.core import (Calibration, PROOF, direct_sm, fit,
    kendall_fast, make_schedule, plan, run_hierarchy, score_nodes)
from experiments.section44.design import confirmation_cells, candidate_grid
from src.manuscript_estimators import (score_order, hierarchy, sharp_center,
    efficient_center, schedule)
from src.models import kendall, pair_counts, kemeny_cost


def test_direct_subset_law():
    n,r,N=4,3,60000
    truth=np.array([2,0,3,1]); beta=.8
    y=direct_sm(np.random.default_rng(127),N,n,r,truth,beta)
    counts=Counter(map(tuple,y))
    for S in combinations(range(n),r):
        target=[x for x in truth if x in S]
        possibilities=list(permutations(S))
        w=np.array([math.exp(-beta*sum(target.index(p[i])>target.index(p[j])
                    for i in range(r) for j in range(i+1,r))) for p in possibilities])
        w=w/w.sum()/math.comb(n,r)
        for p,probability in zip(possibilities,w):
            # Fixed-seed stochastic acceptance bound, independent exact PMF.
            assert abs(counts[p]/N-probability)<6*math.sqrt(probability*(1-probability)/N)
    assert np.all(np.diff(np.sort(y,axis=1),axis=1)>0)


def test_streamed_scores_and_hierarchy_equal_literal_reference():
    rng=np.random.default_rng(23);n=128;r=8
    y=direct_sm(rng,350,n,r,rng.permutation(n),.8)
    priority=rng.permutation(n)
    labels=[np.arange(n),np.arange(8,73),np.arange(16,120),np.array([1,2,70,110])]
    got,_=score_nodes(y,labels,n,r,priority,chunk=37)
    for B,a in zip(labels,got):
        assert np.array_equal(a,score_order(y,B,n,r,priority))
    stages=[dict(width=8,cap=64,batch=60,ell=1.),dict(width=2,cap=16,batch=90,ell=1.)]
    for terminal in (True,False):
        a,info=run_hierarchy(y,n,dict(stages=stages),priority,terminal)
        b,used,leaves=hierarchy(y,n,stages,priority,terminal_scores=terminal)
        assert np.array_equal(a,b)
        assert info['used']==used and info['terminal_nodes']==leaves
        assert sorted(a)==list(range(n))


def test_proof_methods_match_existing_estimators(tmp_path):
    for N,r in ((20,2),(9,3),(4,4)):
        rng=np.random.default_rng(60+N); n=8
        y=direct_sm(rng,N,n,r,rng.permutation(n),.8)
        a,meta=fit(y,n,'sharp',PROOF,.8,91,tmp_path)
        b,info=sharp_center(y,n,91,.8)
        assert np.array_equal(a,b)
        assert meta['status']=='ok'
        if N*r*(r-1)<=n*(n-1):
            a,_=fit(y,n,'efficient',PROOF,.8,91,tmp_path)
            b,_=efficient_center(y,n,91,.8)
            assert np.array_equal(a,b)


def test_noncontracting_is_not_a_fictitious_depth():
    p=make_schedule(64,2,2016,1.,.8,Calibration(A=32,K=.001))
    assert p['status']=='noncontracting' and len(p['stages'])==0


def test_original_schedule_and_budget():
    n,r,N,eta=512,32,263,.01
    got=make_schedule(n,r,N,eta,.8,PROOF)
    assert got['stages']==schedule(n,r,N,eta,.8)
    p=plan(512,8,4672,.8,Calibration(A=4,c_width=1/16,K=.01),'efficient')
    assert p['status']=='feasible' and len(p['stages'])>0 and p['used']<=4672//2


def test_kendall_and_exact_objective():
    rng=np.random.default_rng(4)
    for n in (4,8,32):
        a,b=rng.permutation(n),rng.permutation(n)
        assert kendall_fast(a,b)==kendall(a,b)
    y=direct_sm(rng,12,4,3,rng.permutation(4),.8)
    order,meta=fit(y,4,'exact')
    w=pair_counts(y,4)
    assert meta['certified'] and kemeny_cost(w,order)==min(kemeny_cost(w,p) for p in permutations(range(4)))


def test_design_identity_and_domain():
    cells=confirmation_cells()
    assert len({c['id'] for c in cells})==len(cells)
    assert all(c['r']<=10 for c in cells if 'bounded_r_R10' in c['panels'])
    assert plan(8,8,2,.8,PROOF,'efficient')['status']=='outside_lambda_domain'
    assert candidate_grid()['proof']['config']==PROOF.asdict()
