# P0: main experiment — Algorithm 4.1

[Design](../../docs/predictive_comparison.md) · [Summary CSV](summary.csv) · [Per-partition scores](repeat_scores.csv.gz) · [Thirty-partition precision](split_precision.md) · [Separate E0 estimator comparison](../estimator_comparison/README.md)

This is the study's only main experiment. It implements the grouped predictive-comparison framework of manuscript Algorithm 4.1: fit a whole-ranking likelihood-center SM with bounded dispersion, tune positive-ridge PL using training data only, refit on development data, and compare the two on identical outer-test reports. Sharp, Fotakis, Efficient and the global pair-sieve are outside this main comparison. No test outcome selects an SM center method.

## Design and complete results

There are 23 empirical tasks and 30 randomized outer allocations per task: **690 paired SM–PL predictions, all finite**. The final predictors use 80% of allocation units; the 60%/20% division inside those units is for PL training and validation. Identifiable repeated assessors remain together. Anonymous tasks retain their documented report-level allocation and unresolved dependence. P0 targets another observation/unit from the sampled task population; chronological forecasting is separately named T1.

Each table entry averages the 30 separately fitted test scores with equal weight. Delta is SM minus PL whole-ranking NLL in **nats per report**; negative favors SM. The MCSE is the sample SD of the 30 paired differences divided by sqrt(30). It measures numerical precision over random allocations of this fixed dataset, not population sampling uncertainty. Split counts describe the same 30 allocations, not independent model-victory trials.

| Task | SM NLL | PL NLL | Mean delta | Partition MCSE | Splits with lower SM loss | Exact centers |
|---|---|---|---|---|---|---|
| Dots 2013, gap 3 | 3.11430 | 3.12671 | -0.01241 | 0.00226 | 26/30 | 30/30 |
| Dots 2013, gap 5 | 3.04443 | 3.05895 | -0.01452 | 0.00223 | 26/30 | 30/30 |
| Dots 2013, gap 7 | 2.89668 | 2.90924 | -0.01255 | 0.00311 | 22/30 | 30/30 |
| Dots 2013, gap 9 | 2.81760 | 2.85274 | -0.03515 | 0.00413 | 26/30 | 30/30 |
| Puzzle, minimum 11 steps | 3.07860 | 3.09021 | -0.01161 | 0.00273 | 24/30 | 30/30 |
| Puzzle, minimum 5 steps | 2.81910 | 2.87766 | -0.05855 | 0.00365 | 30/30 | 30/30 |
| Puzzle, minimum 7 steps | 2.84041 | 2.86335 | -0.02293 | 0.00368 | 26/30 | 30/30 |
| Puzzle, minimum 9 steps | 3.02456 | 3.03337 | -0.00881 | 0.00265 | 21/30 | 30/30 |
| Beans | 1.80313 | 1.79039 | 0.01275 | 0.00240 | 3/30 | 30/30 |
| Dots 2024 A r2 | 0.64607 | 0.55226 | 0.09381 | 0.01382 | 1/30 | 30/30 |
| Dots 2024 A r3 | 1.44773 | 1.34176 | 0.10598 | 0.01671 | 3/30 | 30/30 |
| Dots 2024 A r5 | 4.12297 | 4.07385 | 0.04912 | 0.01987 | 11/30 | 30/30 |
| Dots 2024 A r6 | 5.61476 | 5.53523 | 0.07953 | 0.02108 | 7/30 | 30/30 |
| Dots 2024 B r2 | 0.80592 | 0.68902 | 0.11691 | 0.01358 | 2/30 | 30/30 |
| Dots 2024 B r3 | 1.73697 | 1.61931 | 0.11766 | 0.01532 | 4/30 | 30/30 |
| Dots 2024 B r5 | 4.39836 | 4.38638 | 0.01198 | 0.01465 | 12/30 | 30/30 |
| Dots 2024 B r6 | 6.08146 | 6.12766 | -0.04621 | 0.01352 | 21/30 | 30/30 |
| PatrasIQ cost | 5.18865 | 4.90526 | 0.28339 | 0.01974 | 0/30 | 30/30 |
| PatrasIQ population | 5.66837 | 5.59259 | 0.07579 | 0.02056 | 7/30 | 30/30 |
| Sounds | 0.69358 | 0.68053 | 0.01304 | 0.00267 | 6/30 | 30/30 |
| Sushi A | 14.26788 | 14.24245 | 0.02543 | 0.00330 | 2/30 | 30/30 |
| Sushi B | 14.23169 | 14.22194 | 0.00975 | 0.00509 | 11/30 | 5/30 |
| Wheat | 1.54420 | 1.38502 | 0.15917 | 0.01337 | 0/30 | 30/30 |

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
