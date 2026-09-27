# Protocol chronology

The STRICT_FEATURE_* and STRICT_SOURCE_ADDENDUM files are the frozen original study designs. CONTEXT_FOLLOWUP includes the original wheat design and pre-fit metadata amendment. They remain unchanged as historical records.

BASELINE_REPLACEMENT was committed before its replacement fits. AUDIT_AMENDMENT is a retrospective correction, explicitly informed by the completed experiments. It supersedes prior working-CI provisions for unidentified sampling units; it does not change original rankings or select favorable fit parameters.

Current methods are defined once in ../algorithms.md. Do not interpret an earlier protocol's superseded interval convention as current practice.

[GROUP_SENSITIVITY_20260927](GROUP_SENSITIVITY_20260927.md) was committed at `69541057711c08ff1508f25676bb6abfdd12c27d` before production runs. It fixes 100 primary splits, two 20-split training-budget checks, equal-budget pooled controls, and 100 whole-group holdouts. It adds only the requested original Fotakis estimator and an explicitly recorded sharp-to-efficient fallback policy. Repeated-split ranges are descriptive, not confidence intervals.

[VALIDATION_EXTENSION_20260926](VALIDATION_EXTENSION_20260926.md) was frozen at ddad79788574374d3c31699c74a145ff75d9008f before the three additional real tasks and 1,400 synthetic datasets. Its [source amendment](VALIDATION_SOURCE_AMENDMENT.md), commit 6e3cef2e97978153f5c4c6911f5a62b94d905bd0, excluded the upstream-filtered Beaches release before any new fit and fixed the remaining source indices. This source audit changes eligibility, not observations or estimator definitions. PatrasIQ's per-task intervals rely on its documented one-report-per-person design; they do not reinstate the older unidentified-unit intervals.
