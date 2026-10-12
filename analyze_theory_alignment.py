"""Relate saved estimator results to manuscript regimes; never fit a model."""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'results/theory_alignment'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dimensions(n, r, N, beta=None):
    lam = N*r*(r-1)/(n*(n-1))
    mu, nu = N*r/n, n*lam
    v = np.inf if r == n else -N*np.log1p(-r/n)
    return dict(n=n, r=r, N=N, lambda_=lam, mu=mu, nu=nu,
        coverage_ratio=mu/np.log(np.e*r), Vcov=v, Q=n/lam,
        Bcov=n*n*np.exp(-v), lambda_le_one=lam<=1+1e-12,
        nu_le_one=nu<=1+1e-12, full_ranking=r==n, one_report=N==1,
        coverage_dominated=nu>=1 and v<=.5*np.log(nu),
        full_rank_shape=(n/np.sqrt(N+1)*np.cosh(beta/2)**(-N)
                         if r==n and beta is not None else np.nan))


def finite_mean(values, require_all=True):
    values=np.asarray(values,float)
    finite=values[np.isfinite(values)]
    return float(finite.mean()) if len(finite) and (not require_all or len(finite)==len(values)) else np.nan


def summarize():
    source=json.loads((OUT/'sources.json').read_text())
    for entry in source['saved_inputs']:
        assert digest(ROOT/entry['destination']) == entry['sha256'], entry['destination']
    p1=pd.read_csv(ROOT/'results/repeated_holdout/repeat_scores.csv.gz').query('split == "confirmation"')
    assert len(p1)==23*30*5
    exposure=[]; methods=[]; contrasts=[]
    for name,group in p1.groupby('dataset',sort=True):
        base=group.loc[group.method.eq('mle')]
        first=base.iloc[0]
        for col in ['n','r','n_train']:
            assert base[col].nunique()==1
        row=dict(dataset=name,**dimensions(int(first.n),int(first.r),int(first.n_train)),
            pair_min_across_partitions=int(base.min_pair_count.min()),
            max_unseen_items=int(base.unseen_items.max()),
            all_pairs_observed_every_partition=bool(base.min_pair_count.gt(0).all()),
            model_and_sampling_assumptions='not established for empirical data')
        exposure.append(row)
        for method,g in group.groupby('method'):
            methods.append(dict(dataset=name,method=method,partitions=len(g),
                successful_fits=int(g.status.eq('ok').sum()),
                status_counts=json.dumps(g.status.value_counts().to_dict(),sort_keys=True),
                branch_counts=json.dumps(g.branch.value_counts().to_dict(),sort_keys=True),
                maximum_recorded_depth=g.depth.max(),finite_nll_partitions=int(np.isfinite(g.nll).sum()),
                nll_mean=finite_mean(g.nll),finite_conditional_nll=finite_mean(g.nll,False),
                objective_reference_kendall=finite_mean(g.objective_kendall)))
        wide=group.pivot(index='repeat',columns='method',values='nll')
        for a,b in [('borda','mle'),('sharp','mle'),('efficient','borda')]:
            difference=wide[a]-wide[b]
            finite=np.isfinite(difference)
            contrasts.append(dict(dataset=name,method_a=a,method_b=b,partitions=len(wide),
                finite_paired_partitions=int(finite.sum()),mean_nll_difference=finite_mean(difference),
                finite_conditional_nll_difference=finite_mean(difference,False),
                equal_nll_partitions=int((finite&difference.abs().le(1e-12)).sum())))
    result={'p1_regimes':pd.DataFrame(exposure),'p1_methods':pd.DataFrame(methods),
            'p1_estimator_contrasts':pd.DataFrame(contrasts)}

    synthetic=[]
    for part in ['bridge','shell','coverage']:
        data=pd.read_csv(ROOT/f'results/strict_features/{part}_summary.csv')
        for row in data.loc[data.value.eq(0)].itertuples():
            synthetic.append(dict(component='S1_S2',part=part,shape=row.shape,method=row.method,
                **dimensions(row.n,row.r,row.N,.8),risk=row.risk,risk_lo=row.risk_lo,risk_hi=row.risk_hi,
                repetitions=row.repetitions,successful_fits=row.ok,
                status_counts=row.statuses,nll=row.nll,
                algorithm_scope=('outside schedule domain' if row.method=='efficient' and row.lambda_>1
                    else 'depth-zero global scores' if row.method in ['borda','efficient']
                    else 'global one-pair-per-report sieve' if row.method=='sharp'
                    else 'likelihood benchmark'),source=f'results/strict_features/{part}_summary.csv'))
    for part in ['small','coverage']:
        path=f'results/theory_alignment/inputs/s3_{part}_summary.csv'
        data=pd.read_csv(ROOT/path)
        for row in data.loc[data.dgp.eq('SM')].itertuples():
            synthetic.append(dict(component='S3',part=part,shape='SM',method=row.method,
                **dimensions(row.n,row.r,row.N,.8),risk=row.risk,risk_lo=row.risk_lo,risk_hi=row.risk_hi,
                repetitions=row.repetitions,successful_fits=row.repetitions,status_counts='saved finite fits',
                nll=row.nll,algorithm_scope=('depth-zero global scores; capped-resolution extension if lambda>1'
                    if row.method=='efficient' else 'global one-pair-per-report sieve' if row.method=='sharp'
                    else 'bounded/regularized likelihood benchmark'),source=path))
    result['pure_sm_results']=pd.DataFrame(synthetic)

    g1=pd.read_csv(ROOT/'results/group_sensitivity/repeat_scores.csv.gz')
    wide=g1.pivot(index=['dataset','design','percent','scheme','repeat'],columns='method',values='nll_all')
    rows=[]
    for key,g in wide.groupby(level=['dataset','design','percent','scheme']):
        diff=g.sm_fotakis-g.sm_mle;ok=np.isfinite(diff)
        rows.append(dict(zip(['dataset','design','percent','scheme'],key),repetitions=len(g),
            complete_finite_pairs=int(ok.sum()),fotakis_minus_exact=finite_mean(diff),
            finite_conditional_difference=finite_mean(diff,False),
            identical_nll_repetitions=int((ok&diff.abs().le(1e-12)).sum()),
            max_absolute_difference=float(diff.loc[ok].abs().max()) if ok.any() else np.nan))
    result['g1_fotakis_vs_exact']=pd.DataFrame(rows)
    c1=pd.read_csv(OUT/'inputs/c1_synthetic_algorithms.csv').query('dgp == "SM"')
    rows=[]
    for (N,method),g in c1.groupby(['N','algorithm']):
        rows.append(dict(method=method,**dimensions(10,3,int(N),.8),
            repetitions=len(g),risk=finite_mean(g.central_kendall),
            mean_training_objective_gap=finite_mean(g.objective_gap),
            max_training_objective_gap=g.objective_gap.max(),
            zero_objective_gap_repetitions=int(g.objective_gap.eq(0).sum())))
    result['c1_sm_centers']=pd.DataFrame(rows)
    return result


def display_table(frame,columns,rename=None):
    frame=frame[columns].rename(columns=rename or {})
    def f(x):
        if isinstance(x,(float,np.floating)):
            if np.isnan(x):return 'NA'
            if np.isinf(x):return '∞'
            return f'{x:.5g}'
        return str(x)
    return '\n'.join(['| '+' | '.join(frame.columns)+' |','|'+'|'.join(['---']*len(frame.columns))+'|']+
                     ['| '+' | '.join(f(x) for x in row)+' |' for row in frame.itertuples(index=False,name=None)])


def render_tables(tables):
    p=tables['p1_regimes'];s=tables['pure_sm_results'];g=tables['g1_fotakis_vs_exact']
    lines=['# Saved results used in the theory comparison','',
        '[Interpretation and theorem conditions](../../docs/theory_alignment.md) · [Files and reproduction](README.md)','',
        'These are arithmetic summaries of existing runs. N always counts training reports. Risk is unnormalized Kendall loss '
        'only in the pure-SM simulation tables; empirical NLL is not that risk. NA remains unavailable. No new fit or sample was generated.','',
        '## P1 training regimes','',
        'Only dots2024 A/B r=2 pass the numerical λ≤1 screen. All rows still lack a verified homogeneous-SM, independent-uniform-display sampling law. '
        'The coverage ratio μ/log(er) is not certification of the unknown sufficient constant C0.','',
        display_table(p,['dataset','n','r','N','lambda_','mu','coverage_ratio','pair_min_across_partitions','full_ranking']), '',
        '## P1 estimator predictions','',
        'All differences are paired on the same confirmation reports and averaged over the same 30 partitions. '
        'The table displays only complete means; the CSV preserves finite-conditional differences and their denominators. '
        'Signs here compare SM center estimators, not SM versus PL.','']
    c=tables['p1_estimator_contrasts'];wide=c.pivot(index='dataset',columns='method_a',values='mean_nll_difference').reset_index()
    lines+=[display_table(wide,['dataset','borda','sharp','efficient'],
                         {'borda':'Borda − exact','sharp':'Sharp − exact','efficient':'Efficient − Borda'}),'',
        'The [method inventory](p1_methods.csv) records all five methods for every task, including status counts, branches, '
        'depth, complete/conditional NLL and external-objective distance. That external distance is not true-center risk.','',
        '## Pure-SM center-risk comparisons','',
        'SM β=.8 and uniformly sampled displays. Intervals below are the saved working t intervals over independent training draws, '
        'not new CIs and not minimax envelopes. A randomized generating center removes favorable fixed-label choices; '
        'an average across sampled centers does not numerically evaluate a supremum over centers.','',
        '### S1 bridge endpoint: n=8, equal-gap stream','',
        display_table(s.query('component=="S1_S2" and part=="bridge" and shape=="equal"'),
            ['r','N','lambda_','method','risk','risk_lo','risk_hi','successful_fits','repetitions']), '',
        'The second gap-shape stream and the shell-tilt-zero endpoint are retained separately in [all pure-SM results](pure_sm_results.csv); '
        'they are additional saved streams, not pooled as extra settings or selected by performance.','',
        '### S2: n=32, r=3','',
        display_table(s.query('component=="S1_S2" and part=="coverage"'),
            ['N','lambda_','mu','method','risk','risk_lo','risk_hi','successful_fits']), '',
        '### S3 complete rankings: n=r=8','',
        display_table(s.query('component=="S3" and part=="small" and full_ranking'),
            ['N','method','risk','risk_lo','risk_hi','repetitions']), '',
        'The saved efficient label is depth-zero Borda, which equals sorting average positions here. Sharp uses a pair sieve, '
        'not Theorem 2.17’s tournament estimator. There is no saved full-ranking majority-estimator risk series.','',
        '### S3 coverage: n=64, depth-zero global scores','',
        display_table(s.query('component=="S3" and part=="coverage" and method=="efficient"'),
            ['r','N','lambda_','mu','nu','Vcov','coverage_dominated','risk','risk_lo','risk_hi','repetitions']), '',
        '## C1 / S3 learning: center benchmarks under SM','',
        'n=10, r=3, β=.8; 30 independent streams, with nested budgets within each stream. '
        'These are means of saved per-stream errors; no new intervals are attached. The objective gap uses the exact DP optimum. '
        'A zero gap certifies the attained training objective, not a general risk guarantee for the algorithm.','',
        display_table(tables['c1_sm_centers'],['N','lambda_','method','risk','mean_training_objective_gap',
            'max_training_objective_gap','zero_objective_gap_repetitions','repetitions']), '',
        '## G1: Fotakis versus exact SM','',
        'Primary 70% within-group allocations, 100 repetitions. Only complete all-report NLL comparisons enter a complete mean; '
        'local unavailable groups are not silently removed. Negative means favor Fotakis-center SM prediction. '
        'All 50%/80% and group-holdout comparisons are also in [the CSV](g1_fotakis_vs_exact.csv).','',
        display_table(g.query('design=="within" and percent==70'),
            ['dataset','scheme','complete_finite_pairs','repetitions','fotakis_minus_exact','identical_nll_repetitions']), '']
    (OUT/'tables.md').write_text('\n'.join(lines))


def run():
    tables=summarize()
    for name,frame in tables.items():
        frame.to_csv(OUT/(name+'.csv'),index=False,float_format='%.15g')
    render_tables(tables)
    paths=[str(p.relative_to(ROOT)) for p in [OUT/(name+'.csv') for name in tables]+[OUT/'tables.md']]
    manifest=dict(purpose='Saved-result interpretation only; no new experiments',
        outputs={p:digest(ROOT/p) for p in paths},
        code={p:digest(ROOT/p) for p in ['analyze_theory_alignment.py','validate_theory_alignment.py']},
        rows={name:len(frame) for name,frame in tables.items()})
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest['rows']))


if __name__=='__main__':
    run()
