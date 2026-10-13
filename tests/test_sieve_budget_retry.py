from itertools import permutations
import numpy as np
import pytest
from src.models import kemeny_cost
from src.resource_sieve import build_packing,SieveResourceError,sieve_order
from src.sieve_budget_retry import (build_ball_packing,even_permutation_dp,
    lex_ranks,lex_unrank,ball_size,inversion_ball,cached_ball_packing,retry_sieve_order)


def test_ball_cover_reproduces_literal_greedy_packing():
    for n in range(3,7):
        orders=np.asarray(list(permutations(range(n))))
        np.testing.assert_array_equal(lex_ranks(orders),np.arange(len(orders)))
        for rank,order in enumerate(orders):
            assert list(order)==lex_unrank(rank,n)
        for radius in range(1,min(6,n*(n-1)//2)):
            new,_=build_ball_packing(n,radius)
            old,_=build_packing(n,radius)
            np.testing.assert_array_equal(new,old)
            assert ball_size(n,radius)==len(inversion_ball(n,radius))


def test_radius_one_parity_shortcut_preserves_optimum_and_lex_ties():
    for n in range(3,7):
        old,_=build_packing(n,1)
        expected=[p for p in permutations(range(n))
            if sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))%2==0]
        np.testing.assert_array_equal(old,expected)
        for w in (np.zeros((n,n),int),np.random.default_rng(n).integers(0,5,(n,n))):
            np.fill_diagonal(w,0)
            order,meta=even_permutation_dp(w)
            best=min(expected,key=lambda p:(kemeny_cost(w,p),p))
            assert tuple(order)==best and meta['objective']==kemeny_cost(w,best)


def test_retry_memory_refusal_and_cache_are_explicit(tmp_path):
    with pytest.raises(SieveResourceError) as exc:
        cached_ball_packing(16,4,cache=tmp_path)
    assert exc.value.metadata['reason']=='working_array_memory_budget'
    assert exc.value.metadata['memory_bytes']==4<<30
    with pytest.raises(SieveResourceError) as again:
        cached_ball_packing(16,4,cache=tmp_path)
    assert again.value.metadata['reused_resource_receipt']
    a,_=cached_ball_packing(4,2,cache=tmp_path)
    b,meta=cached_ball_packing(4,2,cache=tmp_path)
    np.testing.assert_array_equal(a,b)
    assert meta['packing_cache_hit'] and meta['complete']


def test_completed_center_matches_original_selected_pair_estimator(tmp_path):
    rng=np.random.default_rng(817)
    for n in range(3,7):
        for count in (n,2*n,5*n,n*n*n):
            pairs=np.array([rng.choice(n,2,replace=False) for _ in range(count)])
            old,_=sieve_order(pairs,np.arange(n),cache=tmp_path/'old')
            new,_=retry_sieve_order(pairs,np.arange(n),cache=tmp_path/'new')
            np.testing.assert_array_equal(new,old)
