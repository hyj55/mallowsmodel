# Baseline replacement outputs

The real-data files here retain the original single split. Their repeated-refit averages are in [repeated_holdout](../repeated_holdout/README.md); simulations and source-only audits in this directory are unchanged.

[Report](../../docs/baseline_replacement.md) · [frozen protocol](../../docs/protocols/BASELINE_REPLACEMENT.md).

`scores.csv` contains every method status and conditional confirmation NLL; `parameters.json` stores the actual centers, beta, PL worths and optimum/convergence certificates. `datasets.json` reports source and training coverage. `splits.csv` preserves all source row memberships and shared Sushi respondent folds. `data_manifest.json` verifies the original source bytes. `validation.json` records replay from stored fits and source reports.

Beans receives no inferential interval because assessor identities are unavailable. Sushi intervals are conditional on fixed fits and use whole respondents. No respondent ranking data are distributed. Run `python run_baseline_replacement.py` in a separate checkout to reproduce.
