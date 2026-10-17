# Findings across the study

[Design](experiments.md) · [Data](../data/README.md) · [Criteria](criteria.md) · [Uncertainty](uncertainty.md) · [Complete tables](../results/README.md)

Delta is SM minus PL whole-ranking NLL in nats/report; negative favors SM. Differences describe fitted procedures on specified evaluation populations. Neither a predictive advantage nor a descriptive feature identifies a generating model. Different ranking lengths are not on a common effect-size scale.

## Main experiment: Algorithm 4.1 (P0)

P0 is the only main experiment. Every task has five finite paired comparisons, for 115 in total. Fit on 80% development units, tune PL only inside development, and evaluate both families on identical outer tests. The [main report](../results/main/README.md) gives all 23 results, split-win counts and exact-center certificates.

The mean favors SM in ten tasks and PL in thirteen. These directions are not significance decisions; related tasks share observations or participants. The eight Dots 2013/Puzzle conditions favor SM on average. Wheat and PatrasIQ cost show clear PL-favorable directions relative to their partition MCSEs. Several other differences are poorly resolved.

- Puzzle, minimum 11 steps: Δ=-0.01042 (partition MCSE 0.00294).
- Wheat: Δ=+0.14126 (partition MCSE 0.02133).
- PatrasIQ cost: Δ=+0.33462 (partition MCSE 0.04120).
- Sushi A: Δ=+0.02711 (partition MCSE 0.00870).
- Sushi B: Δ=-0.00398 (partition MCSE 0.00657).
- Dots 2024 B r6: Δ=-0.01824 (partition MCSE 0.04181).

All five likelihood centers are certified for 22 tasks. Sushi B has 2/5 certificates; its other centers remain explicitly approximate. Its small loss difference cannot support a general family-winner conclusion. Optimization gaps bound training objectives, not test loss. Figures show ±1 partition MCSE, not population confidence intervals. Five values give only four degrees of freedom for estimating the split variance.

![P0: five allocations, partition MCSE bars](../figures/predictive/primary.png)

Identified test units support 2,000-draw paired bootstrap intervals inside each split, conditional on the fitted predictors. Those endpoints are not averaged into an interval for the five-fit mean. Anonymous sources retain unresolved dependence. Random allocation does not enforce seasonal or demographic balance.

## Supplementary estimator comparison (E0) and global sieve (B0)

Sharp completes five fits each for eleven tasks: Beans, Sushi A, Sounds and the eight Dots 2013/Puzzle conditions. The remaining twelve tasks have 60 explicit resource failures. B0's 55 available rows alias the same Sharp fits, because these schedules have no consumed pilot reports and one catalogue-wide terminal block. They are not additional independent fits.

Fotakis is admitted in 71/115 empirical contexts. Efficient is assessed independently of Sharp in all 115 contexts, with ten admitted depth-zero fits on dots2024 A/B r2 and 105 exclusions outside the lambda<=1 schedule domain. Global clipped Borda completes all 115 fits. The ten admitted Efficient fits equal Borda in order, dispersion and test predictions under the common tie rule; no positive-depth hierarchy is observed.

The [unified E0 comparison](../results/estimator_comparison/README.md) includes all methods, their availability and paired Borda contrasts. Against likelihood-center SM, Borda has lower five-allocation mean NLL in eleven tasks, equal mean in eight and higher mean in four. Dots 2024 B r2 has Borda-minus-likelihood delta -0.10832 (paired MCSE 0.01687); Wheat has +0.01894 (0.00765). Among the eleven tasks with complete Sharp results, Borda is lower in four and equal in seven. These are descriptive comparisons, not significance decisions or true-center risk tests. No outer-test winner is promoted to P0.

There are 155 unavailable Sharp contexts across E0 (60), L0 (15) and S0 (80), without double-counting aliases or linked endpoints. None has n≤10; the smallest missing catalogue is n=16. Thus no tuned-width variant is needed to complete the specified n≤10 scope. A and W_star retain the manuscript construction. These missing supplementary fits do not remove any P0 main result. [Exact computation and limitations](sieve_computation.md).

## Supplementary training-size and catalogue-size experiments (L0/S0)

L0 uses five aligned Sushi respondent allocations, nested development budgets and the same outer test within each repetition. Its SM likelihood-center differences are:

| Task | N | Mean delta | Partition MCSE |
|---|---:|---:|---:|
| sushi_a | 20 | -0.11349 | 0.09465 |
| sushi_a | 50 | -0.03070 | 0.09429 |
| sushi_a | 100 | +0.02638 | 0.01392 |
| sushi_a | 300 | +0.03691 | 0.00645 |
| sushi_a | 1000 | +0.03412 | 0.00800 |
| sushi_a | 3000 | +0.02962 | 0.00711 |
| sushi_b | 20 | +3.24335 | 0.36589 |
| sushi_b | 50 | +0.91086 | 0.11107 |
| sushi_b | 100 | +0.36112 | 0.03252 |
| sushi_b | 300 | +0.07580 | 0.02017 |
| sushi_b | 1000 | +0.03123 | 0.00771 |
| sushi_b | 3000 | -0.00221 | 0.00941 |
| sushi_a | 4000 | +0.02711 | 0.00870 |
| sushi_b | 4000 | -0.00398 | 0.00657 |

The comparison changes with training budget; realized curves need not be monotone. At small N, estimation, coverage and regularization matter alongside model specification. All Sushi A Sharp budgets are complete. Missing Sushi B Sharp points remain unavailable.

![Five-allocation Sushi curves](../figures/predictive/learning.png)

S0 uses twenty independent generated training/test datasets per cell, not five shuffles of one dataset. With r=3 and fixed R=10, it varies N at n=10 and n at N=100. Under the SM generator the likelihood-center delta is +.24261 at N=20, −.04265 at N=100 and −.06156 at N=500; mean true-center Kendall errors are 12.35, 2.95 and .15. A correctly specified model family can lose at a small training budget. All 240 likelihood centers are certified. Under the PL generator, the likelihood-center comparison favors PL in every cell. [S0 definitions and tables](predictive_learning.md#s0-independent-data-with-fixed-r3-and-r10).

![Independent simulations: 95% Student-t mean intervals](../figures/predictive/synthetic.png)

L1 has five development permutations per budget for Beans and Sushi A/B, with one fixed test per task. Its [current tables](../results/regularized_learning/README.md) separate unshrunk SM, training-validation dispersion shrinkage and PL penalty controls. L1 test-only bootstrap intervals differ from L0 partition MCSEs. [L2/S3](learning_curves.md) supply small-budget and exposure controls.

## Full-data ranking characteristics

[All three characteristics beside P0 NLL](../data/features/predictive_comparison.md) use every eligible observation and a full-data descriptive reference center. They do not choose a fitted predictor. Dots 2013/Puzzle have equal-gap pair-rate dispersion about 1.00–3.34 percentage points and dense support; all eight P0 mean gaps favor SM. Sushi A has dispersion 7.36 points and a PL-favorable mean. This small, related collection does not establish a general feature-to-winner law.

Sushi A's within-shell total variation .99351 is close to its nominal sampling reference .99335 because the order space is large. Beans has a +2.66-point one-item replacement contrast over 420 well-supported contrasts, yet its NLL mean favors PL. Wheat's +7.56-point contrast has repeated support on both sides in only 70/2,022 cases. Sparse cells, mixtures and estimated centers qualify all three characteristics; they are descriptions, not calibrated tests or causal explanations.

## Estimator risk and theorem correspondence

[The theory chapter](theory_alignment.md) distinguishes true-center Kendall risk, real-data predictive NLL and external objective-order distances. Finite grids of random-center simulations are not a supremum over centers or an asymptotic minimax verification. Fixed R alone does not verify lambda≤1 or uniform independent displays. Successful Efficient fits have depth zero and do not test an active multilevel hierarchy. Theorem 2.17 and Fotakis also retain their tie-rule differences.

## Trial and assessor heterogeneity

[G1](group_sensitivity.md) compares local, fully pooled and matched-count pooled training with five allocations at each fraction. Its current tables include paired four-way finite coverage and observed min–max ranges. Group information and training count jointly affect prediction; local gains are not a causal board effect or evidence of a universally more group-sensitive family. Sounds' small per-person training sets frequently fail finite-MLE or finite-prediction checks, so its finite-only local comparisons cannot establish overall predictive risk.

## Controlled mechanisms

S1's fixed-shell intervention isolates an aspect of ranking structure that total noise does not describe. For n=8,r=3,N=448 and equal-gap reference PL, every intervention retains mean inversions .826685 and the full inversion-count distribution, yet the mean exact-SM-minus-PL difference changes as follows:

| Within-shell tilt h | Mean Δ | 95% interval across 40 independent training draws |
|---:|---:|---|
| 0 | −.0555 | [−.0577,−.0533] |
| .5 | −.0270 | [−.0295,−.0245] |
| 1 | −.0026 | [−.0052,.0000] |
| 2 | +.0388 | [.0350,.0426] |
| 4 | +.0708 | [.0685,.0732] |

The final displayed zero is rounded. The conclusion is a controlled predictive reversal as probability allocation within shells changes, not proof that a single empirical context slope identifies the preferred model. The bridge, shell and coverage grids preserve finite-MLE failures and divergent losses. At n=32,N=40, all PL fits in each coverage mixture cell lack a unique finite MLE. [Simulation design and exact outputs](strict_feature_analysis.md).

## Diagnostic calibration

Estimated-center error attenuates or changes the apparent SM context effect. The heterogeneous-PL control produces a nonzero pooled effect through assessor/display association even though each group is PL and has zero within-group context effect. Adjusting by true group removes the population effect, but its sample bootstrap can fail when overlap is sparse.

At confounding strength .90 and diagnostic budget 60, only 143/200 adjusted diagnostics exist, and 30.8% of those reject the true zero effect using nominal 95% intervals. At budgets 200 and 1,000, availability/rejection are 199/200 with 7.5% and 200/200 with 3.0%. This is evidence against treating the diagnostic's nominal interval as a universally calibrated test. [D2](validation_extension.md) distinguishes inner bootstrap intervals from outer Wilson rate intervals.

Wheat's context support is small and its clustering metadata incomplete. The SP-Rank objective-gap screen has no eligible changing-gap pairs. No reliable positive empirical identification of the selective-Mallows context mechanism follows from these analyses. [Observation-design limits](context_followup.md).

## Temporal and structural controls

ATP's ten equal-weight season means favor ridge PL: the bounded/shrunk efficient-center SM difference is +.02455 with working across-season interval [.01497,.03412]. Fixing SM to PL's fitted order still gives +.02169 [.01340,.02997]. This is consistent with pair-specific strength differences helping beyond a common order. The intervals do not resolve dependence from recurring players and years. [Temporal design and tables](temporal_prediction.md).

On Sushi A, a common-order control still favors PL in a conditional comparison; within-shell probabilities can help even when the fitted order is held fixed. Optimization benchmarks and Sushi B objective bounds explain which comparisons are exact and which use approximations. Their bounds apply to training objectives, not predictive loss. [Structural controls](structural_controls.md).

These findings leave distinct open questions: sampling-population uncertainty for the complete repeated-fit procedure, unidentified participant dependence, uniform-display theorem applicability, performance of active multilevel estimator hierarchies, and robust model selection from sparse context data. The study records these limitations alongside the results rather than treating repeated shuffles as additional people or corrected metadata as new observations.
