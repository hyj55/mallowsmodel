from itertools import permutations
import math
import numpy as np
import pytest
from scipy.optimize._numdiff import approx_derivative

from src.models import pair_counts, kemeny_cost, kendall, logz_mean
from src.resource_sieve import (lexicographic_dp, sieve_order, build_packing,
    orientation_words, sharp_center, global_sieve_center, SieveResourceError)
from src.manuscript_estimators import sieve_order as frozen_sieve_order
from src.predictive_models import bounded_beta, ridge_pl, pl_objective, insertion_search
from src.predictive_study import paired_bootstrap,curve_parts,primary_parts
from src.repeated_holdout import Task


def test_lexicographic_dp_matches_exhaustive_optimum_and_ties():
    rng = np.random.default_rng(71)
    for n in (3,4,5,6):
        for w in (np.zeros((n,n), int), rng.integers(0,4,size=(n,n))):
            np.fill_diagonal(w,0)
            expected = min(permutations(range(n)), key=lambda p:(kemeny_cost(w,p),p))
            order,meta = lexicographic_dp(w)
            assert tuple(order) == expected and meta['certified']


def test_exact_sieve_reproduces_frozen_small_block_results(tmp_path):
    rng = np.random.default_rng(27)
    for n in (3,4,5):
        for k in (n,2*n,5*n,100):
            pairs = np.array([rng.choice(n,2,replace=False) for _ in range(k)])
            old,old_meta = frozen_sieve_order(pairs,np.arange(n))
            new,new_meta = sieve_order(pairs,np.arange(n),cache=tmp_path)
            np.testing.assert_array_equal(new,old)
            assert new_meta['sieve_size'] == old_meta['sieve_size']


def test_greedy_packing_is_separated_covers_space_and_obeys_lex_order():
    n,radius=4,2
    orders,_ = build_packing(n,radius)
    all_orders = list(permutations(range(n)))
    expected=[]
    for order in all_orders:
        if all(kendall(order,p)>radius for p in expected):
            expected.append(order)
    assert [tuple(p) for p in orders] == expected
    assert all(any(kendall(order,p)<=radius for p in orders) for order in all_orders)


def test_more_than_eight_items_and_more_than_64_pair_bits(tmp_path):
    for n in (9,10,12):
        truth=np.arange(n)[::-1]
        # All reversed directed pairs repeated enough to give radius < 1.
        pairs=np.array([(i,j) for i in truth for j in truth if i>j]* (n+1))
        order,meta=sieve_order(pairs,np.arange(n),cache=tmp_path)
        np.testing.assert_array_equal(order,truth)
        assert meta['path']=='full_space_dp' and meta['sieve_size']==math.factorial(n)
    words=orientation_words(np.array([np.arange(13),np.arange(13)[::-1]]))
    assert words.shape==(2,2)
    assert int(np.bitwise_count(words[0]^words[1]).sum())==78


def test_large_singleton_shortcut_and_resource_failure_are_distinct(tmp_path):
    order,meta=sieve_order(np.array([[99,0]]),np.arange(100),cache=tmp_path)
    np.testing.assert_array_equal(order,np.arange(100))
    assert meta['path']=='singleton'
    with pytest.raises(SieveResourceError) as exc:
        build_packing(12,20,memory_bytes=1024)
    assert exc.value.metadata['reason']=='working_array_memory_budget'


def test_sharp_global_identity_uses_same_retained_pairs(tmp_path):
    rng=np.random.default_rng(77)
    y=np.array([rng.permutation(10) for _ in range(700)])
    sharp,meta=sharp_center(y,10,seed=87,cache=tmp_path)
    global_order,_=global_sieve_center(y,10,seed=87,cache=tmp_path)
    np.testing.assert_array_equal(sharp,global_order)
    assert meta['global_sieve_identical'] and meta['W_star']==2048


def test_finite_boundaries_and_ridge_on_disconnected_data():
    assert bounded_beta(0,10,3)==10
    assert bounded_beta(15,10,3)==0
    y=np.array([[0,1],[0,1],[2,3]])
    fit=ridge_pl(y,5,.1)
    assert np.isfinite(fit.nll(np.array([[1,0],[4,3],[3,2]]))).all()
    assert abs(fit.theta.sum())<1e-10
    assert fit.metadata['gradient_per_report']<1e-7
    x=np.array([.3,-.2,.4,.5,-1.])
    numeric=approx_derivative(lambda t:pl_objective(t,y,.7)[0],x).ravel()
    np.testing.assert_allclose(numeric,pl_objective(x,y,.7)[1],atol=1e-7)


def test_insertion_returns_no_single_move_improvement():
    rng=np.random.default_rng(812); w=rng.integers(0,8,size=(12,12)); np.fill_diagonal(w,0)
    order=list(insertion_search(w,rng.permutation(12))); cost=kemeny_cost(w,order)
    for i,item in enumerate(order):
        rest=order[:i]+order[i+1:]
        for j in range(12):
            assert kemeny_cost(w,rest[:j]+[item]+rest[j:])>=cost


def test_cluster_bootstrap_preserves_pairing_and_report_weighting():
    units=np.array([0,0,1])
    losses={'pl':np.array([1.,3.,7.]),'shifted':np.array([3.,5.,9.])}
    result=paired_bootstrap(losses,units,42,resamples=2000)
    assert result['shifted']['delta_ci_low']==result['shifted']['delta_ci_high']==2
    assert result['pl']['nll_ci_low']==2 and result['pl']['nll_ci_high']==7
    # Each resampled person contributes both reports or neither; individual
    # resampling would have allowed NLL 1 below the person-level lower endpoint.


def test_sushi_nested_budgets_align_respondents_and_exclude_outer_test():
    y=np.tile([0,1],(5000,1))
    a=Task('sushi_a','baseline',y,10,np.arange(5000),1,92,'respondent')
    b=Task('sushi_b','baseline',y,100,np.arange(5000),1,92,'respondent')
    for repeat in (0,4):
        small=curve_parts(a,repeat,20);large=curve_parts(a,repeat,100)
        other=curve_parts(b,repeat,100);outer=primary_parts(a,repeat)
        np.testing.assert_array_equal(small['development'],large['development'][:20])
        np.testing.assert_array_equal(large['development'],other['development'])
        assert not np.intersect1d(large['development'],outer['test']).size
        assert len(large['inner'])==75 and len(large['validation'])==25
