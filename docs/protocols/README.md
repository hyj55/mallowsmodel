# Execution specifications and source-design records

[Experiment map](../experiments.md) · [Methods](../algorithms.md) · [Uncertainty](../uncertainty.md) · [Implementation registry](../implementation_registry.md)

**Current reading nomenclature:** P0 alone is the Algorithm 4.1 main experiment. E0 names the additional empirical center-estimator comparison and B0 the global sieve. Frozen protocol references to a common P0 batch include those separate supplements; that storage/design grouping does not make them main experiments. Other uses of “primary” in a frozen protocol mean that component's prespecified endpoint or allocation, not another main experiment.

The three repeated-allocation specifications below describe the current five-allocation design; they are not prospective preregistrations. Immutable producer fingerprints for saved fits live in [technical provenance](../../results/provenance/README.md). Other source and simulation design records retain the versions referenced by their own manifests. Use the integrated study chapters for results and interpretation.

| Record | Scope | Role |
|---|---|---|
| [PREDICTIVE_COMPARISON_20261013](PREDICTIVE_COMPARISON_20261013.md) | Shared runner: P0 main, E0/B0 estimator supplements, and L0/S0 curves | Current execution specification; five empirical allocations, fixed R=10, twenty independent S0 draws per cell |
| [STRICT_FEATURE_PROTOCOL](STRICT_FEATURE_PROTOCOL.md) | S1/S2/D1 mechanism and coverage experiments | Pre-fit design |
| [STRICT_SOURCE_ADDENDUM](STRICT_SOURCE_ADDENDUM.md) | PrefLib, dots2024 and agricultural source scope | Pre-fit source/decoding rules |
| [STRICT_FEATURE_FOLLOWUP](STRICT_FEATURE_FOLLOWUP.md) | Diagnostic budgets and objective-reference checks | Explicit exploratory controls |
| [CONTEXT_FOLLOWUP](CONTEXT_FOLLOWUP.md) | Wheat and SP-Rank observation design | Source/design record and metadata amendment |
| [BASELINE_REPLACEMENT](BASELINE_REPLACEMENT.md) | P2 Beans/Sushi unpenalized fits | Pre-fit estimator and split specification |
| [VALIDATION_EXTENSION_20260926](VALIDATION_EXTENSION_20260926.md) | D2 and Sounds/PatrasIQ fixed prediction | Pre-fit design, commit `ddad79788574374d3c31699c74a145ff75d9008f` |
| [VALIDATION_SOURCE_AMENDMENT](VALIDATION_SOURCE_AMENDMENT.md) | Beaches exclusion, identified-unit source rules | Pre-fit amendment, commit `6e3cef2e97978153f5c4c6911f5a62b94d905bd0` |
| [GROUP_SENSITIVITY_20260927](GROUP_SENSITIVITY_20260927.md) | G1 trial/person splits and estimator admission | Current execution specification; five allocations per design/fraction |
| [REPEATED_HOLDOUT_20260928](REPEATED_HOLDOUT_20260928.md) | P1 five full refits per task | Current five-allocation specification |
| [AUDIT_AMENDMENT](AUDIT_AMENDMENT.md) | Unsupported intervals and method attribution | Retrospective correction informed by completed evidence |

L1/L2/S3/T1/C1 design records are retained with their [matching implementation snapshot](https://github.com/hyj55/mallowsmodel/tree/89b21645d5f7eb463cc90c4e982c3a66ce805b41/docs/protocols). Frozen filenames preserve their original identifiers; all components are included in the same experiment map.

The audit amendment supersedes unidentified-assessor and artificial-village interval conventions. It changes the supported interpretation, not source reports or fitted point estimates. A superseded rule quoted inside a frozen document must not be used to reassert a withdrawn inference. Repeated split ranges, partition MCSEs and sampling CIs are distinguished in the shared uncertainty chapter.
