# Source eligibility and design screens

[Data catalogue](README.md) · [Experiment map](../docs/experiments.md)

A source screen is not an SM–PL performance experiment. Excluded or unsuitable tasks have zero fits, and are not counted as model wins or losses. Screening decisions and missing information remain part of the study's evidence.

## Agricultural project catalogue

The [AgrDataSci/tricot-data release](https://github.com/AgrDataSci/tricot-data/tree/169edfaba947b5afee52c1e217e0ff275fb71e34) and [Zenodo record](https://doi.org/10.5281/zenodo.17112492) were screened by a fixed rule: all nine projects listing at least 500 participants. [Candidate metadata](strict_tricot_candidates.json), [source variables and hashes](strict_tricot_sources.json), and [eligibility results](../results/strict_features/tricot_eligibility.csv) preserve the details.

The JSON schema separates `metadata` (genotypes and variables), `block_data` (assigned blocks and project-specific metadata) and `plot_data` (genotype/trait values). Relevant fields are `block_id`, `genotype_name`, `trait`, `collection_moment`, `value_type`, and `value`. Group observations by block and collection moment; a complete strict ranking requires three distinct genotypes and values exactly 1,2,3 for the overall-ranking trait. Project fields differ; a block ID is not automatically a cross-project person ID.

| Project file | Crop / country | Listed participants | Genotypes | Screen outcome |
|---|---|---:|---:|---|
| `amaranth-e7c470820fcb.json` | Amaranth / Benin | 988 | 11 | No overall-ranking trait |
| `okra-9d74b18afc10.json` | Okra / Mali | 675 | 7 | No overall-ranking trait |
| `amaranth-d5ebb545926f.json` | Amaranth / Mali | 675 | 9 | No overall-ranking trait |
| `okra-3aec31c2d6e6.json` | Okra / Benin | 505 | 8 | No overall-ranking trait |
| `amaranth-37af14eaf361.json` | Amaranth / Benin | 543 | 11 | No overall-ranking trait |
| `groundnut-c3c46a31b5cb.json` | Groundnut / Tanzania | 1,000 | 21 | 240 strict of 265 reported; 25 non-strict/incomplete |
| `groundnut-f9d88801f7fa.json` | Groundnut / Tanzania | 599 | 21 | 306 strict of 406 reported; 100 non-strict/incomplete |
| `groundnut-7525d0c24f31.json` | Groundnut / Tanzania | 873 | 40 | 350 strict of 573 reported; 223 non-strict/incomplete |
| `cowpea-46c9305acadb.json` | Cowpea / Nigeria | 504 | 21 | 192 strict of 385 reported; 193 non-strict/incomplete |

Listed participants, reported assessments and complete strict reports are different counts. The whole-task rule rejects the four mixed strict/non-strict tasks rather than retaining only favorable complete responses or breaking ties. Consequently none of these nine projects enters a fitted comparison. This does not exclude the separately specified Beans or Wheat sample tasks.

## Beaches

The BayesMallows release contains 1,442 pair records from 60 assessors over 15 images, with fields `assessor`, `top_item`, `bottom_item`. [Pinned release and upstream objects](validation_extension_sources.json) were inspected. The originating analysis in [Vitelli et al. (2018), Section 6.2](https://jmlr.org/papers/v18/15-481.html) removes nontransitive response patterns. A verified unfiltered table was not recovered. The source was therefore excluded before fitting; no new deletion or tie repair was attempted. This is a provenance decision, not a mathematical incompatibility of two-item reports with the models.

## SP-Rank

The [author release](https://github.com/amrit19/SP-Rank-Dataset/tree/d9ceab3386ac04aca7791fd83da8508851f87dc9) provides fields `workerid`, `problem`, `treatment`, `domain`, `questions`, `options`, `votes`, `predictions`, and `elicitation_format`. Worker IDs identify repeated assessors. Options describe the display; votes contain the response; predictions are separate elicited information, not another observed ranking.

The audit selects actual first-order Rank treatments 4/5/6 and keeps the four-item and five-item cohorts separate using the source worker-ID allocation. Across three domains this yields six tasks and 5,328 strict responses. Parsing validates that each response orders its complete displayed set. In these tasks, no fixed pair changes its objective displayed gap, so they do not identify the targeted within-pair context contrast. [Audit output](../results/context_followup/sprank_audit.csv) records displays, pairs and worker counts. No ranking model was fitted. The screen does not claim these data are useless for every ranking question.

## Other scoped screens

| Source | Available design information | Decision |
|---|---|---|
| BayesMallows potato visual and weighing data | 12 assessors, fixed 20-item display; two assessment modes | Metadata-only screen; not selected for changing-display context, no fit |
| [PrefLib breakfast](https://preflib.github.io/PrefLib-Jekyll/dataset/00035) | 21 households, fixed food display, six meal scenarios | Context changes the scenario rather than the displayed set; metadata-only screen, no fit |
| [Seshadri et al. choice study](https://proceedings.mlr.press/v97/seshadri19a.html) | Context-choice background | No additional eligible complete-ranking release verified; choices are not converted to complete rankings |

[The recorded source screen](../results/validation_extension/source_screen.csv) gives source links and scope. Metadata-only screens do not establish an exhaustive variable inventory or empirical n/r/N/coverage analysis. N and fitted-estimator/CI fields are inapplicable when no experiment was run.
