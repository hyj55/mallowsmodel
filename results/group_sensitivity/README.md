# Group-sensitivity result dictionary

[G1 design and findings](../../docs/group_sensitivity.md) · [Aggregation formulas](../../docs/criteria.md#group-comparisons-and-aggregation) · [Split ranges](../../docs/uncertainty.md#group-split-percentiles).

All nine tasks, groups, candidate methods and failed contexts are retained. These artifacts contain aggregate summaries, not newly redistributed respondent ranking records. The frozen protocol and seed precede the production runs.

| File | Contents |
|---|---|
| `manifest.json` | Source identities, task sizes, fixed seeds/design, runtime versions, core-code and output SHA256 hashes |
| `scores.csv` | Across-repeat summaries by task/design/training percentage/scheme/method: means, medians, 5th–95th split percentiles, sign frequencies, fit and finite coverage |
| `contrasts.csv` | Local-minus-pooled/matched changes for each family and their interaction, on four-way common finite prediction masks |
| `eligibility.csv` | Every candidate's status counts, training sizes, observed item/pair coverage, lambda/mu and actual efficient depth |
| `group_scores.csv.gz` | 18,300 repeated-split group summaries, including all 320 original trial groups and 46 assessor groups across schemes/candidates/budgets |
| `repeat_scores.csv.gz` | 23,400 individual repeat summaries; supports inspecting repeat outcomes and recomputing `scores.csv` |
| `repeat_contrasts.csv.gz` | Per-repeat paired contrasts and common coverage, underlying `contrasts.csv` |
| `validation.json` | Read-only source/membership/prediction replay and aggregate verification receipt; no new fits |

`pooled` uses all training groups; `local` only the target group; `matched_pool` is a uniform subset of pooled training with the local training count. `within` uses every group's reports on both sides, while `group_holdout` keeps whole groups disjoint and has pooled predictions only. `percent` denotes the intended training percentage; within-group sample counts are rounded down. Group codes are stable source-order ordinal codes, not asserted cross-task identities.

NLL is conditional whole-report negative log likelihood in nats. Delta is SM−PL. A negative interaction shifts relative performance toward SM when switching to local fitting. `macro_` fields weight each nonempty eligible group equally; other loss fields weight reports. All cross-scheme interaction comparisons use the same four-way finite mask, not independently selected finite means. Coverage is part of every interpretation.

Empty/NaN values indicate unavailable statistics, not zero. Infinite losses remain represented in counts and complete-risk fields in repeat summaries. `fully_available_repeats` distinguishes a defined fit from `complete_finite_repeats`; `any_infinite_repeats` also records infinity when other groups have missing fits. Finite-only summaries are explicitly conditional and must not be used to declare unconditional superiority. Sounds personal-fit summaries are particularly unsuitable for winner claims because usable PL coverage is below 1% at 70% training.

The 5th–95th split percentiles are **not confidence intervals**; repetitions reuse the same people and observations. No population inference follows from increasing the number of shuffles.

```bash
python validate_group_sensitivity.py --repository-only
```

Full local reproduction and prediction replay use `run_group_sensitivity.py` then `validate_group_sensitivity.py`; detailed fit parameters and training membership records are generated in ignored `results/private/group_sensitivity/`. No original ranking rows are in the files listed above.
