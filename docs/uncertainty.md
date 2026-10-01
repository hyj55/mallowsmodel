# Uncertainty, confidence intervals and resampling

[Experiment map](experiments.md) · [Criteria](criteria.md) · [Data identities](../data/README.md)

## Identify the target before reading a bar

A fitted model's performance on new respondents, a learning procedure's average performance over newly collected training samples, and the average over random partitions of one fixed dataset are different quantities. No single interval in this study covers all three.

| Experiment/output | Random unit used in its uncertainty calculation | Calculation | Interpretation |
|---|---|---|---|
| P1 repeated prediction | Random partition of the same fixed source data | Mean ± **one** SD/√30 in figures | Conditional partition Monte Carlo precision; not a 95% CI |
| G1 group comparison | Refit outcome across randomized partitions | 5th–95th percentiles; figure center is median | Central 90% empirical split range; not a CI |
| P2 identified-unit prediction/shells | Held-out person or whole report, with fitted models fixed | 2,000 paired bootstrap draws; 2.5th–97.5th percentiles | Pointwise nominal 95% conditional interval |
| P2 context slope | Whole ranking report, with ranking-model parameters fixed | 2,000 report bootstrap draws; refit diagnostic slope | Exploratory plug-in percentile interval |
| L1/L2 and regularized C1 empirical summaries | Held-out report after averaging its losses over saved training fits | 2,000 paired report bootstrap draws | Conditional on the particular fitted model collection |
| S1/S2, S3 per-cell means | Independent generated training/evaluation repetition | Student-t mean interval, R=40 or 30 | Monte Carlo uncertainty for a specified simulation mean |
| D2 prediction means | Independent generated training dataset | Student-t mean interval, R=200 | Monte Carlo uncertainty for mean population loss difference |
| D2 within-repetition context diagnostic | Whole diagnostic report | 499 bootstrap draws | One repetition's nominal 95% slope/residual interval |
| D2 detection/rejection/correctness rates | Independent simulated repetition with defined outcome | Wilson 95% binomial interval | Probability of that event, conditional on availability where required |
| T1 ATP, one season | Held-out tournament | 2,000 whole-tournament bootstrap draws | Conditional interval assuming independent tournament clusters |
| T1 ATP, ten-season mean | Annual paired loss difference | Student-t interval with ten yearly values | Working across-season interval; serial/player dependence is unresolved |
| Five-fold Beans/Sushi control | Five disjoint test folds | Pooled point estimate and fold minimum/maximum | Descriptive comparison; no independent-fold CI |

All stated confidence levels are pointwise, without adjustment for the many tasks, methods, budgets and diagnostics. They are not posterior probabilities that one model is true. A 95% confidence procedure concerns repeated-sampling coverage under its assumptions. Approximate procedures need not attain 95% in a small or dependent sample.

## Paired whole-report bootstrap

Fix trained SM and PL models. For T test reports compute dₜ=ℓSM,t−ℓPL,t and Δ̂=T⁻¹Σₜdₜ. For each b=1,…,B:

1. Draw T indices independently and uniformly **with replacement** from {1,…,T}.
2. Use the same indices for both models, equivalently select the precomputed paired d values.
3. Compute Δ*b as their mean.

The interval is

```math
[Q_{.025}(\Delta^*_1,\ldots,\Delta^*_B),\ Q_{.975}(\Delta^*_1,\ldots,\Delta^*_B)],\qquad B=2000.
```

A size-T draw contains repetitions and omissions; it is not a permutation of all T reports. Neither the ranking center, β nor PL worths is re-estimated in this bootstrap. Shell components and other report-level means use the same construction on their corresponding report contributions.

**Why this construction is reasonable:** for independent, identically distributed sampling units with finite-variance losses, the empirical distribution approximates the sampling population; resampling it approximates the sampling variation of a mean. Pairing retains the covariance between the two models' losses. Percentile endpoints are an asymptotic approximation, not an exact finite-sample guarantee. See [Efron's bootstrap formulation](https://doi.org/10.1214/aos/1176344552). Fixing the fit defines the target as conditional predictive performance; it does not estimate training-sample variability.

P2 uses one report per person in each Sushi task (T=1,000), dots2024 arm/size task (T=60), and PatrasIQ task (T=79). These justifications are per task. Shared people across Sushi A/B, PatrasIQ tasks, or dots2024 sizes prevent treating task-level results as independent replications. Observational sampling and source selection may also limit population generalization.

## Whole-person and tournament bootstrap

For cluster g, let Aᵍ=Σₜ∈g dₜ and Bᵍ be the number of scored reports. Draw G cluster IDs J₁,…,Jᴳ with replacement from the G held-out clusters, and calculate

```math
\Delta^*=\frac{\sum_{j=1}^{G}A^{J_j}}{\sum_{j=1}^{G}B^{J_j}}.
```

Repeat 2,000 times and take percentile endpoints. Every report of a selected cluster travels together, including when the cluster is selected more than once. The ratio targets mean **report** loss; averaging cluster means with equal weights would target a different quantity when cluster sizes differ.

For Sounds P2, G=10 assessors and Bᵍ=30 for each. For ATP, G is the held-out season's tournament count and tournament sizes vary. The cluster bootstrap is justified by treating the clusters as independently sampled units while allowing arbitrary dependence inside each cluster. Ten Sounds test people provide limited precision; tournament grouping does not account for a player appearing in multiple tournaments.

Sounds pair-profile intervals use the same ratio with Aᵍ equal to the sum of observed agreements in a training-defined bin and Bᵍ the number of bin occurrences. People with no occurrence in that bin remain in the sampling frame with zero numerator/denominator. Draws with zero total denominator are unavailable. The fitted model probabilities remain fixed. See `unit_interval` in [the implementation](../src/validation_extension.py).

ATP strength-bin and calibration-bin observed-frequency intervals use the same ratio bootstrap on year–tournament identifiers, preserving matches inside each contributing cluster. The bins are held fixed from fitted predictions. Because these calculations first restrict to a bin, their resampling frame consists of clusters represented in that bin; it is not a bootstrap over all possible seasons, players or future bins. Sparse bin counts and players recurring across tournaments remain limitations. Mean predicted probabilities and paired-loss point columns do not acquire CIs merely because an observed-frequency interval appears beside them.

## Context-slope bootstrap

The [context criterion](criteria.md#context-slope) uses all eligible pair occurrences from each report. Eligibility is determined from the original diagnostic sample using displays and the frozen reference order: at least two gap levels, each seen at least twice within a pair or pair × stratum cell.

For each bootstrap draw, sample complete reports with replacement. A report's multiplicity weights **all** its pairs. Recompute the within-cell weighted means and the diagnostic slopes for observed outcomes, fitted SM probabilities and fitted PL probabilities. The center, dispersion, worths, reference choice and eligible-cell list are fixed.

Residual intervals use the paired differences inside each draw:

```math
\gamma^*_{obs,b}-\gamma^*_{SM,b},\qquad
\gamma^*_{obs,b}-\gamma^*_{PL,b}.
```

They are not obtained by subtracting endpoints of separate intervals. If a draw has zero remaining within-cell gap variance, it is undefined. Only draws with all three finite slopes enter the quantiles, and `valid_bootstraps` records the count. With no original eligible variation the diagnostic is unavailable, not zero.

P2 uses B=2,000 where independent report units are supported. D2 uses B=499 **inside each independent simulation repetition**. Budgets of 60, 200 and 1,000 reports are nested prefixes of the same diagnostic sample. The 499 draws are not independent training experiments. Regularized Beans/Sushi diagnostic analyses use the same report indices across their saved training repetitions and average the relevant diagnostic draws.

**Theoretical scope:** report resampling preserves within-report pair dependence. A ratio/slope bootstrap can approximate uncertainty when independent units supply enough stable within-cell variation and denominators remain away from zero. Freezing estimated centers and data-dependent eligibility omits their uncertainty. Sparse cells can make this approximation poor. D2 explicitly finds failure: at ρ=.90 and diagnostic budget 60, only 143/200 adjusted diagnostics are available, and 30.8% reject the true zero effect despite a nominal 5% test. These intervals remain exploratory. This calibration result does not test the separate whole-ranking NLL bootstrap.

## Partition Monte Carlo standard error

For P1, let Dᵇ be the mean paired confirmation loss after fitting on partition b. The dataset is fixed; partition seeds are independently randomized. When all R=30 values are finite,

```math
\bar D=\frac1R\sum_bD^b,\qquad
s_D^2=\frac1{R-1}\sum_b(D^b-\bar D)^2,\qquad
MCSE=\frac{s_D}{\sqrt R}.
```

This follows from Varpartition(D̄ | data)=Varpartition(D | data)/R for independent partition draws conditional on the observed data and specified fitting rules. Reusing people across partitions does not invalidate this **conditional Monte Carlo** target. It does prevent interpreting those R partitions as R independent collections of people.

The [P1 figure](../figures/repeated_holdout/confirmation_means.png) plots **D̄ ± MCSE**, not ±1.96 MCSE and not a population confidence interval. The point is an average of separately trained models' losses, not an ensemble's log loss. Increasing R reduces integration error over partitions; it does not make a finite source sample arbitrarily informative about a population.

P1 does not bootstrap within partitions, average bootstrap endpoints, or combine a P2 CI with a P1 mean. Its diagnostic records use zero bootstrap draws and aggregate descriptive point estimates only. Different bins/eligible diagnostics can contribute different numbers of repetitions.

## Group split percentiles

G1 refits on 100 primary 70/30 within-group partitions, 20 partitions each at 50/50 and 80/20, and 100 separate whole-group holdouts. For each scalar metric, the summary retains finite repetition values and computes mean, median, Q.05, Q.95 and the fraction below zero. Figures show the median and [Q.05,Q.95]; tables generally show means.

These quantiles describe the spread of **individual split outcomes**, not uncertainty in their mean. They contain the central 90% of the observed finite-result distribution, not a 95% CI. No independent-splits t test is used. Local/reference interactions use common four-way finite report masks within a repetition; missing or infinite outcomes and coverage are reported separately. A narrow conditional range with very poor coverage is not evidence of good unconditional performance.

## Student-t simulation intervals

For a fixed generating law, catalogue, report size, training budget and estimator, obtain one scalar Zᵇ per independent generated repetition. Use

```math
\bar Z\ \pm\ t_{.975,R-1}\frac{s_Z}{\sqrt R}.
```

S1/S2 use R=40; D2 predictive means use R=200; S3 uses R=30 per specified generated cell (rounded duplicate exposure designs can yield 60). Pair SM and PL within each repetition **before** calculating a Δ interval. Discovery-budget comparisons also take within-repetition regret differences before calculating an interval across repetitions.

The t pivot is exact for independent normally distributed scalar outcomes with unknown variance and is used here as an approximate mean interval justified by independent repetitions and a finite-variance central-limit approximation. Forty or 200 repetitions do not guarantee normality or immunity to heavy tails. See [NIST's mean-interval definition](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm). The normality concerns the scalar repetition distribution, not whether rankings are Gaussian.

S1/D2 use exact population loss per fit, so their loss intervals contain training/estimation Monte Carlo variation without finite-test error. S2/S3 empirical test means contain both training and fresh-test variation. S3 n=10 budgets share a nested training stream and test sample within a repetition; each fixed-budget mean has 30 independent repetitions, but budgets are not mutually independent experiments.

S1/S2 also use this t formula for some binary selector-correctness averages. Such intervals are approximations and may extend beyond [0,1]; they should not be confused with D2's Wilson intervals.

## Wilson intervals for rates

In D2, each independent repetition provides a binary event: positive detection, rejection of zero, rejection of the fitted SM slope, or correct model selection. If K repetitions have a defined event and x are successes, p̂=x/K. With z=Φ⁻¹(.975), the interval is

```math
\frac{\hat p+z^2/(2K)\ \pm\ z\sqrt{\hat p(1-\hat p)/K+z^2/(4K^2)}}{1+z^2/K}.
```

This is the inversion of the binomial score test, not a bootstrap over the 499 inner draws. It respects probability boundaries and avoids the zero-width Wald interval at zero observed events, but is still not an exact-coverage binomial interval. [Wilson score construction](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm).

K is the metric's actual available count, not automatically 200. Thus rejection rates among 143 available diagnostics target an availability-conditional probability. The graph's Wilson bars describe uncertainty in the rate, not a single diagnostic slope. With K=0 there is no interval. D2's stored average slopes, model-predicted slopes and regret means do not all have attached mean CIs.

## Learning-curve and temporal intervals

For L1/L2 and related fixed-test empirical controls, multiple trained fits share a test set. First calculate the per-report average paired loss

```math
\bar d_t=\frac1R\sum_{b=1}^{R}(\ell_{SM,b,t}-\ell_{PL,b,t}),
```

then apply the 2,000-draw report bootstrap to the vector of d̄ values. L1 has R=5 for Beans/Sushi A and R=3 for Sushi B; L2 has R=5. These intervals condition on that fitted collection. They do not resample the training subsets or quantify outer-split variability. Averaging log losses is also different from scoring averaged probabilities.

Beans year transfer uses five permutations of the same 2015 training reports, the same 2016 test rows, and that same test-only bootstrap. Missing farmer IDs make its saved endpoints assumption-dependent descriptive evidence, not a verified cluster-valid CI. The five-fold control reports no fold-based CI.

ATP's season-level bootstrap is described above. Across seasons, the reported mean gives each of ten years equal weight and applies a t interval to ten annual paired differences, with nine degrees of freedom. This is a working independence approximation; repeated players, evolving abilities and serial dependence mean it is not a validated time-series or new-season coverage guarantee. The same caveat applies to its common-order seasonal aggregate.

## Nonfinite results and denominators

- **P1:** any undefined repetition makes the full mean unavailable; all-defined results retain infinite loss. The full MCSE requires all 30 values finite. `finite_conditional_mean` and its MCSE use only K finite repetitions, dividing their SD by √K. Finite-report summaries are separately named and have another denominator.
- **S1/S2:** full mean CIs require all repetitions finite. `finite_conditional` intervals apply the t formula to K finite values with K−1 degrees of freedom. This changes the estimand.
- **D2 prediction:** full t intervals require all values finite; a finite-conditional mean and counts are saved, without a separate finite-conditional CI in that table.
- **P2 bootstrap:** ordinary predictive intervals are not supplied when required paired losses are nonfinite or independent sampling units cannot be justified.
- **G1:** finite report masks and finite repetition values determine descriptive summaries; all coverage and failure counts must accompany them.

An unbounded SM fit can put probability one on a center ordering after a zero-disagreement training sample. With a full-support generating law, this has positive probability at finite N and can make unconditional expected plug-in log loss infinite. Observing all-finite outcomes in a finite simulation does not establish finite unconditional expected loss; center-risk means are a different target.

## Metadata limitations and what is not estimated

Beans has no farmer ID. Anonymous PrefLib records lose cross-trial worker identities; recovering a stimulus-set filename does not recover people. Wheat has redacted names and 113 missing village labels. Their unverified report/cluster intervals are not used for inferential conclusions; corresponding P2 CI fields are absent or empty. Repeating partitions cannot repair unidentified sampling units.

The study does not estimate a population sampling CI for the complete 30-partition learning procedure, perform a bootstrap that refits both models on resampled training populations, or correct intervals for source search and multiple testing. Seasons, locations and participant mixtures can change the target distribution even when omitted from model fitting. These limits define how the numerical intervals should be read; they do not alter the saved point estimates.
