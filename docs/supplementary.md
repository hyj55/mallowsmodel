# Complementary evidence

[Main predictive comparison](predictive_comparison.md) · [Learning and catalogue size](predictive_learning.md) · [Experiment map](experiments.md)

The study uses one source catalogue and related analyses to answer several questions. P0 supplies the main finite predictive comparison; L0/S0 supply learning and catalogue-size curves under the same fitting rules. The components below retain additional scientific questions, rather than repeating the main table in several reports. Their parameter rules, splits and uncertainty targets remain attached to their results.

| Question | Evidence to read | What it adds |
|---|---|---|
| What structure is present in the complete observed dataset? | [Three data characteristics](../data/features/README.md) | Equal-gap pair frequencies, within-shell frequencies and same-pair display changes; descriptive, not extra experiments |
| How does prediction behave without finite regularization? | [P1 unpenalized repeated comparison](repeated_holdout.md) | Thirty 60/20/20 allocations, finite-MLE existence and exact-solver admission; different predictors from P0 |
| What do particular fitted predictors get wrong? | [P2 fixed-fit diagnostics](baseline_replacement.md), [ranking diagnostics](strict_feature_analysis.md) | Conditional test-unit bootstrap, pair profiles, shell decomposition and context effects |
| Do physical trial or assessor groups matter? | [G1 group sensitivity](group_sensitivity.md) | Pooled versus group-local fits, equal-budget controls and transfer to unseen groups |
| Can particular mechanisms reverse relative prediction? | [S1/S2 mechanism and coverage controls](strict_feature_analysis.md) | Shell-preserving interventions, mixtures and sparse-coverage effects |
| Are apparent context effects specific and calibrated? | [D2 diagnostic validation](validation_extension.md), [context controls](context_followup.md) | Center error, heterogeneous PL and sparse-overlap counterexamples |
| How do very low budgets and other regularizers behave? | [L1/L2/S3 supplementary learning designs](learning_curves.md) | Dispersion shrinkage, penalty controls, broader exposure grids and fixed-outer-test analyses |
| Does the comparison transfer across time? | [T1 temporal prediction](temporal_prediction.md) | Beans year transfer and chronological ATP prediction |
| Could optimization or the fitted order explain the gap? | [C1 structural controls](structural_controls.md) | Common-order comparisons, optimization benchmarks and objective bounds |
| Which source and observation claims are defensible? | [A1 source screening](../data/screening.md), [scientific audit](scientific_audit.md) | Source exclusions, unchanged reports, missing identities and verifiable evidence |
| How do estimators relate to minimax results? | [Theory correspondence](theory_alignment.md), [B0 global sieve](sieve_computation.md) | Regime assumptions, risk-versus-NLL distinctions and actual algorithm branches |

Numerical overlap is not extra evidence. B0 explicitly reuses Sharp when the procedures coincide; L0 uses P0's full-development endpoint; S0 fits its intersecting sample-size/catalogue-size cell once. P1 and P0 share outer test allocations but use different training budgets and regularization, so their difference is not a pure causal effect of the penalty alone. Shared Sushi respondents and related task conditions also prevent treating datasets as independent study replications.

Saved source reports, numeric artifacts, frozen protocols and byte-locked fitting modules are retained for reproducibility. Reader-facing explanations use this integrated map. The [implementation registry](implementation_registry.md) records which executable produced each output; a frozen implementation detail does not prescribe the active primary fitting procedure.
