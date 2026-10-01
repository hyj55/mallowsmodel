# Temporal prediction

[Experiment T1](experiments.md) · [Beans](../data/beans.md) · [ATP](../data/tennis.md) · [Uncertainty](uncertainty.md#learning-curve-and-temporal-intervals)

## Beans: 2015 to 2016

Use the year suffix of the source season labels to allocate all 658 reports from 2015 to development and all 184 reports from 2016 to test. Fit exact-DP SM with bounded β, its validation-selected β multiplier, and ridge PL under the L1 inner-tuning procedure. Five permutations of the same development reports vary inner tuning membership; each final fit still uses all 658 development rows and the same 184 test rows.

Compute whole-ranking loss and average each test report's paired differences across the five fits. A 2,000-draw report bootstrap supplies the saved endpoints, but unidentified farmers prevent a verified independence-based population interpretation. Report the point comparison descriptively. This is a temporal transfer target, not a season-balanced random split. Temperature, location and other season-associated changes remain potential contributors to transfer loss.

[Summary](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results/beans_transfer_summary.json), [fit repetitions](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results/beans_transfer_replicates.csv), and [runner](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/run_followups.py) define the exact variant.

## ATP: ten chronological seasons

For each year 2010–2019, fix the catalogue using eligible matches from the previous season. Apply the completed-match and catalogue rules in [the source chapter](../data/tennis.md). The first half of the year trains, the second half tests; the first and second quarters form inner training/validation. Tournament start dates keep entire tournaments together. No outer shuffle is used.

Fit ridge PL/Bradley–Terry, efficient/Borda-center SM and insertion-refined-center SM. Fit β on [0,10], retain raw and validation-shrunk predictions, and tune PL over {.1,1,10}. At r=2, SM's correct-order probability is constant within a fitted season; PL allows pair-specific strength differences. These scalable centers are used because n exceeds 400; no exact or Sharp large-catalogue result is claimed. The recorded efficient hierarchy has depth zero.

The primary test evaluates matches with both players seen in training. A separate all-catalogue target includes cold-start matches among catalogue players. Whole-ranking log loss and binary Brier loss are averaged within a season. A 2,000-draw whole-tournament bootstrap preserves each tournament's reports and gives a season-level conditional interval. Across the ten years, the summary averages seasonal means equally and uses a t interval across ten annual paired differences. Repeated players and serial dependence make that aggregate interval a working approximation, not a validated time-series CI.

A common-order control takes PL's fitted order as the SM center, profiles/shrinks β on training/validation, and compares predictions on the same seen-player test matches. Training PL-strength bins also show empirical and predicted win rates. These controls diagnose heterogeneous strength; they do not claim that temporal independence or uniform matchups holds.

[Season results](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results/exposure/tennis_by_year.csv), [aggregate results](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results/exposure/tennis_summary.csv), [common-order results](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results/exposure/tennis_same_order_summary.csv), [figure](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/figures/exposure_tennis.png), and [implementation](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/run_exposure.py) are retained at their matching snapshot. No new tennis calculation is implied by their inclusion in the study guide.
