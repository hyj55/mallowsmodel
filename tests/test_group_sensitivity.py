from collections import Counter
from itertools import permutations
import numpy as np
import pytest

from src.group_sensitivity import (exact_dp_batched, fotakis_center, fit_candidates,
    within_split, holdout_split, matched_training, group_score, paired_contrast)
from src.models import exact_dp, pair_counts, kemeny_cost
from src.strict_models import fit_sm_strict, StrictFit


def test_batched_exact_dp_matches_reference_ties_and_exhaustive_optima():
    rng = np.random.default_rng(21)
    for n in [2, 4, 6, 12]:
        for sample in range(4):
            w = rng.integers(0, 4, size=(n, n)) if sample else np.zeros((n, n), int)
            np.fill_diagonal(w, 0)
            for seed in [0, 93847]:
                actual = exact_dp_batched(w, seed)
                np.testing.assert_array_equal(actual, exact_dp(w, seed))
                if n <= 6:
                    assert kemeny_cost(w, actual) == min(kemeny_cost(w, p) for p in permutations(range(n)))


def test_fotakis_majority_predecessors_and_ties():
    y = np.tile([3, 0, 2, 1], (5, 1))
    np.testing.assert_array_equal(fotakis_center(pair_counts(y, 4)), [3, 0, 2, 1])
    # A directed 3-cycle gives equal predecessor counts, so only the declared priority resolves it.
    w = np.array([[0, 2, 1], [1, 0, 2], [2, 1, 0]])
    expected = np.argsort(np.random.default_rng(2042).permutation(3))
    np.testing.assert_array_equal(fotakis_center(w, 2042), expected)
    # A pair tied 1:1 contributes a predecessor to BOTH alternatives.
    w = np.array([[0, 1, 1], [1, 0, 1], [0, 0, 0]])
    assert set(fotakis_center(w)[:2]) == {0, 1}
    with pytest.raises(ValueError, match='every pair'):
        fotakis_center(np.zeros((4, 4), int))


def test_splits_are_reproducible_disjoint_and_outcome_blind():
    groups = np.repeat(np.arange(5), [17, 19, 20, 21, 22])
    for percent in [50, 70, 80]:
        a, b = within_split(groups, 3, percent, 5)
        aa, bb = within_split(groups, 3, percent, 5)
        assert np.array_equal(a, aa) and np.array_equal(b, bb)
        assert not np.intersect1d(a, b).size
        assert np.array_equal(np.sort(np.r_[a, b]), np.arange(len(groups)))
        for g in range(5):
            count = int((groups[a] == g).sum())
            assert count == percent * (groups == g).sum() // 100
            matched = matched_training(a, count, 3, percent, 5, g)
            assert len(matched) == len(np.unique(matched)) == count
            assert np.isin(matched, a).all() and not np.intersect1d(matched, b).size
        assert not np.array_equal(a, within_split(groups, 3, percent, 6)[0])
    a, b = holdout_split(groups, 3, 5)
    assert not np.intersect1d(groups[a], groups[b]).size


def test_fit_admission_does_not_silently_repair_missing_coverage():
    y = np.tile(np.arange(4), (10, 1))
    fits = fit_candidates(y, 4)
    assert fits['sm_mle'].status == fits['sm_fotakis'].status == 'ok'
    assert fits['sm_sharp'].status == 'excluded_outside_theorem_regime'
    assert fits['pl'].status == 'no_unique_finite_mle'
    assert np.isinf(fits['sm_mle'].nll(np.array([[1, 0, 2, 3]]))[0])
    missing = fit_candidates(np.array([[0, 1], [1, 0]]), 4)
    assert missing['sm_mle'].status == 'unseen_catalog_items'
    sparse = fit_candidates(np.array([[i, (i+1) % 12] for i in range(12)]), 12)
    assert sparse['sm_fotakis'].status == 'not_p_frequent'
    assert sparse['sm_sharp'].status == 'exact_sieve_unavailable'
    assert sparse['sm_efficient'].status == 'ok'
    assert sparse['sm_efficient'].metadata['depth'] == 0


def test_exact_fit_likelihood_unchanged_from_existing_estimator():
    y = np.array(list(permutations(range(4)))[::3])
    actual = fit_candidates(y, 4)['sm_mle']
    expected = fit_sm_strict(y, 4, 'mle')
    np.testing.assert_array_equal(actual.order, expected.order)
    assert actual.beta == expected.beta
    np.testing.assert_allclose(actual.nll(y), expected.nll(y))


def test_infinite_and_unavailable_scores_remain_distinct():
    good = StrictFit('sm', np.arange(2), beta=np.inf)
    values = good.nll(np.array([[0, 1], [1, 0]]))
    result = group_score(values, good, 2)
    assert result['n_available'] == 2 and result['n_finite'] == result['n_infinite'] == 1
    assert np.isinf(result['all_sum'])
    failed = StrictFit('pl', None, status='no_unique_finite_mle')
    result = group_score(failed.nll(np.array([[0, 1]])), failed, 1)
    assert result['n_available'] == result['n_finite'] == result['n_infinite'] == 0
    assert np.isnan(result['all_sum'])


def test_interaction_uses_one_common_four_prediction_mask():
    a = np.array([1., 2., np.inf, 3.])
    b = np.array([2., np.nan, 4., 5.])
    c = np.array([2., 2., 1., 4.])
    d = np.array([2., 2., 1., 3.])
    out = paired_contrast(a, b, c, d)
    assert out == dict(n_common=2, sm_change_sum=-2., pl_change_sum=2., interaction_sum=-4.)


def test_summary_weights_and_failure_denominators_have_hand_computed_answers():
    import pandas as pd
    from src.group_sensitivity_summary import score_repeats, summarize_scores
    common = dict(dataset='toy', design='within', percent=70, repeat=0,
                  scheme='local', method='sm_mle', status='ok')
    frame = pd.DataFrame([
        dict(common, n_test=2, n_available=2, n_finite=2, n_infinite=0,
             finite_sum=4., n_paired=2, delta_sum=2.),
        dict(common, n_test=6, n_available=6, n_finite=3, n_infinite=3,
             finite_sum=9., n_paired=3, delta_sum=-3.)])
    row = score_repeats(frame).iloc[0]
    assert row.finite_nll == 2.6 and row.macro_finite_nll == 2.5
    assert row.delta == -.2 and row.macro_delta == 0.
    assert row.paired_coverage == 5/8 and np.isinf(row.nll_all)
    summary = summarize_scores(score_repeats(frame)).iloc[0]
    assert summary.infinite_nll_repeats == 1 and summary.unavailable_repeats == 0
    frame.loc[1, ['status','n_available','n_finite','n_infinite','finite_sum','n_paired','delta_sum']] = [
        'unavailable', 0, 0, 0, 0., 0, 0.]
    summary = summarize_scores(score_repeats(frame)).iloc[0]
    assert summary.infinite_nll_repeats == 0 and summary.unavailable_repeats == 1
    assert summary.finite_nll_mean == 2.0 and summary.finite_coverage_mean == .25
