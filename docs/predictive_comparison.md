# P0: main experiment — Algorithm 4.1

[Study guide](../README.md) · [Main results and analysis](../results/main/README.md) · [Data](../data/README.md) · [Learning curves](predictive_learning.md) · [Supplementary evidence](supplementary.md)

**P0 is the study's only main experiment: manuscript Algorithm 4.1.** Its two competitors are whole-ranking likelihood-center SM and tuned ridge PL. Sharp, Fotakis and Efficient belong to [E0](estimator_comparison.md); global pair-sieve belongs to [B0](sieve_computation.md). They share allocations but are not part of this main comparison.

## Question and observation

P0 compares how selective Mallows and Plackett–Luce predict a complete noisy ordering **of the items actually displayed**. Both families receive the same training rankings and score the same held-out rankings, conditioning on each report's displayed set. A ranking of ten displayed items is different from a censored top-three response to those ten. The eligible sources are described in the [data catalogue](../data/README.md); no top-k censoring is silently recoded as a smaller display.

There are 23 empirical tasks, including separately coded difficulty conditions, dots2024 arms and report sizes, and Sushi A/B. A task is not necessarily an independent study. The current reporting budget uses fixed repetition IDs 0–4, without choosing allocations by their outcomes. [Fit provenance](../results/provenance/README.md) records the producer versions. Its prediction target is a new allocated unit from the same sampled task population, rather than transfer to another year, location or task.

## Five outer allocations, with training-only tuning

For U allocation units, use the prespecified permutation indexed by root seed 202609280, task split key and repetition b=0,...,4. Define a=floor(0.6U), c=floor(0.8U).

| Permutation positions | Purpose |
|---|---|
| First a units | Inner training: fit each PL penalty candidate |
| Next c−a units | Inner validation: select the PL penalty by whole-ranking NLL |
| First c units together | Development: refit PL with its selected penalty; fit each SM center and dispersion |
| Final U−c units | Outer test: evaluate the prespecified competitors |

Algorithm 4.1 requires chronological splitting **for forecasting**, not for every predictive target. P0 uses repeated random grouped allocations for same-population prediction; [T1](temporal_prediction.md) addresses future years/seasons.

Thus the final predictors use 80% of units. The 60/20 division lies entirely inside this development set. Validation chooses a parameter **within PL**, not a winner between SM and PL. SM's dispersion bound and center methods are fixed in advance. No method or hyperparameter is chosen using outer-test outcomes. Each repetition fits a different predictor; the study averages their scores, not their probabilities into an ensemble.

| Tasks | Allocation unit | Alignment and limits |
|---|---|---|
| Beans, Wheat | Anonymous report row | Farmer/village dependence cannot be reconstructed |
| PrefLib Dots 2013 and Puzzle | Expanded anonymous ranking report | Recorded multiplicity is preserved; person identity is unavailable |
| Sushi A/B | Source respondent row | The two tasks share the same respondent permutation |
| dots2024 | Reconstructed participant block | The four sizes in each arm share participant allocations |
| Sounds | Source assessor ID | All thirty reports from a person move together |
| PatrasIQ | One-report-per-volunteer row within each task | Cross-task person matching is unavailable |

Every available person's reports stay in one partition. Anonymous rows are a computational allocation rule, not an assertion of independent people. All source reports and catalogue items remain eligible. There is no reshuffle to improve coverage or obtain a finite estimate.

Year, season, climate, location, demographics and displayed-set category are not fitted covariates or stratification variables in P0. Repeating allocations reduces dependence on one particular split but does not enforce exact covariate balance or remove confounding. [Group](group_sensitivity.md) and [temporal](temporal_prediction.md) analyses address distinct targets.

## Prespecified fitting procedures

For SM, let D(pi) be the sum of Kendall inversions between each development ranking and pi restricted to its own display. The primary center minimizes D when an exact solution is available. For n<=18 use exact subset dynamic programming. For larger catalogues, initialize with five deterministic insertion searches, then attempt the integer linear-order formulation for 30 seconds. Keep the best objective and a valid lower bound. Equal integer bounds certify exactness; a nonzero gap is explicitly an **approximate likelihood-center fit**. A timed-out solve is not reported as exact MLE.

All SM center variants use the same finite dispersion rule:

```math
\widehat\beta=\arg\min_{0\le\beta\le10}
\left\{\beta D(\widehat\pi)+N\log Z_r(\beta)\right\},\qquad
Z_r(\beta)=\prod_{j=1}^{r}\sum_{v=0}^{j-1}e^{-\beta v}.
```

The fixed cap 10 makes prediction finite even when the training reports agree perfectly. It is a declared practical bound, not a constant supplied by the minimax theorem. It is not selected after seeing a boundary fit or a test error. The selected value, zero/cap/interior status and training objective are saved for every fit.

PL minimizes the regularized listwise objective on the **sum** scale:

```math
\widehat\theta_\tau=\arg\min_{\sum_i\theta_i=0}
\left\{\sum_{t=1}^{N}-\log P_{\mathrm{PL}}(Y_t\mid S_t,\theta)
+\frac\tau2\sum_i\theta_i^2\right\},\qquad
\tau\in\{0.01,0.1,1,10,100\}.
```

Positive ridge gives a unique finite parameter vector even with unobserved items or a disconnected comparison graph. Choose tau by inner-validation NLL and refit on the full development partition. An exact validation tie uses the first grid value. The same grid is used across tasks and sample sizes; because the data objective is a sum, a fixed tau has relatively greater influence at small N. Independent gradient checks verify numerical convergence, including a Newton refinement of the same objective when necessary.

## Separate estimator supplement

[E0](estimator_comparison.md) evaluates Sharp, Fotakis and an admitted Efficient fallback on the same allocations, with their own results and availability. [B0](sieve_computation.md) describes the global pair-sieve. These are not steps required by Algorithm 4.1 and are not candidates from which P0 chooses a winner. No sieve computation is needed to produce P0's main comparison.

## Loss, averaging and intervals

For each outer-test report t, score the complete reported ranking:

```math
\ell_{M,b,t}=-\log P_M(Y_t\mid S_t;\widehat\vartheta_{M,b}),\qquad
\Delta_b=\frac1{T_b}\sum_{t\in\mathcal T_b}
(\ell_{\mathrm{SM},b,t}-\ell_{\mathrm{PL},b,t}),\qquad
\overline\Delta=\frac1{5}\sum_{b=1}^{5}\Delta_b.
```

Negative delta favors SM. Test pairs are never treated as independent observations. Report length affects the scale of whole-ranking loss; a larger numerical gap at r=10 is not automatically a stronger scientific effect than one at r=2. The P0 table therefore also gives delta / log(r!) and its scaled MCSE beside the raw difference. This dimensionless uniform-reference ratio uses the fixed displayed/report size r, not catalogue n. [Definition and limits](criteria.md#uniform-reference-scaled-loss-difference).

Two different kinds of uncertainty are saved:

1. **Partition precision and spread.** The MCSE is SD(delta_b)/sqrt(5); split quantiles are the empirical 2.5th and 97.5th percentiles. Conditional on the fixed dataset, independently generated permutations justify the Monte Carlo SE for their average. The overlapping observations do not create five independent population samples. Neither this SE nor the split range is a population sampling CI.
2. **Conditional test-unit bootstrap.** Within one split, keep fitted parameters fixed and resample the G identified test units with replacement 2,000 times, using identical draws for both models. If A_g is a unit's sum of paired losses and B_g its report count, each draw is sum(A_g*)/sum(B_g*). Its 2.5th and 97.5th percentiles form a nominal 95% conditional interval. Independent sampled clusters with finite-variance losses motivate this empirical-distribution approximation; within-person dependence is retained. Small G and nonrepresentative sampling limit coverage. These intervals do not include training or tuning variability and are not averaged into a CI for the five-split mean.

No anonymous-row population CI is supplied for Beans, Wheat or the eight PrefLib tasks. Known units support an assumption about independence; identifiers alone do not prove it. Cross-task intervals are pointwise, without a multiple-comparison correction. See the shared [uncertainty guide](uncertainty.md).

## Reading results and reproducing them

Start with the [independent P0 report and 23-task table](../results/main/README.md). [P0 summary.csv](../results/main/summary.csv) contains only the main likelihood-center comparison and its paired PL reference; [per-partition scores](../results/main/repeat_scores.csv.gz) contain exactly the two main methods. [E0](../results/estimator_comparison/README.md) has separate estimator tables. The raw `results/predictive/primary.csv` retains mixed-method allocation records solely for reproducibility; its filename does not classify every row as a main result. The [result dictionary](../results/predictive/README.md) locates per-repetition intervals, fitted parameters, optimization bounds and code/source fingerprints. A summary mean is left unavailable when not all planned repetitions are available; a separately named conditional mean is not substituted for it.

All 115 primary SM/PL paired predictions are finite. The likelihood center is certified in every repetition of 22 tasks, and in 2/5 Sushi B repetitions. Those 115 paired predictions are the complete main result. The separate E0 report records Sharp availability and Fotakis admission; their exclusions do not remove a P0 result. [Findings](findings.md) interprets the observed differences alongside these limits.

The [five-allocation precision report](../results/main/split_precision.md) gives each task’s MCSE and observed range. Five is a computation budget, not a threshold guaranteeing stable conclusions; the sample SD has only four degrees of freedom. Split percentiles based on five values are coarse descriptive summaries.

P0 is the main Algorithm 4.1 comparison. The unpenalized P1 comparison and fixed-fit P2 diagnostics remain [supplementary](supplementary.md), with their own fitting rules and inference targets. They are not independent replications of P0: P0 reuses the same source data and outer test allocations. Mechanism simulations, group controls and temporal transfer retain the additional questions they answer.
