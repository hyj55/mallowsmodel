import numpy as np
from src.manuscript_estimators import block_scores,efficient_center,extract_pairs,hierarchy,permutation_sieve,permutation_table,sharp_center,sieve_order
from src.models import borda,kemeny_cost,logz_mean,pair_counts,distances,exact_dp,kendall
from run_exposure import draw,estimator_seed

def test_exact_sieve_separation_cover_and_objective():
    m,radius=5,3;orders,masks,bits=permutation_table(m);keep=permutation_sieve(m,radius)
    d=np.bitwise_count(masks[keep,None]^masks[None,keep])
    assert np.all(d[np.triu_indices(len(keep),1)]>radius)
    assert np.all(np.min(np.bitwise_count(masks[:,None]^masks[None,keep]),axis=1)<=radius)
    rng=np.random.default_rng(19);y=np.array([rng.choice(m,2,replace=False) for _ in range(16)])
    fitted,info=sieve_order(y,np.arange(m))
    candidates=permutation_sieve(m,int(m*(m*(m-1)//2)/len(y)));w=pair_counts(y,m)
    assert kemeny_cost(w,fitted)==min(kemeny_cost(w,o) for o in orders[candidates])
    assert info['sieve_size']==len(candidates)

def test_pair_selection_does_not_use_orientation():
    y=np.array([[4,0,2,1],[3,1,4,0],[1,2,3,4]])
    a=extract_pairs(y,np.arange(5),np.random.default_rng(17))
    b=extract_pairs(y[:,::-1],np.arange(5),np.random.default_rng(17))
    np.testing.assert_array_equal(a,b[:,::-1])

def test_block_exposure_counts_and_depth_zero_borda():
    y=np.array([[0,1],[0,2],[3,0],[1,2]])
    np.testing.assert_allclose(block_scores(y,[0,1],4,2),[1.,-1.5])
    for seed in [0,37]:
        order,meta=efficient_center(y,4,seed)
        np.testing.assert_array_equal(order,borda(pair_counts(y,4),seed))
        assert meta['depth']==0

def test_multilevel_offsets_reconstruct_consistent_complete_orders():
    truth=np.random.default_rng(2).permutation(24);y=np.tile(truth,(12,1))
    order,used,leaves=hierarchy(y,24,[dict(width=2,batch=3),dict(width=1,batch=3)],np.arange(24))
    np.testing.assert_array_equal(order,truth)
    assert used==6 and leaves>1

def test_sharp_does_not_silently_become_mle():
    order,info=sharp_center(np.tile(np.arange(7,-1,-1),(2,1)),8,seed=42)
    np.testing.assert_array_equal(order,np.arange(8));assert info['sieve_size']==1
    try:sharp_center(np.array([[1,0],[2,1]]),9)
    except ValueError as error:assert 'no MLE substitution' in str(error)
    else:raise AssertionError('Must reject unavailable exact sieve')

def test_vectorized_sampler_matches_subset_mallows():
    rng=np.random.default_rng(990);truth=np.array([3,0,4,1,2])
    y=draw(rng,12000,5,3,truth,'SM',.8,np.zeros(5))
    assert abs(distances(y,truth).mean()-logz_mean(3,.8)[1])<.025
    assert np.max(abs(np.bincount(y.ravel(),minlength=5)-7200))<200

def test_truth_and_estimator_tie_streams_are_independent():
    risks=[]
    for seed in range(100):
        truth=np.random.default_rng(seed).permutation(8)
        fitted=exact_dp(np.zeros((8,8),dtype=int),estimator_seed(seed))
        risks.append(kendall(fitted,truth))
    assert 12.5<np.mean(risks)<15.5
