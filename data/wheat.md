# Bread wheat: three-variety evaluations in India

[Data catalogue](README.md) · [Prediction](../docs/repeated_holdout.md) · [Uncertainty](../docs/uncertainty.md)

## Source and variables

The gosset [breadwheat documentation](https://agrdatasci.github.io/gosset/reference/breadwheat.html) describes trials in Vaishali, India, in the 2014 Rabi season. The [pinned R documentation](https://github.com/AgrDataSci/gosset/blob/bb5eb75c08fe3ab0f28931c093dcb66dea7c4185/R/breadwheat.R) and [data object](https://github.com/AgrDataSci/gosset/blob/bb5eb75c08fe3ab0f28931c093dcb66dea7c4185/data/breadwheat.rda) are recorded in [context_followup_sources.json](context_followup_sources.json).

The object has 493 rows and 19 fields:

| Fields | Contents | Use |
|---|---|---|
| `variety_a`, `variety_b`, `variety_c` | Three assigned varieties | Display identities |
| `overall_best`, `overall_worst` | Best/worst overall performance | Fitted ranking response |
| `germination_best/worst`, `grainquality_best/worst`, `yield_best/worst` | Three other trait evaluations | Not pooled as additional reports |
| `district`, `village` | Administrative grouping | Metadata audit; village adjustment is unavailable |
| `participant_name` | Field exists, but names are redacted | Cannot recover a usable participant identity |
| `age`, `gender` | Participant attributes | Not fitted or used as split strata |
| `planting_date`, `lon`, `lat` | Date and coordinates | Not fitted or used for temporal/geographic holdout |

The documented year/season describes the collection; these are not separate `year` and `season` columns in this 19-field object. Some metadata are missing. There are 14 recorded villages and 113 rows without a village label.

## Processing and role

Best, the remaining item, and worst determine a strict complete order of the assigned triple. All 493 overall reports pass validation. The task retains n=16 varieties and r=3, all 120 catalogue pairs and 418 distinct displays. Full-source item counts range 85–98. Other traits do not become independent observations from the same farmer.

P1/P2 allocate 295/99/99 reports. Training λ=7.375 and μ=55.3125. Random report splits do not keep villages together or balance age, gender or geography. The source describes randomized incomplete blocks, but the released sample alone does not establish every model-theory assumption.

This task evaluates whole-ranking prediction and an unadjusted context slope. A recorded missing-village code is a missing-data marker, not a real cluster. Neither that artificial cluster nor the redacted name field supports a participant/village bootstrap. No inferential NLL CI or village-adjusted slope is supplied. P1's partition MCSE remains a conditional randomization summary of these fixed rows.
