"""Full-task empirical shell frequencies and exact-display pair frequencies.

No model fits, train/test allocations, bootstrap draws, or significance tests.
Detailed ranking/context tables are returned for local source replay only.
"""
from collections import Counter, defaultdict
from itertools import combinations
import json
import numpy as np
import pandas as pd
from scipy.stats import binom

from .models import validate_rankings
from .diagnostics import shell_counts


def nominal_uniform_tv(m, a):
    """Exact E[empirical TV] for m iid uniform draws from a fixed a-cell shell.

    A sampling-scale reference, not a calibrated test for estimated centers,
    dependent reports, or unknown assessor mixtures.
    """
    if m < 1 or a < 2:
        return np.nan
    return float((1-1/a)*binom.pmf(m//a, m-1, 1/a))


def empirical_tables(y, order):
    order = np.asarray(order, dtype=int)
    if sorted(order.tolist()) != list(range(len(order))):
        raise ValueError('Reference must be a full catalogue permutation')
    y = validate_rankings(y, len(order))
    position = np.argsort(order)
    displays = sorted({tuple(sorted(map(int,row))) for row in y})
    display_id = {s:i for i,s in enumerate(displays)}
    display_counts, ranking_counts = Counter(), Counter()
    context = defaultdict(lambda: [0,0,0])
    for row in y:
        ranking = tuple(map(int,row))
        sid = display_id[tuple(sorted(ranking))]
        center_display = sorted(ranking, key=lambda i:position[i])
        observed_position = {item:i for i,item in enumerate(ranking)}
        d = sum(observed_position[i] > observed_position[j]
                for i,j in combinations(center_display,2))
        display_counts[sid] += 1
        ranking_counts[(sid,d,ranking)] += 1
        for a,b in combinations(range(len(ranking)),2):
            i,j = center_display[a],center_display[b]
            record = context[(sid,i,j)]
            record[0] += int(observed_position[i] < observed_position[j])
            record[1] += 1
            record[2] = b-a
    ranking = pd.DataFrame([dict(display_id=sid,d=d,ranking=json.dumps(rank,separators=(',',':')),
        count=count,display_reports=display_counts[sid])
        for (sid,d,rank),count in sorted(ranking_counts.items())])
    cells = pd.DataFrame([dict(display_id=sid,item_i=i,item_j=j,h=h,wins=w,count=m,win_rate=w/m)
        for (sid,i,j),(w,m,h) in sorted(context.items())])
    display = pd.DataFrame([dict(display_id=i,items=json.dumps(s,separators=(',',':')),
        reports=display_counts[i]) for i,s in enumerate(displays)])
    assert ranking['count'].sum() == len(y)
    assert cells['count'].sum() == len(y)*y.shape[1]*(y.shape[1]-1)//2
    return display,ranking,cells


def shell_features(ranking, r):
    sizes = shell_counts(r)
    shells = []
    for (sid,d),g in ranking.groupby(['display_id','d'],sort=True):
        m,a = int(g['count'].sum()),int(sizes[d])
        p = g['count'].to_numpy()/m
        tv = float(.5*(np.abs(p-1/a).sum()+(a-len(g))/a)) if a>1 else np.nan
        expected = nominal_uniform_tv(m,a)
        shells.append(dict(display_id=int(sid),d=int(d),reports=m,
            display_reports=int(g.display_reports.iloc[0]),possible_rankings=a,
            observed_rankings=len(g),zero_count_rankings=a-len(g),
            uniform_expected_count=m/a,comparable=a>1,frequency_tv=tv,
            iid_uniform_expected_tv=expected,
            excess_tv_over_iid_uniform=tv-expected,
            status=('singleton_shell_no_constraint' if a==1 else
                    'one_observation_only' if m==1 else 'repeated_shell')))
    shells = pd.DataFrame(shells)
    supported = shells.loc[shells.comparable]
    m = int(supported.reports.sum())
    summary = dict(shell_status='available_descriptive' if m else 'no_nontrivial_shell',
        shell_occupied_cells=len(shells),shell_nontrivial_cells=len(supported),
        shell_comparable_reports=m,shell_comparable_report_share=m/ranking['count'].sum(),
        shell_count_median=float(supported.reports.median()) if m else np.nan,
        shell_occurrence_share_count_ge2=float(supported.loc[supported.reports.ge(2),'reports'].sum()/m) if m else np.nan,
        shell_occurrence_share_count_ge5=float(supported.loc[supported.reports.ge(5),'reports'].sum()/m) if m else np.nan,
        shell_expected_count_median=float(supported.uniform_expected_count.median()) if m else np.nan)
    for name,column in [('shell_tv','frequency_tv'),('shell_iid_uniform_expected_tv','iid_uniform_expected_tv'),
                        ('shell_excess_tv','excess_tv_over_iid_uniform')]:
        summary[name]=float(np.average(supported[column],weights=supported.reports)) if m else np.nan
    totals = shells.set_index(['display_id','d']).reports
    ranking = ranking.copy()
    ranking['shell_reports']=[int(totals.loc[s,d]) for s,d in zip(ranking.display_id,ranking.d)]
    ranking['frequency_within_display']=ranking['count']/ranking.display_reports
    ranking['frequency_within_shell']=ranking['count']/ranking.shell_reports
    return shells,ranking,summary


def context_features(cells):
    pairs = []
    for (i,j),g in cells.groupby(['item_i','item_j'],sort=True):
        m = int(g['count'].sum()); mean = float(g.wins.sum()/m)
        by_h = g.groupby('h',sort=True)[['wins','count']].sum()
        by_h['win_rate']=by_h.wins/by_h['count']
        mean_h = float(np.average(by_h.index,weights=by_h['count']))
        sse_display = float(np.sum(g['count']*(g.win_rate-mean)**2))
        sse_gap = float(np.sum(by_h['count']*(by_h.win_rate-mean)**2))
        sse_same_gap = float(sum(np.sum(z['count']*(z.win_rate-z.wins.sum()/z['count'].sum())**2)
                                  for _,z in g.groupby('h')))
        assert np.isclose(sse_display,sse_gap+sse_same_gap,atol=1e-9)
        den = float(np.sum(by_h['count']*(by_h.index-mean_h)**2))
        num = float(np.sum(by_h['count']*(by_h.index-mean_h)*(by_h.win_rate-mean)))
        lo,hi = by_h.iloc[0],by_h.iloc[-1]
        pairs.append(dict(item_i=int(i),item_j=int(j),contexts=len(g),gaps=len(by_h),
            pair_occurrences=m,mean_win_rate=mean,context_count_min=int(g['count'].min()),
            context_count_median=float(g['count'].median()),context_count_max=int(g['count'].max()),
            repeated_context_occurrences=int(g.loc[g['count'].ge(2),'count'].sum()),
            sse_display=sse_display,sse_gap=sse_gap,sse_same_gap=sse_same_gap,
            display_sd=np.sqrt(sse_display/m) if len(g)>=2 else np.nan,
            gap_slope=num/den if den>0 else np.nan,gap_slope_numerator=num,gap_slope_denominator=den,
            h_low=int(by_h.index[0]),h_high=int(by_h.index[-1]),
            low_h_count=int(lo['count']),high_h_count=int(hi['count']),
            low_h_win_rate=lo.win_rate,high_h_win_rate=hi.win_rate,
            high_minus_low_rate=float(hi.win_rate-lo.win_rate) if len(by_h)>=2 else np.nan,
            status='one_display_only' if len(g)<2 else 'changing_h' if len(by_h)>1 else 'same_h_across_displays'))
    pairs = pd.DataFrame(pairs)
    eligible=pairs.loc[pairs.contexts.ge(2)]
    changing=pairs.loc[pairs.gaps.ge(2)]
    m=int(eligible.pair_occurrences.sum()); den=float(changing.gap_slope_denominator.sum())
    summary=dict(context_status='available_descriptive' if m else 'no_pair_in_multiple_displays',
        context_pairs=len(eligible),context_pair_occurrences=m,
        context_occurrence_share=m/cells['count'].sum(),
        context_changing_h_pairs=len(changing),context_changing_h_occurrences=int(changing.pair_occurrences.sum()),
        context_gap_status='available_descriptive' if den else 'no_within_pair_h_variation',
        context_gap_slope=float(changing.gap_slope_numerator.sum()/den) if den else np.nan,
        context_occurrence_share_repeated_display=float(eligible.repeated_context_occurrences.sum()/m) if m else np.nan,
        context_cell_count_median=float(cells['count'].median()))
    for name,column in [('context_display_sd','sse_display'),('context_gap_component_sd','sse_gap'),
                        ('context_same_gap_component_sd','sse_same_gap')]:
        summary[name]=float(np.sqrt(eligible[column].sum()/m)) if m else np.nan
    return pairs,summary


SWAP_COLUMNS=['display_1','display_2','item_i','item_j','removed_item','added_item','h1','h2',
              'count1','count2','rate1','rate2','h_change','rate_change','weight',
              'higher_h_minus_lower_h','both_displays_repeated']


def replacement_features(displays,cells,order):
    """Change exactly one nonfocal displayed item, holding the rest fixed."""
    position=np.argsort(order)
    sets={int(row.display_id):tuple(json.loads(row.items)) for row in displays.itertuples()}
    cores=defaultdict(list)
    for sid,s in sets.items():
        if len(s)<3:
            continue
        for removed in s:
            cores[tuple(x for x in s if x!=removed)].append((sid,removed))
    lookup={(int(row.display_id),int(row.item_i),int(row.item_j)):row for row in cells.itertuples()}
    records=[]
    for core,members in sorted(cores.items()):
        if len(members)<2:
            continue
        for (s1,removed),(s2,added) in combinations(sorted(members),2):
            for i,j in combinations(sorted(core,key=lambda i:position[i]),2):
                a,b=lookup[(s1,i,j)],lookup[(s2,i,j)]
                dh=b.h-a.h; dp=b.win_rate-a.win_rate
                assert dh in (-1,0,1)
                records.append(dict(display_1=s1,display_2=s2,item_i=i,item_j=j,
                    removed_item=removed,added_item=added,h1=a.h,h2=b.h,count1=a.count,count2=b.count,
                    rate1=a.win_rate,rate2=b.win_rate,h_change=dh,rate_change=dp,
                    weight=a.count*b.count/(a.count+b.count),
                    higher_h_minus_lower_h=dp*dh if dh else np.nan,
                    both_displays_repeated=a.count>=2 and b.count>=2))
    swaps=pd.DataFrame(records,columns=SWAP_COLUMNS)
    changing=swaps.loc[swaps.h_change.ne(0)]
    repeated=changing.loc[changing.both_displays_repeated.eq(True)]
    same=swaps.loc[swaps.h_change.eq(0)]
    summary=dict(swap_edges=len(swaps),swap_gap_edges=len(changing),swap_same_h_edges=len(same),
        swap_gap_pairs=len(changing[['item_i','item_j']].drop_duplicates()),
        swap_gap_edges_both_repeated=len(repeated),
        swap_status='available_descriptive' if len(changing) else 'no_single_replacement_h_contrast',
        swap_gap_effect=float(np.average(changing.higher_h_minus_lower_h,weights=changing.weight)) if len(changing) else np.nan,
        swap_gap_effect_both_repeated=float(np.average(repeated.higher_h_minus_lower_h,weights=repeated.weight)) if len(repeated) else np.nan,
        swap_positive_fraction=float(changing.higher_h_minus_lower_h.gt(0).mean()) if len(changing) else np.nan,
        swap_negative_fraction=float(changing.higher_h_minus_lower_h.lt(0).mean()) if len(changing) else np.nan,
        swap_same_h_absolute_change=float(np.average(same.rate_change.abs(),weights=same.weight)) if len(same) else np.nan)
    return swaps,summary


def describe_structure(y,order):
    display,ranking,cells=empirical_tables(y,order)
    shells,ranking,shell_summary=shell_features(ranking,y.shape[1])
    pairs,context_summary=context_features(cells)
    swaps,swap_summary=replacement_features(display,cells,order)
    summary=dict(reports=len(y),n=len(order),r=y.shape[1],displays=len(display),
        display_count_median=float(display.reports.median()),
        display_reports_in_repeated_sets=int(display.loc[display.reports.ge(2),'reports'].sum()),
        **shell_summary,**context_summary,**swap_summary)
    return dict(summary=summary,displays=display,rankings=ranking,shells=shells,
                context_cells=cells,pairs=pairs,swaps=swaps)
