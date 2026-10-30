"""Build current named result reports from saved scores; no fitting or resampling."""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.reporting_metrics import uniform_scaled_differences

ROOT=Path(__file__).resolve().parent
P=ROOT/'results/predictive'
INPUTS=('results/predictive/primary.csv','results/predictive/repeat_scores.csv.gz',
        'results/predictive/predictors.jsonl.gz','results/estimator_comparison/repeat_scores.csv.gz',
        'results/estimator_comparison/predictors.jsonl.gz','results/estimator_comparison/manifest.json',
        'src/estimator_reporting.py','src/reporting_metrics.py',
        'results/predictive/learning.csv','results/predictive/synthetic.csv',
        'results/estimator_execution/snippets/E0.md',
        'results/estimator_execution/snippets/L0.md',
        'results/estimator_execution/snippets/S0.md')
REPETITIONS=5


def digest(data):
    return hashlib.sha256(data).hexdigest()


def compressed_csv(frame):
    output=io.BytesIO()
    with gzip.GzipFile(fileobj=output,mode='wb',filename='',mtime=0) as stream:
        stream.write(frame.to_csv(index=False,float_format='%.12g').encode())
    return output.getvalue()


def table(frame, columns):
    rows=['| '+' | '.join(label for _,label in columns)+' |','|'+'|'.join('---' for _ in columns)+'|']
    for _,row in frame.iterrows():
        cells=[]
        for key,_ in columns:
            value=row[key]
            cells.append('NA' if pd.isna(value) else f'{value:.5f}' if isinstance(value,(float,np.floating)) else str(value))
        rows.append('| '+' | '.join(cells)+' |')
    return '\n'.join(rows)


def artifacts():
    from summarize_predictive_study import task_label
    summary=pd.read_csv(P/'primary.csv');scores=pd.read_csv(P/'repeat_scores.csv.gz')
    empirical=scores[scores.study.eq('P0')].copy()
    selected=empirical[empirical.method.isin(['pl','sm_likelihood'])].copy()
    assert len(selected)==230 and selected.status.eq('ok').all()
    assert set(selected['repeat'])==set(range(5))
    main=summary[summary.method.eq('sm_likelihood')].copy()
    pl=summary[summary.method.eq('pl')].set_index('dataset')
    assert len(main)==23 and main.available.eq(5).all()
    main['sm_nll']=main.nll_mean;main['pl_nll']=main.dataset.map(pl.nll_mean)
    main['task']=main.dataset.map(task_label)
    paired=selected[selected.method.eq('sm_likelihood')]
    main['sm_lower_splits']=main.dataset.map(paired.groupby('dataset').delta.apply(lambda x:int((x<0).sum())))
    main['sm_lower_label']=main.sm_lower_splits.astype(str)+'/5'
    main['certificates']=main.certified_centers.astype(str)+'/5'
    assert main.filter(regex='_ci_(low|high)$').isna().all().all()
    np.testing.assert_allclose(main.delta_mean,main.sm_nll-main.pl_nll,atol=2e-9)
    precision=[]
    for dataset,g in paired.groupby('dataset'):
        x=g.sort_values('repeat').delta.to_numpy()
        assert len(x)==5
        assert g.r.nunique()==1
        precision.append(dict(dataset=dataset,task=task_label(dataset),r=int(g.r.iloc[0]),partitions=5,
            delta_mean=x.mean(),delta_sd=x.std(ddof=1),delta_mcse=x.std(ddof=1)/np.sqrt(5),
            delta_min=x.min(),delta_max=x.max()))
    precision=pd.DataFrame(precision)
    np.testing.assert_allclose(main.delta_mcse,main.dataset.map(precision.set_index('dataset').delta_mcse),atol=2e-9)
    from summarize_predictive_study import summarize
    from src.estimator_reporting import report as estimator_report
    e_scores=pd.read_csv(ROOT/'results/estimator_comparison/repeat_scores.csv.gz')
    e0=summarize(e_scores)
    e0.insert(0,'raw_study','P0')
    b0=summary[summary.method.eq('sm_global_sieve')].copy()
    for label,frame in [('B0',b0)]:
        frame.insert(0,'raw_study',frame.study);frame['study']=label
    assert len(e0)==138 and len(b0)==23
    assert set(e0.study)=={'E0'} and len(e_scores)==690
    main=uniform_scaled_differences(main)
    selected=uniform_scaled_differences(selected)
    precision=uniform_scaled_differences(precision)
    e0=uniform_scaled_differences(e0)
    b0=uniform_scaled_differences(b0)
    learning=uniform_scaled_differences(pd.read_csv(P/'learning.csv'))
    synthetic=uniform_scaled_differences(pd.read_csv(P/'synthetic.csv'))
    curve_scores=scores[scores.study.isin(['L0','S0']) |
        (scores.study.eq('P0') & scores.dataset.isin(['sushi_a','sushi_b']))]
    out={}
    def put(path,content):out[path]=content.encode() if isinstance(content,str) else content
    def csv(path,frame):put(path,frame.to_csv(index=False,float_format='%.12g'))
    csv('results/main/summary.csv',main);put('results/main/repeat_scores.csv.gz',compressed_csv(selected))
    csv('results/main/split_precision.csv',precision)
    csv('results/estimator_comparison/summary.csv',e0);csv('results/global_sieve/summary.csv',b0)
    put('results/estimator_comparison/scaled_repeat_scores.csv.gz',
        compressed_csv(uniform_scaled_differences(e_scores)))
    csv('results/predictive/learning_comparison.csv',learning)
    csv('results/predictive/synthetic_comparison.csv',synthetic)
    put('results/predictive/scaled_curve_scores.csv.gz',
        compressed_csv(uniform_scaled_differences(curve_scores)))
    cols=[('task','Task'),('r','r'),('sm_nll','SM NLL'),('pl_nll','PL NLL'),('delta_mean','Mean delta'),
        ('delta_uniform_mean','Delta / log(r!)'),('delta_mcse','Partition MCSE'),
        ('delta_uniform_mcse','Scaled MCSE'),('sm_lower_label','Splits with lower SM loss'),('certificates','Exact centers')]
    indexed=main.set_index('dataset')
    def result(name):
        a=indexed.loc[name]
        return f"{a['task']}: delta {a.delta_mean:+.5f}, MCSE {a.delta_mcse:.5f}, lower SM loss in {a.sm_lower_splits}/5 splits"
    certified=int(main.certified_centers.sum());sm_better=int((main.delta_mean<0).sum())
    put('results/main/README.md',f'''# P0: main experiment — Algorithm 4.1

[Design](../../docs/predictive_comparison.md) · [Summary CSV](summary.csv) · [Per-partition scores](repeat_scores.csv.gz) · [Partition precision](split_precision.md) · [E0 estimator comparison](../estimator_comparison/README.md)

P0 is the only main experiment. It implements the grouped predictive-comparison framework of manuscript Algorithm 4.1: fit whole-ranking likelihood-center SM with bounded dispersion, tune positive-ridge PL within development data, refit on development data, and compare both on the same outer-test reports. Sharp, Fotakis, Efficient and global sieve are supplementary estimators, not main competitors. Test outcomes never choose the SM center method.

## Design and complete results

Each of 23 tasks has five grouped random allocations, with repetition IDs 0–4: **115 paired predictions, all finite**. The final predictors use 80% of allocation units; the first 60% and next 20% tune PL inside those development units. Identifiable repeated assessors stay together. Anonymous reports retain unresolved dependence. P0 targets prediction in the sampled population; chronological forecasting is T1.

All means give each of the five separately fitted test scores equal weight. Delta is SM minus PL whole-ranking NLL, in nats/report; negative favors SM. MCSE is the sample SD of the five paired differences divided by sqrt(5). It describes integration over random allocations of these fixed observations, not population sampling uncertainty.

The adjacent **Delta / log(r!)** column divides the paired difference by the uniform-ranking loss on an r-item display. It is a dimensionless ratio (0.01 means 1% of that reference), not an accuracy percentage. r is the report size, not the catalogue size n. Scaled MCSE divides raw MCSE by the same positive constant. [Definition and limitations](../../docs/criteria.md#uniform-reference-scaled-loss-difference).

'''+table(main,cols)+f'''

The [per-partition file](repeat_scores.csv.gz) contains only the two main methods, with two rows per paired prediction. The [summary CSV](summary.csv) also records n, r, development count N and availability. A split-win count is descriptive, not a binomial significance test.

## Interpretation

The mean favors SM in **{sm_better} tasks** and PL in **{23-sm_better} tasks**. Related tasks share participants and are not independent replications. The count does not establish statistically significant winners. The raw column measures extra nats/report; the scaled column expresses that difference relative to log(r!). This adjusts for the size of the ranking outcome space without making task populations, difficulty or estimation uncertainty identical. Neither column is a universal ranking of dataset suitability.

For example, PatrasIQ cost has delta +0.33462, larger than Dots 2024 B r2 at +0.13836. Relative to log(6!) and log(2!), respectively, the gaps are about 5.09% and 19.96%: their ordering reverses. Sushi A and B both use log(10!), despite their different catalogue sizes. A positive value still favors PL; scaling never changes the winner within a task.

Representative results:

- {result('wheat')}.
- {result('patras_cost')}.
- {result('00025-00000002')}.
- {result('sushi_b')}.
- {result('dots2024_B_r6')}.

The last two comparisons illustrate why a favorable mean can be poorly resolved relative to its MCSE. Five repetitions estimate partition variance with only four degrees of freedom. Neither their observed range nor interpolated tail quantiles provide a population confidence interval. The report therefore shows the five-score **minimum and maximum**, alongside MCSE, in its precision table. Small differences should remain descriptive.

There are **{certified}/115 certified likelihood centers**. All five centers are certified for 22 tasks; Sushi B has {int(indexed.loc['sushi_b','certified_centers'])}/5 certificates. Its other centers are explicitly approximate, so that comparison evaluates an implemented fitting procedure rather than certified exact MLE. Training-objective gaps are not test-loss error bounds.

![P0: five grouped allocations, bars are one partition MCSE](../../figures/predictive/primary.png)

## Uncertainty and boundaries

Mean-level CI fields are empty. Figure bars are **±1 MCSE**, not 95% population CIs. Within each eligible split, 2,000 paired bootstrap draws resample complete test units while both models remain fixed. Ratio losses are report-weighted. Percentiles 2.5 and 97.5 give nominal conditional test-sampling CIs under independent-unit sampling. They preserve within-person dependence but omit training and tuning uncertainty. These CIs cover 65 paired contexts across 13 identified tasks. Beans, Wheat and the eight anonymous PrefLib tasks have no supported sampling CI. Bootstrap endpoints are not averaged across splits.

Five random allocations do not enforce seasonal or demographic balance, establish independence of anonymous assessors, or validate future-year transfer. [G1](../../docs/group_sensitivity.md) and [T1](../../docs/temporal_prediction.md) address different targets. The [full-data characteristics](../../data/features/predictive_comparison.md) describe all observations; they do not choose these predictors or causally explain their performance.

P0 does not require Sharp or a sieve. Missing supplementary E0/L0/S0 fits are not missing main comparisons. See their separate reports for availability and computation limits.
''')
    put('results/main/split_precision.md',r'''# Precision of five random allocations

[Main results](README.md) · [Numeric precision table](split_precision.csv) · [Uncertainty definitions](../../docs/uncertainty.md)

The empirical repeated-partition budget is B=5, using fixed IDs 0–4. Five is a computation choice, not a guarantee of small error and not a preregistered significance threshold. The allocation indices are selected without ranking their outcomes. The displayed mean averages separately fitted models' losses; it is not the loss of an ensemble.

```math
\overline{\Delta}=\frac{1}{5}\sum_{b=1}^{5}\Delta_b,\qquad
s_\Delta^2=\frac{1}{4}\sum_{b=1}^{5}(\Delta_b-\overline{\Delta})^2,\qquad
\widehat{\mathrm{MCSE}}=\frac{s_\Delta}{\sqrt{5}}.
```

Conditional on fixed data and independently randomized allocations, this estimates the standard error of Monte Carlo integration over allocations. It is not a population CI. Five draws give a noisy variance estimate with four degrees of freedom; apparent precision is not guaranteed to persist in further allocations. Compare MCSE with the model difference, not with an absolute label such as "small". Interpolated split quantiles retained in machine tables are descriptive and especially unstable with five values. The table below uses observed min/max instead.

| Component | Role of the five allocations |
|---|---|
| P0 | Average main NLL/delta; MCSE; finite-fit and exact-center counts |
| E0/B0 | Supplementary estimator means and availability; B0 aliases are not extra repetitions |
| L0 | Each training budget averages five aligned outer tests; budgets are nested and dependent |
| P1 | Five confirmation scores and descriptive diagnostics per task; no inner bootstrap |
| G1 | Five within-group splits per training fraction and five whole-group holdouts |
| Full-data features | One full-data feature value is joined to the five-allocation P0 mean |

The 2,000 bootstrap draws **inside** an eligible P0/E0/L0 split are a different resampling operation and remain 2,000. Simulations generate fresh datasets and keep their independent-repetition designs. Fixed diagnostic allocations and chronological forecasts are not converted into random five-fold or five-shuffle experiments.

Raw and scaled differences appear together below. Scaling divides the difference, MCSE, SD and range endpoints by the task's fixed log(r!); it does not add repetitions or change the uncertainty target. Numeric CSV ratios are not multiplied by 100.

'''+table(precision,[('task','Task'),('delta_mean','Mean delta'),('delta_uniform_mean','Delta / log(r!)'),('delta_mcse','MCSE'),('delta_uniform_mcse','Scaled MCSE'),('delta_min','Smallest split delta'),('delta_max','Largest split delta')])+'\n')
    e_text,e_contrasts=estimator_report(e0,e_scores,table,task_label)
    put('results/estimator_comparison/README.md',e_text)
    csv('results/estimator_comparison/borda_comparisons.csv',e_contrasts)
    put('results/global_sieve/README.md','''# B0: supplementary global pair-sieve comparison

[Construction and theorem scope](../../docs/sieve_computation.md) · [Summary CSV](summary.csv) · [E0](../estimator_comparison/README.md) · [P0 main experiment](../main/README.md)

B0 uses fixed report-size bound R=10. It is supplementary to Algorithm 4.1. In every recorded empirical configuration, Sharp has zero pilot depth and one catalogue-wide terminal block. With identical pair draws and tie rules, global sieve and Sharp coincide. The 55 available and 60 unavailable empirical B0 contexts therefore alias E0 Sharp, rather than adding fits. L0/S0 aliases follow the same rule.

The table pairs raw delta (sieve minus PL, nats/report) with delta / log(r!), a dimensionless uniform-reference ratio. NA retains unavailable full five-fit comparisons. Scaling does not resolve missing fits or create independent evidence from an alias.

'''+table(b0.assign(task=b0.dataset.map(task_label)),[('task','Task'),('r','r'),('available','Available / 5'),('delta_mean','Mean delta'),('delta_uniform_mean','Delta / log(r!)'),('delta_mcse','MCSE'),('delta_uniform_mcse','Scaled MCSE')])+'''

The report-size bound alone does not establish uniform displays, independent reports, a true SM law or the corollary's lambda condition. Empirical predictive NLL differs from minimax Kendall center risk. The summary has `study=B0` and preserves `raw_study=P0` solely as the original allocation-family key.
''')
    put('results/predictive/tables.md','''# Predictive result directory

P0 is the main experiment: manuscript Algorithm 4.1, likelihood-center SM versus tuned PL. All other rows are named supplements.

| Analysis | Results |
|---|---|
| P0 main | [Independent report and all 23 tasks](../main/README.md) |
| E0 estimators | [Sharp, Fotakis, Efficient and global Borda](../estimator_comparison/README.md) |
| B0 global sieve | [Identity, theory scope and availability](../global_sieve/README.md) |
| L0 Sushi learning | [Design](../../docs/predictive_learning.md), [raw and scaled differences](scaled_curves.md#l0-sushi-learning), [all-method CSV](learning_comparison.csv) |
| S0 independent simulations | [Design](../../docs/predictive_learning.md), [raw and scaled differences](scaled_curves.md#s0-independent-simulations), [all-method CSV](synthetic_comparison.csv) |

The raw export combines methods by allocation family; the reports above separate their scientific roles. [Field dictionary](README.md) defines all method identities, units, and uncertainty fields.
''')
    curve_text='''# L0/S0: raw and uniform-reference-scaled differences

[Design and uncertainty](../../docs/predictive_learning.md) · [Metric definition](../../docs/criteria.md#uniform-reference-scaled-loss-difference) · [Per-repetition scores and conditional intervals](scaled_curve_scores.csv.gz)

Delta is each SM estimator's NLL minus paired PL NLL; negative favors SM. The adjacent ratio divides by log(r!), the loss of uniform ranking on the actual display. Ratios are dimensionless, not percentages or accuracies. Raw scores, fitted parameters, test reports, repetitions and availability are unchanged. All delta statistics and existing interval endpoints in the linked numeric views have matching `delta_uniform*` columns. NA stays NA.

## L0: Sushi learning

The table shows likelihood-center SM versus PL; the [all-estimator CSV](learning_comparison.csv) additionally preserves Sharp, Fotakis, admitted Efficient fallback and the global-sieve alias. These curve estimators retain their stated identities; this is not the independently admitted six-method E0 table. N=4000 is the linked P0/E0 endpoint, not another fit. Each point uses five allocations and r=10. MCSE describes fixed-data partition precision, not population sampling uncertainty. All points share the divisor log(10!), so scaling changes neither within-curve trends nor the ordering of Sushi A/B gaps. Conditional test-unit bootstrap endpoints are in the per-repetition view; no bootstrap endpoints are averaged into a curve-mean CI.

'''
    curve_main=learning[learning.method.eq('sm_likelihood')].copy()
    curve_main['task']=curve_main.dataset.map(task_label)
    curve_text+=table(curve_main,[('task','Task'),('N','Development N'),('available','Available / 5'),
        ('delta_mean','Mean delta'),('delta_uniform_mean','Delta / log(r!)'),
        ('delta_mcse','MCSE'),('delta_uniform_mcse','Scaled MCSE')])+'\n\n'
    curve_text+='''## S0: independent simulations

The table shows likelihood-center SM versus PL; the [all-estimator CSV](synthetic_comparison.csv) retains every estimator and unavailable cell. Each cell has twenty independent training/test draws. All use r=3, including the growing-catalogue n curve, so the divisor is always log(3!), not log(n!). The intervals are the existing pointwise Student-t 95% intervals for the independent-repetition mean. Divide each endpoint by log(3!) to obtain the scaled interval. This is a change of units, not an additional inference; it does not make these simulated populations interchangeable with empirical tasks.

'''
    curve_main=synthetic[synthetic.method.eq('sm_likelihood')].copy()
    for prefix in ('delta','delta_uniform'):
        curve_main[prefix+'_interval']=[f'[{lo:+.5f}, {hi:+.5f}]' if pd.notna(lo) else 'NA'
            for lo,hi in zip(curve_main[prefix+'_ci_low'],curve_main[prefix+'_ci_high'])]
    curve_text+=table(curve_main,[('dataset','Generating law'),('n','n'),('N','Development N'),
        ('available','Available / 20'),('delta_mean','Mean delta'),('delta_uniform_mean','Delta / log(r!)'),
        ('delta_interval','Raw 95% interval'),('delta_uniform_interval','Scaled 95% interval')])+'\n'
    put('results/predictive/scaled_curves.md',curve_text)
    for report,studies in [('results/estimator_comparison/README.md',['E0']),
                           ('results/predictive/scaled_curves.md',['L0','S0'])]:
        for study in studies:
            snippet=(ROOT/f'results/estimator_execution/snippets/{study}.md').read_text()
            snippet=snippet.replace('](../','](../estimator_execution/')
            out[report]+=('\n'+snippet.replace('## Sharp/Efficient execution and stopping',f'## {study}: Sharp/Efficient execution and stopping')).encode()
    out['results/global_sieve/README.md']+=b'\n## Execution and stopping\n\nB0 aliases the 115 E0 Sharp contexts: 55 complete terminal sieves and 60 resource exclusions, all with zero pilot depth. The [E0 per-task table](../estimator_execution/E0.md) gives n, N, r, first-round w/M, W*, actual blocks and the resource receipt for every case. These are the same fits, not additional experiments.\n'
    manifest=dict(producer='build_study_reports.py',producer_sha256=digest(Path(__file__).read_bytes()),
        source_sha256={p:digest((ROOT/p).read_bytes()) for p in INPUTS},
        interpretation='Named current result views; no fitting or resampling.',
        main_selection=dict(raw_study='P0',methods=['pl','sm_likelihood'],repetitions=5,paired_contexts=115),
        outputs_sha256={p:digest(b) for p,b in out.items()})
    put('results/study_reports_manifest.json',json.dumps(manifest,indent=2)+'\n')
    return out


def build(check=False,update_manifest=True):
    outputs=artifacts()
    for name,content in outputs.items():
        path=ROOT/name
        if check:assert path.read_bytes()==content,name
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(content)
    if update_manifest:
        path=P/'manifest.json';manifest=json.loads(path.read_text())
        for name,value in manifest['published_sha256'].items():
            if name!='tables.md':assert digest((P/name).read_bytes())==value,name
        manifest['summary_code_sha256']=digest((ROOT/'summarize_predictive_study.py').read_bytes())
        manifest['published_sha256']['tables.md']=digest((P/'tables.md').read_bytes())
        if check:assert json.loads(path.read_text())==manifest
        else:path.write_text(json.dumps(manifest,indent=2)+'\n')
    print(('Verified' if check else 'Built')+f' {len(outputs)} report artifacts; 115 main comparisons')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true')
    build(check=parser.parse_args().check)
