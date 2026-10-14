"""Entire candidate sequences and final estimators, not only objective values."""
import numpy as np
import pytest

from src.models import kemeny_cost
from src.resource_sieve import build_packing, SieveResourceError
from src.streaming_sieve import streamed_packing, streaming_sieve_order


def test_concurrent_cold_compilation_uses_distinct_temporary_files(tmp_path,monkeypatch):
    from concurrent.futures import ThreadPoolExecutor
    import threading
    from src import streaming_sieve as module
    barrier=threading.Barrier(2); original=module.subprocess.run
    def overlap(command,**kwargs):
        if '-o' in command:barrier.wait(timeout=30)
        return original(command,**kwargs)
    monkeypatch.setattr(module.subprocess,'run',overlap)
    with ThreadPoolExecutor(max_workers=2) as pool:
        results=list(pool.map(lambda _:module.native_binary(tmp_path),range(2)))
    assert results[0][0]==results[1][0] and results[0][0].is_file()
    assert not list((tmp_path/'bin').glob('*.tmp'))


def test_all_small_packings_preserve_every_candidate_and_its_order(tmp_path):
    for n in range(2, 7):
        for radius in range(n*(n-1)//2+1):
            expected, _ = build_packing(n, radius)
            actual, meta = streamed_packing(n, radius, cache=tmp_path)
            np.testing.assert_array_equal(actual, expected)
            assert meta['complete'] and meta['exact']
            assert meta['sieve_size'] == len(expected)
            if radius>=n:
                joint,joint_meta=streamed_packing(n,radius,cache=tmp_path/'joint',joint_cover=True)
                np.testing.assert_array_equal(joint,expected)
                assert joint_meta['joint_cover']


def test_multiword_orientations_and_factorial_rank_overflow(tmp_path):
    # n=26 has both >64 pair bits and n!>2**64. This exact two-center
    # packing tests both representations without enumerating n! permutations.
    n=26; J=n*(n-1)//2
    actual, meta=streamed_packing(n,J-1,cache=tmp_path,seconds=10)
    np.testing.assert_array_equal(actual,[np.arange(n),np.arange(n)[::-1]])
    assert meta['complete'] and meta['prefix_jumps']>0
    assert meta['allocated_working_bytes'] < 3<<20
    assert meta['joint_prefix_jumps']>0
    assert meta['resolved_permutations']==meta['total_permutations']


def test_disk_eviction_and_reload_preserve_the_entire_packing(tmp_path):
    # Force a one-block resident cache plus one read buffer. Thousands of
    # references must actually come back from disk, not an untested code path.
    actual,meta=streamed_packing(9,4,cache=tmp_path,memory_bytes=2108000,seconds=30)
    expected,_=build_packing(9,4)
    np.testing.assert_array_equal(actual,expected)
    assert meta['disk_block_writes']>0 and meta['disk_block_reads']>0
    assert meta['allocated_working_bytes']<=2108000
    assert not list(tmp_path.glob('*.index'))


def test_selected_pair_objective_and_first_lexicographic_tie(tmp_path):
    n=6; pairs=np.asarray([[i,j] for i in range(n) for j in range(n) if i!=j])
    # Every pair is tied, so every candidate has the same objective.
    for labels in (np.arange(n),np.arange(n)*7+19):
        order, meta=streaming_sieve_order(labels[pairs],labels,cache=tmp_path)
        np.testing.assert_array_equal(order,labels)
        assert meta['objective']==len(pairs)//2
    rng=np.random.default_rng(219)
    for k in (12,30,60):
        pairs=np.asarray([rng.choice(n,2,replace=False) for _ in range(k)])
        from src.models import pair_counts
        expected,_=build_packing(n,n*(n*(n-1)//2)//k)
        w=pair_counts(pairs,n)
        best=min(map(tuple,expected),key=lambda p:(kemeny_cost(w,p),p))
        actual,meta=streaming_sieve_order(pairs,np.arange(n),cache=tmp_path)
        assert tuple(actual)==best and meta['objective']==kemeny_cost(w,best)


def test_full_sharp_center_preserves_extraction_seed_and_width(tmp_path):
    from src.resource_sieve import sharp_center
    from src.streaming_sieve import streaming_sharp_center
    rng=np.random.default_rng(471)
    for n,N in ((4,8),(5,15),(6,20)):
        y=np.asarray([rng.choice(n,3,replace=False) for _ in range(N)])
        for seed in (0,37,173):
            old,original=sharp_center(y,n,seed=seed,cache=tmp_path/'old')
            new,meta=streaming_sharp_center(y,n,seed,cache=tmp_path/'new')
            np.testing.assert_array_equal(new,old)
            assert meta['A']==original['A']==256
            assert meta['W_star']==original['W_star']
            assert meta['pairs']==original['pairs']==N
            assert meta['blocks'][0]['objective']==original['blocks'][0]['objective']


def test_resume_is_exact_and_partial_packing_never_becomes_a_fit(tmp_path):
    with pytest.raises(SieveResourceError) as failure:
        streamed_packing(9,4,cache=tmp_path,seconds=.01,memory_bytes=2108000)
    assert not failure.value.metadata['complete']
    with pytest.raises(SieveResourceError) as cached:
        streamed_packing(9,4,cache=tmp_path)
    assert cached.value.metadata['reused_resource_receipt']
    actual,meta=streamed_packing(9,4,cache=tmp_path,resume=True,seconds=30,memory_bytes=2108000)
    expected,_=build_packing(9,4)
    np.testing.assert_array_equal(actual,expected)
    assert len(meta['sessions'])==2
    assert meta['disk_block_writes']>0 and meta['disk_block_reads']>0
    assert meta['sessions'][1]['retained_before']==failure.value.metadata['packing_so_far']
    # Corrupted saved candidates must never be silently resumed or reused.
    rows=next(tmp_path.glob('*.orders'))
    with rows.open('r+b') as stream:stream.write(b'\xff\xff')
    with pytest.raises(AssertionError):streamed_packing(9,4,cache=tmp_path)


def test_resource_limit_tracks_actual_growth_and_validates_inputs(tmp_path):
    with pytest.raises(SieveResourceError) as failure:
        streamed_packing(16,4,cache=tmp_path,memory_bytes=2<<20)
    assert failure.value.metadata['reason']=='working_array_memory_budget'
    assert failure.value.metadata['packing_so_far']==0
    with pytest.raises(ValueError):streamed_packing(5,-1,cache=tmp_path)
