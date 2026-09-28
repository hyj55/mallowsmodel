# Repeated holdout correction for the existing real-data comparison

28 September 2026. Requested by the repository owner after the trial/assessor follow-up. Freeze this amendment before production fits. The purpose is to estimate average predictive performance over random train/test allocation and reduce Monte Carlo error from a single partition, not to make a new split-sensitivity study.

## Audit and scope

Current main at 551368d48a0b87e7f8573d0f28efa1ac66e4c625 contains 23 previously fitted real tasks with only one frozen 60/20/20 training/discovery/confirmation split: 3 baseline replacements (Beans, Sushi A/B), 16 strict-feature tasks (8 PrefLib and 8 dots2024), wheat, and Sounds plus 2 PatrasIQ tasks. Test-only bootstrap draws are not new training splits. Source-only exclusions and SP-Rank structural audits have no fitted experiment to repeat.

The existing 4,760-dataset strict simulation uses 40 independently generated training datasets per cell; the 1,400-dataset validation simulation uses 200 per cell. These already average over training randomness and are not rerun. The separate group-sensitivity study remains unchanged.

Historical learning curves already exist at commit 89b21645d5f7eb463cc90c4e982c3a66ce805b41: Beans N=20,50,100,200,400,673 and Sushi A N=20,50,100,300,1000,3000 (5 training subsamples each); Sushi B N=100,300,1000,3000 (3 each). Those curves reuse one outer test set, and use legacy stabilization/optimization choices. They must not be presented as repeated outer splits or current exact-MLE results. The current strict simulations also vary N. Per the user's permission to reuse an existing learning-curve study, this amendment indexes those studies and does not duplicate the historical curves.

## Repeated estimation

Use 30 new, independently seeded random partitions per task, root seed 202609280. Keep the original 60/20/20 fractions, integer rounding and sampling-unit definitions; re-fit all models from scratch for every partition. Average confirmation losses across repetitions. Retain original single-split results as historical records and present repeated estimates as the current predictive comparison. Do not overwrite results to make older protocols appear prospectively repeated.

- Sushi A/B use the same respondent membership in every repetition; their results are not independent studies.
- Each dots2024 arm uses aligned participant assignments across its four report-length tasks. Different arms have separate streams.
- Sounds keeps every assessor's reports on one side of the split, preserving the original new-assessor prediction target. It is not the within-person design of the group-sensitivity study.
- Beans, wheat and anonymous PrefLib use the original report-level allocation; unavailable identities are not invented. No new stratification or grouping is introduced under the guise of correcting repetition. Their results remain descriptive with respect to unknown person/field dependence. PatrasIQ retains its documented one-report-per-volunteer-per-task units; cross-task identities cannot be recovered.
- Each original report appears exactly once in training, discovery or confirmation per repetition. Keep the complete item catalog and original ranking lengths. No outcome-dependent split retry, deletion, repair, tuning or coverage rescue. The discovery set stays separate, even for tasks without a selection step.

## Estimators and diagnostics

Use the five existing methods unchanged: original Hunter unpenalized PL, exact SM center (subset DP up to n=18, certified integer formulation above that, 120-second limit), literal Sharp, Section 3 efficient, and separately named clipped Borda. Keep their original beta0=.1 and task-specific estimator seeds, independent of the new partition stream. Do not introduce Fotakis, new regularization or a new estimator-admission policy into this correction. Sharp is mechanically evaluated as in the earlier experiment, without claiming its sparse-regime theorem applies outside its stated domain; efficient's existing schedule guard remains in force. Record all item/pair coverage, missing finite PL MLEs, solver non-certification and SM boundary losses. Unknown sufficient constants and uniform-design/independence assumptions are not certified by empirical coverage.

Recompute the existing descriptive context/shell diagnostic points for tasks that originally used them, with fitted and available objective reference orders as applicable. Recompute discovery selectors for the strict-feature tasks and evaluate them only on confirmation. Do not average old bootstrap interval endpoints or reinterpret 30 overlapping datasets as new independent participants. This amendment does not repeat thousands of test-only bootstraps: the original conditional intervals stay with their original fixed fits; new diagnostic averages are explicitly descriptive, conditional on diagnostic availability.

## Loss accounting and numerical precision

The primary statistic is the arithmetic average over repetitions of each confirmation whole-ranking mean NLL. Also average the paired difference delta=NLL(SM)-NLL(PL) on the same confirmation reports; negative favors SM. This is an average loss of separately trained models, not the likelihood of an ensemble formed by averaging predictive probabilities.

Distinguish unavailable estimates (NaN) from a defined predictor assigning zero probability (positive-infinite NLL). If any repetition is unavailable, the unconditional across-all-repetitions mean is unavailable; if all are defined and any is infinite, it is infinite. Publish success/finite counts and explicitly conditional finite-only means separately. Pairwise finite-case means must disclose their denominator and do not establish unconditional superiority. Do not average SM/PL means over different successful split sets and call their difference paired.

For all-finite scalar metrics, report SD/sqrt(30) only as conditional Monte Carlo standard error from independent partition randomization on this fixed dataset. This numerical precision measure does not estimate population sampling uncertainty, does not assume independently sampled overlapping participants, and does not justify a population significance test. For availability-restricted means, any analogous precision field is labeled finite-conditional with its number of eligible repetitions. No split percentile band is presented as a confidence interval. Repetition reduces partition Monte Carlo variation; it does not remove sampling bias, unidentified dependence or finite-data uncertainty.

## Verification and publication

Verify pinned source hashes and record the source/algorithm/code versions. Tests must check exact counts, coverage of all reports, disjoint memberships, independent repeat streams, Sushi and dots alignment, whole-person Sounds separation, failure/infinity accounting and conditional Monte Carlo summaries. Replay every stored fit's predictions, split memberships, diagnostic points and selection outputs without re-fitting, then recompute public summaries. Keep raw source records and detailed per-report caches local. Publish all repeats, not a selected subset, plus English/Chinese reporting and links to the already completed learning-curve studies. Read-only CI checks public integrity and aggregation.
