from itertools import permutations
import numpy as np

from controls.tuned_sharp.model import (block_grid, pilot_partition, pilot_order,
                                      block_center, validation_order)
from src.manuscript_estimators import extract_pairs
from src.models import kemeny_cost, pair_counts


def test_whole_units_and_no_overlap():
    units = np.repeat(np.arange(11), [2,3,1,4,2,3,1,2,4,1,2])
    first, second = pilot_partition(units, 43)
    assert not set(units[first]) & set(units[second])
    assert set(first) | set(second) == set(range(len(units)))
    assert len(set(units[first])) == 5


def test_orientation_blind_pair_extraction():
    y = np.array([[0,1,2,3],[3,1,2,0],[2,0,3,1]])
    a=extract_pairs(y, np.arange(4), np.random.default_rng(19))
    b=extract_pairs(y[:,::-1], np.arange(4), np.random.default_rng(19))
    np.testing.assert_array_equal(np.sort(a,axis=1),np.sort(b,axis=1))
    np.testing.assert_array_equal(a,b[:,::-1])


def test_block_center_matches_exhaustive_and_freezes_cross_block_order(tmp_path):
    rng=np.random.default_rng(81)
    y=np.asarray([rng.permutation(6) for _ in range(120)])
    units=np.arange(len(y)); seed=74; blocks=2
    center,meta=block_center(y,6,units,blocks,seed,cache=tmp_path)
    pilot,pi,si=pilot_order(y,6,units,seed)
    assert not set(pi)&set(si)
    expected=[]
    for index,labels in enumerate(np.array_split(pilot,blocks)):
        pairs=extract_pairs(y[si],labels,np.random.default_rng(
            np.random.SeedSequence([seed,blocks,index,173])))
        canonical=np.sort(labels); lookup={v:i for i,v in enumerate(canonical)}
        w=pair_counts(np.array([[lookup[a],lookup[b]] for a,b in pairs]),3)
        assert 3*3//len(pairs)==0
        order=min(permutations(range(3)),key=lambda p:(kemeny_cost(w,p),p))
        expected.extend(canonical[list(order)])
    np.testing.assert_array_equal(center,expected)
    assert meta['exact_within_blocks']


def test_grid_and_validation_only_selection():
    assert block_grid(100)==[2,3,4,10,13]
    assert block_grid(48)==[2,3,4,5,6]
    candidates=[dict(blocks=2,status='sieve_resource_budget',validation_nll=None),
                dict(blocks=4,status='ok',validation_nll=1.2,test_nll=-999),
                dict(blocks=3,status='ok',validation_nll=1.2,test_nll=999)]
    assert [c['blocks'] for c in validation_order(candidates)]==[3,4]
