# Selective Mallows and Plackett–Luce: a comparative study

This repository studies how selective Mallows (SM) and Plackett–Luce (PL) predict a noisy ordering of a displayed set. Both models receive the same ranking reports. The study combines human preferences, objective ordering tasks, agricultural trials, tennis matches, and controlled simulations to examine prediction, sample size, item coverage, population heterogeneity, and model structure.

The main score is the mean negative log probability of a held-out **whole ranking conditional on its displayed set**. Throughout, **$`\Delta=\mathrm{NLL}(\mathrm{SM})-\mathrm{NLL}(\mathrm{PL})`$**: a negative value favors SM. Years, seasons, locations, participant attributes, and numerical ratings are not fitted covariates. Where available, metadata support splitting, grouping, source checks, or explicitly identified diagnostics.

## Read the study

| Start with | What it explains |
|---|---|
| [Data catalogue](data/README.md) | Every dataset, source files, variables, participant identifiers, preprocessing, sample sizes, coverage, and experimental uses |
| [Full-data ranking characteristics](data/features/README.md) | Equal-gap pair rates, frequencies within the same display and Kendall shell, same-pair display effects, sampling support, and every dataset's existing SM–PL NLL gap |
| [Primary predictive comparison](docs/predictive_comparison.md) | Algorithm 4.1, thirty grouped outer splits, finite SM dispersion, training-only PL tuning, exactness certificates and paired uncertainty |
| [Primary results](results/predictive/tables.md) | All 23 tasks, estimator availability, loss differences and explicit solver status |
| [Learning and catalogue size](docs/predictive_learning.md) | Thirty-repeat Sushi curves and independent fixed-r simulations, with R=10 throughout |
| [Sieve computation](docs/sieve_computation.md) | Sharp without an eight-item guard, exact shortcuts, measured resource limits and the global-sieve supplement |
| [Research questions and experiment map](docs/experiments.md) | How all analyses fit together; datasets, estimators, repetitions, and result locations |
| [Models and estimators](docs/algorithms.md) | Probability laws, center and dispersion estimation, regularization variants, and admission requirements |
| [Estimator theory and recorded results](docs/theory_alignment.md) | Minimax regimes, which saved comparisons meet their conditions, actual estimator branches, and Theorem 2.17 versus Fotakis |
| [Evaluation criteria](docs/criteria.md) | Mathematical definitions of prediction loss, center error, coverage, shell and context diagnostics, and model selection |
| [Uncertainty and resampling](docs/uncertainty.md) | Exactly how each CI, bootstrap, split range, and Monte Carlo standard error is calculated, and the assumptions behind it |
| [Findings](docs/findings.md) | Results organized by scientific question, with links to complete tables and figures |
| [Reproduction guide](docs/reproducibility.md) | How to verify saved outputs or reproduce a specified experiment |
| [Complementary evidence](docs/supplementary.md) | Unpenalized controls, mechanisms, group and temporal analyses, diagnostic validation and optimization controls |

## Experimental structure

1. **Primary prediction (P0):** 23 empirical tasks and 30 grouped 80/20 outer allocations. PL is tuned within development data; final fits use all development reports. SM uses a prespecified finite dispersion bound. Center comparisons retain exactness and resource status.
2. **Learning and catalogue size (L0/S0):** thirty-repeat Sushi A/B learning curves and 240 independent synthetic draws hold the report-size bound R=10 fixed. Sharp is tried before any eligible efficient fallback. The global pair-sieve supplement (B0) explicitly reuses Sharp where they coincide.
3. **Group heterogeneity:** Puzzle and Dots trial groups and Sounds assessors compare pooled and local fitting, equal training budgets, and transfer to unseen groups.
4. **Mechanism controls:** matched-noise mixtures and fixed-shell interventions separate overall noise from the allocation of probability among mistaken rankings. Calibration experiments test how center error and assessor/display confounding affect diagnostics.
5. **Temporal prediction and structural controls:** Beans year transfer, ATP season forecasts, common-order comparisons, and optimization checks test specific alternative explanations.

These are components of one study. The [supplementary guide](docs/supplementary.md) locates unpenalized P1/P2 controls and the additional questions they answer. Their data reuse does not create independent replications, and numerical outcomes from different fitting rules are not pooled. The [experiment map](docs/experiments.md) covers every component, including results stored at immutable implementation snapshots.

## Reading the evidence

Controlled simulations exhibit a reversal of the SM–PL predictive ranking while keeping the complete distribution of inversion counts fixed. On empirical data, results depend on the task, fitting procedure, coverage, and evaluation target. Group-specific fitting can help both families at matched training budgets. A reliable real-data diagnostic for identifying an SM generating mechanism has not been established.

P0 has thirty finite paired predictions for every task. The likelihood-center mean favors SM in the eight Dots 2013/Puzzle conditions and dots2024 B r=6; the remaining mean differences favor PL, with varying magnitudes and limitations. Sushi B retains approximate centers in 25/30 repetitions. Sharp is computed for eleven tasks, including ten- and twelve-item catalogues. [The findings chapter](docs/findings.md) connects these results to the fixed-R learning curves and the complementary evidence.

The [enlarged-budget exact-sieve completion](docs/sieve_computation.md#completion-results-and-remaining-limits) fills 100 previously unavailable Sharp fits in the existing learning and synthetic cells. All Sushi A learning budgets and all n=10 synthetic sample-size points now have complete Sharp results. The combined tables preserve the same data splits, random streams and estimator definition, with explicit remaining memory failures.

An error bar is not automatically a confidence interval. Empirical 30-partition figures show **±1 partition Monte Carlo SE**; simulation means use independent-repetition t intervals. P0/L0 also save per-split conditional bootstrap intervals at identified test-unit level. Those intervals do not include training variability or form a population CI for the average over splits. All availability and exact-center counts remain explicit. Start with the [uncertainty guide](docs/uncertainty.md).

## Verify the saved study

```bash
python -m pip install -r requirements-lock.txt
python validation_artifacts.py
python -m pytest -q
python validate_predictive_study.py --repository-only
python validate_scientific_audit.py --repository-only
python validate_validation_extension.py --repository-only
python validate_group_sensitivity.py --repository-only
python validate_repeated_holdout.py --repository-only
```

These checks do not refit the models. The archive restoration command reconstructs recorded outputs and verifies their bytes. Some detailed empirical caches require local source acquisition and are not redistributed. See [reproduction](docs/reproducibility.md), [result dictionaries](results/README.md), [references](docs/references.md), and [third-party notices](THIRD_PARTY_NOTICES.md).
