# Wheat diagnostics and SP-Rank design audit

[Observation design](../../docs/context_followup.md) · [Wheat fields](../../data/wheat.md) · [Screened data](../../data/screening.md) · [Uncertainty](../../docs/uncertainty.md)

Wheat uses one specified P2 partition and all 493 source reports. CI fields and the village-adjusted statistic are unavailable because identities do not support the required clustering assumptions. P1's repeated wheat means are in [repeated_holdout](../repeated_holdout/README.md). SP-Rank receives an observation-design audit and no model fit.

| File | Contents |
|---|---|
| `scores.csv` | Five candidate statuses on both held-out partitions; whole-ranking NLL and paired difference; unsupported interval fields empty |
| `context.csv` | Unadjusted slopes, eligible pairs and occurrence counts; explicit unavailable village-adjusted status |
| `coverage.json` | Catalogue, displays, exposure and missing-village counts |
| `splits.csv` | Source row/split indices; village=−1 denotes missing metadata, never one inferential cluster |
| `parameters.json` | Centers, dispersion, worths and optimizer metadata |
| `sprank_audit.csv` | Every cohort/domain task and its count of changing objective-gap pairs |
| `validation.json` | Source, calculation and supported-interval checks |

Reproduce with `python run_context_followup.py` under [the shared guide](../../docs/reproducibility.md). Raw inputs are verified against `data/context_followup_sources.json`; no source rankings are rehosted.
