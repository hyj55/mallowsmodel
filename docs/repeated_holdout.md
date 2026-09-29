# Repeated estimation of the original real-data comparisons

28 September 2026. [中文报告](repeated_holdout_zh.md) · [Results and field dictionary](../results/repeated_holdout/README.md) · [Existing learning curves](learning_curves.md).

The original active real comparison used one fixed training/discovery/confirmation partition per task. This amendment runs **30 new partitions and full refits for all 23 tasks**, and reports the average predictive loss. The target is better numerical estimation of average performance over random partitions, not a new study of sensitivity to choosing a split. The recently completed [trial/assessor sensitivity study](group_sensitivity.md) remains separate and unchanged.

The [protocol](protocols/REPEATED_HOLDOUT_20260928.md) was committed before production fits at [3da7e993](https://github.com/hyj55/mallowsmodel/commit/3da7e993c9ce2ae23a85a418cfa19ac2b138f01d), based on main [551368d4](https://github.com/hyj55/mallowsmodel/tree/551368d48a0b87e7f8573d0f28efa1ac66e4c625). Existing numeric result files are preserved. Earlier real reports now point here for repeated average estimates; their bootstrap intervals still describe only their original frozen fits.

## Audit of what had already been repeated

| Earlier experiment | Original repetition | Action |
|---|---|---|
| Current Beans, Sushi A/B replacement | One 60/20/20 partition per task | 30 new partitions and full refits |
| 8 PrefLib Dots/Puzzle and 8 dots2024 tasks | One 60/20/20 partition per task | 30 new partitions and full refits |
| Wheat follow-up | One 60/20/20 partition | 30 new partitions and full refits |
| Sounds, PatrasIQ cost and population | One 60/20/20 unit partition per task | 30 new partitions and full refits |
| Strict synthetic study | 40 independent generated training datasets per cell, 4,760 in total | Already repeated; unchanged |
| Additional mechanism simulation | 200 independent generated training datasets per cell, 1,400 in total | Already repeated; unchanged |
| Recent trial/assessor study | 100 primary splits plus prespecified controls | Outside this request; unchanged |
| Historical real learning curves | 5 training subsamples for Beans/Sushi A; 3 for Sushi B; one fixed outer test set | Indexed, not rerun with retired estimators |
| Historical Beans/Sushi A outer-fold follow-up | Five disjoint test folds with refits | Already multiple train/test sets, but older fitting protocol; unchanged |

Resampling losses from a fixed test set 2,000 times does not change the training data or refit either model. It therefore did not solve the single-partition issue. SP-Rank source-only audits and the pre-fit Beaches exclusion contain no eligible fitted experiment to repeat.

## What changes and what stays fixed

Each repetition redraws a 60/20/20 split, refits all five original methods on the training part, uses discovery only for the already defined strict-feature selectors, and evaluates confirmation separately. Original integer rounding is retained. The root seed is 202609280; partition streams and estimator streams are separate. No split is retried or discarded because a model fails or performs poorly.

- Sushi A/B use the same respondent memberships in every repetition. Their results are paired across tasks, not independent population replications.
- Each dots2024 arm uses the same participant memberships across its four report lengths. Each separate r task still has fixed report length.
- Sounds assigns all 30 reports from an assessor to one partition: 27 assessors train, 9 discovery, 10 confirmation. It estimates prediction for held-out assessors, unlike the separate within-person sensitivity experiment.
- Beans, wheat and anonymous PrefLib retain their original report-level partition units. This does not solve unidentified person, year/season, trial or location dependence. No year/season balancing or new recovered-group stratification is silently added here; that would change the experiment beyond repeating its original allocation rule. Known groups are treated by the separate group study.
- PatrasIQ retains its documented one-report-per-volunteer-per-task units. Unknown cross-task identities are not invented.

Original strict reports, complete item catalogs, likelihoods, tuning settings and computational guards are unchanged. Metadata remain outside model fitting. Exact SM uses subset DP for n≤18 and certified integral optimization otherwise, retaining the 120-second limit. PL remains unpenalized Hunter MM. Literal Sharp, Section 3 efficient and clipped Borda remain separately named; no fallback or regularization is added. The original mechanically feasible Sharp evaluations do not certify its sparse-regime theorem. Efficient retains its original λ≤1 guard. This correction does not adopt the different estimator-admission policy of the group study.

## Primary average predictive performance

For repeat b, first compute the mean confirmation whole-ranking loss for each independently fitted model, and its paired difference Δ_b = NLL(SM_b) − NLL(PL_b) on the same reports. The primary estimate is the arithmetic mean of the 30 Δ_b values. Negative favors SM. The comparison below uses **exact/certified SM MLE**; all five methods are in [scores.csv](../results/repeated_holdout/scores.csv).

The reported Monte Carlo SE is SD(Δ_b)/sqrt(30), conditional on these fixed observed data and the partition generator. It measures remaining partition-averaging error. It is **not** a population confidence interval or evidence of 30 independent participant samples. Repeating partitions does not remove sampling bias, finite-data uncertainty, missing identities or outcome/display confounding. It also does not guarantee that the mean of 30 partitions equals the average over all possible partitions.

| Task | Mean PL NLL | Mean SM NLL | Mean Δ | Partition MCSE | Finite paired repeats | Original single Δ |
|---|---:|---:|---:|---:|---:|---:|
| Beans | 1.79388 | 1.80639 | +0.01251 | 0.00166 | 30/30 | -0.00118 |
| Sushi A | 14.24254 | 14.26809 | +0.02555 | 0.00353 | 30/30 | +0.01468 |
| Sushi B | 14.22534 | unavailable | unavailable | unavailable | 8/30 | -0.01726 |
| Wheat | 1.39564 | 1.54305 | +0.14741 | 0.01004 | 30/30 | +0.10069 |
| Sounds | 0.68718 | 0.69515 | +0.00797 | 0.00249 | 30/30 | +0.01919 |
| Patras Cost | 4.91841 | 5.19634 | +0.27794 | 0.02371 | 30/30 | +0.08173 |
| Patras Population | unavailable | 5.71790 | unavailable | unavailable | 29/30 | +0.06407 |
| Dots 2013: 200x3 | 3.12758 | 3.11438 | -0.01319 | 0.00221 | 30/30 | -0.02622 |
| Dots 2013: 200x5 | 3.06009 | 3.04544 | -0.01466 | 0.00212 | 30/30 | -0.00545 |
| Dots 2013: 200x7 | 2.90972 | 2.89800 | -0.01172 | 0.00264 | 30/30 | -0.03453 |
| Dots 2013: 200x9 | 2.85147 | 2.81740 | -0.03407 | 0.00350 | 30/30 | -0.04955 |
| Puzzle: 11/14/17/20 | 3.08879 | 3.07802 | -0.01077 | 0.00263 | 30/30 | +0.01591 |
| Puzzle: 5/8/11/14 | 2.87745 | 2.81989 | -0.05756 | 0.00301 | 30/30 | -0.07702 |
| Puzzle: 7/10/13/16 | 2.86100 | 2.84079 | -0.02021 | 0.00318 | 30/30 | -0.04010 |
| Puzzle: 9/12/15/18 | 3.03466 | 3.02470 | -0.00996 | 0.00267 | 30/30 | -0.01055 |
| Dots 2024 A, r=2 | unavailable | 0.79619 | unavailable | unavailable | 14/30 | unavailable |
| Dots 2024 A, r=3 | 1.37654 | 1.54831 | +0.17177 | 0.01645 | 30/30 | +0.05592 |
| Dots 2024 A, r=5 | 4.06336 | 4.17019 | +0.10684 | 0.01590 | 30/30 | +0.20344 |
| Dots 2024 A, r=6 | 5.52788 | 5.63072 | +0.10285 | 0.02151 | 30/30 | +0.34964 |
| Dots 2024 B, r=2 | unavailable | 0.86744 | unavailable | unavailable | 23/30 | +0.08869 |
| Dots 2024 B, r=3 | 1.66156 | 1.79990 | +0.13834 | 0.01859 | 30/30 | +0.28998 |
| Dots 2024 B, r=5 | 4.40227 | 4.45454 | +0.05227 | 0.01680 | 30/30 | +0.15321 |
| Dots 2024 B, r=6 | 6.13215 | 6.11659 | -0.01556 | 0.02202 | 30/30 | -0.12607 |

“Unavailable” in the all-30 mean means at least one required predictor was unavailable. A defined predictor assigning zero probability has infinite loss instead. Neither is converted to a finite value or silently dropped. For comparisons with fewer than 30 finite paired repetitions, the separate conditional table below is descriptive and must not be called an all-repetition winner.

| Task | Finite paired repeats | Conditional mean Δ | Conditional partition MCSE | Successful SM fits | Successful PL fits |
|---|---:|---:|---:|---:|---:|
| Sushi B | 8/30 | +0.01086 | 0.01285 | 8/30 | 30/30 |
| Patras Population | 29/30 | +0.07527 | 0.02887 | 30/30 | 29/30 |
| Dots 2024 A, r=2 | 14/30 | +0.20081 | 0.03041 | 30/30 | 14/30 |
| Dots 2024 B, r=2 | 23/30 | +0.10420 | 0.01846 | 30/30 | 23/30 |

Nineteen tasks have all 30 finite exact-SM/PL comparisons. The numerical averages favor SM on all eight PrefLib tasks and favor PL on Beans, Sushi A, wheat, Sounds, PatrasIQ cost and five of the six dots2024 tasks with r≥3. Dots2024 B, r=6 has mean Δ=−0.01557 with partition MCSE 0.02202: even the precision of this fixed-data partition average is limited, so its sign should not be emphasized. These are predictive point comparisons, not population-significance conclusions or a count of independent studies.

Beans illustrates the correction: the original Δ=−0.00118 becomes a 30-repeat average +0.01251 (MCSE 0.00166). Sushi A averages +0.02555 (0.00353), wheat +0.14741 (0.01004), and PatrasIQ cost +0.27794 (0.02371). The original single split is not an estimate of the partition average with negligible Monte Carlo error.

Four tasks do not have a complete all-repeat paired MLE average. Unpenalized PL lacks a unique finite estimate in 16/30 dots2024 A r=2 partitions, 7/30 B r=2 partitions and 1/30 PatrasIQ population partitions. Their conditional paired means use 14, 23 and 29 repetitions, respectively. All catalog items being observed is not sufficient: PL also needs the relevant comparison-graph condition. Sushi B obtains a certified exact SM center in **8/30** partitions; 22 fail the unchanged wall-clock certificate budget. Its conditional Δ=+0.01086 does not establish its average exact-SM performance across all 30 partitions. This certificate limit also depends on hardware and concurrent load; it is a computational outcome, not nonexistence of an SM optimum. Clipped Borda provides a separate all-30 Sushi B comparison, Δ=+0.00253 with MCSE 0.00509, and is not renamed MLE.

The 30-repeat score records contain no positive-infinite prediction losses in this particular run. Availability failures are still present and retained; the same code/tests distinguish actual infinite losses from missing fits. No fit was retried or a seed selected to obtain a preferred result.

![Recorded confirmation averages](../figures/repeated_holdout/confirmation_means.png)

The figure uses whole-ranking loss; effect sizes across different r or tasks are not a universal ranking of model superiority. Hollow points explicitly condition on available finite comparisons.

## Diagnostics, limits and verification

Context slopes, shell decompositions, pair profiles and discovery-selected confirmation losses are recalculated for every relevant repeat. Their averages are descriptive and conditional on availability; a particular gap/bin may not occur in all 30 repetitions. We do not average old bootstrap bounds, introduce new significance labels, or infer a generating mechanism from an average residual. Every method status, report denominator and retained-repeat count is published.

Completed **690 training contexts, 3450 candidate fits and 6900 held-out score rows**. All 37 source files passed checksum verification; 34 tests passed. Full saved-predictor replay verified every partition, parameter check, prediction, diagnostic and selector, and recomputed all six public tables without refitting. [Validation record](../results/repeated_holdout/validation.json).

Read-only CI verifies public hashes, counts, availability accounting and aggregation without requiring respondent data. Full local replay additionally reconstructs every membership, checks PL stationarity and SM profile dispersion/certificates, and recomputes predictions, diagnostic points and selectors from saved fits without refitting. Original reports and detailed fit/membership caches remain local; public outputs contain aggregate per-repeat scores. See [reproduction](reproducibility.md#repeated-estimation-of-the-original-real-comparison).

## Does varying the number of observations help?

Yes. Holding the item catalog n, report length r and evaluation design fixed, a learning curve can distinguish small-sample estimation/coverage difficulties from a gap that persists with more training observations. Neither the realized curve nor the SM−PL gap must be monotone. Sushi A is computationally cleaner (same ten items in each report); Sushi B is the complementary selective-ranking task (ten of 100) but mixes sample size with coverage and fit/solver availability. Sushi A alone cannot test varying-display effects.

The requested empirical experiment **already exists for Beans and Sushi A/B**, with direct figure/table links and exact budgets in the [learning-curve index](learning_curves.md). It uses historical fitting rules and one fixed outer test set; it is not evidence for the current exact/unpenalized learning curve. Following the owner's permission to avoid duplicating an existing study, no new real learning curve is run in this amendment. Current strict synthetic studies already vary N with 40 independent training draws per cell; the additional validation uses 200 per cell at its two training sizes. These distinctions are explicit rather than treating different protocols as one experiment.
