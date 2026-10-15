"""Build named reader views of saved results; never split, fit, or resample data."""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
P = ROOT / 'results/predictive'
INPUTS = ('results/predictive/primary.csv', 'results/predictive/repeat_scores.csv.gz',
          'results/predictive/predictors.jsonl.gz')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def compressed_csv(frame):
    # GzipFile keeps OS=255 on Python 3.12 as well as 3.13; gzip.compress
    # with mtime=0 delegates the header to zlib on 3.12 and varies by OS.
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode='wb', filename='', mtime=0) as stream:
        stream.write(frame.to_csv(index=False, float_format='%.12g').encode())
    return buffer.getvalue()


def table(frame, columns):
    lines = ['| ' + ' | '.join(label for _, label in columns) + ' |',
             '|' + '|'.join('---' for _ in columns) + '|']
    for _, row in frame.iterrows():
        cells = []
        for key, _ in columns:
            value = row[key]
            cells.append('NA' if pd.isna(value) else f'{value:.5f}'
                         if isinstance(value, (float, np.floating)) else str(value))
        lines.append('| ' + ' | '.join(cells) + ' |')
    return '\n'.join(lines)


def artifacts():
    from summarize_predictive_study import task_label
    summary = pd.read_csv(P / 'primary.csv')
    scores = pd.read_csv(P / 'repeat_scores.csv.gz')
    empirical = scores[scores.study.eq('P0')].copy()
    main_scores = empirical[empirical.method.isin(['pl', 'sm_likelihood'])].copy()
    assert len(main_scores) == 1380 and main_scores.status.eq('ok').all()
    main = summary[summary.method.eq('sm_likelihood')].copy()
    pl = summary[summary.method.eq('pl')].set_index('dataset')
    assert len(main) == 23 and main.available.eq(30).all()
    main['sm_nll'] = main.nll_mean
    main['pl_nll'] = main.dataset.map(pl.nll_mean)
    main['task'] = main.dataset.map(task_label)
    main['sm_lower_splits'] = main.dataset.map(
        main_scores[main_scores.method.eq('sm_likelihood')].groupby('dataset').delta.apply(lambda x: int((x < 0).sum())))
    main['sm_lower_label'] = main.sm_lower_splits.astype(str) + '/30'
    main['certificates'] = main.certified_centers.astype(str) + '/30'
    assert main.certified_centers.sum() == 665
    assert main.filter(regex='_ci_(low|high)$').isna().all().all()
    np.testing.assert_allclose(main.delta_mean, main.sm_nll-main.pl_nll, atol=2e-9)
    precision = []
    for dataset, group in main_scores[main_scores.method.eq('sm_likelihood')].groupby('dataset'):
        values = group.sort_values('repeat').delta.to_numpy()
        assert len(values) == 30 and set(group['repeat']) == set(range(30))
        for count in (5, 10, 20, 30):
            x = values[:count]
            precision.append(dict(dataset=dataset, task=task_label(dataset), partitions=count,
                delta_mean=float(x.mean()), delta_sd=float(x.std(ddof=1)),
                delta_mcse=float(x.std(ddof=1)/np.sqrt(count)),
                difference_from_30=float(x.mean()-values.mean())))
    precision = pd.DataFrame(precision)
    p30 = precision[precision.partitions.eq(30)].set_index('dataset')
    np.testing.assert_allclose(main.delta_mcse, main.dataset.map(p30.delta_mcse), atol=2e-9)
    e0 = summary[summary.method.isin(['sm_sharp', 'sm_fotakis', 'sm_efficient_fallback'])].copy()
    e0.insert(0, 'raw_study', e0['study']); e0['study'] = 'E0'
    b0 = summary[summary.method.eq('sm_global_sieve')].copy()
    b0.insert(0, 'raw_study', b0['study']); b0['study'] = 'B0'
    assert len(e0) == 69 and len(b0) == 23
    assert e0[e0.method.eq('sm_sharp')].available.sum() == 330
    assert set(main_scores.method).isdisjoint(set(e0.method))
    out = {}
    def put(path, content):
        out[path] = content.encode() if isinstance(content, str) else content
    def csv(path, frame):
        put(path, frame.to_csv(index=False, float_format='%.12g'))
    csv('results/main/summary.csv', main)
    put('results/main/repeat_scores.csv.gz', compressed_csv(main_scores))
    csv('results/main/split_precision.csv', precision)
    csv('results/estimator_comparison/summary.csv', e0)
    csv('results/global_sieve/summary.csv', b0)
    main_table = table(main, [('task','Task'),('sm_nll','SM NLL'),('pl_nll','PL NLL'),
        ('delta_mean','Mean delta'),('delta_mcse','Partition MCSE'),
        ('sm_lower_label','Splits with lower SM loss'),('certificates','Exact centers')])
    put('results/main/README.md', '''# P0: main experiment — Algorithm 4.1

[Design](../../docs/predictive_comparison.md) · [Summary CSV](summary.csv) · [Per-partition scores](repeat_scores.csv.gz) · [Thirty-partition precision](split_precision.md) · [Separate E0 estimator comparison](../estimator_comparison/README.md)

This is the study's only main experiment. It implements the grouped predictive-comparison framework of manuscript Algorithm 4.1: fit a whole-ranking likelihood-center SM with bounded dispersion, tune positive-ridge PL using training data only, refit on development data, and compare the two on identical outer-test reports. Sharp, Fotakis, Efficient and the global pair-sieve are outside this main comparison. No test outcome selects an SM center method.

## Design and complete results

There are 23 empirical tasks and 30 randomized outer allocations per task: **690 paired SM–PL predictions, all finite**. The final predictors use 80% of allocation units; the 60%/20% division inside those units is for PL training and validation. Identifiable repeated assessors remain together. Anonymous tasks retain their documented report-level allocation and unresolved dependence. P0 targets another observation/unit from the sampled task population; chronological forecasting is separately named T1.

Each table entry averages the 30 separately fitted test scores with equal weight. Delta is SM minus PL whole-ranking NLL in **nats per report**; negative favors SM. The MCSE is the sample SD of the 30 paired differences divided by sqrt(30). It measures numerical precision over random allocations of this fixed dataset, not population sampling uncertainty. Split counts describe the same 30 allocations, not independent model-victory trials.

''' + main_table + '''

The [summary CSV](summary.csv) additionally supplies n, r, development count N, individual-loss MCSEs, split quantiles and availability. The [per-partition file](repeat_scores.csv.gz) contains only `pl` and `sm_likelihood`; each of the 690 paired comparisons occupies two method rows. These are views of unchanged saved scores, with no new fitting or selected repetitions.

## What the main experiment shows

**The direction depends on the task.** The observed mean favors SM in nine tasks: all four Dots 2013 conditions, all four Puzzle conditions, and dots2024 B with r=6. The other fourteen means favor PL. This count is descriptive: related conditions and shared participants are not 23 independent studies, and no multiple-testing-adjusted model-winner claim is made.

**Within comparable report lengths, some patterns are clearer than others.** For r=3, Wheat has delta +0.15917 and Beans +0.01275. For r=6, PatrasIQ cost has +0.28339, PatrasIQ population +0.07579, dots2024 A +0.07953, and dots2024 B −0.04621. These differences concern the recorded populations and fitting procedures; they do not isolate a causal data property. Raw differences at different r are not a common effect-size scale. Whole-ranking probabilities multiply more terms as r grows.

**A mean advantage does not imply the same ordering on every split.** Puzzle minimum five steps favors SM in 30/30 allocations; Wheat and PatrasIQ cost favor PL in 30/30. By contrast, dots2024 B r=5 favors SM in 12/30 despite its PL-favorable mean +0.01198 (MCSE 0.01465). Sushi B favors SM in 11/30, with mean +0.00975 (MCSE 0.00509). These near-zero averages need cautious interpretation. The saved 2.5th–97.5th split quantiles describe individual-allocation variability, not confidence limits for the average.

**Optimization certification matters.** All 30 SM likelihood centers are certified for 22 tasks. Sushi B has 5/30 certified centers and 25 explicitly approximate centers, so 665/690 centers are certified overall. The Sushi B comparison evaluates the implemented approximate fitting procedure; it is not an exact-MLE family comparison. Recorded training-objective bound gaps are neither test-loss bounds nor actual distances to an optimal order. Exact optimization elsewhere also does not establish model correctness.

![P0 Algorithm 4.1 comparison; bars are one partition MCSE](../../figures/predictive/primary.png)

## What uncertainty is and is not reported

P0 uses all 30 splits for mean NLL, paired mean delta, partition MCSE, descriptive split quantiles, and optimization/availability counts. The means' `*_ci_low/high` fields are intentionally empty. The figure shows **plus/minus one MCSE**, not a 95% population CI.

Within each split, eligible identified test units are resampled with replacement 2,000 times while both fitted models stay fixed. The same sampled units are used for both models; each draw recomputes total paired loss divided by total report count. The 2.5th/97.5th percentiles are a nominal 95% conditional test-sampling interval under independent-unit sampling. This preserves dependence inside an identified person but omits training/tuning variability. These intervals are recorded for 390 paired comparisons across 13 tasks; the 300 comparisons across Beans, Wheat and the eight anonymous PrefLib tasks do not receive a supported sampling CI. Small numbers of clusters and volunteer sampling remain limitations. Thirty bootstrap intervals are never averaged into a CI for the thirty-split mean.

## Interpretation and boundaries

The main result compares conditional predictive laws, not the minimax Kendall risk of Sharp. P0 does not require a sieve calculation. The 360 unavailable empirical Sharp fits belong to **E0**, and the total 530 unavailable Sharp fits also include L0/S0 supplements. They are not missing P0 main comparisons. Their limitations are reported in their own chapters.

These same-population random splits do not guarantee season, year, location or demographic balance, establish independent anonymous assessors, or measure future-season transfer. The [full-data characteristics](../../data/features/predictive_comparison.md) can help describe the observed pattern, but they use all reports and are neither held-out diagnostics nor inputs used to choose the main estimator. [G1](../../docs/group_sensitivity.md), [T1](../../docs/temporal_prediction.md), and [controlled mechanisms](../../docs/strict_feature_analysis.md) address distinct explanatory questions.
''')
    wide = pd.DataFrame({'task': main.set_index('dataset').task})
    for count in (10,20,30):
        subset=precision[precision.partitions.eq(count)].set_index('dataset')
        wide[f'mean{count}']=subset.delta_mean
        wide[f'error{count}']=subset.difference_from_30.abs()
    wide['mcse30']=p30.delta_mcse
    prefix_table=table(wide,[('task','Task'),('mean10','First 10 mean'),('mean20','First 20 mean'),
        ('mean30','All 30 mean'),('mcse30','All 30 MCSE'),('error10','Absolute 10-to-30 difference'),
        ('error20','Absolute 20-to-30 difference')])
    put('results/main/split_precision.md', r'''# P0: what thirty random allocations contribute

[Main results](README.md) · [Computed prefix summaries](split_precision.csv) · [Uncertainty definitions](../../docs/uncertainty.md#partition-monte-carlo-standard-error)

This is an arithmetic audit of saved P0 results, not another experiment, new simulation, or selection of a better split. The models, splits and scientific comparisons are unchanged. Prefixes use the prespecified repetition order (IDs 0–4, 0–9, 0–19 and 0–29); none is chosen for a favorable result.

## Uses across the study

| Component | Use of the 30 allocations | Interval interpretation |
|---|---|---|
| P0 main experiment | Average whole-ranking NLL and paired delta; MCSE, split quantiles, fit/certificate counts | MCSE is conditional partition precision; no population CI for the 30-split mean |
| E0 estimator comparison / B0 sieve aliases | Corresponding summaries for separately named estimators; unavailable fits keep their denominators | Same distinction; aliases are not extra repetitions |
| L0 Sushi learning curves | At each N average 30 test losses; compare nested budgets on the same test within a repetition | Bars are MCSEs; budget points and Sushi A/B share allocations |
| P1 unpenalized control | Average 30 confirmation scores and descriptive diagnostics; report coverage and split spread | No within-split bootstrap in P1; its bars are MCSEs |
| Full-data feature comparison | Join each unchanged full-data feature to P0's 30-split mean NLL difference | Features themselves are not recomputed on 30 splits; no causal or sampling CI is created |

P0/E0/L0 additionally save a separate 2,000-draw test-unit bootstrap inside each eligible split. That bootstrap conditions on the fitted model and does not use the 30 split outcomes as its resampling units. B0 reuses the corresponding Sharp quantities. S0 instead uses **20 independently generated training/test datasets**, whose Student-t mean intervals have a different target. The number 30 is not a universal repetition rule for G1, T1 or the other simulations.

## How many allocations are useful?

Conditional on the observed dataset and fixed fitting rules, independently randomized partitions give

```math
\widehat{\mathrm{MCSE}}_B=\frac{s_\Delta}{\sqrt{B}},\qquad
\mathrm{Var}(\overline{\Delta}_B\mid\mathcal{D})
=\frac{\mathrm{Var}(\Delta_b\mid\mathcal{D})}{B}.
```

Thirty has no special theoretical status. At a fixed partition variance, increasing B from 10 to 30 reduces MCSE by about **42%**, and increasing it from 20 to 30 by about **18%**. Doubling 30 to 60 reduces it by about 29%; halving the MCSE requires approximately four times as many fits. The estimated SD can change as repetitions are added, so observed MCSE need not decrease monotonically.

Thirty is a defensible precision/computation tradeoff here, not a requirement or a guarantee of adequate precision. The 23 task MCSEs range from 0.00223 to 0.02108 nats/report. A useful budget depends on the reporting precision and effect sizes that matter for the particular task and r, rather than obtaining a desired sign or significance decision. For future studies, a separate pilot can estimate partition SD and support a prespecified repetition budget approximately proportional to (SD / desired MCSE)^2. This does not create a population CI or justify stopping when a preferred model wins.

The completed 30 fits should be retained. Reducing their number now saves no fitting work and discards information. For a new expensive exploratory run, 10–20 partitions can be a starting budget, followed by a documented precision assessment; the current results do not prove that ten will suffice in a new dataset. The Sharp bottleneck is construction of ten distinct shared packings, not 530 independent reconstructions. Fewer partitions would therefore not remove the catalogue-scale exact-sieve obstacle.

## Observed prefix arithmetic

''' + prefix_table + '''

The first 10 and first 20 means have the same direction as all 30 for all 23 tasks. Nevertheless, their largest absolute differences from the 30-split means are **0.04963** and **0.02125** nats/report, respectively; their median absolute differences are **0.00612** and **0.00248**. Sushi B changes mean sign between the first five and all thirty splits. Matching signs therefore do not show that numerical precision is already adequate.

These are overlapping prefixes of one prespecified sequence, not independent experiments or a formal convergence test. The 30-split mean is a reference for this audit, not a known population truth or the exact expectation over all possible partitions. No repetition was removed and no model or hyperparameter was selected using this audit.
''')
    e_text='''# E0: supplementary center-estimator comparison

[Design and naming](../../docs/estimator_comparison.md) · [All E0 rows](summary.csv) · [Separate P0 main results](../main/README.md) · [B0 global sieve](../global_sieve/README.md)

E0 compares Sharp, Fotakis and the admitted Efficient fallback with the same tuned PL reference, on the 23-task allocations used by P0. It asks how a different SM center procedure changes prediction. **E0 is not Algorithm 4.1's main experiment.** Its results do not replace `sm_likelihood`, and the best test-scoring estimator is never selected as the main SM result.

The 30 allocations, data and PL reference are shared, so this is a paired supplementary comparison, not an independent replication of P0. Delta is the named SM estimator minus PL whole-ranking NLL. Full means/MCSEs remain NA unless all 30 planned fits exist. Conditional means in the CSV have explicit denominators and must not substitute for missing full comparisons.

'''
    for method,label in [('sm_sharp','Sharp'),('sm_fotakis','Fotakis / PosEst'),('sm_efficient_fallback','Efficient fallback')]:
        q=e0[e0.method.eq(method)].copy();q['task']=q.dataset.map(task_label)
        q['availability']=q.available.astype(str)+'/30'
        e_text += f'## {label}\n\n'+table(q,[('task','Task'),('delta_mean','Mean delta'),('delta_mcse','Partition MCSE'),('availability','Available'),('statuses','Statuses')])+'\n\n'
    e_text+='''## Interpretation and computation

Sharp has 330 completed fits across eleven tasks and 360 unavailable fits across twelve tasks. For Beans, Sharp-minus-PL is +0.00314, compared with P0's likelihood-center delta +0.01275; for Sushi A the respective values are +0.06029 and +0.02543. Both comparisons retain the same held-out reports. They show that estimator choice matters without selecting a replacement after observing test scores.

Fotakis passes its complete-pair gate in 416 of 690 contexts. Efficient is available in the 60 dots2024 r=2 contexts under its declared lambda<=1 fallback policy. Neither missing coverage nor resource failure is a zero loss. The B0 global sieve aliases Sharp in these configurations and is not an additional independent result.

The outstanding 530 Sharp fits comprise **360 E0, 90 L0 and 80 S0**. None is a missing P0 main comparison. See the [exact computation account](../../docs/sieve_computation.md#completion-results-and-remaining-limits). In the immutable raw files these E0 rows retain `study=P0` as their allocation-family key; this view records `raw_study=P0, study=E0`. A shared storage key does not define the scientific experiment name.
'''
    put('results/estimator_comparison/README.md',e_text)
    put('results/global_sieve/README.md','''# B0: supplementary global pair-sieve comparison

[Construction and theorem scope](../../docs/sieve_computation.md#b0-global-pair-sieve-for-bounded-report-sizes) · [Empirical B0 summary](summary.csv) · [E0 Sharp results](../estimator_comparison/README.md) · [P0 main experiment](../main/README.md)

B0 concerns the exact global pair-sieve and the bounded-report-size theory with fixed R=10. It is not Algorithm 4.1's main experiment. Its empirical summary has 23 tasks, with `raw_study=P0` preserving their shared allocation-family key and `study=B0` naming this supplementary comparison.

In every recorded empirical configuration, Sharp has zero pilot depth and a single catalogue-wide terminal block. With the same selected pairs and tie rule, global sieve and Sharp are identical. The 330 available empirical B0 rows and 360 unavailable rows therefore alias E0 Sharp; they are not another 690 independent fits. The same alias rule is recorded in the L0/S0 raw tables. An unavailable Sharp/global-sieve pair is counted only once in the 530 outstanding computations.

The report-size bound alone does not verify uniform displays, independence, a true SM law, or the corollary's lambda condition. Empirical predictive NLL is a different target from minimax center Kendall risk. Full details and resource limits are in the linked construction chapter.
''')
    put('results/predictive/tables.md','''# Predictive result directory

The main experiment is **P0: manuscript Algorithm 4.1**, comparing likelihood-center SM with tuned ridge PL. Its result table and analysis are separate from all estimator supplements.

| Named analysis | Results |
|---|---|
| P0 — main Algorithm 4.1 comparison | [Independent main report and 23-task table](../main/README.md) |
| E0 — supplementary center-estimator comparison | [Sharp, Fotakis and Efficient tables](../estimator_comparison/README.md) |
| B0 — supplementary global pair-sieve | [Construction identity and results](../global_sieve/README.md) |
| L0 — supplementary Sushi learning curves | [Design and interpretation](../../docs/predictive_learning.md#l0-sushi-ab-with-thirty-outer-partitions), [numeric results](learning.csv) |
| S0 — supplementary independent simulation curves | [Design and interpretation](../../docs/predictive_learning.md#s0-independent-data-with-fixed-r3-and-r10), [numeric results](synthetic.csv) |

The raw `primary.csv` is a reproducibility export containing several methods under one allocation-family key. Use the named reports above for scientific interpretation. [Raw field dictionary and exact method mapping](README.md#keys-and-method-identity) explain that storage convention. No saved fit, split or NLL has changed.
''')
    manifest=dict(producer='build_study_reports.py',producer_sha256=digest(Path(__file__).read_bytes()),
        source_sha256={p:digest((ROOT/p).read_bytes()) for p in INPUTS},
        interpretation='Presentation views and arithmetic of existing scores only; no fitting or resampling.',
        main_selection=dict(raw_study='P0',methods=['pl','sm_likelihood'],paired_contexts=690),
        estimator_selection=dict(raw_study='P0',reading_name='E0',methods=['sm_sharp','sm_fotakis','sm_efficient_fallback']),
        global_sieve_selection=dict(raw_study='P0',reading_name='B0',method='sm_global_sieve'),
        outputs_sha256={p:digest(b) for p,b in out.items()})
    put('results/study_reports_manifest.json',json.dumps(manifest,indent=2)+'\n')
    return out


def build(check=False, update_manifest=True):
    outputs=artifacts()
    for name,content in outputs.items():
        path=ROOT/name
        if check:
            assert path.read_bytes()==content, name
        else:
            path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(content)
    if update_manifest:
        path=P/'manifest.json'; manifest=json.loads(path.read_text())
        # Only the presentation producer and the table-directory page change.
        # Every numerical source remains checked against its recorded hash.
        for name,value in manifest['published_sha256'].items():
            if name!='tables.md':assert digest((P/name).read_bytes())==value,name
        manifest['summary_code_sha256']=digest((ROOT/'summarize_predictive_study.py').read_bytes())
        manifest['published_sha256']['tables.md']=digest((P/'tables.md').read_bytes())
        if check:
            assert json.loads(path.read_text())==manifest
        else:path.write_text(json.dumps(manifest,indent=2)+'\n')
    print(('Verified' if check else 'Built')+f' {len(outputs)} named report artifacts; 690 main comparisons; numerical source files unchanged')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true')
    build(check=parser.parse_args().check)
