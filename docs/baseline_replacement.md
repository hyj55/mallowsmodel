# Fixed-partition prediction and diagnostics

[Experiment P2](experiments.md) · [Criteria](criteria.md) · [Uncertainty](uncertainty.md) · [Data catalogue](../data/README.md)

## Purpose

A specified fitted model can be examined in detail on a disjoint diagnostic or confirmation set. P2 supplies these conditional analyses alongside P1's average across partitions. The point estimate and bootstrap interval in a P2 row describe **that row's fixed training allocation**; its interval must not be placed around a P1 mean.

## Datasets and allocation

The 23 tasks and 60/20/20 report counts are listed in [P1 task sizes](repeated_holdout.md#task-sizes). P2 uses one separately specified permutation per task, with whole-assessor Sounds splits and aligned Sushi and within-arm dots2024 participant splits. Anonymous Beans, Wheat and PrefLib rows are split as reports. No year/season/geographic/demographic stratification is imposed. Ranking content is preserved.

| Tasks | Root seed / runner | Output directory |
|---|---|---|
| Beans, Sushi A/B | 202609253; `run_baseline_replacement.py` | `results/baseline_replacement/` |
| Eight PrefLib Dots/Puzzle and eight dots2024 tasks | 202609251; `run_strict_real.py` | `results/strict_features/real_*` |
| Wheat | 202609252; `run_context_followup.py` | `results/context_followup/` |
| Sounds, PatrasIQ cost/population | 202609260 with source-index streams; `run_validation_real.py` | `results/validation_extension/real_*` |

All use the specified exact/Sharp/efficient/clipped-Borda SM candidates and Hunter MM PL, recording unavailability. [The dataset-by-estimator table](experiments.md#estimator-allocation-by-empirical-dataset) states why each method is feasible, excluded or attempted. Exact means subset DP through n=18 and a certified integer optimum above that limit; no confirmation-based optimizer selection occurs.

## Criteria and interval units

The principal score is mean confirmation whole-ranking NLL. Pair SM−PL losses on each report before averaging. Identified-unit intervals use 2,000 percentile bootstrap draws conditional on the fixed fits: individual respondents within Sushi/dots2024/PatrasIQ tasks, whole assessors for Sounds. Beans, anonymous PrefLib and Wheat have no supported inferential CI. The [resampling chapter](uncertainty.md) supplies formulas, assumptions, nonfinite handling and limits.

PrefLib/dots2024 and PatrasIQ also have shell-mass/within-shell components and context slopes on discovery and confirmation; Sounds has direct-pair reliability profiles. Wheat has an unadjusted slope and explicitly unavailable village adjustment. The objective-reference follow-up uses the external answer order only for its named diagnostic, never for training the primary model. Beans/Sushi P2 supplies predictive scores; their richer saved mechanism diagnostics belong to the separately specified C1 regularized fitting control.

A task can have an exact fitted center and still have no reliable sampling interval. Conversely, an available bootstrap interval is conditional on the fixed fit, not proof of correct model specification. [Findings](findings.md) combines these analyses by question; [result dictionaries](../results/README.md) link every complete table.
