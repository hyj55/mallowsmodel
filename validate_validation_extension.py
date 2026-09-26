"""Source, estimator-identity and saved-prediction checks for the extension."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import rdata
from scipy.sparse.csgraph import connected_components

from src.models import pair_counts, kendall
from src.diagnostics import pair_arrays, context_slope, shell_decomposition
from src.strict_features import small_law
from src.validation_extension import real_tasks, split_units, SEED, confounded_law, unit_interval, download_sources
from validate_scientific_audit import restore, check_fit

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results/validation_extension'


def run(repository_only=False):
    original=json.loads((ROOT/'results/audit/validation.json').read_text())['implementation_hashes']
    unchanged=['src/strict_models.py','src/manuscript_estimators.py','src/models.py','src/diagnostics.py','src/strict_features.py']
    for path in unchanged:
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==original[path],path
    f=pd.read_csv(OUT/'synthetic_fits.csv')
    d=pd.read_csv(OUT/'synthetic_diagnostics.csv')
    assert len(f)==2800 and len(d)==8400
    assert not f.duplicated(['cell','rep','method']).any()
    assert not d.duplicated(['cell','rep','M','diagnostic']).any()
    assert f.groupby(['cell','rep']).size().eq(2).all()
    assert d.groupby(['cell','rep']).size().eq(6).all()
    assert f.groupby('cell').rep.nunique().eq(200).all()
    parameter_records=[json.loads(line) for line in (OUT/'synthetic_parameters.jsonl').read_text().splitlines()]
    parameter_ids=[(item['cell'],item['rep']) for item in parameter_records]
    expected_ids=set(map(tuple,f[['cell','rep']].drop_duplicates().to_numpy()))
    assert len(parameter_ids)==1400 and len(set(parameter_ids))==1400
    assert set(parameter_ids)==expected_ids
    with np.load(OUT/'synthetic_draws.npz',allow_pickle=False) as archive:
        assert archive['diagnostic'].shape==(1400,1000,3)
        assert archive['training_offsets'].shape==(1401,)
        assert archive['cell_rep'].shape==(1400,2)
        assert np.array_equal(archive['cell_rep'],parameter_ids)
    scores=pd.read_csv(OUT/'real_scores.csv')
    assert len(scores)==20
    assert scores[scores.dataset=='beach_preferences'].status.eq('excluded_upstream_response_filtering').all()
    assert scores[(scores.dataset!='beach_preferences')&(scores.method=='mle')].status.eq('ok').all()
    assert scores[(scores.dataset!='beach_preferences')&(scores.method=='sharp')].status.eq('exact_sieve_unavailable').all()
    assert scores[(scores.dataset!='beach_preferences')&(scores.method=='efficient')].status.eq('outside_schedule_domain').all()
    result=dict(status='passed',unchanged_estimator_and_diagnostic_modules=unchanged,
                independent_synthetic_training_datasets=1400,synthetic_fit_rows=2800,
                synthetic_diagnostic_rows=8400,included_real_tasks=3,
                upstream_filtered_sources_not_fitted=1)
    if repository_only:
        print(json.dumps(result,indent=2))
        return
    sources=download_sources()
    raw=ROOT/'data/raw/validation_extension'
    pd.testing.assert_frame_equal(rdata.read_rda(raw/'Sounds.RData')['prefs4BM'],
                                  rdata.read_rda(raw/'sounds.rda')['sounds'])
    params=json.loads((OUT/'real_parameters.json').read_text())
    splits=pd.read_csv(OUT/'real_splits.csv') if (OUT/'real_splits.csv').exists() else None
    predictions=pd.read_csv(OUT/'real_predictions.csv') if (OUT/'real_predictions.csv').exists() else None
    contexts=pd.read_csv(OUT/'real_context.csv')
    shells=pd.read_csv(OUT/'real_shells.csv')
    row_count=0; point_count=0
    for task in real_tasks():
        if not task['eligible']:
            continue
        parts=split_units(task,task['source_index']); name=task['name']
        for split,ids in parts.items():
            if splits is not None:
                saved=splits[(splits.dataset==name)&(splits.split==split)]
                assert np.array_equal(saved.record.to_numpy(),ids)
        unit_sets=[set(task['groups'][ids]) for ids in parts.values()]
        assert all(not (unit_sets[i]&unit_sets[j]) for i,j in [(0,1),(0,2),(1,2)])
        assert sum(map(len,parts.values()))==len(task['y'])
        train=task['y'][parts['fit']];test=task['y'][parts['confirmation']]
        groups=task['groups'][parts['confirmation']]
        pl=restore('pl',params[name]['pl'])
        for method,saved in params[name].items():
            fit=restore(method,saved);check_fit(fit,train,task['n'])
            row=scores[(scores.dataset==name)&(scores.method==method)].iloc[0]
            loss=fit.nll(test);delta=loss-pl.nll(test)
            if predictions is not None:
                p=predictions[(predictions.dataset==name)&(predictions.method==method)]
                assert np.allclose(loss,p.nll,rtol=0,atol=1e-12,equal_nan=True)
            assert np.allclose([row.nll,row.delta],[loss.mean(),delta.mean()],rtol=0,atol=1e-12,equal_nan=True)
            ci=unit_interval(delta,groups,SEED+task['source_index'])
            assert np.allclose([row.delta_lo,row.delta_hi],[ci['lo'],ci['hi']],atol=1e-12,rtol=0,equal_nan=True)
            row_count+=1
        if task['r']==6:
            sm=restore('mle',params[name]['mle'])
            for split in ['discovery','confirmation']:
                held=task['y'][parts[split]]
                comp=shell_decomposition(held,sm.order,sm.beta,pl.theta)
                for component in ['total','shell_mass','within_shell']:
                    row=shells[(shells.dataset==name)&(shells.split==split)&(shells.component==component)].iloc[0]
                    assert np.isclose(row.value,comp[component].mean(),atol=1e-12,rtol=0)
                for reference,order in [('fitted',sm.order),('objective',task['truth'])]:
                    answer=context_slope(pair_arrays(held,order,sm.beta,pl.theta),resamples=0)
                    row=contexts[(contexts.dataset==name)&(contexts.split==split)&(contexts.reference==reference)].iloc[0]
                    for key in ['observed','sm_predicted','pl_predicted','eligible_pairs','pair_observations']:
                        assert np.isclose(row[key],answer[key],rtol=0,atol=1e-12)
                    point_count+=1
    # Replay all declared training draws and population predictions from saved
    # parameters; there is no optimizer rerun and no new independent data.
    with np.load(OUT/'synthetic_draws.npz') as archive:
        archived_train=archive['train']
        archived_offsets=archive['training_offsets']
        archived_diagnostic=archive['diagnostic']
        archived_groups=archive['groups']
        archived_ids=archive['cell_rep']
    for record_index,item in enumerate(parameter_records):
        family,setting,N,rep,cell=(item[k] for k in ['family','setting','N','rep','cell'])
        stream=np.random.SeedSequence([SEED,10,cell,rep])
        labels_rng,train_rng,diagnostic_rng=[np.random.default_rng(s) for s in stream.spawn(3)]
        n=8 if family=='calibration' else 4
        truth=labels_rng.permutation(n)
        assert np.array_equal(truth,item['truth'])
        if family=='calibration':
            support,mass,_=small_law(n,3,'bridge',setting,'equal');support=truth[support]
            source_groups=np.zeros(len(support),int)
        else:
            support,mass,source_groups,_=confounded_law(setting,truth)
        train=support[train_rng.choice(len(support),N,p=mass)]
        indices=diagnostic_rng.choice(len(support),1000,p=mass)
        a,b=archived_offsets[record_index:record_index+2]
        assert np.array_equal([cell,rep],archived_ids[record_index])
        assert np.array_equal(train,archived_train[a:b])
        assert np.array_equal(support[indices],archived_diagnostic[record_index])
        assert np.array_equal(source_groups[indices],archived_groups[record_index])
        for method,saved in item['models'].items():
            fit=restore(method,saved);check_fit(fit,train,n)
            row=f[(f.cell==cell)&(f.rep==rep)&(f.method==method)].iloc[0]
            assert row.status==fit.status
            assert np.allclose(row.nll,mass@fit.nll(support),atol=1e-12,rtol=0,equal_nan=True)
            if fit.status=='ok':
                assert row.risk==kendall(fit.order,truth)
            elif method=='pl':
                count,_=connected_components(pair_counts(train,n)>0,directed=True,connection='strong')
                assert count>1 and fit.status=='no_unique_finite_mle'
    result.update(source_files_verified=len(sources),eligible_original_reports_preserved=2164,
                  real_fit_score_rows_checked=row_count,real_context_points_checked=point_count,
                  local_prediction_cache_checked=predictions is not None,
                  local_split_cache_checked=splits is not None,
                  empirical_record_level_outputs_published=False,
                  all_saved_synthetic_population_predictions_recomputed=True,
                  all_synthetic_training_draws_replayed=True,
                  synthetic_draw_archive_matches_frozen_streams=True,
                  public_sounds_matches_upstream_original_object=True,
                  protocol_sha256=hashlib.sha256((ROOT/'docs/protocols/VALIDATION_EXTENSION_20260926.md').read_bytes()).hexdigest())
    (OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--repository-only',action='store_true')
    run(parser.parse_args().repository_only)
