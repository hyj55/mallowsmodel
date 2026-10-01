# Selective Mallows and Plackett–Luce: a comparative study

This repository studies how selective Mallows (SM) and Plackett–Luce (PL) predict a noisy ordering of a displayed set. Both models receive the same ranking reports. The study combines human preferences, objective ordering tasks, agricultural trials, tennis matches, and controlled simulations to examine prediction, sample size, item coverage, population heterogeneity, and model structure.

The main score is the mean negative log probability of a held-out **whole ranking conditional on its displayed set**. Throughout, **Δ = NLL(SM) − NLL(PL)**: a negative value favors SM. Years, seasons, locations, participant attributes, and numerical ratings are not fitted covariates. Where available, metadata support splitting, grouping, source checks, or explicitly identified diagnostics.

## Read the study

| Start with | What it explains |
|---|---|
| [Data catalogue](data/README.md) | Every dataset, source files, variables, participant identifiers, preprocessing, sample sizes, coverage, and experimental uses |
| [Research questions and experiment map](docs/experiments.md) | How all analyses fit together; datasets, estimators, repetitions, and result locations |
| [Models and estimators](docs/algorithms.md) | Probability laws, center and dispersion estimation, regularization variants, and admission requirements |
| [Evaluation criteria](docs/criteria.md) | Mathematical definitions of prediction loss, center error, coverage, shell and context diagnostics, and model selection |
| [Uncertainty and resampling](docs/uncertainty.md) | Exactly how each CI, bootstrap, split range, and Monte Carlo standard error is calculated, and the assumptions behind it |
| [Findings](docs/findings.md) | Results organized by scientific question, with links to complete tables and figures |
| [Reproduction guide](docs/reproducibility.md) | How to verify saved outputs or reproduce a specified experiment |

## Experimental structure

1. **Predictive comparison:** 23 empirical tasks, with 30 training/discovery/confirmation partitions and complete refitting on each partition. Fixed-partition analyses provide detailed conditional diagnostics and identified-unit bootstrap intervals.
2. **Sample size and coverage:** empirical learning curves, small-budget comparisons, and independent simulations vary the number of training reports while recording estimator availability.
3. **Group heterogeneity:** Puzzle and Dots trial groups and Sounds assessors compare pooled and local fitting, equal training budgets, and transfer to unseen groups.
4. **Mechanism controls:** matched-noise mixtures and fixed-shell interventions separate overall noise from the allocation of probability among mistaken rankings. Calibration experiments test how center error and assessor/display confounding affect diagnostics.
5. **Temporal prediction and structural controls:** Beans year transfer, ATP season forecasts, common-order comparisons, and optimization checks test specific alternative explanations.

These are components of one study. Each component retains its specified estimator, data membership, and inference target. In particular, a regularized learning curve and an unpenalized repeated comparison estimate different procedures' performance; their numerical results are not pooled as if the procedures were identical. The [experiment map](docs/experiments.md) covers all components, including results stored at immutable implementation snapshots.

## Reading the evidence

Controlled simulations exhibit a reversal of the SM–PL predictive ranking while keeping the complete distribution of inversion counts fixed. On empirical data, results depend on the task, fitting procedure, coverage, and evaluation target. Group-specific fitting can help both families at matched training budgets. A reliable real-data diagnostic for identifying an SM generating mechanism has not been established.

An error bar is not automatically a confidence interval. The 30-partition figures show **±1 partition Monte Carlo SE**, while group figures show **5th–95th split percentiles**. Bootstrap and simulation confidence intervals have different sampling units and assumptions. Unavailable fits, infinite losses, and finite-only summaries are recorded explicitly. Start with the [uncertainty guide](docs/uncertainty.md) before interpreting an apparent difference as statistically resolved.

## Verify the saved study

```bash
python -m pip install -r requirements-lock.txt
python validation_artifacts.py
python -m pytest -q
python validate_scientific_audit.py --repository-only
python validate_validation_extension.py --repository-only
python validate_group_sensitivity.py --repository-only
python validate_repeated_holdout.py --repository-only
```

These checks do not refit the models. The archive restoration command reconstructs recorded outputs and verifies their bytes. Some detailed empirical caches require local source acquisition and are not redistributed. See [reproduction](docs/reproducibility.md), [result dictionaries](results/README.md), [references](docs/references.md), and [third-party notices](THIRD_PARTY_NOTICES.md).
