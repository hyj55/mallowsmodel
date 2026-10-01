# Optimization and common-order controls

[Experiment C1](experiments.md) · [Models](algorithms.md) · [Criteria](criteria.md) · [Learning design](learning_curves.md)

## Center-objective benchmark

For Beans and Sushi A, compare exposure-normalized Borda, Fotakis PosEst, equal-reliability greedy MAL, multistart insertion and exact subset DP at Beans N=50/673 and Sushi A N=50/3,000, using one fixed development-pool permutation. Score their excess training Kendall objective relative to exact DP, not error relative to an unobserved true preference center. These methods test how optimization choices affect an SM fit; they are not five different ranking probability families. PosEst's benchmark evaluation does not carry G1's full-pair admission claim or its theorem guarantee automatically.

Sushi B N=100/3,000 has a large-catalogue multistart insertion/MILP-bound benchmark and a cutting-plane pilot. One N=3,000 instance has a feasible objective 44,736 and lower bound 44,724; this bounds its center objective, not its test NLL. A 12-unit gap is not an exact certificate. P1/P2's certified integer fits use their own specified samples and acceptance rules, so numerical differences cannot be attributed solely to optimizer changes.

[Benchmark table](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results/algorithm_benchmark.csv), [cutting-plane pilot](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results/cutting_plane_pilot.json).

## Holding the fitted order common

For Beans N=673 and Sushi A N=3,000 under L1's five saved training fits, refit ridge PL subject to $`\theta_{\pi_1}\ge\cdots\ge\theta_{\pi_n}`$, where π is the fitted SM center. The penalty is the same training-selected penalty; ties are allowed, and confirmation data do not tune it. Compare original SM with this order-constrained PL on the same test reports.

The converse control fixes SM's center to the order of fitted PL worths and profiles bounded β using training reports. Comparing that SM with the original PL asks how their probability laws differ after equalizing their order. The ATP version profiles and validation-shrinks SM β on the PL order within each year.

For Beans/Sushi, average paired differences across fits for each test report, then use 2,000 report-bootstrap draws. Missing Beans farmer IDs still limit inference. Shell decomposition under the common center partitions each loss difference exactly into shell-mass and within-shell terms. These constraints change the fitted procedures deliberately; they do not establish a causal effect of “model family alone.” [Common-order results](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results/same_order_summary.csv), [shell control](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results/shell_same_center_sensitivity.csv).

## Pair, shell and context diagnostics on saved fits

L1's fixed-test Beans/Sushi fits supply pair log/Brier losses, training-gap bins, shell components and within-pair context slopes. Beans also uses pair×season cells, and Sushi B pair×current east/west region cells. These strata enter only the diagnostic calculation, not SM/PL fitting or the outer split. The same report-bootstrap indices carry all within-report pairs and all saved-fit contributions together.

Sushi A's complete fixed display has no within-pair changing-gap context contrast. Sushi B's varying display can have one, but approximate-center error and respondent/display composition limit interpretation. [Diagnostic tables](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results/context_effects.csv), [shell decomposition](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results/shell_decomposition.csv), and [criterion definitions](criteria.md) give the exact quantities.

## Five-fold allocation control

Beans and Sushi A also use one random permutation divided into five disjoint outer test folds. Shuffle the other four folds and use min(3,000, their total size) training reports: Beans uses 673 or 674, while Sushi A uses 3,000 of the 4,000 available. Refit L1's bounded/regularized procedure, with inner tuning within that training portion. Report the pooled out-of-fold paired mean and the minimum/maximum fold means. Training sets overlap; no t interval treats the five folds as independent datasets. This is not an extra set of independently recruited respondents. [Five-fold table](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results/outer_fold_summary.csv).

## Mathematical checks and controls

Enumeration at small r verifies normalization, SM pair probabilities, Mahonian shell counts and the PL shell recursion. Generated known-parameter controls confirm the changing-gap SM probability and PL's pair invariance before fitted diagnostic interpretation. Solver/likelihood tests compare independent implementations and replay saved predictions. Such checks verify calculations; they are not independent evidence that either family describes an empirical population.
