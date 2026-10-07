"""Read-only checks for full-data characteristics 2 and 3."""
import argparse
from collections import Counter
from itertools import combinations
import json
import numpy as np
import pandas as pd

from describe_pair_features import ROOT,OUT as PAIR_OUT,digest,tennis_tasks,array_digest
from describe_structure_features import OUT,PRIVATE


def verify(sources=False):
    manifest=json.loads((OUT/'manifest.json').read_text())
    for group in ['inputs','code_sha256']:
        for path,expected in manifest[group].items():
            assert digest(ROOT/path)==expected,path
    for path,expected in manifest['output_sha256'].items():
        assert digest(OUT/path)==expected,path
    summary=pd.read_csv(OUT/'summary.csv')
    joined=pd.read_csv(OUT/'nll_comparison.csv')
    previous=pd.read_csv(PAIR_OUT/'nll_comparison.csv').set_index('dataset')
    assert len(summary)==51 and len(joined)==33
    for row in joined.itertuples():
        for field in ['delta','conditional_delta','paired_repetitions','delta_partition_mcse']:
            np.testing.assert_allclose(getattr(row,field),previous.loc[row.dataset,field],equal_nan=True)
    for name,group in summary.groupby('dataset'):
        shells=pd.read_csv(OUT/'shells'/(name+'.csv'))
        pairs=pd.read_csv(OUT/'pairs'/(name+'.csv'))
        for row in group.itertuples():
            sh=shells.loc[shells.reference.eq(row.reference)]
            pa=pairs.loc[pairs.reference.eq(row.reference)]
            assert sh.reports.sum()==row.reports
            assert pa.pair_occurrences.sum()==row.reports*row.r*(row.r-1)//2
            assert (sh.observed_rankings+sh.zero_count_rankings).eq(sh.possible_rankings).all()
            assert sh.reports.ge(sh.observed_rankings).all()
            assert sh[['display_id','d']].duplicated().sum()==0
            supported=sh.loc[sh.possible_rankings.gt(1)]
            for field,column in [('shell_tv','frequency_tv'),('shell_iid_uniform_expected_tv','iid_uniform_expected_tv'),
                                 ('shell_excess_tv','excess_tv_over_iid_uniform')]:
                expected=np.average(supported[column],weights=supported.reports) if len(supported) else np.nan
                np.testing.assert_allclose(getattr(row,field),expected,equal_nan=True,atol=1e-14)
            eligible=pa.loc[pa.contexts.ge(2)]
            count=eligible.pair_occurrences.sum()
            for field,column in [('context_display_sd','sse_display'),('context_gap_component_sd','sse_gap'),
                                 ('context_same_gap_component_sd','sse_same_gap')]:
                expected=np.sqrt(eligible[column].sum()/count) if count else np.nan
                np.testing.assert_allclose(getattr(row,field),expected,equal_nan=True,atol=1e-14)
            den=pa.gap_slope_denominator.sum()
            expected=pa.gap_slope_numerator.sum()/den if den else np.nan
            np.testing.assert_allclose(row.context_gap_slope,expected,equal_nan=True,atol=1e-14)
            if row.r==2:
                assert np.isnan(row.shell_tv) and np.isnan(row.context_display_sd)
    if sources:
        from src.repeated_holdout import load_tasks
        centers=json.loads((PAIR_OUT/'centers.json').read_text())
        tasks=[dict(name=t.name,y=t.y,truth=t.truth) for t in load_tasks()]+tennis_tasks()
        for path,expected in manifest['private_output_sha256'].items():
            assert digest(ROOT/path)==expected,path
        for task in tasks:
            name,y=task['name'],task['y']
            assert array_digest(y)==centers[name]['reports_sha256']
            refs=[('full_data',centers[name]['order'])]
            if task['truth'] is not None:
                refs.append(('objective',task['truth']))
            for ref,order in refs:
                folder=PRIVATE/name
                displays=pd.read_csv(folder/f'{ref}_displays.csv.gz')
                ranks=pd.read_csv(folder/f'{ref}_rankings.csv.gz')
                context=pd.read_csv(folder/f'{ref}_context_cells.csv.gz')
                swaps=pd.read_csv(folder/f'{ref}_swaps.csv.gz')
                sid={tuple(json.loads(row.items)):row.display_id for row in displays.itertuples()}
                pos={int(item):i for i,item in enumerate(order)}
                ranks_expected=Counter(tuple(map(int,row)) for row in y)
                ranks_actual={tuple(json.loads(row.ranking)):row.count for row in ranks.itertuples()}
                assert ranks_expected==ranks_actual
                counts,wins=Counter(),Counter()
                for report in y:
                    report=list(map(int,report)); shown=sorted(report,key=pos.get)
                    display=sid[tuple(sorted(report))]
                    for i,j in combinations(shown,2):
                        h=shown.index(j)-shown.index(i);key=(display,i,j,h)
                        counts[key]+=1;wins[key]+=int(report.index(i)<report.index(j))
                assert len(counts)==len(context)
                for row in context.itertuples():
                    key=(row.display_id,row.item_i,row.item_j,row.h)
                    assert row.count==counts[key] and row.wins==wins[key]
                shells=pd.read_csv(OUT/'shells'/(name+'.csv')).query('reference == @ref')
                for row in shells.itertuples():
                    g=ranks.loc[ranks.display_id.eq(row.display_id)&ranks.d.eq(row.d)]
                    expected=sum(abs(float(c/row.reports)-1/row.possible_rankings) for c in g['count'])
                    expected=.5*(expected+row.zero_count_rankings/row.possible_rankings)
                    if row.possible_rankings>1:
                        np.testing.assert_allclose(row.frequency_tv,expected,atol=1e-14)
                    for rrow in g.itertuples():
                        rank=json.loads(rrow.ranking)
                        assert sum(pos[i]>pos[j] for i,j in combinations(rank,2))==row.d
                lookup={row.display_id:set(json.loads(row.items)) for row in displays.itertuples()}
                assert not swaps[['display_1','display_2','item_i','item_j']].duplicated().any()
                for edge in swaps.itertuples():
                    a,b=lookup[edge.display_1],lookup[edge.display_2]
                    assert len(a^b)==2 and {edge.item_i,edge.item_j}<=a&b
                    for k in [1,2]:
                        key=(getattr(edge,f'display_{k}'),edge.item_i,edge.item_j,getattr(edge,f'h{k}'))
                        assert getattr(edge,f'count{k}')==counts[key]
                        np.testing.assert_allclose(getattr(edge,f'rate{k}'),wins[key]/counts[key])
                changed=swaps.loc[swaps.h_change.ne(0)]
                s=summary.loc[summary.dataset.eq(name)&summary.reference.eq(ref)].iloc[0]
                expected=np.average(changed.higher_h_minus_lower_h,weights=changed.weight) if len(changed) else np.nan
                np.testing.assert_allclose(s.swap_gap_effect,expected,equal_nan=True,atol=1e-14)
    print('Verified all 33 task summaries, 51 references, structural availability and unchanged NLL join.'
          + (' Independent complete-source frequency replay passed.' if sources else ''))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sources',action='store_true')
    verify(parser.parse_args().sources)
