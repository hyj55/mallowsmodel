# P0: main experiment — Algorithm 4.1

[Design](../../docs/predictive_comparison.md) · [Summary CSV](summary.csv) · [Per-partition scores](repeat_scores.csv.gz) · [Partition precision](split_precision.md) · [E0 estimator comparison](../estimator_comparison/README.md)

P0 is the only main experiment. It implements the grouped predictive-comparison framework of manuscript Algorithm 4.1: fit whole-ranking likelihood-center SM with bounded dispersion, tune positive-ridge PL within development data, refit on development data, and compare both on the same outer-test reports. Sharp, Fotakis, Efficient and global sieve are supplementary estimators, not main competitors. Test outcomes never choose the SM center method.

## Design and complete results

Each of 23 tasks has five grouped random allocations, with repetition IDs 0–4: **115 paired predictions, all finite**. The final predictors use 80% of allocation units; the first 60% and next 20% tune PL inside those development units. Identifiable repeated assessors stay together. Anonymous reports retain unresolved dependence. P0 targets prediction in the sampled population; chronological forecasting is T1.

All means give each of the five separately fitted test scores equal weight. Delta is SM minus PL whole-ranking NLL, in nats/report; negative favors SM. MCSE is the sample SD of the five paired differences divided by sqrt(5). It describes integration over random allocations of these fixed observations, not population sampling uncertainty.

| Task | SM NLL | PL NLL | Mean delta | Partition MCSE | Splits with lower SM loss | Exact centers |
|---|---|---|---|---|---|---|
| Dots 2013, gap 3 | 3.11623 | 3.13793 | -0.02170 | 0.00576 | 5/5 | 5/5 |
| Dots 2013, gap 5 | 3.08019 | 3.09017 | -0.00998 | 0.00413 | 4/5 | 5/5 |
| Dots 2013, gap 7 | 2.90742 | 2.90931 | -0.00189 | 0.00541 | 3/5 | 5/5 |
| Dots 2013, gap 9 | 2.80998 | 2.85413 | -0.04415 | 0.00337 | 5/5 | 5/5 |
| Puzzle, minimum 11 steps | 3.09985 | 3.11026 | -0.01042 | 0.00294 | 5/5 | 5/5 |
| Puzzle, minimum 5 steps | 2.77503 | 2.84437 | -0.06934 | 0.00523 | 5/5 | 5/5 |
| Puzzle, minimum 7 steps | 2.85703 | 2.87793 | -0.02090 | 0.01363 | 4/5 | 5/5 |
| Puzzle, minimum 9 steps | 3.00423 | 3.01953 | -0.01530 | 0.00906 | 4/5 | 5/5 |
| Beans | 1.80301 | 1.78969 | 0.01333 | 0.01001 | 1/5 | 5/5 |
| Dots 2024 A r2 | 0.62505 | 0.58080 | 0.04426 | 0.01430 | 1/5 | 5/5 |
| Dots 2024 A r3 | 1.48428 | 1.35561 | 0.12868 | 0.02169 | 0/5 | 5/5 |
| Dots 2024 A r5 | 4.15226 | 4.11050 | 0.04176 | 0.03857 | 2/5 | 5/5 |
| Dots 2024 A r6 | 5.72212 | 5.63734 | 0.08479 | 0.04061 | 1/5 | 5/5 |
| Dots 2024 B r2 | 0.81687 | 0.67852 | 0.13836 | 0.01780 | 0/5 | 5/5 |
| Dots 2024 B r3 | 1.68061 | 1.56516 | 0.11545 | 0.01852 | 0/5 | 5/5 |
| Dots 2024 B r5 | 4.39048 | 4.33936 | 0.05113 | 0.02977 | 1/5 | 5/5 |
| Dots 2024 B r6 | 6.04469 | 6.06293 | -0.01824 | 0.04181 | 2/5 | 5/5 |
| PatrasIQ cost | 5.32014 | 4.98551 | 0.33462 | 0.04120 | 0/5 | 5/5 |
| PatrasIQ population | 5.62551 | 5.52365 | 0.10186 | 0.06354 | 1/5 | 5/5 |
| Sounds | 0.68172 | 0.67411 | 0.00761 | 0.00724 | 2/5 | 5/5 |
| Sushi A | 14.26433 | 14.23722 | 0.02711 | 0.00870 | 0/5 | 5/5 |
| Sushi B | 14.23601 | 14.23999 | -0.00398 | 0.00657 | 3/5 | 2/5 |
| Wheat | 1.58081 | 1.43954 | 0.14126 | 0.02133 | 0/5 | 5/5 |

The [per-partition file](repeat_scores.csv.gz) contains only the two main methods, with two rows per paired prediction. The [summary CSV](summary.csv) also records n, r, development count N and availability. A split-win count is descriptive, not a binomial significance test.

## Interpretation

The mean favors SM in **10 tasks** and PL in **13 tasks**. Related tasks share participants and are not independent replications. The count does not establish statistically significant winners. Raw NLL differences at different report lengths r are not a common effect-size scale.

Representative results:

- Wheat: delta +0.14126, MCSE 0.02133, lower SM loss in 0/5 splits.
- PatrasIQ cost: delta +0.33462, MCSE 0.04120, lower SM loss in 0/5 splits.
- Puzzle, minimum 5 steps: delta -0.06934, MCSE 0.00523, lower SM loss in 5/5 splits.
- Sushi B: delta -0.00398, MCSE 0.00657, lower SM loss in 3/5 splits.
- Dots 2024 B r6: delta -0.01824, MCSE 0.04181, lower SM loss in 2/5 splits.

The last two comparisons illustrate why a favorable mean can be poorly resolved relative to its MCSE. Five repetitions estimate partition variance with only four degrees of freedom. Neither their observed range nor interpolated tail quantiles provide a population confidence interval. The report therefore shows the five-score **minimum and maximum**, alongside MCSE, in its precision table. Small differences should remain descriptive.

There are **112/115 certified likelihood centers**. All five centers are certified for 22 tasks; Sushi B has 2/5 certificates. Its other centers are explicitly approximate, so that comparison evaluates an implemented fitting procedure rather than certified exact MLE. Training-objective gaps are not test-loss error bounds.

![P0: five grouped allocations, bars are one partition MCSE](../../figures/predictive/primary.png)

## Uncertainty and boundaries

Mean-level CI fields are empty. Figure bars are **±1 MCSE**, not 95% population CIs. Within each eligible split, 2,000 paired bootstrap draws resample complete test units while both models remain fixed. Ratio losses are report-weighted. Percentiles 2.5 and 97.5 give nominal conditional test-sampling CIs under independent-unit sampling. They preserve within-person dependence but omit training and tuning uncertainty. These CIs cover 65 paired contexts across 13 identified tasks. Beans, Wheat and the eight anonymous PrefLib tasks have no supported sampling CI. Bootstrap endpoints are not averaged across splits.

Five random allocations do not enforce seasonal or demographic balance, establish independence of anonymous assessors, or validate future-year transfer. [G1](../../docs/group_sensitivity.md) and [T1](../../docs/temporal_prediction.md) address different targets. The [full-data characteristics](../../data/features/predictive_comparison.md) describe all observations; they do not choose these predictors or causally explain their performance.

P0 does not require Sharp or a sieve. Missing supplementary E0/L0/S0 fits are not missing main comparisons. See their separate reports for availability and computation limits.
