# Repeated-split trial and assessor sensitivity

27 September 2026. This follow-up is requested by the repository owner. Freeze this design before the production runs. Existing empirical results and recovered source counts are known; small implementation/runtime checks are not new confirmatory evidence.

## Questions and sources

Primary: does fitting one law per physical stimulus set change SM versus PL prediction, compared with a shared law within the same difficulty condition? Use all four original Puzzle conditions (40 original trial files each, 3,180 rankings). Replicate descriptively on all four 2013 Dots conditions (40 files each, 3,183 rankings). These are not dots2024. Verify all 24 ranking multiplicities against each currently pinned PrefLib file before fitting. Each original trial file identifies one repeated set of four stimuli; exact board layouts and globally unique board identities remain unavailable. Pooled item labels are difficulty categories; within-trial labels identify that trial's fixed stimuli. Do not merge the four difficulty conditions.

The author archive is https://dl.dropboxusercontent.com/s/mf0mm153pe3f12w/voting-results.tar.gz, linked at https://www.andrewmao.net/code/. Expected SHA256 is 2906b0ce3fc375813f7fd061e55fd642e6e9ac472a385a56d2b8e36ef838e0d4 (16,620 bytes). Original files, normalized observations, fit parameters, and per-report caches remain local and ignored. Publish provenance and aggregate results only.

Assessor analogue: Sounds, 46 identified assessors with 30 original pair reports each, using the already pinned BayesMallows source. Do not invent identities for Puzzle/Dots, Beans or wheat. Sushi, dots2024 and Patras have one report per person within each separately fitted task; their different item catalogs/tasks cannot be pooled to manufacture a per-person replication experiment.

## Frozen split design

Root seed 202609270. Primary: 100 independent random split seeds, 70% training within every trial/assessor. Budget sensitivities: 20 seeds each at 50% and 80% training. For each group of size m, use floor(f*m) intact reports for training and all remaining reports for testing. These are repeated partitions of a fixed dataset, not independent new datasets. Do not reroll a split to improve item coverage, fit existence, or prediction. No tuning or estimator selection uses test outcomes.

On the identical held-out reports for each group, compare:

1. `pooled`: one model trained on all groups' training reports.
2. `local`: one model trained only on the target group's training reports.
3. `matched_pool`: one model trained on a random subset of pooled training reports with exactly the local model's training size. Sampling is without replacement and independent of ranking outcomes. This separates the benefit of sharing a larger sample from the association with group identity; it is not a causal identification of a board/person effect.

The local and matched models have the same training budget. The pooled and local predictors differ in model capacity and access to group identity for routing; both SM and PL receive the same routing information. In Sounds, within-assessor splitting deliberately targets future reports of **known** assessors. It must not be described as a new-person evaluation or as satisfying Algorithm 4.1's new-assessor grouped split.

Additional target: repeat 100 70/30 splits of entire groups, fitting pooled models on all reports of training groups and evaluating all reports of held-out groups. This estimates new-trial or new-assessor transfer. There is no local fit for a group with no training reports. Puzzle trial holdout cannot establish assessor disjointness. These tests are separate predictive targets, not paired report-for-report with the within-group experiment.

## Estimators and admission checks

Use the repository's unchanged direct conditional likelihoods, unbounded profile SM dispersion MLE and unpenalized Hunter equation-30 PL fit. This remains the declared unregularized variant, not the regularized entirety of manuscript Algorithm 4.1. Preserve infinite SM losses and nonexistent/nonunique/nonconverged PL fits; do not cap, add pseudo-observations, drop catalog items, reroll splits, or silently repair estimates. There are no model-selection hyperparameters.

- **SM exact center**: use the existing certified subset dynamic program (n=4 and n=12 are supported). Audit item and pair coverage. Conservatively skip this follow-up's fit if a catalog item is never observed; report center nonidentifiability/ties as a limitation when pair coverage is incomplete. Full pair coverage is not a mathematical requirement for existence of a Kemeny minimizer. No approximate MLE substitution is needed.
- **Fotakis PosEst**: implement Algorithm 1 of Fotakis, Kalavasis & Stavropoulos (AISTATS 2021), counting majority predecessors, including pairwise equal-count ties in both predecessor counts, then sorting scores with a fixed seeded uniform random tie priority. Require every unordered item pair to have at least one joint training appearance, and log empirical p=min(pair count)/N. This verifies the structural p-frequent condition, not a true-model or high-probability recovery guarantee. It is a center estimator, not an MLE; fit beta by the same profile likelihood as the exact center.
- **Sharp / efficient**: distinguish executable algorithms from their statistical theorem domains. Theorems 2.1 and 3.1 impose lambda=N*r*(r-1)/(n*(n-1))<=1. Under the user's request to check applicability, this follow-up conservatively excludes those estimators outside that regime, although the sharp algorithm can mechanically return an order there. Hence the full four-item Puzzle/Dots tasks will not be labeled applications of the sparse-regime sharp theorem. Record exclusions explicitly.
- Inside lambda<=1, use literal Algorithm 2.1 if its exact sieve blocks fit the existing size-8 guard. If unavailable, use the existing Algorithm 3.1/3.2 implementation as the user's allowed computational fallback, only with all items observed. Fix beta0=.1 and report its actual branch, depth, mu=N*r/n and mu/log(e*r). The unknown sufficient constant C0, true beta>=beta0, independent responses and uniform displayed-set assumptions are not established on these real data. Never claim that mu>log(e*r) alone verifies the theorem. No modified schedule or proof constants. The efficient implementation may reduce to its published score-only branch.
- **PL**: require a strongly connected directed comparison graph and the existing numerical convergence checks. Failure is an unavailable estimate, not a zero score or an infinite score invented for an undefined fit.

All candidate fit statuses are recorded even when an estimator is skipped. Tie priorities are fixed before outcomes and independent of the objective reference order. Objective step counts are used only for category decoding, never as the fitted center.

## Metrics and interpretation

Primary loss: conditional whole-report NLL in nats/report. Negative delta=NLL(SM)-NLL(PL) favors SM. Preserve all original reports in the split and eligibility accounting. For each scheme report fit availability, finite-prediction coverage, and finite-only losses with their exact denominators. A conditional comparison on available finite fits cannot establish unconditional superiority.

Compare pooled versus local on a common subset where all four relevant predictions (SM/PL times pooled/local) are finite. Report local-minus-pooled changes separately for each family and the interaction `(SM_local-PL_local)-(SM_pooled-PL_pooled)`. Do the analogous comparison against matched_pool, again using the same four-way mask. Also report how much data these masks exclude and the full-data fit failure/infinite-loss rates. For each group save aggregate repeated-split summaries; do not claim rank-ordered groups with a few test reports have precise effects.

Report report-weighted means and equal-group means. Summarize repetition medians/means, 5th–95th percentile split ranges and sign frequencies. These ranges measure random-partition sensitivity on these fixed observations; they are **not population confidence intervals**, and the 100 splits are not independent subjects. Do not divide uncertainty by sqrt(100), perform an independent-splits t-test, or interpret missing assessor identities as resolved by recovering trial IDs. No causal board effect or true SM/PL mechanism claim follows from this observational exercise.

## Verification and publication

Before production runs, test original-archive parsing and frequency matching; fixed-seed reproducibility; report disjointness; within-group proportions; entire-group disjointness; identical test reports and matched training counts; Fotakis tie/coverage behavior; optimized calculations against the existing likelihood/DP implementations; and failure/infinite-score accounting. Run existing tests plus these controls. Save seeds, source and code hashes, runtime versions, detailed local audit records and aggregate CSVs. A read-only validator must reproduce all published aggregates from cached run records without refitting. Publish an English methods report and a Chinese interpretation. Do not alter earlier results to improve consistency with this follow-up.
