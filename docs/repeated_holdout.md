# Predictive comparison across repeated data partitions

[Experiment P1](experiments.md) · [Data](../data/README.md) · [Methods](algorithms.md) · [Uncertainty](uncertainty.md#partition-monte-carlo-standard-error) · [Results](findings.md#empirical-prediction)

## Question and procedure

How well do separately fitted SM and PL models predict held-out whole rankings, averaged over random training allocations of the observed data? For each of 23 tasks, make 30 newly randomized 60/20/20 training/discovery/confirmation partitions. Fit each candidate anew on each training partition and evaluate on the same held-out reports. Confirmation mean NLL and the within-partition paired SM−PL difference are the primary predictive quantities.

The candidates are exact-center SM, Sharp, efficient, clipped Borda, and unpenalized PL. Their dataset-specific availability rules are in [the estimator allocation table](experiments.md#estimator-allocation-by-empirical-dataset). Exact is the prespecified main SM comparison; no candidate replaces it merely because it achieved smaller confirmation loss. Five candidate statuses are retained for every task/repetition, whether successful or unavailable.

## Sampling units and shuffling

For U distinct allocation units, permute their IDs with the task/repetition random stream. The first floor(.6U) train, the next floor(.8U)−floor(.6U) supply discovery, and the rest supply confirmation. Every report of a unit follows its allocation.

| Tasks | Allocation unit | Cross-task alignment |
|---|---|---|
| Beans, Wheat | Anonymous report row | None; unknown farmer dependence remains |
| PrefLib Dots/Puzzle | Expanded anonymous report | Separate conditions; no trial stratification in P1 |
| Sushi A/B | Respondent row | Same permutation for both tasks |
| dots2024 | Reconstructed participant block | Same permutation across four sizes within each arm |
| Sounds | Source assessor ID | Thirty reports travel together |
| PatrasIQ | Documented one-report-per-volunteer row within a task | Cross-task matching cannot be recovered |

Root seed 202609280 and the sequence `(root seed, task split key, repetition)` define partition streams. Original estimator randomization seeds are fixed separately from partition randomness. A report's item order is never shuffled. No split is rerolled to achieve a finite fit or better coverage.

Year, season, temperature, coordinates, demographic attributes and displayed-set categories are not P1 stratification variables. Repeated randomization reduces the numerical influence of one allocation, but does not guarantee their exact proportions or address time/geographic transfer. G1 and T1 answer the corresponding distinct group/temporal questions.

## Task sizes

N, discovery and confirmation are report counts. For Sounds these represent 27, 9 and 10 whole assessors. λ and μ use training N, not M. Observed pair counts vary across partitions even when these design averages are constant.

| Task | M | n | r | N / discovery / confirmation | λ | μ |
|---|---:|---:|---:|---|---:|---:|
| `beans` | 842 | 10 | 3 | 505 / 168 / 169 | 33.6667 | 151.5000 |
| `sushi_a` | 5000 | 10 | 10 | 3000 / 1000 / 1000 | 3000.0000 | 3000.0000 |
| `sushi_b` | 5000 | 100 | 10 | 3000 / 1000 / 1000 | 27.2727 | 300.0000 |
| `00024-00000001` | 795 | 4 | 4 | 477 / 159 / 159 | 477.0000 | 477.0000 |
| `00024-00000002` | 794 | 4 | 4 | 476 / 159 / 159 | 476.0000 | 476.0000 |
| `00024-00000003` | 800 | 4 | 4 | 480 / 160 / 160 | 480.0000 | 480.0000 |
| `00024-00000004` | 794 | 4 | 4 | 476 / 159 / 159 | 476.0000 | 476.0000 |
| `00025-00000001` | 793 | 4 | 4 | 475 / 159 / 159 | 475.0000 | 475.0000 |
| `00025-00000002` | 795 | 4 | 4 | 477 / 159 / 159 | 477.0000 | 477.0000 |
| `00025-00000003` | 795 | 4 | 4 | 477 / 159 / 159 | 477.0000 | 477.0000 |
| `00025-00000004` | 797 | 4 | 4 | 478 / 159 / 160 | 478.0000 | 478.0000 |
| `dots2024_A_r2` | 300 | 30 | 2 | 180 / 60 / 60 | 0.4138 | 12.0000 |
| `dots2024_A_r3` | 300 | 30 | 3 | 180 / 60 / 60 | 1.2414 | 18.0000 |
| `dots2024_A_r5` | 300 | 30 | 5 | 180 / 60 / 60 | 4.1379 | 30.0000 |
| `dots2024_A_r6` | 300 | 30 | 6 | 180 / 60 / 60 | 6.2069 | 36.0000 |
| `dots2024_B_r2` | 300 | 30 | 2 | 180 / 60 / 60 | 0.4138 | 12.0000 |
| `dots2024_B_r3` | 300 | 30 | 3 | 180 / 60 / 60 | 1.2414 | 18.0000 |
| `dots2024_B_r5` | 300 | 30 | 5 | 180 / 60 / 60 | 4.1379 | 30.0000 |
| `dots2024_B_r6` | 300 | 30 | 6 | 180 / 60 / 60 | 6.2069 | 36.0000 |
| `wheat` | 493 | 16 | 3 | 295 / 99 / 99 | 7.3750 | 55.3125 |
| `sounds` | 1380 | 12 | 2 | 810 / 270 / 300 | 12.2727 | 135.0000 |
| `patras_cost` | 392 | 36 | 6 | 235 / 78 / 79 | 5.5952 | 39.1667 |
| `patras_population` | 392 | 48 | 6 | 235 / 78 / 79 | 3.1250 | 29.3750 |

## Averaging and availability

For partition b, score Dᵇ=Tᵇ⁻¹Σₜ(ℓSM,b,t−ℓPL,b,t), then average Dᵇ over the 30 partitions. The point estimate is not obtained by evaluating an ensemble or by pooling different available SM and PL partition sets.

A full mean is undefined if any required fit is unavailable. A defined infinite predictive loss remains infinite. Separate finite-conditional averages and counts describe the subset of finite comparisons; finite-report averages inside a partition have another denominator. These alternatives are clearly named in [the output dictionary](../results/repeated_holdout/README.md).

The figure shows mean ±1 partition Monte Carlo SE, SD(Dᵇ)/√30 when all 30 are finite. For conditional summaries the finite count replaces 30. This is precision over partition randomization given the fixed dataset, not a 95% population CI. No inner bootstrap is run.

## Diagnostics and selection

The same fits also supply descriptive context slopes, shell components and pair-profile averages for the tasks where those statistics are defined. Fitted/objective reference conventions are unchanged across repetitions. The 16 PrefLib/dots2024 tasks also make discovery-only pair/context model selections and score the selected candidate on confirmation. A missing diagnostic is not assigned zero, and bin-specific averages can have fewer than 30 contributing partitions.

## Recorded outputs

The run has 690 task/partition contexts, 3,450 candidate fit statuses and 6,900 method-by-held-out-split score rows. [Scores and counts](../results/repeated_holdout/scores.csv), [manifest](../results/repeated_holdout/manifest.json), [validation](../results/repeated_holdout/validation.json), and [reproduction](reproducibility.md) retain the sources, memberships, fitting rules and checks. The figures and interpretation are collected in [Findings](findings.md).
