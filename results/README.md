# Result files and field guides

[Study guide](../README.md) · [Findings](../docs/findings.md) · [Criteria](../docs/criteria.md) · [Uncertainty](../docs/uncertainty.md)

P0/E0/B0 result tables and [L0/S0 comparison views](predictive/scaled_curves.md) display raw SM-minus-PL delta beside delta / log(r!), with applicable uncertainty scaled by the same positive constant. CSV ratios are dimensionless; [definitions](../docs/criteria.md#uniform-reference-scaled-loss-difference) explain why this assists cross-report-length reading without making different prediction populations interchangeable.

Read results by experiment, dataset, estimator, evaluation target and denominator. Filenames are stable artifact identifiers; several scientific components share a directory.

| Location | Components | What to read |
|---|---|---|
| [main](main/README.md) | **P0 main experiment: Algorithm 4.1** | Independent likelihood-center SM versus PL table and analysis; all 115 paired comparisons; uncertainty and five-shuffle precision |
| [estimator_comparison](estimator_comparison/README.md) | **E0 supplementary estimator comparison** | Sharp, Fotakis, independently admitted Efficient and global Borda, with saved PL/likelihood-SM references; unified losses, paired Borda contrasts and depth/admission |
| [global_sieve](global_sieve/README.md) | **B0 supplementary global sieve** | Exact identity with Sharp where applicable; aliases are not extra fits |
| [tuned_block_sieve](../docs/tuned_block_sieve.md) | Single-allocation Borda-pilot variant | One report explains all 19 settings, validation candidates, exact local solver status, comparisons and conditional intervals |
| [predictive](predictive/README.md) | Shared raw allocation records; L0/S0 supplementary curves | Stable raw keys, parameters and hashes; explicit mapping to P0/E0/B0 reader views |
| [theory_alignment](theory_alignment/README.md) | Estimator interpretation across P1/G1/S1/S2/S3/C1 | Regime conditions, actual branches, same-partition estimator NLL and known-center risk; arithmetic reuse of saved outputs |
| [repeated_holdout](repeated_holdout/README.md) | P1: 23 tasks ×5 refits | Mean loss, paired Δ, partition MCSE, all fit/finite counts |
| [baseline_replacement](baseline_replacement/README.md) | P2: Beans/Sushi | Fixed-fit prediction, certificates and supported test-unit intervals |
| [strict_features](strict_features/README.md) | S1/S2/D1; P2 PrefLib/dots2024; tricot screen | Controlled laws, coverage, selectors, shells and context diagnostics |
| [context_followup](context_followup/README.md) | P2 wheat; A1 SP-Rank | Point prediction, metadata-limited diagnostics and observation-design audit |
| [validation_extension](validation_extension/README.md) | D2; P2 Sounds/PatrasIQ; Beaches screen | Calibration/confounding draws, rates and Wilson bars, identified-unit empirical intervals |
| [group_sensitivity](group_sensitivity/README.md) | G1 | Pooled/local/matched controls, group transfer, common masks and split ranges |
| [audit](audit/README.md) | Calculation and evidence verification | Source/fit replay and integrity receipts; no additional scientific replicates |
| [Regularized prediction artifacts](https://github.com/hyj55/mallowsmodel/tree/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results) | L1, S3 n=10, T1 Beans, C1 | `real_*`, `synthetic_*`, `beans_transfer_*`, `same_order_*`, `outer_fold_*`, diagnostic and optimization tables |
| [Exposure and ATP artifacts](https://github.com/hyj55/mallowsmodel/tree/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results/exposure) | L2, S3 exposure, T1 ATP, C1 | `small_*`, `coverage_*`, `real_*`, `tennis_*`, penalty and feasibility controls |

The last two locations pin implementation `89b21645d5f7eb463cc90c4e982c3a66ce805b41`. They are part of the same study, with bounded/regularized procedures explicitly distinguished from unpenalized ones. [The learning chapter](../docs/learning_curves.md) and [implementation registry](../docs/implementation_registry.md) locate their exact files and meanings.

$`\Delta=\mathrm{NLL}(\mathrm{SM})-\mathrm{NLL}(\mathrm{PL})`$; negative favors SM. A fixed-fit bootstrap interval, independent-simulation t interval, Wilson rate interval, split percentile range and partition MCSE are different objects. No bootstrap endpoints are averaged to form P1 uncertainty. All unavailable/infinite/finite-conditional counts must accompany a comparison. [Definitions and formulas](../docs/uncertainty.md).

Three large D2 artifacts are restored with `python validation_artifacts.py`. Public empirical artifacts generally contain fitted parameters and aggregate results; detailed private membership/prediction caches are needed for some local replay. See [reproduction](../docs/reproducibility.md) for those distinctions.

[L1 fixed-test learning](regularized_learning/README.md) and [C1 five-fit diagnostics](regularized_diagnostics/README.md) each use five saved fits per budget/task, with their own conditional bootstrap target.

## Sharp/Efficient execution audit

The [execution index](estimator_execution/README.md) provides per-setting tables for E0, L0/S0, P1/P2, G1, S1–S3, L2/T1, S4 calibration/confirmation/resource profiles and the tuned block-sieve supplement. Tables distinguish zero executed depth from a method that was not attempted, and pair the reason with first-round geometry, sample budgets and saved resource limits. B0 and other aliases link to the same originating fits. This is a derived result view; no scientific fits or losses change.
