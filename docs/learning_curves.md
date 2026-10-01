# Sample size, exposure and regularization

[Experiments L1/L2/S3](experiments.md) · [Data](../data/README.md) · [Estimator variants](algorithms.md#bounded-and-regularized-predictive-procedures) · [Uncertainty](uncertainty.md)

A learning curve varies training reports N while holding the task's catalogue n, report length r and evaluation target fixed. It can reveal estimation error, coverage failures and regularization effects. Increasing r instead changes the information inside each report and is a different intervention. All completed budget analyses below are part of the study; their fitting variants are identified explicitly.

## Empirical learning curves

| Dataset | n,r | N budgets | Training permutations at each N | Fixed outer test |
|---|---|---|---:|---:|
| Beans | 10,3 | 20,50,100,200,400,673 | 5 | 169 |
| Sushi A | 10,10 | 20,50,100,300,1,000,3,000 | 5 | 1,000 |
| Sushi B | 100,10 | 100,300,1,000,3,000 | 3 | 1,000 |

Make one 80/20 outer report split. Within each repetition, permute the development pool and use nested prefixes for N. A/B respondents share the outer split. The inner first floor(.8N) reports tune PL's ridge penalty and the optional SM dispersion multiplier on the remainder; final fits use all N. Thus N includes inner validation. At Beans N=673 the five permutations contain the same full development sample; they are not five new samples.

SM uses exact subset DP for Beans/Sushi A and a declared multistart insertion/integer-bound pipeline for Sushi B. The latter's 12 primary fits were not certified global optima. β is bounded at 10; unshrunk and validation-shrunk results are separate. PL tunes τ over {.01,.1,1,10,100}; τ=10⁻⁶ is a separate sensitivity, not the unpenalized MM fit. These choices make small-budget predictions finite and test regularization, while differing from P1/P2's unbounded/unpenalized procedure.

For each fixed test report, average its paired losses across the saved training repetitions, then bootstrap those report averages 2,000 times. This yields test-only conditional intervals; it does not include outer partition or training-sample uncertainty. Beans lacks farmer IDs, so its stored endpoints do not justify population inference. See [the formula](uncertainty.md#learning-curve-and-temporal-intervals).

[Complete summaries](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results/real_summary.csv), [repetitions](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results/real_replicates.csv), [figure](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/figures/real_learning_curves.png), and [implementation](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/run_experiments.py) are pinned to the matching implementation snapshot.

## Small-budget prediction

L2 uses Beans N=2,5,10,14,30,100 and Sushi B N=5,10,25,50,100,300. Five development-pool permutations supply nested prefixes, with the same fixed outer test definition as L1. All catalogue labels and original reports are retained.

Both tasks fit the efficient/Borda center; Beans additionally fits exact DP, while Sushi B fits insertion initialized by the efficient order. Exact Sharp terminal blocks exceed the eight-item guard here, so this is not a large-catalogue Sharp comparison. Dispersion is bounded and optionally shrunk; PL tunes {.1,1,10}. N<5 fixes α=.5 and τ=1 without pretending to validate on an insufficient sample. Separate fixed-penalty PL controls use τ=1 and 10. The efficient λ>1 schedule cap in this implementation is labeled an empirical domain extension.

NLL, unseen items/pairs, actual exposure, branches and concentration choices are recorded. The interval averages each test report over the five fits, then resamples reports; it is not a t interval over five independent outer splits. The [complete result directory](https://github.com/hyj55/mallowsmodel/tree/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results/exposure) includes `real_summary.csv`, `real_replicates.csv`, `real_exposure.csv`, and `real_penalty_sensitivity.csv`.

At Sushi B N=100, changing the PL tuning comparison to fixed τ=10 changes a reported SM advantage into a near-zero difference. This is evidence that small validation budgets can determine the fitted-procedure ranking, not a reason to choose a penalty using the test set.

## Simulation learning and exposure grids

All displays are sampled uniformly and independently and then ranked directly within the set. True center labels are randomized independently of estimator tie-breaking. In the n=10 learning grid, PL equal-gap scores are linearly spaced and the unequal-gap vector has one separated top item followed by nine closely spaced items; this differs from S1’s alternating-gap control. The SM signal is β=.8; PL strength scales match its expected inversion count. A matched mean noise level does not imply equal ranking entropy or equal pair reliability.

| Design | Generating laws and sizes | N | Repetitions and evaluation | Estimators |
|---|---|---|---|---|
| S3 learning | n=10,r=3; SM, equal-gap PL, unequal-gap PL | 20,50,100,300 | 30 independent streams per law; nested training budgets and a shared fresh 2,000-report test within stream | Exact DP SM, bounded/shrunk β, tuned ridge PL; center benchmarks |
| S3 small exposure | n=8; SM and matched PL | r=2: 2,4,8,16,28,56,112; r=4: 1,2,4,8,16,64; r=8: 1,2,8,32 | 30 fresh draws per cell, 2,000 independent test reports | Exact center, Sharp, efficient/Borda, ridge PL; raw/shrunk β |
| S3 large exposure | n=64; r=2,8,32; SM and matched PL | max(1,round(λtarget·64·63/[r(r−1)])), λtarget=.03,.3,1,3 | 30 fresh draws per requested design, 1,000 independent test reports | Efficient/Borda with bounded/shrunk β and ridge PL; no exact center |
| S1/S2 likelihood controls | n=8 or 32 | Multiple budgets in [the mechanism design](strict_feature_analysis.md) | 40 independent training draws per cell | Unbounded SM variants and unpenalized PL |
| D2 diagnostic calibration | n=8,r=3 | 28 and 448 | 200 independent draws per law/budget | Exact SM and unpenalized PL |

The n=10 design has 90 independent law/repetition streams and 360 budget-specific training/evaluation contexts. Its four budgets reuse each stream; they are not 360 independent source draws. Small/large exposure grids have 1,020 and 720 independent datasets, respectively. Rounding can map two requested n=64,r=32 exposure targets to N=1; their independent streams produce 60 repetitions in the corresponding merged table cell.

Within a fixed exposure cell, saved mean-loss and center-error intervals use Student-t formulas across independent repetitions. The n=10 learning summary supplies a paired Δ interval; its separate loss, calibrated-loss and center-error columns are means without attached intervals. The [uncertainty chapter](uncertainty.md#student-t-simulation-intervals) explains why independence matters and how this differs from empirical repeated splitting. Reference-shape normalizations and coverage diagnostics are defined in [Criteria](criteria.md).

[Simulation learning tables](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results/synthetic_summary.csv), [exposure tables](https://github.com/hyj55/mallowsmodel/tree/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results/exposure), and [exposure runner](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/run_exposure.py) preserve the exact procedures. Runtime and schedule-feasibility checks do not create new statistical repetitions.

## Interpretation

Sample-size effects can arise from better center/strength estimation, more complete exposure, finite-MLE existence, solver certification or concentration tuning. Report those alongside loss. A persistent large-N gap may reflect model mismatch, but these finite grids do not identify the true family on an arbitrary empirical dataset. P1 supplies repeated-partition estimates at one budget per task; it is not a replacement for a multi-budget curve or evidence that L1/L2 used identical estimators.
