"""Read-only checks of saved-prediction distances, aggregation and provenance.

--write-manifest records reviewed artifact bytes after numerical checks. Normal
verification never rewrites results and does not need licensed raw datasets.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results/heldout_kendall'
EXPECTED={'predictive':2835,'repeated':1150,'fixed_real':230,'groups':55800,
          'learning':320,'tuned_blocks':201,'validation_simulations':2800,
          's4t':172800,'strict_bridge':16000,'strict_shell':6000,'strict_coverage':1080,
          'legacy_real':420,'legacy_tennis':120,'legacy_controls':102,
          'legacy_synthetic':1800,'legacy_small':7140,'legacy_coverage':2160,'selectors':11312}
CODE=['build_heldout_kendall.py','replay_strict_kendall.py','replay_legacy_kendall.py',
      'build_kendall_selectors.py','summarize_heldout_kendall.py','verify_heldout_kendall.py',
      'src/heldout_kendall.py','src/heldout_kendall_reporting.py','tests/test_heldout_kendall.py']


def read(name):return pd.read_csv(ROOT/name,low_memory=False)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def close(a,b):np.testing.assert_allclose(a,b,rtol=3e-7,atol=3e-7,equal_nan=True)


def main(write=False):
    assert {p.name.removesuffix('_fits.csv.gz') for p in OUT.glob('*_fits.csv.gz')}==set(EXPECTED)
    frames={name:read(f'results/heldout_kendall/{name}_fits.csv.gz') for name in EXPECTED}
    for name,df in frames.items():
        assert len(df)==EXPECTED[name],name
        assert (df.evaluation_count>0).all(),name
        ok=df.test_kendall_mean.notna()
        assert df.loc[ok,'test_kendall_mean'].between(-1e-7,df.loc[ok,'r']*(df.loc[ok,'r']-1)/2+1e-7).all(),name
        finite=ok & df.evaluation_target.eq('test_reports')
        close(df.loc[finite,'test_kendall_mean']*df.loc[finite,'evaluation_count'],df.loc[finite,'test_kendall_sum'])
        close(df.loc[finite,'test_kendall_sum'],np.round(df.loc[finite,'test_kendall_sum']))
        assert df.loc[df.evaluation_target.eq('population'),'test_kendall_sum'].isna().all(),name

    # P2 covers every empirical task and both evaluation partitions.
    p2=frames['fixed_real'];assert p2.dataset.nunique()==23
    for source in ['results/baseline_replacement/scores.csv','results/strict_features/real_results.csv',
                   'results/context_followup/scores.csv','results/validation_extension/real_scores.csv']:
        original=read(source)
        if 'dataset' not in original:original['dataset']='wheat'
        if 'split' not in original:original['split']='confirmation'
        original=original[original.dataset.isin(p2.dataset.unique())]
        joined=original.merge(p2,on=['dataset','split','method'],suffixes=('_old',''),validate='one_to_one')
        assert len(joined)==len(original),source
        close(joined.nll,joined.nll_old)

    # G1 must weight disjoint groups by reports, not by fitted-model count.
    group=frames['groups'];keys=['dataset','design','percent','repeat','scheme','method']
    scores=[]
    for key,g in group.groupby(keys):
        w=g.evaluation_count.to_numpy();available=g.test_kendall_mean.notna()
        scores.append(dict(zip(keys,key),n_test=w.sum(),n_available=w[available].sum(),
                           nll_all=float(w@g.nll.to_numpy()/w.sum()) if g.nll.notna().all() else np.nan))
    new=pd.DataFrame(scores);old=read('results/group_sensitivity/repeat_scores.csv.gz')
    joined=old.merge(new,on=keys,suffixes=('_old',''),validate='one_to_one')
    assert len(joined)==len(old)==len(new)==2250
    for column in ['n_test','n_available','nll_all']:close(joined[column],joined[column+'_old'])

    # Fixed-ridge PL controls are reproduced, then checked against their saved
    # aggregate contrasts (the original table did not store per-fit centers).
    original=read('results/heldout_kendall/inputs/legacy/results/exposure/real_penalty_sensitivity.csv')
    new=frames['legacy_real'].groupby(['dataset','N','method']).nll.mean()
    for row in original.itertuples():
        for tau in (1,10):
            close(new.loc[(row.dataset,row.N,f'pl_fixed_{tau}')],row.nll-getattr(row,f'pl_fixed_{tau}_delta'))

    # Recompute every allocation and every repetition mean, not only E0.
    full=pd.concat(frames.values(),ignore_index=True)
    full['setting']=full.setting.fillna('')
    keys=['study','dataset','setting','method','split','evaluation_target','repeat']
    saved=read('results/heldout_kendall/allocation_scores.csv.gz').fillna({'setting':''}).set_index(keys)
    assert not saved.index.duplicated().any()
    full['kd_sum']=full.test_kendall_mean*full.evaluation_count
    full['nll_sum']=full.nll.where(np.isfinite(full.nll),0)*full.evaluation_count
    full['available_count']=full.evaluation_count.where(full.test_kendall_mean.notna(),0)
    full['nll_infinite']=np.isinf(full.nll)
    pooled=full.groupby(keys,dropna=False).agg(kd_sum=('kd_sum','sum'),nll_sum=('nll_sum','sum'),
        weight=('evaluation_count','sum'),available=('available_count','sum'),rows=('status','size'),
        kd_count=('test_kendall_mean','count'),nll_count=('nll','count'),infinite=('nll_infinite','any'))
    assert set(pooled.index)==set(saved.index)
    pooled=pooled.reindex(saved.index);count=len(pooled)
    kd=(pooled.kd_sum/pooled.weight).where(pooled.kd_count.eq(pooled.rows))
    nll=(pooled.nll_sum/pooled.weight).mask(pooled.infinite,np.inf).where(pooled.nll_count.eq(pooled.rows))
    close(saved.test_kendall_mean,kd);close(saved.nll_mean,nll);close(saved.available_reports,pooled.available)
    summary=read('results/heldout_kendall/summary.csv').fillna({'setting':''}).set_index(keys[:-1])
    rep=saved.reset_index();rep['nll_finite']=rep.nll_mean.where(np.isfinite(rep.nll_mean),0);rep['infinite']=np.isinf(rep.nll_mean)
    means=rep.groupby(keys[:-1],dropna=False).agg(kd=('test_kendall_mean','mean'),sd=('test_kendall_mean','std'),
        kd_count=('test_kendall_mean','count'),nll=('nll_finite','mean'),nll_count=('nll_mean','count'),
        infinite=('infinite','any'),repetitions=('models','size'))
    assert set(means.index)==set(summary.index);means=means.reindex(summary.index)
    close(summary.test_kendall_mean,means.kd.where(means.kd_count.eq(means.repetitions)))
    close(summary.nll_mean,means.nll.mask(means.infinite,np.inf).where(means.nll_count.eq(means.repetitions)))
    close(summary.test_kendall_mcse,(means.sd/np.sqrt(means.repetitions)).where(means.kd_count.eq(means.repetitions)))
    close(summary.repetitions,means.repetitions)

    beta=read('results/heldout_kendall/beta_audit.csv.gz')
    available=beta.beta_fit.notna()
    assert beta.loc[available,'beta_fit_below_beta0'].astype(bool).eq(beta.loc[available,'beta_fit']<beta.loc[available,'algorithm_beta0']).all()
    assert beta.loc[~available,'beta_fit_below_beta0'].isna().all()
    e0=beta[beta.study.eq('E0') & beta.method.eq('sm_sharp') & beta.beta_fit_below_beta0.eq(True)]
    assert len(e0)==1 and e0.dataset.iloc[0]=='beans' and e0['repeat'].iloc[0]==0
    s4=frames['s4t'];known=s4.beta_true.notna() & s4.algorithm_beta0.notna()
    assert s4.loc[known,'true_beta_below_beta0'].eq(s4.loc[known,'beta_true']<s4.loc[known,'algorithm_beta0']).all()

    # Frozen producer sources are exact Git blobs, including line endings.
    tree=json.loads((OUT/'inputs/legacy_tree.json').read_text());legacy=OUT/'inputs/legacy';pinned=0
    for path in legacy.rglob('*'):
        if not path.is_file() or '__pycache__' in path.parts:continue
        name=str(path.relative_to(legacy));b=path.read_bytes()
        assert hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()==tree[name]['sha'],name
        pinned+=1
    sections=json.loads((OUT/'report_sections.json').read_text())
    for name,section in sections.items():assert section in (ROOT/name).read_text(),name
    for p in list(OUT.glob('*.md'))+[ROOT/'docs/dispersion_assumptions.md']:
        assert not any(ord(c)<32 and c not in '\n\r\t' for c in p.read_text()),p

    files={str(p.relative_to(ROOT)) for p in OUT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='manifest.json'}
    files.update(CODE);files.update(['docs/criteria.md','docs/dispersion_assumptions.md'])
    sources=set()
    for p in OUT.glob('*_sources.json'):sources.update(json.loads(p.read_text()))
    sources.update(['results/group_sensitivity/repeat_scores.csv.gz',
                    'results/baseline_replacement/scores.csv','results/strict_features/real_results.csv',
                    'results/context_followup/scores.csv','results/validation_extension/real_scores.csv',
                    'experiments/section44_per_setting/results/selection.json',
                    'experiments/section44_per_setting/results/draw_archives.json'])
    manifest=dict(definition='Mean report discordances; original fits, NLL and selections preserved',
                  score_records=len(full),pinned_blobs=pinned,
                  source_sha256={name:sha(ROOT/name) for name in sorted(sources)},
                  artifact_sha256={name:sha(ROOT/name) for name in sorted(files)})
    path=OUT/'manifest.json'
    if write:path.write_text(json.dumps(manifest,indent=2)+'\n')
    else:assert json.loads(path.read_text())==manifest,'score artifact or provenance hash changed'
    print(f'PASS: {len(full)} score records; {count} allocation scores; {len(summary)} summaries; '
          f'P2 and G1 NLL replay; fixed-ridge controls; beta audit; {pinned} exact source blobs.')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write-manifest',action='store_true');main(p.parse_args().write_manifest)
