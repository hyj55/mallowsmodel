# Data catalogue

[Study guide](../README.md) · [Experiment map](../docs/experiments.md) · [Models](../docs/algorithms.md)

The study includes preference reports, objective ordering tasks, agricultural evaluations, and match outcomes. A ranking model receives an ordered list of item labels; its displayed set is the set of labels in that list. Metadata remain separate from model parameters. Source-specific details below distinguish fields available in the release from fields actually used in an experiment.

## Notation and coverage

- **M:** all reports in a task before experimental splitting.
- **n:** catalogue size; unused labels are not removed merely to obtain a finite fit.
- **r:** displayed and completely ordered items in each report. Each fitted task has fixed r.
- **N:** training reports in a particular experiment. A dataset has no unique N independent of its split or budget.
- **$`\mu=Nr/n`$:** average training appearances per catalogue item.
- **$`\lambda=Nr(r-1)/(n(n-1))`$:** average training co-occurrences per unordered catalogue pair.
- **Observed pair coverage:** distinct pairs seen / $`n(n-1)/2`$. Minimum item/pair counts and directed connectivity describe features that averages miss.

μ and λ are also per-item/per-pair expectations under uniform independent display sampling. Real-data averages alone do not verify that sampling assumption. All empirical source items appear at least once in their full P1 task; this does not imply every training partition has adequate coverage.

## Dataset families

| Dataset | Reports and catalogue | Metadata/identity | Experimental uses |
|---|---|---|---|
| [Beans](beans.md) | M=842; n=10; r=3 | Year, season, temperature, coordinates, date; no farmer ID | P1/P2 prediction; L1/L2 budgets; T1 year transfer; C1 controls |
| [Sushi A and B](sushi.md) | M=5,000 each; n=10/100; r=10 | Shared respondent rows; user/item attribute files | P1/P2 prediction; L1 budgets; Sushi B L2; C1 diagnostics/optimization |
| [Dots 2013 and Puzzle](dots_puzzle.md) | Eight tasks, M=793–800 each; n=r=4 | Objective category labels; 40 recovered trials per condition; no cross-trial worker IDs | P1/P2 prediction and shells; G1 trial-specific fitting |
| [Dots 2024](dots2024.md) | Eight arm/size tasks, M=300 each; n=30; r=2/3/5/6 | Four-report participant blocks, task batch, numerical responses and times | P1/P2 prediction, center-reference and mechanism diagnostics |
| [Bread wheat](wheat.md) | M=493; n=16; r=3 | Location/demographics and four traits; names redacted; missing villages | P1/P2 prediction and unadjusted context diagnostics |
| [Sounds](sounds_patras.md#sounds) | M=1,380; n=12; r=2 | 46 assessor IDs, 30 reports each | P1/P2 prediction and pair profiles; G1 person-specific/transfer analysis |
| [PatrasIQ](sounds_patras.md#patrasiq-cost-and-population) | M=392 each; n=36/48; r=6 | Documented one report/person/task; cross-task matching absent | P1/P2 prediction, shells, objective-reference diagnostics |
| [ATP tennis](tennis.md) | Ten 2010–2019 tasks; n=418–469; r=2 | Player and tournament IDs, dates, surfaces, match statistics | T1 chronological prediction; C1 common-order and strength controls |
| [Screened sources](screening.md) | Tricot projects, Beaches, SP-Rank, potato, breakfast | Source-dependent | A1 eligibility/design audit; no SM–PL fits for excluded tasks |
| [Synthetic populations](../docs/strict_feature_analysis.md) | n=4/8/10/32/64 and declared budgets | Known generating order and parameters; D2 also has known group labels | S1–S3, D1–D2 controlled experiments |

P1's 23 tasks are three Beans/Sushi tasks, eight Dots/Puzzle tasks, eight dots2024 tasks, Wheat, Sounds and two PatrasIQ tasks. Their reuse in group, budget or diagnostic analyses is not counted as new independent data collection.

## Source-to-ranking processing

Verify source version and SHA256, decode item labels and observation format, validate the full task, then split intact reports or documented sampling units. P1/P2/G1 preserve all eligible reports and their ordering. PrefLib frequency expansion repeats the reported ranking exactly its recorded number of times; it does not reconstruct lost identities. Best/worst among three displayed items uniquely determines a complete ordering of those three. No rating-to-ranking conversion, tie breaking, or outcome-based removal is added in these fits.

A displayed-set ranking is different from “show ten items but retain only the top three.” The latter is censored and requires its original ten-item display plus a likelihood that marginalizes the unobserved tail. None of the included ranking tasks is deliberately recoded from such a top-k observation into a three-item display. A sports match is a direct two-item outcome. ATP has its own explicit completed-match and prior-catalogue eligibility rules; [those exclusions](tennis.md) must not be generalized into a claim that no source ever has filtering.

## Files and provenance

| Manifest | Pinned materials |
|---|---|
| [sources.json](sources.json) | Beans R object and Sushi archive |
| [strict_feature_sources.json](strict_feature_sources.json) | Eight PrefLib files, ten dots2024 JSON exports, four decoding/export scripts |
| [group_sensitivity_sources.json](group_sensitivity_sources.json) | Original voting trial archive, mapping to PrefLib, Sounds identity source |
| [context_followup_sources.json](context_followup_sources.json) | Wheat object/documentation and SP-Rank data/documentation |
| [validation_extension_sources.json](validation_extension_sources.json) | Sounds, Beaches, upstream objects, PatrasIQ rankings and study description |
| [strict_tricot_sources.json](strict_tricot_sources.json) | Nine project JSONs and variable metadata; [candidate list](strict_tricot_candidates.json) |
| [ATP manifest](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/data/tennis_sources.json) | Annual files, data dictionary, attribution and licence |

Immutable source commits or archive checksums identify the actual inputs. A mutable download URL is not itself a version guarantee. Raw source caches and detailed respondent records are generally not redistributed. [Third-party notices](../THIRD_PARTY_NOTICES.md) explain the bundled Beans file and source terms.

## Full-source coverage

The table below was calculated directly from the decoded source reports, without fitting a model. “Displays” counts distinct unordered item sets under each task's coding; for Dots/Puzzle these are difficulty-category sets, not a count of distinct physical stimuli. Participant-row placeholders for anonymous data are not person identifiers.

| Task ID | M | n | r | Displays | Item count range | Observed / possible pairs |
|---|---:|---:|---:|---:|---|---|
| `beans` | 842 | 10 | 3 | 120 | 234–270 | 45/45 |
| `sushi_a` | 5000 | 10 | 10 | 1 | 5000–5000 | 45/45 |
| `sushi_b` | 5000 | 100 | 10 | 4983 | 50–1546 | 4809/4950 |
| `00024-00000001` | 795 | 4 | 4 | 1 | 795–795 | 6/6 |
| `00024-00000002` | 794 | 4 | 4 | 1 | 794–794 | 6/6 |
| `00024-00000003` | 800 | 4 | 4 | 1 | 800–800 | 6/6 |
| `00024-00000004` | 794 | 4 | 4 | 1 | 794–794 | 6/6 |
| `00025-00000001` | 793 | 4 | 4 | 1 | 793–793 | 6/6 |
| `00025-00000002` | 795 | 4 | 4 | 1 | 795–795 | 6/6 |
| `00025-00000003` | 795 | 4 | 4 | 1 | 795–795 | 6/6 |
| `00025-00000004` | 797 | 4 | 4 | 1 | 797–797 | 6/6 |
| `dots2024_A_r2` | 300 | 30 | 2 | 214 | 20–20 | 214/435 |
| `dots2024_A_r3` | 300 | 30 | 3 | 294 | 30–30 | 386/435 |
| `dots2024_A_r5` | 300 | 30 | 5 | 300 | 50–50 | 435/435 |
| `dots2024_A_r6` | 300 | 30 | 6 | 298 | 59–62 | 435/435 |
| `dots2024_B_r2` | 300 | 30 | 2 | 221 | 20–20 | 221/435 |
| `dots2024_B_r3` | 300 | 30 | 3 | 290 | 30–30 | 387/435 |
| `dots2024_B_r5` | 300 | 30 | 5 | 300 | 50–50 | 435/435 |
| `dots2024_B_r6` | 300 | 30 | 6 | 299 | 59–61 | 435/435 |
| `wheat` | 493 | 16 | 3 | 418 | 85–98 | 120/120 |
| `sounds` | 1380 | 12 | 2 | 66 | 207–243 | 66/66 |
| `patras_cost` | 392 | 36 | 6 | 80 | 58–70 | 538/630 |
| `patras_population` | 392 | 48 | 6 | 80 | 46–51 | 795/1128 |

Training coverage differs from full-source coverage. Exact P1/P2 sample sizes and design-average training λ/μ are in [the prediction design](../docs/repeated_holdout.md#task-sizes); per-partition observed coverage is saved in `results/repeated_holdout/repeat_scores.csv.gz`. G1 and learning curves use their own N values.
