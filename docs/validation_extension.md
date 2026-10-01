# Diagnostic calibration, center error and confounding

[Experiment D2](experiments.md) · [Context criterion](criteria.md#context-slope) · [Bootstrap and rate intervals](uncertainty.md) · [Findings](findings.md#diagnostic-calibration)

## Purpose and design

A context slope can disagree with a fitted SM prediction because the center is estimated imperfectly. A pooled slope can also arise when different assessor groups face different displays. D2 tests these explanations and the calibration of the actual context-bootstrap procedure, using exact finite-state populations with known answers.

There are seven training settings and 200 independently generated datasets per setting: 1,400 in total. Every dataset fits exact-center SM and unpenalized Hunter-MM PL. Small catalogues make exact optimization practical and remove large-instance center certification as an explanation. Other center estimators are not compared in D2.

| Component | Population | n,r | Training N | Settings |
|---|---|---|---|---|
| Center calibration | Pure SM β=.8 or equal-gap PL matched in mean inversions | 8,3 | 28,448 | Four cells |
| Group/display confounding | Two PL groups with different strengths and display assignment | 4,3 | 448 | ρ=0,.45,.90, three cells |

For each repetition, a fresh diagnostic sample of 1,000 reports is generated independently of training. Budgets Mdiag=60,200,1,000 are nested prefixes. The fitted pair's population NLL is summed over the exact support and does not use the diagnostic sample as a test approximation. Root seed 202609260 provides independent label, training and diagnostic streams.

## Oracle and fitted center controls

In the calibration populations, compare context slopes oriented around the true generating center and around the estimated SM center. The oracle reference uses the declared reference dispersion .8; the fitted reference uses fitted β. Both use the same diagnostic observations. The oracle is a diagnostic control, not privileged information supplied to primary training.

A positive detection means the nominal 95% observed-slope interval lies wholly above zero. Zero-effect rejection means the interval excludes zero in either direction. Rejection of fitted SM uses the interval for observed minus SM-predicted slope. The fitted-center selection rule compares distance to the fitted SM slope versus distance to zero; correctness is evaluated against the exact population-NLL winner, excluding unavailable/tied winners.

## Known heterogeneous-PL counterexample

Use equally likely displays S₁={0,1,2} and S₂={0,2,3}. Each report belongs to one of two groups with log-worth vectors θᵍᵢ=−sᵍi, where sᵍ=.2 or .8 (before randomized relabeling). The stronger group's probability is (1+ρ)/2 for S₁ and (1−ρ)/2 for S₂.

Within either group PL has no pair context effect. For the shared pair (0,2), the pooled agreement contrast between displays is exactly

```math
\rho\,[\mathrm{logistic}(1.6)-\mathrm{logistic}(.4)].
```

Thus display/assessor association creates a pooled effect even though each group follows PL. Compare pair-only cells with pair × true-group cells using the same observations. These true group labels are used only for the diagnostic control; the fitted ranking models remain pooled.

## Two levels of uncertainty

Inside each repetition, take 499 whole-report bootstrap draws to form percentile intervals for observed, predicted and residual slopes. Reference orders, fitted parameters and original eligible cells remain fixed; diagnostic weighted slopes are recalculated. Undefined draws are counted.

Across independent repetitions, compute rejection/detection/selection rates and their 95% Wilson intervals using each metric's available denominator. The error bars on rate figures are **Wilson intervals**, not the inner bootstrap intervals. Prediction mean differences use paired t intervals over 200 independent training datasets. Mean slopes or regret columns without interval columns are only descriptive means. [Uncertainty formulas and theory](uncertainty.md) explain each layer.

## Calibration result and empirical scope

At ρ=.90 and diagnostic budget 60, adjusted diagnostics are available in 143/200 repetitions and reject the true zero effect 30.8% of the time among those available. At budget 200, availability is 199/200 and rejection 7.5%; at 1,000, availability is 200/200 and rejection 3.0%. Sparse overlap makes the plug-in percentile slope bootstrap unreliable. Eligibility thresholds or intervals were not retuned after this result.

Consequently, empirical context intervals are exploratory evidence about particular fits, not calibrated universal model-family tests. This experiment does not assess the separate mean-NLL bootstrap. The Sounds and PatrasIQ empirical tasks share the `validation_extension` output directory, but their data, fitting and inference are described jointly with all empirical tasks in [the catalogue](../data/sounds_patras.md) and [P1/P2](repeated_holdout.md).

[Saved settings, fits, diagnostics and draws](../results/validation_extension/README.md), [complete findings](findings.md), and [reproduction](reproducibility.md) provide the numerical records.
