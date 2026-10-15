"""Verify five fixed-test learning fits per budget; --sources replays all held-out losses."""
import argparse, hashlib, json
from pathlib import Path
import numpy as np
import pandas as pd
from run import ROOT, OUT, PRIVATE, SEED, outer_split, paired_ci
from src.models import distances, logz_mean, pl_nll
from src.data import load_all

CODE = ['controls/l1/run.py','controls/l1/src/models.py','controls/l1/src/data.py','controls/l1/validate.py']
FILES = ['real_replicates.csv','real_summary.csv','fitted_parameters.json','environment.json','data_manifest.json','data_audit.json']

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def manifest():
    return dict(design='L1: five nested development permutations, one fixed outer test; 80 fits',
        code_sha256={p:digest(ROOT/p) for p in CODE},
        outputs={p:digest(OUT/p) for p in FILES},
        repetitions=5,bootstrap_draws=2000,bootstrap_target='Test-report sampling conditional on the five fitted predictors')

def validate(sources=False):
    meta=json.loads((OUT/'manifest.json').read_text())
    assert meta==manifest()
    rows=pd.read_csv(OUT/'real_replicates.csv');summary=pd.read_csv(OUT/'real_summary.csv')
    params=json.loads((OUT/'fitted_parameters.json').read_text())
    assert len(rows)==len(params)==80 and len(summary)==16
    tasks={d.name:d for d in load_all()} if sources else {}
    for (name,N),g in rows.groupby(['dataset','N']):
        assert set(g.replicate)==set(range(5)) and len(g)==5
        s=summary.loc[summary.dataset.eq(name)&summary.N.eq(N)].iloc[0]
        for c in ['SM_nll','PL_nll','delta','SM_calibrated_nll','PL_near_mle_nll']:
            np.testing.assert_allclose(g[c].mean(),s[c],atol=1e-11)
        np.testing.assert_allclose(s.calibrated_delta,s.SM_calibrated_nll-s.PL_nll,atol=1e-11)
        np.testing.assert_allclose(s.near_mle_delta,s.SM_nll-s.PL_near_mle_nll,atol=1e-11)
        assert s.repetitions==5
        if not sources:continue
        data=tasks[name];pool,test=outer_split(data);fits=[]
        for row in g.sort_values('replicate').itertuples():
            key=f'{name}_N{N}_rep{row.replicate}';p=params[key]
            a=np.load(PRIVATE/(key+'.npz'))
            expected=np.random.default_rng(SEED+11+row.replicate).permutation(pool)[:N]
            assert np.array_equal(expected,a['train_indices']) and np.array_equal(test,a['test_indices'])
            assert not set(expected)&set(test)
            y=data.y[test];d=distances(y,np.array(p['sm_order']));beta=p['beta']
            sm=beta*d+logz_mean(y.shape[1],beta)[0]
            cb=beta*p['beta_factor'];cal=cb*d+logz_mean(y.shape[1],cb)[0]
            losses=np.stack([sm,pl_nll(y,p['pl_theta']),cal,pl_nll(y,p['pl_near_theta'])])
            np.testing.assert_allclose(losses,a['losses'],atol=1e-11)
            np.testing.assert_allclose(losses.mean(axis=1),[row.SM_nll,row.PL_nll,row.SM_calibrated_nll,row.PL_near_mle_nll],atol=1e-11)
            fits.append(losses)
        avg=np.mean(fits,axis=0)
        for a,b,prefix in [(0,1,''),(2,1,'calibrated_'),(0,3,'near_mle_')]:
            np.testing.assert_allclose(paired_ci(avg[a]-avg[b]),[s[prefix+'ci_low'],s[prefix+'ci_high']],atol=1e-11)
    print('L1: verified 80 fits, 16 budget summaries, five repetitions each'+('; source memberships, losses and 48 bootstrap intervals replayed' if sources else ''))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--sources',action='store_true');p.add_argument('--write-manifest',action='store_true');a=p.parse_args()
    if a.write_manifest:(OUT/'manifest.json').write_text(json.dumps(manifest(),indent=2)+'\n')
    validate(a.sources)
