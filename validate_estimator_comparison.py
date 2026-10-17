"""Validate integrated E0; --sources replays all development and test reports."""
import argparse
import gzip
import json

import numpy as np
import pandas as pd

from src.estimator_comparison import (ROOT, PUBLIC, METHODS, SOURCES, source_records,
    code_hashes, digest, fit_score_estimators, borda_comparisons)
from src.predictive_study import empirical_context, array_hash, paired_bootstrap, BOOTSTRAP_SEED
from src.repeated_holdout import load_tasks, restore_fit, save_fit
from src.models import distances
from src.predictive_models import bounded_beta


def validate(sources=False):
    manifest = json.loads((PUBLIC/'manifest.json').read_text())
    assert manifest['code_sha256'] == code_hashes()
    for p, sha in manifest['source_sha256'].items(): assert digest(ROOT/p) == sha, p
    for p, sha in manifest['published_sha256'].items(): assert digest(PUBLIC/p) == sha, p
    with gzip.open(PUBLIC/'predictors.jsonl.gz', 'rt') as stream:
        records = [json.loads(line) for line in stream]
    old = {(r['dataset'],r['repeat']):r for r in source_records()}
    frame = pd.read_csv(PUBLIC/'repeat_scores.csv.gz')
    raw = pd.read_csv(ROOT/SOURCES[1]); raw = raw[raw.study == 'P0']
    assert len(records) == len(old) == 115 and len(frame) == 690
    assert set(frame.method) == set(METHODS) and set(frame.study) == {'E0'}
    assert not frame.duplicated(['dataset','repeat','method']).any()
    assert frame.groupby(['dataset','method']).size().eq(5).all()
    assert set(frame['repeat']) == set(range(5))
    assert np.isfinite(frame.loc[frame.status == 'ok','nll']).all()
    assert frame.loc[frame.status != 'ok','nll'].isna().all()
    assert frame[frame.method == 'sm_global_borda'].status.eq('ok').all()
    tasks = {t.name:t for t in load_tasks()} if sources else None
    aligned = {}
    for record in records:
        key = (record['dataset'],record['repeat']); source = old[key]
        assert record['fingerprint']['code'] == code_hashes()
        assert record['fingerprint']['sources'] == manifest['source_sha256']
        assert record['data_sha256'] == source['data_sha256']
        rows = frame[(frame.dataset == key[0]) & (frame['repeat'] == key[1])].set_index('method')
        old_rows = raw[(raw.dataset == key[0]) & (raw['repeat'] == key[1])].set_index('method')
        fits = {m:restore_fit(v) for m,v in record['models'].items()}
        assert set(fits) == set(METHODS)
        for method in METHODS[:4]:
            assert record['models'][method] == source['models'][method]
            for field in ('nll','delta','beta','nll_ci_low','nll_ci_high','delta_ci_low','delta_ci_high'):
                np.testing.assert_allclose(rows.loc[method,field], old_rows.loc[method,field],
                                           atol=2e-9, rtol=2e-9, equal_nan=True)
        efficient, borda = fits['sm_efficient'], fits['sm_global_borda']
        admitted = record['N']*record['r']*(record['r']-1) <= record['n']*(record['n']-1)
        assert (efficient.status == 'ok') == admitted
        if admitted and efficient.metadata['depth'] == 0:
            np.testing.assert_array_equal(efficient.order, borda.order)
            assert efficient.beta == borda.beta
            assert efficient.metadata['alias_of'] == 'sm_global_borda'
            for field in ('nll','delta','nll_ci_low','nll_ci_high','delta_ci_low','delta_ci_high'):
                np.testing.assert_allclose(rows.loc['sm_efficient',field], rows.loc['sm_global_borda',field],
                                           atol=1e-12, equal_nan=True)
        elif not admitted:
            assert efficient.metadata['depth'] is None and efficient.order is None
        np.testing.assert_array_equal(np.sort(borda.order), np.arange(record['n']))
        np.testing.assert_allclose(rows.delta, rows.nll-rows.loc['pl','nll'],
                                   atol=2e-9, rtol=2e-9, equal_nan=True)
        if not record['identified_units']:
            assert rows.ci_kind.eq('unavailable').all()
            assert rows[['nll_ci_low','nll_ci_high','delta_ci_low','delta_ci_high']].isna().all().all()
        if not sources: continue
        task = tasks[key[0]]; context = empirical_context(task,key[1])
        assert {k:array_hash(v) for k,v in context['data'].items()} == record['data_sha256']
        for part, ids in context['parts'].items():
            units = np.unique(task.units[ids]); shared = (context['split_key'],key[1],part)
            if shared in aligned: np.testing.assert_array_equal(units, aligned[shared])
            aligned[shared] = units
        assert not np.intersect1d(task.units[context['parts']['development']], context['units']).size
        expected = fit_score_estimators(context['data']['development'], task.n)
        for method in expected:
            recomputed = save_fit(expected[method])
            saved = record['models'][method]
            assert {k:v for k,v in recomputed.items() if k != 'beta'} == {
                k:v for k,v in saved.items() if k != 'beta'}
            np.testing.assert_allclose(float(recomputed['beta']),float(saved['beta']),
                                       atol=1e-10,rtol=1e-10,equal_nan=True)
        loss = {m:fit.nll(context['data']['test']) for m,fit in fits.items()}
        for method, fit in fits.items():
            np.testing.assert_allclose(loss[method].mean(), rows.loc[method,'nll'], atol=2e-9, equal_nan=True)
            if method.startswith('sm_') and fit.status == 'ok':
                total = int(distances(context['data']['development'],fit.order).sum())
                np.testing.assert_allclose(fit.beta, bounded_beta(total,record['N'],record['r']),
                                           atol=1e-10, rtol=1e-10)
        if context['identified_units']:
            seed = np.random.SeedSequence([BOOTSTRAP_SEED,context['split_key'],key[1],record['N']])
            intervals = paired_bootstrap(loss, context['units'], seed)
            for method, fields in intervals.items():
                for field,value in fields.items():
                    np.testing.assert_allclose(value, rows.loc[method,field], atol=2e-9, rtol=2e-9)
        print('REPLAY',*key,flush=True)
    from summarize_predictive_study import summarize
    expected = summarize(frame); expected.insert(0,'raw_study','P0')
    pd.testing.assert_frame_equal(pd.read_csv(PUBLIC/'summary.csv'),expected,
                                 check_dtype=False,atol=2e-9,rtol=2e-9)
    pd.testing.assert_frame_equal(pd.read_csv(PUBLIC/'borda_comparisons.csv'),borda_comparisons(frame),
                                 check_dtype=False,atol=2e-9,rtol=2e-9)
    print('E0: 115 unchanged allocations; all six methods, admission, depth-zero aliases and paired summaries verified')


if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--sources',action='store_true')
    validate(parser.parse_args().sources)
