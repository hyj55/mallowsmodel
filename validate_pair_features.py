"""Read-only verification of full-data descriptive tables and reused NLLs."""
import argparse
from collections import Counter
import json

import numpy as np
import pandas as pd

from describe_pair_features import ROOT, OUT, digest, array_digest, tennis_tasks


def verify(with_sources=False):
    manifest = json.loads((OUT/'manifest.json').read_text())
    for group in ['code_sha256','nll_input_sha256']:
        for path, expected in manifest[group].items():
            assert digest(ROOT/path) == expected, path
    for path, expected in manifest['output_sha256'].items():
        assert digest(OUT/path) == expected, path
    assert digest(OUT/'tennis_sources.json') == manifest['tennis_manifest_sha256']
    pairs = pd.read_csv(OUT/'pair_rates.csv.gz')
    gaps = pd.read_csv(OUT/'by_gap.csv')
    summary = pd.read_csv(OUT/'summary.csv')
    centers = json.loads((OUT/'centers.json').read_text())
    assert pairs.groupby(['dataset','reference','h','item_i','item_j']).size().eq(1).all()
    assert (pairs.wins+pairs.losses).eq(pairs['count']).all()
    assert pairs['count'].ge(1).all()
    np.testing.assert_allclose(pairs.win_rate, pairs.wins/pairs['count'])
    for (dataset, ref), s in pairs.groupby(['dataset','reference']):
        row = summary.loc[summary.dataset.eq(dataset) & summary.reference.eq(ref)].iloc[0]
        assert s['count'].sum() == row.reports*row.r*(row.r-1)/2
        order = centers[dataset]['order'] if ref == 'full_data' else list(range(int(row.n)))
        pos = {item:i for i,item in enumerate(order)}
        assert all(pos[i] < pos[j] for i,j in zip(s.item_i, s.item_j))
        numerator, denominator = 0., 0
        for h,g in s.groupby('h'):
            actual = gaps.loc[gaps.dataset.eq(dataset) & gaps.reference.eq(ref) & gaps.h.eq(h)].iloc[0]
            assert len(g) == actual.pairs and g['count'].sum() == actual.pair_occurrences
            mean = g.wins.sum()/g['count'].sum()
            np.testing.assert_allclose(mean, actual.mean_win_rate)
            if len(g) < 2:
                assert np.isnan(actual.heterogeneity_sd)
                continue
            sse = sum(m*(w/m-mean)**2 for w,m in zip(g.wins, g['count']))
            np.testing.assert_allclose(np.sqrt(sse/g['count'].sum()), actual.heterogeneity_sd, atol=1e-14)
            numerator += sse
            denominator += int(g['count'].sum())
        np.testing.assert_allclose(np.sqrt(numerator/denominator), row.heterogeneity_sd, atol=1e-14)
    joined = pd.read_csv(OUT/'nll_comparison.csv')
    combined = pd.read_csv(OUT/'all_features.csv').set_index('dataset')
    assert len(combined) == 33 and combined.index.is_unique
    for source in [joined, pd.read_csv(OUT/'structure/nll_comparison.csv')]:
        indexed = source.set_index('dataset')
        pd.testing.assert_frame_equal(combined[indexed.columns].sort_index(), indexed.sort_index())
    saved = pd.read_csv(ROOT/'results/repeated_holdout/scores.csv')
    temporal = pd.read_csv(OUT/'tennis_nll_source.csv')
    assert len(joined) == len(centers) == 33
    for _, row in joined.iterrows():
        if row.nll_study == 'P1':
            original = saved.loc[saved.dataset.eq(row.dataset) & saved.method.eq('mle')
                                 & saved.split.eq('confirmation')].iloc[0]
            assert row.paired_repetitions == original.paired_delta_finite_repeats
            if row.paired_repetitions < 30:
                assert np.isnan(row.delta)
                np.testing.assert_allclose(row.conditional_delta, original.paired_delta_finite_conditional_mean)
            else:
                np.testing.assert_allclose(row.delta, original.paired_delta_mean)
        else:
            original = temporal.loc[temporal.year.eq(int(row.dataset[-4:])) & temporal.target.eq('seen')
                                    & temporal.method.eq('efficient_shrunk')].iloc[0]
            np.testing.assert_allclose(row.delta, original.delta)
    if with_sources:
        from src.repeated_holdout import load_tasks
        tasks = [dict(name=t.name, y=t.y, truth=t.truth) for t in load_tasks()] + tennis_tasks()
        for task in tasks:
            assert array_digest(task['y']) == centers[task['name']]['reports_sha256']
            references = [('full_data', centers[task['name']]['order'])]
            if task['truth'] is not None:
                references.append(('objective', task['truth']))
            for ref, order in references:
                position = {int(item):i for i,item in enumerate(order)}
                counts, wins = Counter(), Counter()
                for report in task['y']:
                    report = list(map(int, report))
                    display = sorted(report, key=position.get)
                    for a,i in enumerate(display):
                        for b in range(a+1,len(display)):
                            j=display[b]; key=(b-a,i,j)
                            counts[key] += 1
                            wins[key] += int(report.index(i) < report.index(j))
                got=pairs.loc[pairs.dataset.eq(task['name']) & pairs.reference.eq(ref)]
                assert len(counts)==len(got)
                for row in got.itertuples():
                    key=(row.h,row.item_i,row.item_j)
                    assert counts[key]==row.count and wins[key]==row.wins
    print('Verified 33 full-data tasks, equal-h counts and summaries, and unchanged recorded NLLs.'
          + (' Independent source replay passed.' if with_sources else ''))


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sources', action='store_true')
    verify(parser.parse_args().sources)
