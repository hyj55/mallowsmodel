# Where the existing learning curves are recorded

Checked against the actual code and saved tables on 28 September 2026. A learning curve varies the **number of training ranking reports N**, holding the item catalog n and ranking length r fixed within a task. It is different from changing the number of ranked items in each observation.

## Real data: already completed, historical fitting protocol

The original real learning curves remain at the immutable pre-audit commit **89b21645d5f7eb463cc90c4e982c3a66ce805b41**:

- [Figure: Beans and Sushi A/B learning curves](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/figures/real_learning_curves.png).
- [Numerical summaries](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results/real_summary.csv) and [individual fitted repetitions](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results/real_replicates.csv).
- [Runner and exact budget/split definitions](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/run_experiments.py): `outer_split`, `fit_compare`, `real_experiments`.

| Task | n | r | Training report counts N | Training subsamples at each N | Fixed test reports |
|---|---:|---:|---|---:|---:|
| Beans | 10 | 3 | 20, 50, 100, 200, 400, 673 | 5 | 169 |
| Sushi A | 10 | 10 | 20, 50, 100, 300, 1,000, 3,000 | 5 | 1,000 |
| Sushi B | 100 | 10 | 100, 300, 1,000, 3,000 | 3 | 1,000 |

The outer 80/20 partition was made **once**. Each repetition reshuffled the development pool and used nested prefixes for the budgets, with the same outer test set. Thus these are repeated training subsamples, not multiple independent outer train/test partitions. Beans at N=673 uses the entire same development pool in all repetitions; changing its ordering does not create new observations.

A separate historical [five-fold follow-up](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/run_followups.py) did refit Beans and Sushi A on five disjoint outer test folds, with results in [outer_fold_summary.csv](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results/outer_fold_summary.csv). That fixed-budget check already used multiple training/test sets, but still used the historical `fit_compare` protocol. It is not the later single-split unpenalized replacement and is not part of the new 30-partition correction.

These are **historical model variants**: validation-selected PL ridge, a capped SM dispersion fit, additional validation-shrinkage sensitivity results, and an uncertified large-catalog optimization pipeline. The main, calibrated and near-MLE columns must not be interchanged. They do not establish the learning curve of the current unpenalized PL versus certified exact SM comparison. The audit did not delete their Git history. The later [baseline replacement](baseline_replacement.md) and [30-repeat correction](repeated_holdout.md) use the current estimators at one training budget per task.

The repository owner's request allowed an already completed learning-curve experiment to be indexed instead of duplicated. Therefore the 28 September amendment does **not** run another real learning-curve study. It corrects the single-partition current real comparisons separately and discloses the historical protocol difference.

## Current strict synthetic studies: training size already varies

The [strict-feature report](strict_feature_analysis.md) and its runners record:

| Experiment | Fixed catalog/report length | Training N | Independent generated training datasets per cell |
|---|---|---|---:|
| Bridge | n=8, r=2 or 3 | 8, 28, 112, 448 | 40 |
| Shell | n=8, r=3 | 28, 112, 448 | 40 |
| Coverage | n=32, r=3 | 40, 160, 640 | 40 |

See [bridge_summary.csv](../results/strict_features/bridge_summary.csv), [shell_summary.csv](../results/strict_features/shell_summary.csv), [coverage_summary.csv](../results/strict_features/coverage_summary.csv) and [run_strict_simulations.py](../run_strict_simulations.py). The coverage comparison deliberately does not fit exact MLE: read its method column instead of attributing efficient/Borda results to MLE. The [validation extension](validation_extension.md) additionally compares calibration settings at N=28 and N=448 with 200 independent training draws per cell; it is a mechanism/calibration experiment, not another empirical Sushi curve. Its three diagnostic-sample budgets are not three independently trained models.

## Why a learning curve is useful

More observations may reduce center/worth estimation error, increase item/pair coverage, make a finite PL MLE exist, and reduce SM boundary fits. A persistent predictive gap at larger N may instead be consistent with model mismatch. Neither a monotonically improving realized curve nor a particular crossover is guaranteed. Hold n, r, the data population and loss definition fixed; changing them alongside N would confound the interpretation. On real data, even a persistent gap does not identify the true generating mechanism.

For a new study under the current estimators, **Sushi A is the cleanest initial benchmark for sample-size effects**: every report ranks the same ten items, and exact SM optimization is practical. It is the full-ranking special case and cannot test a varying displayed-set mechanism. **Sushi B is the complementary partial-ranking benchmark**: each respondent ranks ten items drawn from a catalog of 100. Small-N behavior mixes statistical estimation with item/pair coverage and finite-MLE/solver availability, so all of those must be reported. Its nonuniform display design also remains a limitation for the manuscript's uniform-design theory. The two tasks have aligned respondents and are not independent population replications.

A future current-estimator curve should use fresh repeated respondent partitions, a fixed confirmation set across budgets within each repetition, nested training prefixes, paired SM/PL evaluation, and prespecified failure accounting. Compare average losses of separately fitted models; do not turn the experiment into a probability-averaging ensemble. Treat repetition precision as conditional on the observed dataset, not as additional independent people.
