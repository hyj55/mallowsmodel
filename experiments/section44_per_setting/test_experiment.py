"""Scientific safeguards: likelihood, exact reuse, and held-out selection."""
from copy import deepcopy
import math
import numpy as np

from experiments.section44.core import direct_sm, fit, Calibration
from experiments.section44.design import candidate_grid
from experiments.section44_per_setting.design import cells, group_key, holdout_size
from experiments.section44_per_setting.engine import (report_distances, normalizer,
    score, generate, computational_plan)
from experiments.section44_per_setting.run import select_records
from src.models import distances, logz_mean
from src.predictive_models import bounded_beta


def test_inversion_counts_and_geometric_normalizer():
    rng = np.random.default_rng(71)
    for n,r,N in ((6,3,20),(64,32,8),(512,512,3)):
        order = rng.permutation(n)
        y = np.array([rng.choice(n,r,replace=False) for _ in range(N)])
        np.testing.assert_array_equal(report_distances(y,order),distances(y,order))
        for beta in (0.,1e-7,1e-4,.1,.8,10.):
            np.testing.assert_allclose(normalizer(r,beta),logz_mean(r,beta),rtol=1e-9,atol=1e-7)


def test_training_only_dispersion_and_likelihood():
    rng = np.random.default_rng(17)
    order = rng.permutation(12)
    y = direct_sm(rng,80,12,4,order,.8)
    v = direct_sm(rng,30,12,4,order,.8)
    a = score(y,v,order)
    b = score(y,v[:,::-1],order)
    assert a['beta'] == b['beta'] and a['train_nll']==b['train_nll']
    assert a['holdout_nll'] != b['holdout_nll']
    expected = bounded_beta(int(distances(y,order).sum()),len(y),4)
    assert abs(a['beta']-expected)<1e-10
    assert abs(a['holdout_nll']-(expected*distances(v,order)+logz_mean(4,expected)[0]).mean())<1e-10


def test_stream_roles_and_training_budget():
    assert len(cells())==90 and len({group_key(c) for c in cells()})==82
    c=cells()[5]
    truth,y,v,seed=generate(c,0,5,2)
    truth2,y2,v2,seed2=generate(c,0,5,2)
    np.testing.assert_array_equal(y,y2)
    np.testing.assert_array_equal(v,v2)
    assert len(y)==c['N'] and len(v)==holdout_size(c['N'])
    assert seed==seed2 and seed!=generate(c,1,5,2)[3]
    assert not np.array_equal(y[:min(len(y),len(v))],v[:min(len(y),len(v))])


def test_plan_reuse_matches_unaliased_original(tmp_path):
    # Covers direct Borda equivalence, positive-depth hierarchy, local sieves,
    # terminal-window equivalence and unavailable exact resource paths.
    for n,r,N in ((16,3,40),(64,16,8)):
        c=dict(n=n,r=r,N=N,beta0=.8)
        rng=np.random.default_rng(N+73)
        y=direct_sm(rng,N,n,r,rng.permutation(n),.8)
        cache={}
        for entry in candidate_grid().values():
            for family in entry['families']:
                _,key,_=computational_plan(c,family,entry['config'])
                order,meta=fit(y,n,family,Calibration(**entry['config']),.8,71,tmp_path)
                if key in cache:
                    previous,status=cache[key]
                    assert status==meta['status']
                    if order is not None:
                        np.testing.assert_array_equal(order,previous)
                else:
                    cache[key]=(order,meta['status'])


def test_group_selection_uses_validation_only_and_allows_zero_depth():
    draws=[]
    for c in cells():
        for rep in range(20):
            models={};fits={}
            wanted='anchor_K0.1' if c['n']<128 else 'anchor_K0.3'
            for name,cfg in candidate_grid().items():
                for family in cfg['families']:
                    key=family+'__'+name
                    models[key]=dict(fit_key=key,depth=0,branch='borda_fallback')
                    fits[key]=dict(status='ok',holdout_nll=1. if name==wanted else 2.,
                                   kendall=-1e9 if name!=wanted else 1e9)
            draws.append(dict(cell=c,group=group_key(c),repeat=rep,models=models,fits=fits))
    selected,_=select_records(draws)
    for c in cells():
        wanted='anchor_K0.1' if c['n']<128 else 'anchor_K0.3'
        for family in ('sharp','efficient'):
            assert selected[group_key(c)][family]['candidate']==wanted
    # Adversarial truth/test fields cannot affect a choice.
    for d in draws:
        d['test_nll']=-1e99;d['truth']=[0]
        for f in d['fits'].values():
            f['kendall']=-f['kendall'];f['test_nll']=np.random.default_rng(3).normal()
    assert select_records(draws)[0]==selected
