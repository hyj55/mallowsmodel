# Selective Mallows and Plackett–Luce: a comparative study

This repository studies how selective Mallows (SM) and Plackett–Luce (PL) predict a noisy ordering of a displayed set. Both models receive the same ranking reports. The study combines human preferences, objective ordering tasks, agricultural trials, tennis matches, and controlled simulations to examine prediction, sample size, item coverage, population heterogeneity, and model structure.

**The main experiment is P0, the grouped predictive comparison in manuscript Algorithm 4.1.** It compares whole-ranking likelihood-center SM with tuned ridge PL. Sharp, Fotakis, Efficient and global clipped Borda are evaluated together in E0; the global pair-sieve is B0. L0/S0 are supplementary learning/simulation experiments. The Borda-pilot tuned block-sieve experiment is a separately defined computational and predictive supplement, with its own results and limitations.

The main score is the mean negative log probability of a held-out **whole ranking conditional on its displayed set**. Throughout, **$`\Delta=\mathrm{NLL}(\mathrm{SM})-\mathrm{NLL}(\mathrm{PL})`$**: a negative value favors SM. P0/E0/B0 tables and the [L0/S0 result views](results/predictive/scaled_curves.md) show both raw delta and [delta / log(r!)](docs/criteria.md#uniform-reference-scaled-loss-difference), using the displayed/report size r to express the gap relative to uniform-ranking loss. Years, seasons, locations, participant attributes, and numerical ratings are not fitted covariates. Where available, metadata support splitting, grouping, source checks, or explicitly identified diagnostics.

## Read the study

| Start with | What it explains |
|---|---|
| [Data catalogue](data/README.md) | Every dataset, source files, variables, participant identifiers, preprocessing, sample sizes, coverage, and experimental uses |
| [Full-data ranking characteristics](data/features/README.md) | Equal-gap pair rates, frequencies within the same display and Kendall shell, same-pair display effects, sampling support, and every dataset's existing SM–PL NLL gap |
| [P0 main experiment: Algorithm 4.1](docs/predictive_comparison.md) | Algorithm 4.1, five grouped outer splits, finite SM dispersion, training-only PL tuning, exactness certificates and paired uncertainty |
| [P0 main results and analysis](results/main/README.md) | Only likelihood-center SM versus PL: 23-task table, interpretation, 115 paired predictions, exactness and uncertainty |
| [E0 supplementary estimator comparison](docs/estimator_comparison.md) | Unified Sharp/Fotakis/Efficient/global-Borda comparison with PL and likelihood-SM references; paired differences, depth and availability |
| [Five-allocation precision](results/main/split_precision.md) | What the repetitions contribute, five-score means and ranges, MCSE versus CI, and computation tradeoffs |
| [Learning and catalogue size](docs/predictive_learning.md) | Five-repeat Sushi curves and independent fixed-r simulations, with R=10 throughout |
| [Sieve computation](docs/sieve_computation.md) | Sharp without an eight-item guard, exact shortcuts, measured resource limits and the global-sieve supplement |
| [Borda-pilot tuned block sieve](docs/tuned_block_sieve.md) | One allocation for every unresolved Sharp cell, validation-selected blocks, exact local sieves and paired comparisons with existing fits |
| [Fixed-test learning and regularization (L1)](results/regularized_learning/README.md) | Beans and Sushi A/B: five training permutations per budget, dispersion shrinkage, ridge controls and conditional test intervals |
| [Five-fit pair, shell and context diagnostics (C1)](results/regularized_diagnostics/README.md) | Diagnostics on the five saved L1 fits, including Sushi B; no extra outer allocation or ranking-model fit |
| [Research questions and experiment map](docs/experiments.md) | How all analyses fit together; datasets, estimators, repetitions, and result locations |
| [Models and estimators](docs/algorithms.md) | Probability laws, center and dispersion estimation, regularization variants, and admission requirements |
| [Estimator theory and recorded results](docs/theory_alignment.md) | Minimax regimes, which saved comparisons meet their conditions, actual estimator branches, and Theorem 2.17 versus Fotakis |
| [S4: independent Section 4.4 simulation](experiments/section44/README.md) | True-center risk, active hierarchies, proof versus calibrated constants, exact sieve windows, coverage, full rankings, runtime and memory; all S4 code and results are isolated in one directory |
| [Evaluation criteria](docs/criteria.md) | Mathematical definitions of prediction loss, center error, coverage, shell and context diagnostics, and model selection |
| [Uncertainty and resampling](docs/uncertainty.md) | Exactly how each CI, bootstrap, split range, and Monte Carlo standard error is calculated, and the assumptions behind it |
| [Findings](docs/findings.md) | Results organized by scientific question, with links to complete tables and figures |
| [Reproduction guide](docs/reproducibility.md) | How to verify saved outputs or reproduce a specified experiment |
| [Complementary evidence](docs/supplementary.md) | Unpenalized controls, mechanisms, group and temporal analyses, diagnostic validation and optimization controls |

## Experimental structure

The table locates every experimental family. P0 alone is the main experiment; all other rows provide supplementary evidence.

| Component | Question, design and result location |
|---|---|
| **P0: primary prediction** | [Algorithm 4.1](docs/predictive_comparison.md): 23 empirical tasks, five grouped 80/20 outer allocations, training-only PL tuning and finite SM dispersion. Final fits use all development reports. [Main results](results/main/README.md) compare likelihood-center SM with PL and retain exactness status. |
| **E0/B0: center estimators and global sieve** | [E0](docs/estimator_comparison.md) compares Sharp, admitted Fotakis, independently admitted Efficient and global Borda with paired PL/likelihood-SM references on all five P0 allocations. [B0](docs/sieve_computation.md) evaluates global pair-sieve under fixed R=10 and explicitly reuses Sharp results where the procedures coincide. |
| **Borda-pilot tuned block sieve** | [Single-allocation supplement](docs/tuned_block_sieve.md): one allocation/draw for each of 19 unresolved Sharp settings; validation chooses smaller exact-sieve blocks. Compare with saved models on identical test reports and with two Borda controls. The procedure differs from manuscript Sharp. |
| **L0/S0: sample and catalogue size** | [Learning design and results](docs/predictive_learning.md): five-repeat Sushi A/B curves and 240 independent synthetic draws, with report-size bound R=10 fixed. Likelihood-center SM and PL curves have explicitly labeled estimator supplements. |
| **P1/P2: unpenalized prediction and fixed-fit diagnostics** | [P1](docs/repeated_holdout.md) uses five 60/20/20 allocations on all 23 tasks and records finite-MLE and solver availability. [P2](docs/baseline_replacement.md) evaluates specified fits and their diagnostics on one allocation per task. These fitting rules differ from P0. |
| **L1/L2/S3: regularization and exposure** | [L1 results](results/regularized_learning/README.md) use five training permutations per budget and a fixed outer test for Beans and Sushi A/B. [L2 and S3](docs/learning_curves.md) add very small empirical budgets, penalty/shrinkage controls and independent simulation exposure grids. These broader grids include report sizes outside the fixed-R=10 study. |
| **G1: group heterogeneity** | [Group results](docs/group_sensitivity.md): Puzzle/Dots trial groups and Sounds assessors; pooled versus local fits, matched training budgets, five within-group splits and transfer to unseen groups. |
| **S1/S2: mechanism and coverage controls** | [Controlled simulations](docs/strict_feature_analysis.md): matched-noise mixtures, fixed-shell interventions and sparse coverage; independent training draws separate noise magnitude, ranking structure and fit availability. |
| **S4: independent theory-facing simulation** | [Standalone experiment](experiments/section44/README.md): separate calibration and 100 fresh confirmation draws per setting; compare Efficient, Borda, Sharp and small-scale exact Kemeny, including smaller stopping/window/batch constants and a separate full-ranking endpoint. Its outputs are not pooled with any existing experiment. |
| **D1/D2: diagnostic selection and calibration** | [D1](docs/strict_feature_analysis.md#discovery-based-selection) tests discovery-based choices among already fitted predictors. [D2](docs/validation_extension.md) and [context controls](docs/context_followup.md) examine center error, heterogeneous PL, assessor/display confounding and interval calibration. Neither selects P0's model family. |
| **T1: temporal transfer** | [Temporal results](docs/temporal_prediction.md): Beans year transfer and chronological ATP season prediction, with calendar boundaries instead of random outer splits. |
| **C1: structural and optimization controls** | [Structural controls](docs/structural_controls.md): common-order fits, center-objective benchmarks, optimization bounds and a five-fold allocation control. [Pair/shell/context diagnostics](results/regularized_diagnostics/README.md) use the five saved L1 fits and conditional bootstrap intervals. |

[A1 source audits](docs/scientific_audit.md) document eligibility and observation-design checks; excluded sources are not fitted experiments. The [three full-data ranking characteristics](data/features/README.md) describe the complete observed datasets and are separate from predictive experiments and held-out diagnostics.

These are components of one study. Shared data, saved fits and aliased computations do not create independent replications, and outcomes from different fitting rules are not pooled. The [experiment map](docs/experiments.md) gives dataset and estimator allocation; the [supplementary guide](docs/supplementary.md) and [implementation registry](docs/implementation_registry.md) locate detailed reports and outputs.

## S4: independent Section 4.4 simulation

[S4](experiments/section44/README.md) studies true-center Kendall risk and computation under directly generated selective Mallows reports. It compares proof-calibrated and empirically calibrated Efficient/Sharp with global Borda and small-scale exact Kemeny, and separately evaluates the full-ranking majority estimator. The design varies information and coverage, holds R=10 fixed in its bounded-report-size panel, and records actual hierarchy depth, failed exact sieves, time and working memory.

Eighty calibration datasets select constants before 100 fresh confirmation datasets are generated for each of 111 distinct settings. The terminal window remains `W_star = ceil(c_star A (n-1)/(r-1))`; the experiment varies its coefficient and A while preserving the manuscript's padded-block geometry and exact sieve. Smaller constants can activate a hierarchy without improving risk. The [standalone report and paired results](experiments/section44/README.md#results-and-interpretation) distinguish performance against the original calibration from performance against Borda. All S4 code, results and figures remain under `experiments/section44/`; they are not pooled with P0/E0 or other simulations.

## Borda-pilot tuned block-sieve supplement

This experiment asks whether a global Borda pilot and validation-selected smaller blocks make the settings with unavailable Sharp fits computationally usable, and whether the resulting predictor improves test NLL. It covers **12 empirical tasks, three smaller Sushi B training budgets and four simulated settings**, using the existing allocation or draw ID 0 once in each setting. It does not add repeated outer shuffles.

Within each fitting pool, disjoint report/participant pools supply the Borda pilot and exact local sieves. Candidate partitions use 2/3/4 blocks and predefined smaller-block options for larger catalogues. Validation NLL selects the block count; the selected procedure is refitted on train plus validation and evaluated on the unchanged test reports. The block geometry and pilot differ from manuscript Sharp, so its minimax guarantee does not transfer to this variant.

**All 19 final fits complete; 39 of 68 training candidates complete.** Across the twelve empirical full-budget tasks, the variant has lower NLL than PL in **5/12**, likelihood-center SM in **6/12**, full-development Borda in **2/12**, and its own pilot-only Borda in **8/12**. These are descriptive task counts, not independent votes or significant-winner counts. Completion therefore does not establish a general predictive advantage over using all development reports for Borda.

The [standalone report](docs/tuned_block_sieve.md) includes every dataset's scores, candidate availability, selected blocks, paired conditional bootstrap intervals, comparator exactness and interpretation. It also explains weakly informed singleton sieves and a source-label alignment effect in Dots. Intervals condition on the fitted models and supported test units; Wheat has no interval because farmer identities are unavailable. Original Sharp failures remain unavailable, and these results are separate from P0's main analysis.

## Reading the evidence

Controlled simulations exhibit a reversal of the SM–PL predictive ranking while keeping the complete distribution of inversion counts fixed. On empirical data, results depend on the task, fitting procedure, coverage, and evaluation target. Group-specific fitting can help both families at matched training budgets. A reliable real-data diagnostic for identifying an SM generating mechanism has not been established.

P0 has five finite paired predictions for every task. Mean differences favor SM in ten tasks and PL in thirteen, without implying significant winners. Sushi B retains approximate centers in three of five fits and has a small gap relative to partition MCSE. The [main analysis](results/main/README.md) gives all task-level evidence and limitations.

E0 fits global Borda on all 23 tasks (115 allocations). Efficient is independently assessed but its lambda<=1 schedule admits only dots2024 A/B r2; all ten admitted fits have depth zero and equal Borda under a shared tie rule. Borda has lower mean NLL than likelihood-center SM in eleven tasks, equal NLL in eight and higher NLL in four; these descriptive counts are not significance tests. The [unified E0 results](results/estimator_comparison/README.md) compare every method on the same reports. Sharp completes eleven tasks, including ten- and twelve-item catalogues. All active n≤10 Sharp/global-sieve cells are complete. The 155 unavailable supplementary contexts have n≥16; none is a missing P0 main result. [Exact-sieve computation](docs/sieve_computation.md) records their resource limits. [L1](results/regularized_learning/README.md) supplies five fixed-test training permutations per budget for Beans and Sushi A/B.

An error bar is not automatically a confidence interval. Empirical five-partition figures show **±1 partition Monte Carlo SE**; simulation means use independent-repetition t intervals. P0/L0 also save per-split conditional bootstrap intervals at identified test-unit level. Those intervals do not include training variability or form a population CI for the average over splits. All availability and exact-center counts remain explicit. Start with the [uncertainty guide](docs/uncertainty.md).

## Verify the saved study

```bash
python -m pip install -r requirements-lock.txt
python validation_artifacts.py
python -m pytest -q
python validate_predictive_study.py --repository-only
python build_study_reports.py --check
python validate_estimator_comparison.py
python controls/tuned_sharp/validate.py
python controls/tuned_sharp/report.py --check
python controls/l1/validate.py
python controls/l1/validate_diagnostics.py
python validate_scientific_audit.py --repository-only
python validate_validation_extension.py --repository-only
python validate_group_sensitivity.py --repository-only
python validate_repeated_holdout.py --repository-only
```

These checks do not refit the models. The archive restoration command reconstructs recorded outputs and verifies their bytes. Some detailed empirical caches require local source acquisition and are not redistributed. See [reproduction](docs/reproducibility.md), [result dictionaries](results/README.md), [references](docs/references.md), and [third-party notices](THIRD_PARTY_NOTICES.md).
