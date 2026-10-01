# Result files and field guides

[Study guide](../README.md) · [Findings](../docs/findings.md) · [Criteria](../docs/criteria.md) · [Uncertainty](../docs/uncertainty.md)

Read results by experiment, dataset, estimator, evaluation target and denominator. Filenames are stable artifact identifiers; several scientific components share a directory.

| Location | Components | What to read |
|---|---|---|
| [repeated_holdout](repeated_holdout/README.md) | P1: 23 tasks ×30 refits | Mean loss, paired Δ, partition MCSE, all fit/finite counts |
| [baseline_replacement](baseline_replacement/README.md) | P2: Beans/Sushi | Fixed-fit prediction, certificates and supported test-unit intervals |
| [strict_features](strict_features/README.md) | S1/S2/D1; P2 PrefLib/dots2024; tricot screen | Controlled laws, coverage, selectors, shells and context diagnostics |
| [context_followup](context_followup/README.md) | P2 wheat; A1 SP-Rank | Point prediction, metadata-limited diagnostics and observation-design audit |
| [validation_extension](validation_extension/README.md) | D2; P2 Sounds/PatrasIQ; Beaches screen | Calibration/confounding draws, rates and Wilson bars, identified-unit empirical intervals |
| [group_sensitivity](group_sensitivity/README.md) | G1 | Pooled/local/matched controls, group transfer, common masks and split ranges |
| [audit](audit/README.md) | Calculation and evidence verification | Source/fit replay and integrity receipts; no additional scientific replicates |
| [Regularized prediction artifacts](https://github.com/hyj55/mallowsmodel/tree/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results) | L1, S3 n=10, T1 Beans, C1 | `real_*`, `synthetic_*`, `beans_transfer_*`, `same_order_*`, `outer_fold_*`, diagnostic and optimization tables |
| [Exposure and ATP artifacts](https://github.com/hyj55/mallowsmodel/tree/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results/exposure) | L2, S3 exposure, T1 ATP, C1 | `small_*`, `coverage_*`, `real_*`, `tennis_*`, penalty and feasibility controls |

The last two locations pin implementation `89b21645d5f7eb463cc90c4e982c3a66ce805b41`. They are part of the same study, with bounded/regularized procedures explicitly distinguished from unpenalized ones. [The learning chapter](../docs/learning_curves.md) and [implementation registry](../docs/history.md) locate their exact files and meanings.

Δ=NLL(SM)−NLL(PL); negative favors SM. A fixed-fit bootstrap interval, independent-simulation t interval, Wilson rate interval, split percentile range and partition MCSE are different objects. No bootstrap endpoints are averaged to form P1 uncertainty. All unavailable/infinite/finite-conditional counts must accompany a comparison. [Definitions and formulas](../docs/uncertainty.md).

Three large D2 artifacts are restored with `python validation_artifacts.py`. Public empirical artifacts generally contain fitted parameters and aggregate results; detailed private membership/prediction caches are needed for some local replay. See [reproduction](../docs/reproducibility.md) for those distinctions.
