# Controlled model structure and coverage

[Experiments S1/S2/D1](experiments.md) · [Criteria](criteria.md) · [Uncertainty](uncertainty.md) · [Findings](findings.md#controlled-mechanisms)

## Generating populations

Sample an r-item display uniformly from n labels, then generate its complete ranking directly conditional on that display. The reference order is randomized independently of estimator tie priorities. SM uses β=.8. PL log-worth gaps are either all equal or alternate 1,4,1,4,… before a common scaling chosen to match SM's expected inversion count averaged over displays.

Two interventions distinguish overall noise from allocation among wrong orders.

**Bridge:** for a∈{0,.25,.5,.75,1},

```math
P_a(Y\mid S)=(1-a)P_{SM}(Y\mid S)+aP_{PL}(Y\mid S).
```

Expected inversions remain matched, but multiple probability features change together. Intermediate populations need not belong to either fitted family.

**Fixed-shell intervention:** let d=dK(Y,π₀ restricted to S). For h∈{0,.5,1,2,4},

```math
P_h(Y\mid S)=P_{SM}(D=d\mid S)\frac{P_{PL}(Y\mid S)^h}{\sum_{Y':D(Y')=d}P_{PL}(Y'\mid S)^h}.
```

Every display retains its entire SM inversion-count distribution. h=0 is uniform within shells; increasing h favors PL-like allocation inside each shell. Pair marginals can change, so this is not a pure intervention on a single pair diagnostic. No empirical report is transformed this way.

## Grids, estimators and evaluation

| Population grid | n,r | Training N | Other factors | Independent datasets |
|---|---|---|---|---:|
| Bridge | n=8; r=2,3 | 8,28,112,448 | Five a values × two gap shapes; 40 repetitions per cell | 3,200 |
| Fixed-shell | n=8,r=3 | 28,112,448 | Five h values × two gap shapes; 40 per cell | 1,200 |
| Coverage | n=32,r=3 | 40,160,640 | a=0,.5,1; equal gaps; 40 per cell | 360 |

Every generated training dataset is shared by all candidate methods. For n=8, attempt exact DP SM, Sharp, efficient, clipped Borda and unpenalized PL. Exact DP provides a feasible small-catalogue likelihood benchmark; Sharp's terminal enumeration is within the guard; efficient is excluded when λ>1; Borda supplies the global-score comparison. Successful efficient fits have no active hierarchy stages.

Each fit receives an independent discovery sample of 1,000 whole reports. The n=8 test criterion is exact population NLL computed over every display/order, so no finite-test noise is added. Root seed 202609251 separates training, discovery, test and algorithm random streams.

## Coverage design

For n=32, fit efficient, clipped Borda and unpenalized PL. Exact MLE and Sharp are not fitted in this grid: it studies scalable score estimation and finite-MLE existence at larger catalogue size, not an unrecorded exact optimization comparison. Primary SM for discovery selection is Borda; for n=8 it is exact SM. n=32 evaluation uses 2,000 fresh test reports per repetition.

| N | λ | μ | Interpretation |
|---:|---:|---:|---|
| 40 | .2419 | 3.75 | Sparse exposure; all 40 PL fits per mixture cell lack a unique finite MLE |
| 160 | .9677 | 15 | Efficient admitted; exact center still not part of this grid |
| 640 | 3.8710 | 60 | Efficient outside its schedule domain; Borda remains a separate estimator |

Numeric coverage is not a theorem certificate. Unseen items, branches, statuses, runtime, Kendall error and all NLL outcomes are saved. Unbounded dispersion can yield infinite population loss; 223 of 3,200 bridge exact-SM runs do so. Those events are retained rather than clipped or dropped from an unconditional average.

Per-cell mean uncertainty uses paired independent-repetition t intervals. Finite-conditional intervals explicitly change the target. See [nonfinite rules](uncertainty.md#nonfinite-results-and-denominators).

## Discovery-based selection

A pair selector compares mean discovery pair log loss. A context selector compares the observed within-pair slope with fitted SM's prediction and PL's zero prediction; insufficient variation leads to abstention. Confirmation/population evaluation is separate from discovery. [Criteria](criteria.md#discovery-selection-and-regret) defines selection accuracy, regret and the shared finite denominators.

The diagnostic-budget analysis reuses the same 200 n=8,r=3,N=448,equal-gap bridge training fits (five mixtures ×40 repetitions). Discovery budgets 20,60,200,1,000 are nested prefixes. There are no additional training datasets. Compute per-cell t intervals over the 40 independent original repetitions and paired differences in regret relative to budget 1,000. Averaging across all five chosen mixtures is a descriptive design average, not accuracy for arbitrary data populations.

The pair/context rules are also applied to the 16 empirical PrefLib/dots2024 tasks in P2 and separately within each P1 partition. Agreement with an empirical confirmation point winner is not accuracy against a known true family. D2 tests the reliability of the context diagnostic itself.

## Outputs

[The result dictionary](../results/strict_features/README.md) identifies every `bridge_*`, `shell_*`, `coverage_*`, `followup_budget_*`, and `real_*` table. [Findings](findings.md) presents the shell-preserving reversal and limitations; [data screening](../data/screening.md) accounts for the nine tricot sources without adding model fits.
