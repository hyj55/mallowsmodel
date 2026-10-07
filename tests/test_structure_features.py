from itertools import combinations, permutations, product
from fractions import Fraction
from math import factorial, prod
import numpy as np

from src.models import distances
from src.structure_features import describe_structure, nominal_uniform_tv


def test_actual_shell_counts_include_unobserved_permutations():
    y=np.array([[0,1,2]]*30+[[1,0,2]]+[[0,2,1]]*9)
    out=describe_structure(y,np.arange(3))
    shell=out['shells'].query('d == 1').iloc[0]
    assert shell.possible_rankings==2 and shell.reports==10
    assert np.isclose(shell.frequency_tv,.4)
    one=describe_structure(np.array([[1,0,2]]),np.arange(3))
    row=one['shells'].iloc[0]
    assert row.zero_count_rankings==1 and row.frequency_tv==.5
    assert row.iid_uniform_expected_tv==.5 and row.excess_tv_over_iid_uniform==0
    assert one['summary']['shell_occurrence_share_count_ge2']==0


def test_uniform_sampling_scale_matches_exact_allocation_enumeration():
    for a in [2,3,4]:
        for m in [1,2,3,4]:
            empirical=[]
            for sample in product(range(a),repeat=m):
                p=np.bincount(sample,minlength=a)/m
                empirical.append(.5*np.abs(p-1/a).sum())
            assert np.isclose(np.mean(empirical),nominal_uniform_tv(m,a))


def test_exact_mallows_example_has_uniform_shells_and_positive_swap():
    rows=[]
    for shown in [[0,1,2],[0,2,3]]:
        for ranking in permutations(shown):
            d=int(distances(np.array([ranking]),np.arange(4))[0])
            rows.extend([ranking]*2**(3-d))
    out=describe_structure(np.array(rows),np.arange(4))
    assert np.isclose(out['summary']['shell_tv'],0)
    assert out['summary']['swap_gap_edges']==1
    assert np.isclose(out['summary']['swap_gap_effect'],2/21)
    assert np.isclose(out['summary']['context_gap_slope'],2/21)
    row=out['pairs'].query('item_i == 0 and item_j == 2').iloc[0]
    assert np.isclose(row.low_h_win_rate,2/3)
    assert np.isclose(row.high_h_win_rate,16/21)


def test_pl_pair_probability_is_invariant_despite_changing_displayed_gap():
    worth=[2,1,1,1]; rows=[]
    for shown in [[0,1,2],[0,2,3]]:
        for ranking in permutations(shown):
            p=prod(Fraction(worth[item],sum(worth[j] for j in ranking[k:]))
                   for k,item in enumerate(ranking))
            rows.extend([ranking]*int(12*p))
    out=describe_structure(np.array(rows),np.arange(4))
    assert out['summary']['shell_tv']>0
    assert np.isclose(out['summary']['context_display_sd'],0)
    assert np.isclose(out['summary']['swap_gap_effect'],0)


def test_missing_contrasts_are_unavailable_not_zero():
    for rows,order in [([[0,1],[1,0],[0,2]],np.arange(3)),
                       ([[0,1,2],[1,0,2]],np.arange(3))]:
        out=describe_structure(np.array(rows),order)
        assert np.isnan(out['summary']['context_display_sd'])
        assert np.isnan(out['summary']['context_gap_slope'])
        assert np.isnan(out['summary']['swap_gap_effect'])
    pair=describe_structure(np.array([[0,1],[1,0],[0,2]]),np.arange(3))
    assert np.isnan(pair['summary']['shell_tv'])


def test_gap_and_same_gap_components_reconcile_and_do_not_pool_pairs():
    y=np.array([[0,1,2],[0,1,2],[2,1,0],[0,2,3],[2,0,3],[0,2,4],[2,0,4]])
    out=describe_structure(y,np.arange(5)); s=out['summary']
    assert np.isclose(s['context_display_sd']**2,
                      s['context_gap_component_sd']**2+s['context_same_gap_component_sd']**2)
    assert out['swaps'].h_change.eq(0).any()
    for row in out['swaps'].itertuples():
        sets=out['displays'].set_index('display_id')
        import json
        a,b=set(json.loads(sets.loc[row.display_1,'items'])),set(json.loads(sets.loc[row.display_2,'items']))
        assert len(a^b)==2 and {row.item_i,row.item_j} <= a&b


def test_record_order_and_item_relabeling_preserve_main_features():
    y=np.array([[0,1,2],[0,1,2],[2,1,0],[0,2,3],[2,0,3]])
    rename=np.array([3,1,0,2]); order=np.arange(4)
    base=describe_structure(y,order)['summary']
    for rows,center in [(y[::-1],order),(rename[y],rename[order])]:
        got=describe_structure(rows,center)['summary']
        for key in ['shell_tv','shell_iid_uniform_expected_tv','context_display_sd',
                    'context_gap_slope','swap_gap_effect']:
            np.testing.assert_allclose(base[key],got[key],equal_nan=True)
