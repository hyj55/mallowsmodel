# Current data and provenance

Sources are pinned by commit or original archive and verified by SHA256; the Sushi URL itself is not immutable. Current parsers retain original strict reports and complete source catalogs. No ranking is repaired, censored top-k list treated as a displayed-set ranking, or missing item removed to obtain a finite fit. Original source screening is not claimed to be unfiltered raw field data.

| Source / tasks | Reports | Catalog and report sizes | Sampling-unit information | Role |
|---|---:|---|---|---|
| PrefLib Dots (4), Puzzle (4) | 6,363 total | n=r=4 | Assessor/trial IDs removed upstream | Descriptive shell structure; no CI or changing-set context contrast |
| Yoo et al. dots 2024 (8 tasks) | 2,400 reports from 600 participants | n=30 per size/arm; r=2,3,5,6 | Participant blocks reconstructed from documented export loop; folds align across sizes | Identified-unit conditional prediction/diagnostics |
| gosset breadwheat | 493 | n=16, r=3 | Farmer names redacted; 113 village labels missing | Descriptive context follow-up; no CI or village-adjusted inference |
| SP-Rank (6 audited tasks) | 5,328 strict first-order Rank responses | r=4/5; cohorts kept separate | Repeated worker IDs available | Audit only: no pair changes objective displayed gap |
| Beans | 842 | n=10, r=3 | No assessor ID | Replacement fit, descriptive only |
| Sushi A / B | 5,000 each, shared respondents | n=10/100, r=10 | One report/task/respondent; aligned row folds | Replacement fits with conditional respondent intervals |
| Sounds | 1,380 from 46 assessors | n=12, r=2 | Source assessor IDs; 30 reports each | Direct-pair structure; whole-assessor split and intervals |
| PatrasIQ cost / population | 392 each, shared volunteers | n=36/48, r=6 | Source documents one report/person/task; cross-task matching unavailable | Whole-ranking and context validation; separate per-task intervals |

Dots/puzzle objective answers are external references, not supplied latent population SM centers. Preference sources supply no true center. Catalogs for different 2024 dots report sizes correspond to different images and are never pooled. Numerical lambda/mu do not certify uniform sampling of display subsets.

PatrasIQ likewise provides external objective answer orders, not true latent SM centers. It has 80 distinct bundles per task, each repeated 4–6 times. Both tasks belong to the same volunteer study. The [new source screen](../results/validation_extension/source_screen.csv) excludes Beaches before fitting because its original analysis filtered nontransitive responses; no unfiltered table was verified. Sounds preserves all released reports, including across-report cycles. Potato and breakfast fixed-display sources were screened but not selected for this changed-display question.

## Decoding and exclusions

PrefLib multiplicities are expanded exactly; anonymous records do not restore assessor identities. The 2024 JSON reports encode ordered local item labels; the pinned author export/UI files establish the mapping back to dot images. Each participant's four reports remain together across sizes. No numerical ratings are converted to rankings.

Breadwheat and Beans report best and worst among three distinct displayed items. Best, remaining item, worst is a lossless complete-order decoding. If an invalid report occurs, the entire task is ineligible; no rows are silently skipped. All recorded Beans and breadwheat rows pass. Sushi uses original strict order files, not ratings. All 5,000 rows per task and all 100 Sushi B labels are retained.

The frozen tricot catalog screen covers nine eligible source projects by its predeclared metadata rule. Five lack the target overall trait; four have non-strict reports. All decisions are recorded in results/strict_features/tricot_eligibility.csv; none was fitted or repaired. This earlier screen does not include the later separately specified gosset wheat task.

## Manifests and sources

- [strict_feature_sources.json](strict_feature_sources.json): all 22 PrefLib/dots data and encoding-provenance files.
- [strict_tricot_sources.json](strict_tricot_sources.json), [candidate scope](strict_tricot_candidates.json): nine agricultural projects and source metadata.
- [context_followup_sources.json](context_followup_sources.json): pinned wheat and SP-Rank sources.
- [sources.json](sources.json): original Beans/Sushi bytes, reused unchanged by the replacement.
- [validation_extension_sources.json](validation_extension_sources.json): pinned Sounds, audited Beaches, original upstream objects and two PatrasIQ files; 12 checked source files.

`download_strict_data.py`, `download_strict_tricot.py`, `run_context_followup.py` and `download_data.py` verify their respective sources. Original report arrays are kept in ignored data/raw directories. The unchanged bundled Beans R data file is covered by its existing GPL notice. Sushi source terms prohibit redistribution. [Notices](../THIRD_PARTY_NOTICES.md) and [publication references](../docs/references.md).

`run_validation_real.py` verifies and downloads its sources through `src/validation_extension.py`. All 2,164 eligible new reports are retained; no source observations are repaired or removed. Package names identify sources, not the fitted algorithms.

Sample splits alter training membership only; they never permute the within-report ranking. Simulation observations are generated from the declared conditional laws and recorded seeds in src/strict_features.py. No synthetic manipulation is applied to real data.
