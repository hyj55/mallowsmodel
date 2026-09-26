"""Independent controls for the declared new experiments, not new estimators."""
import numpy as np
from scipy.special import expit
from src.validation_extension import confounded_law, confounded_focal_contrast, unit_interval


def test_context_confounding_is_only_a_group_mixture_effect():
    for rho in [0., .45, .9]:
        reports, mass, groups, contexts = confounded_law(rho)
        assert np.isclose(mass.sum(),1)
        assert np.isclose(mass[groups==1].sum(),.5)
        assert np.isclose(mass[contexts==1].sum(),.5)
        outcome = np.argmax(reports==0,axis=1)<np.argmax(reports==2,axis=1)
        rates=[]
        for context in [0,1]:
            mask=contexts==context
            rates.append(mass[mask]@outcome[mask]/mass[mask].sum())
            for group, scale in [(0,.2),(1,.8)]:
                mask=(contexts==context)&(groups==group)
                assert np.isclose(mass[mask]@outcome[mask]/mass[mask].sum(),expit(2*scale))
        assert np.isclose(rates[0]-rates[1],confounded_focal_contrast(rho))
        # Renaming items leaves every probability and group assignment unchanged.
        renamed,p,g,c=confounded_law(rho,np.array([3,1,0,2]))
        assert np.array_equal(renamed,np.array([3,1,0,2])[reports])
        assert np.array_equal(mass,p) and np.array_equal(groups,g) and np.array_equal(contexts,c)


def test_unit_bootstrap_keeps_all_reports_of_each_sampled_assessor():
    values=np.array([0.,1.,4.,2.,3.])
    groups=np.array([10,10,20,30,30])
    seed=201; draws=300
    units=np.array([10,20,30])
    rng=np.random.default_rng(seed)
    expected=[]
    for selected in rng.integers(3,size=(draws,3)):
        original_rows=np.concatenate([np.flatnonzero(groups==units[i]) for i in selected])
        expected.append(values[original_rows].mean())
    result=unit_interval(values,groups,seed,resamples=draws)
    assert np.allclose([result['lo'],result['hi']],np.quantile(expected,[.025,.975]))
