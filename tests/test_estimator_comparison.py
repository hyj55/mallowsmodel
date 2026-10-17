import numpy as np
import pandas as pd

from src import estimator_comparison as e0
from src.manuscript_estimators import block_scores
from src.strict_models import TIE_SEED


def test_e0_depth_zero_equals_borda_even_with_unseen_items_and_ties():
    y = np.array([[0,1],[1,0],[2,3],[3,2]])
    fits = e0.fit_score_estimators(y, 6)
    a, b = fits['sm_efficient'], fits['sm_global_borda']
    expected = np.lexsort((np.random.default_rng(TIE_SEED).permutation(6),
                          -block_scores(y, np.arange(6), 6, 2)))
    np.testing.assert_array_equal(a.order, expected)
    np.testing.assert_array_equal(a.order, b.order)
    assert a.beta == b.beta and a.metadata['depth'] == 0
    assert a.metadata['alias_of'] == 'sm_global_borda'
    test = np.array([[5,0],[1,4],[3,2]])
    np.testing.assert_array_equal(a.nll(test), b.nll(test))


def test_e0_domain_check_keeps_borda_without_relabeling_it_efficient():
    fits = e0.fit_score_estimators(np.tile([2,1,0], (5,1)), 3)
    assert fits['sm_efficient'].status == 'outside_schedule_domain'
    assert fits['sm_efficient'].order is None
    assert fits['sm_efficient'].metadata['depth'] is None
    assert fits['sm_global_borda'].status == 'ok'
    np.testing.assert_array_equal(fits['sm_global_borda'].order, [2,1,0])


def test_e0_active_hierarchy_keeps_separate_borda_control(monkeypatch):
    # A controlled hierarchy output tests the reporting contract, not the claim
    # that the current empirical schedules actually attain positive depth.
    monkeypatch.setattr(e0, 'efficient_center',
        lambda y,n,seed,beta0: (np.arange(n)[::-1], dict(depth=1, branch='hierarchy')))
    fits = e0.fit_score_estimators(np.array([[0,1],[0,2]]), 4)
    assert fits['sm_efficient'].metadata['depth'] == 1
    assert 'alias_of' not in fits['sm_efficient'].metadata
    assert not np.array_equal(fits['sm_efficient'].order, fits['sm_global_borda'].order)


def test_e0_comparison_uses_paired_split_differences_and_preserves_missingness():
    rows=[]
    for repeat in range(5):
        for method in e0.METHODS:
            rows.append(dict(dataset='test',repeat=repeat,method=method,
                status='not_p_frequent' if method=='sm_fotakis' and repeat==0 else 'ok',
                nll=100*repeat+(2 if method=='sm_global_borda' else 0)))
    result=e0.borda_comparisons(pd.DataFrame(rows)).set_index('reference')
    assert result.loc['pl','delta_mean'] == 2
    assert result.loc['pl','delta_mcse'] == 0
    assert result.loc['sm_fotakis','available'] == 4
    assert np.isnan(result.loc['sm_fotakis','delta_mean'])
    assert result.loc['sm_fotakis','delta_conditional_mean'] == 2
