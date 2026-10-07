from itertools import permutations
import numpy as np
import pytest

from src.models import distances, pair_counts, kemeny_cost
from src.pair_features import pair_frequencies, summarize_frequencies, reference_center


def test_exact_mallows_counts_match_by_displayed_gap_across_different_sets():
    rows = []
    for shown in [[0,1,2], [0,2,3]]:
        for report in permutations(shown):
            d = int(distances(np.array([report]), np.arange(4))[0])
            rows.extend([report]*(2**(3-d)))
    cells = pair_frequencies(np.array(rows), np.arange(4))
    np.testing.assert_allclose(cells.loc[cells.h.eq(1), 'win_rate'], 2/3)
    np.testing.assert_allclose(cells.loc[cells.h.eq(2), 'win_rate'], 16/21)
    shared = cells.loc[cells.item_i.eq(0) & cells.item_j.eq(2)]
    assert set(shared.h) == {1,2}  # Global distance is two in both sets.
    gaps, summary = summarize_frequencies(cells)
    assert np.isclose(summary['heterogeneity_sd'], 0.)
    assert np.isclose(gaps.heterogeneity_sd, 0.).all()


def test_pl_16_4_1_example_has_nonzero_equal_gap_heterogeneity():
    rows = []
    for i,j,wins in [(0,1,68),(1,2,68),(0,2,80)]:
        rows.extend([[i,j]]*wins + [[j,i]]*(85-wins))
    cells = pair_frequencies(np.array(rows), np.arange(3))
    assert len(cells) == 3 and cells.h.eq(1).all()
    _, summary = summarize_frequencies(cells)
    assert np.isclose(summary['heterogeneity_sd'], np.std([.8,.8,16/17]))


def test_no_majority_flip_and_single_pair_gap_is_uninformative():
    cells = pair_frequencies(np.array([[1,0,2],[1,0,2],[0,1,2]]), np.arange(3))
    assert cells.query('item_i == 0 and item_j == 1').win_rate.iloc[0] == 1/3
    gaps, summary = summarize_frequencies(cells)
    assert np.isnan(gaps.loc[gaps.h.eq(2), 'heterogeneity_sd'].iloc[0])
    assert summary['comparable_pair_occurrences'] == 6
    assert summary['pair_occurrences'] == 9


def test_row_order_duplication_and_label_changes_preserve_feature():
    y = np.array([[0,1,2],[1,0,3],[2,3,1],[0,3,2]])
    order = np.array([2,0,3,1])
    base = summarize_frequencies(pair_frequencies(y, order))[1]
    rename = np.array([3,2,0,1])
    for other, center in [(y[::-1],order), (np.repeat(y,3,axis=0),order), (rename[y],rename[order])]:
        got = summarize_frequencies(pair_frequencies(other, center))[1]
        assert np.isclose(got['heterogeneity_sd'], base['heterogeneity_sd'])


def test_reference_center_agrees_with_bruteforce_objective_and_rejects_bad_order():
    y = np.array([[2,0,3],[1,2,0],[3,1,0],[2,1,3]])
    center, info = reference_center(y, 4)
    w = pair_counts(y, 4)
    assert info['certified']
    assert kemeny_cost(w, center) == min(kemeny_cost(w,p) for p in permutations(range(4)))
    with pytest.raises(ValueError):
        pair_frequencies(y, [0,1,1,3])
