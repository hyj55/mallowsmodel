from itertools import permutations
import numpy as np

from src.repeated_holdout import Task, split_task, score_loss, evaluate, fit_all
from src.repeated_holdout_summary import mean_fields


def task(name='a', units=None, key=1):
    units = np.arange(100) if units is None else np.asarray(units)
    return Task(name, 'baseline_replacement', np.tile([0,1], (len(units),1)),
                2, units, key, 123, 'test_unit')


def test_partition_counts_alignment_reproducibility_and_distinct_repeats():
    a, b = task('sushi_a'), task('sushi_b')
    first = split_task(a, 0)
    assert [len(x) for x in first.values()] == [60,20,20]
    for rep in range(30):
        pa, pb = split_task(a, rep), split_task(b, rep)
        np.testing.assert_array_equal(np.sort(np.concatenate(list(pa.values()))), np.arange(100))
        for name in pa:
            np.testing.assert_array_equal(pa[name], pb[name])
            np.testing.assert_array_equal(pa[name], split_task(a, rep)[name])
        if rep:
            assert not np.array_equal(pa['confirmation'], first['confirmation'])
    different_stream = split_task(task(key=2), 0)
    assert not np.array_equal(first['fit'], different_stream['fit'])


def test_assessor_blocks_never_cross_any_split_boundary():
    t = task(units=np.repeat(np.arange(46), 30))
    for rep in range(30):
        parts = split_task(t, rep)
        assert [len(x) for x in parts.values()] == [810,270,300]
        sets = [set(t.units[ix]) for ix in parts.values()]
        assert not (sets[0]&sets[1] or sets[0]&sets[2] or sets[1]&sets[2])


def test_defined_infinite_loss_is_not_an_unavailable_fit():
    out = score_loss([0., np.inf], [1.,2.], 'ok', 'ok')
    assert np.isinf(out['nll']) and np.isinf(out['paired_delta'])
    assert out['n_available'] == 2 and out['n_infinite'] == 1
    assert out['n_paired_finite'] == 1 and out['finite_report_delta'] == -1.
    missing = score_loss([np.nan,np.nan], [1.,2.], 'unavailable', 'ok')
    assert np.isnan(missing['nll']) and np.isnan(missing['paired_delta'])
    assert missing['n_available'] == missing['n_infinite'] == 0


def test_conditional_partition_mcse_and_nonfinite_denominators():
    out = mean_fields([1.,3.,5.], 'loss')
    assert out['loss_mean'] == 3.
    assert np.isclose(out['loss_partition_mcse'], 2/np.sqrt(3))
    missing = mean_fields([1.,3.,np.nan], 'loss')
    assert np.isnan(missing['loss_mean']) and np.isnan(missing['loss_partition_mcse'])
    assert missing['loss_finite_conditional_mean'] == 2.
    assert missing['loss_finite_repeats'] == 2 and missing['loss_defined_repeats'] == 2
    divergent = mean_fields([1.,3.,np.inf], 'loss')
    assert np.isinf(divergent['loss_mean']) and divergent['loss_infinite_repeats'] == 1
    assert np.isnan(divergent['loss_partition_mcse'])


def test_average_loss_does_not_turn_into_ensemble_probability_loss():
    losses = -np.log([.8,.2])
    actual = mean_fields(losses, 'nll')['nll_mean']
    assert np.isclose(actual, -np.log(.4))
    assert not np.isclose(actual, -np.log((.8+.2)/2))


def test_confirmation_outcomes_do_not_choose_the_model():
    y = np.array(list(permutations(range(3)))*10)
    t = Task('toy', 'strict_features', y, 3, np.arange(len(y)), 1000, 1, 'one_report', np.arange(3))
    parts = split_task(t, 0)
    models = fit_all(t, y[parts['fit']])
    old = evaluate(t, 0, parts, models)
    altered = y.copy(); altered[parts['confirmation']] = [2,1,0]
    t.y = altered
    new = evaluate(t, 0, parts, models)
    assert [r['choice'] for r in old['selections']] == [r['choice'] for r in new['selections']]
    a = [r for r in old['scores'] if r['split'] == 'discovery']
    b = [r for r in new['scores'] if r['split'] == 'discovery']
    np.testing.assert_allclose([r['nll'] for r in a], [r['nll'] for r in b], equal_nan=True)
