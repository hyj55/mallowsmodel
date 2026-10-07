"""Describe entire empirical tasks at equal displayed-center gap h.

Reuse recorded prediction results; do not split data, predict held-out reports,
select a model, bootstrap, or test a hypothesis. Saved full-data reference orders
are replayed unless --refresh-centers is explicitly requested.
"""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

import numpy as np
import pandas as pd

from src.repeated_holdout import load_tasks, source_inventory
from src.pair_features import reference_center, pair_frequencies, summarize_frequencies
from src.models import kemeny_cost, pair_counts

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'data/features'
SNAPSHOT = '89b21645d5f7eb463cc90c4e982c3a66ce805b41'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def array_digest(y):
    return hashlib.sha256(np.asarray(y, dtype='<i8').tobytes()).hexdigest()


def tennis_tasks():
    manifest = json.loads((OUT/'tennis_sources.json').read_text())
    raw = ROOT/'data/raw/tennis'
    raw.mkdir(parents=True, exist_ok=True)
    seasons = {}
    for entry in manifest['files']:
        if not entry['file'].startswith('atp_matches_'):
            continue
        path = raw/entry['file']
        if not path.exists():
            payload = urllib.request.urlopen(entry['url'], timeout=60).read()
            if hashlib.sha256(payload).hexdigest() != entry['sha256']:
                raise ValueError('Changed ATP source')
            path.write_bytes(payload)
        assert digest(path) == entry['sha256'] and path.stat().st_size == entry['bytes']
        df = pd.read_csv(path)
        valid = df[['winner_id','loser_id','tourney_date','score']].notna().all(axis=1)
        valid &= df.winner_id != df.loser_id
        valid &= ~df.score.fillna('').str.upper().str.contains(r'W/O|RET|DEF|ABD|ABN|UNF', regex=True)
        seasons[int(path.stem[-4:])] = (df.loc[valid], int((~valid).sum()))
    tasks = []
    for year in range(2010, 2020):
        previous, _ = seasons[year-1]
        df, excluded = seasons[year]
        catalogue = np.unique(previous[['winner_id','loser_id']].to_numpy(dtype=int))
        lookup = {int(v):i for i,v in enumerate(catalogue)}
        inside = df.winner_id.isin(catalogue) & df.loser_id.isin(catalogue)
        y = np.array([[lookup[int(a)], lookup[int(b)]] for a,b in
                      df.loc[inside, ['winner_id','loser_id']].to_numpy()], dtype=int)
        tasks.append(dict(name=f'atp_{year}', y=y, n=len(catalogue), truth=None,
            family='atp', year=year, catalogue_ids=catalogue.tolist(),
            source_excluded_invalid_or_uncompleted=excluded,
            source_excluded_out_of_prior_catalogue=int((~inside).sum())))
    return tasks


def prediction_comparison(summary):
    saved = pd.read_csv(ROOT/'results/repeated_holdout/scores.csv')
    tennis = pd.read_csv(OUT/'tennis_nll_source.csv')
    rows = []
    for _, feature in summary.loc[summary.reference.eq('full_data')].iterrows():
        name = feature.dataset
        row = feature.to_dict()
        if name.startswith('atp_'):
            g = tennis.loc[tennis.year.eq(int(name[-4:])) & tennis.target.eq('seen')]
            sm = g.loc[g.method.eq('efficient_shrunk')].iloc[0]
            pl = g.loc[g.method.eq('pl')].iloc[0]
            row.update(nll_study='T1', sm_method='bounded_shrunk_efficient', pl_method='ridge',
                nll_target='July-December, both players seen in January-June',
                nll_source=f'{SNAPSHOT}/results/exposure/tennis_by_year.csv',
                sm_nll=sm.nll, pl_nll=pl.nll, delta=sm.delta, paired_repetitions=1,
                planned_repetitions=1, delta_partition_mcse=np.nan,
                conditional_delta=np.nan, delta_status='available_temporal', nll_r=int(sm.r))
        else:
            g = saved.loc[saved.dataset.eq(name) & saved.split.eq('confirmation')]
            sm = g.loc[g.method.eq('mle')].iloc[0]
            pl = g.loc[g.method.eq('pl')].iloc[0]
            complete = int(sm.paired_delta_finite_repeats) == int(sm.repetitions)
            row.update(nll_study='P1', sm_method='exact_certified_mle', pl_method='unpenalized_mm',
                nll_target='mean over 30 original confirmation partitions',
                nll_source='results/repeated_holdout/scores.csv',
                sm_nll=sm.nll_mean, pl_nll=pl.nll_mean,
                delta=sm.paired_delta_mean if complete else np.nan,
                paired_repetitions=int(sm.paired_delta_finite_repeats),
                planned_repetitions=int(sm.repetitions),
                delta_partition_mcse=sm.paired_delta_partition_mcse if complete else np.nan,
                conditional_delta=sm.paired_delta_finite_conditional_mean if not complete else np.nan,
                delta_status='complete' if complete else 'incomplete_not_used_in_association', nll_r=int(sm.r))
        assert int(row['r']) == row['nll_r']
        # Scaling the whole-ranking gap is not a separately computed pair log loss.
        row['delta_per_pair_scale'] = row['delta']/(int(row['r'])*(int(row['r'])-1)/2)
        row['heterogeneity_percentage_points'] = 100*row['heterogeneity_sd']
        row['h1_heterogeneity_percentage_points'] = 100*row['h1_heterogeneity_sd']
        rows.append(row)
    return pd.DataFrame(rows)


def run(refresh=False):
    OUT.mkdir(parents=True, exist_ok=True)
    tasks = [dict(name=t.name, y=t.y, n=t.n, truth=t.truth, family=t.study)
             for t in load_tasks()] + tennis_tasks()
    cache_path = OUT/'centers.json'
    cache = json.loads(cache_path.read_text()) if cache_path.exists() and not refresh else {}
    frequencies, gap_rows, summaries, descriptors = [], [], [], []
    for task in tasks:
        name, y, n = task['name'], task['y'], task['n']
        fingerprint = array_digest(y)
        if name in cache:
            assert cache[name]['reports_sha256'] == fingerprint
            center = np.array(cache[name]['order'], dtype=int)
            info = cache[name]['metadata']
            assert kemeny_cost(pair_counts(y, n), center) == info['objective']
        else:
            print('CENTER', name, 'reports',len(y),'items',n, flush=True)
            center, info = reference_center(y, n)
            cache[name] = dict(order=center.tolist(), metadata=info, reports_sha256=fingerprint)
            cache_path.write_text(json.dumps(cache, indent=2)+'\n')
        print('DESCRIBE', name, info['method'], info['objective'], flush=True)
        references = [('full_data', center, info['method'], info['certified'])]
        if task['truth'] is not None:
            references.append(('objective', np.asarray(task['truth']), 'source_objective_order', False))
        for ref, order, method, certified in references:
            cells = pair_frequencies(y, order)
            gaps, description = summarize_frequencies(cells)
            tag = dict(dataset=name, reference=ref)
            frequencies.append(cells.assign(**tag))
            gap_rows.append(gaps.assign(**tag))
            summaries.append(dict(**tag, reports=len(y), n=n, r=y.shape[1],
                center_method=method, center_certified=certified, **description))
        descriptors.append({k:v for k,v in task.items() if k not in ('y','truth')})
    all_pairs = pd.concat(frequencies, ignore_index=True)
    (OUT/'pairs').mkdir(exist_ok=True)
    pair_files = []
    for dataset, frame in all_pairs.groupby('dataset', sort=True):
        path = f'pairs/{dataset}.csv'
        frame.to_csv(OUT/path, index=False, float_format='%.15g')
        pair_files.append(path)
    for name, frame in [('pair_rates.csv.gz', all_pairs),
                        ('by_gap.csv', pd.concat(gap_rows, ignore_index=True)),
                        ('summary.csv', pd.DataFrame(summaries))]:
        frame.to_csv(OUT/name, index=False, float_format='%.15g',
            compression={'method':'gzip','mtime':0} if name.endswith('.gz') else None)
    comparison = prediction_comparison(pd.DataFrame(summaries))
    comparison.to_csv(OUT/'nll_comparison.csv', index=False, float_format='%.15g')
    sources = source_inventory()
    outputs = ['pair_rates.csv.gz','by_gap.csv','summary.csv','centers.json','nll_comparison.csv'] + pair_files
    manifest = dict(purpose='Full-data descriptive characteristic, not an experiment or model test',
        full_data_tasks=len(tasks), task_descriptors=descriptors,
        source_main_commit='7e7964cc8a001f6c07c79d14e9c9e995ae00eaf8',
        sources=sources, tennis_manifest_sha256=digest(OUT/'tennis_sources.json'),
        nll_input_sha256={p:digest(ROOT/p) for p in ['results/repeated_holdout/scores.csv',
            'data/features/tennis_nll_source.csv']},
        code_sha256={p:digest(ROOT/p) for p in ['describe_pair_features.py','src/pair_features.py']},
        output_sha256={p:digest(OUT/p) for p in outputs},
        weighting='Occurrence-weighted variance across pair frequencies within each exact h; occurrence-weighted across h with at least two pairs',
        full_data_center='Exact DP for n<=18; 120-second certified MILP for n<=100; two-start insertion fallback or n>100',
        limitations=['Data-dependent reference center; descriptive only',
            'Raw frequency dispersion includes sampling variation and mixtures',
            'Unknown identities and correlated reports preclude universal binomial uncertainty',
            'Singleton h strata do not identify cross-pair variation and are not counted as evidence of uniformity'])
    (OUT/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(comparison[['dataset','heterogeneity_percentage_points','count_median',
                      'delta','paired_repetitions']].to_string(index=False), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh-centers', action='store_true')
    run(parser.parse_args().refresh_centers)
