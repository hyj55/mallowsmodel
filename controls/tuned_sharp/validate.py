"""Validate the saved supplement; --replay also reads original source data."""
import argparse
import gzip
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import numpy as np
import pandas as pd

from controls.tuned_sharp.run import (PUBLIC, signature, digest, selected_sources,
    case_id, get_context, paired_interval, seed_for)
from controls.tuned_sharp.model import block_grid, validation_order, pilot_order
from src.repeated_holdout import load_tasks, restore_fit
from src.manuscript_estimators import extract_pairs
from src.models import pair_counts, kemeny_cost, kendall


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--replay',action='store_true')
    args=parser.parse_args()
    manifest=json.loads((PUBLIC/'manifest.json').read_text())
    assert manifest['code_sha256']==signature()
    for path,sha in manifest['inputs'].items(): assert digest(ROOT/path)==sha,path
    for path,sha in manifest['outputs'].items(): assert digest(PUBLIC/path)==sha,path
    with gzip.open(PUBLIC/'models.jsonl.gz','rt') as stream:
        records=[json.loads(line) for line in stream]
    sources={case_id(r):r for r in selected_sources()}
    assert len(records)==manifest['records']==19
    assert {r['case'] for r in records}==set(sources)
    tasks={t.name:t for t in load_tasks()} if args.replay else None
    scores=pd.read_csv(PUBLIC/'scores.csv')
    candidates=pd.read_csv(PUBLIC/'candidates.csv')
    comparisons=pd.read_csv(PUBLIC/'comparisons.csv')
    old_scores=pd.read_csv(ROOT/'results/predictive/repeat_scores.csv.gz')
    for record in records:
        name=record['case']; source=sources[name]
        assert record['repeat']==0 and record['grid']==block_grid(record['n'])
        assert record['data_sha256']==source['data_sha256']
        assert record['code_sha256']==signature()
        ranked=validation_order(record['candidates'])
        assert [r['blocks'] for r in record['refits']]==[r['blocks'] for r in ranked[:len(record['refits'])]]
        assert all(r['status']!='ok' for r in record['refits'][:-1])
        if record['status']=='ok':
            assert record['refits'][-1]['status']=='ok'
            assert record['selected_blocks']==record['refits'][-1]['blocks']
            assert record['models']['borda_block_sieve']==record['refits'][-1]['model']
        for method in ('pl','sm_likelihood','sm_fotakis','sm_efficient_fallback'):
            assert record['models'][method]==source['models'][method]
        for candidate in record['candidates']:
            row=candidates[(candidates['case']==name)&(candidates.blocks==candidate['blocks'])].iloc[0]
            assert row.status==candidate['status']
            if candidate['status']=='ok':
                np.testing.assert_allclose(row.validation_nll,candidate['validation_nll'],atol=1e-9)
        for row in record['scores']:
            saved=scores[(scores['case']==name)&(scores.method==row['method'])].iloc[0]
            assert saved.status==row['status']
            if row['status']=='ok':
                np.testing.assert_allclose(saved.nll,row['nll'],atol=1e-9)
                if row['method'].startswith('sm_') or row['method']=='pl':
                    old=old_scores[(old_scores.study==source['study']) &
                        (old_scores.dataset==source['dataset']) & (old_scores.n==source['n']) &
                        (old_scores.N==source['N']) & (old_scores['repeat']==0) &
                        (old_scores.method==row['method'])].iloc[0]
                    np.testing.assert_allclose(old.nll,row['nll'],atol=1e-9)
        for row in record['comparisons']:
            saved=comparisons[(comparisons['case']==name)&(comparisons.reference==row['reference'])].iloc[0]
            np.testing.assert_allclose(saved.delta,row['delta'],atol=1e-9)
        if not args.replay: continue
        context,units=get_context(source,tasks);d=context['data']; n=record['n']
        for stage,pool,seed in [('candidates','inner',record['seed_train']),
                                ('refits','development',record['seed_final'])]:
            pilot,pi,si=pilot_order(d[pool],n,units[pool],seed)
            assert not set(units[pool][pi])&set(units[pool][si])
            for item in record[stage]:
                if item['status']!='ok': continue
                fit=restore_fit(item['model']); meta=fit.metadata
                np.testing.assert_array_equal(meta['pilot_order'],pilot)
                expected=[]
                for index,labels in enumerate(np.array_split(pilot,item['blocks'])):
                    detail=meta['blocks'][index]
                    np.testing.assert_array_equal(detail['labels'],labels)
                    rng=np.random.default_rng(np.random.SeedSequence([seed,item['blocks'],index,173]))
                    pairs=extract_pairs(d[pool][si],labels,rng)
                    assert detail['pairs']==len(pairs)
                    assert detail['integer_radius']==(len(labels)*(len(labels)*(len(labels)-1)//2)//len(pairs)
                                                       if len(pairs) else None)
                    assert sorted(detail['order'])==sorted(labels)
                    if 'objective' in detail['solver']:
                        canonical=sorted(labels);lookup={v:i for i,v in enumerate(canonical)}
                        local=np.asarray([[lookup[a],lookup[b]] for a,b in pairs],int).reshape(-1,2)
                        w=pair_counts(local,len(labels))
                        assert kemeny_cost(w,[lookup[v] for v in detail['order']])==detail['solver']['objective']
                    expected.extend(detail['order'])
                np.testing.assert_array_equal(fit.order,expected)
                if stage=='candidates':
                    np.testing.assert_allclose(fit.nll(d['validation']).mean(),item['validation_nll'],atol=1e-10)
        loss={m:restore_fit(f).nll(d['test']) for m,f in record['models'].items() if f['status']=='ok'}
        for row in record['scores']:
            if row['status']=='ok':
                np.testing.assert_allclose(loss[row['method']].mean(),row['nll'],atol=1e-10)
                if context['truth'] is not None:
                    assert kendall(record['models'][row['method']]['order'],context['truth'])==row['kendall']
        for row in record['comparisons']:
            np.testing.assert_allclose((loss['borda_block_sieve']-loss[row['reference']]).mean(),row['delta'],atol=1e-10)
            if row['ci_low'] is not None:
                ci=paired_interval(loss['borda_block_sieve'],loss[row['reference']],units['test'],seed_for(context,2))
                np.testing.assert_allclose(ci,[row['ci_low'],row['ci_high']],atol=1e-10)
        print('REPLAY',name,flush=True)
    print('PASS',len(records),'cases; source splits, selection, saved comparators, scores and intervals verified')


if __name__=='__main__':main()
