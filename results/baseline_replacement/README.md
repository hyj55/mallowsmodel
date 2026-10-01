# Fixed-partition Beans and Sushi prediction

[P2 design](../../docs/baseline_replacement.md) · [Data](../../data/README.md) · [Methods](../../docs/algorithms.md) · [Uncertainty](../../docs/uncertainty.md)

These files describe one fixed 60/20/20 allocation of each task under unbounded SM and unpenalized PL. All three exact-center results have optimum certificates. P1 separately averages 30 full refits in [repeated_holdout](../repeated_holdout/README.md).

| File | Contents |
|---|---|
| `scores.csv` | Every method/status, confirmation NLL and paired Δ; conditional test-unit bootstrap endpoints where supported |
| `parameters.json` | Actual centers, β, PL worths, optimum and convergence evidence |
| `datasets.json` | Source sizes and training coverage |
| `splits.csv` | Every source row membership, including aligned Sushi A/B respondent allocations |
| `data_manifest.json` | Original source-byte verification |
| `validation.json` | Saved-fit and source-report replay receipt |

Beans has no supported independent-person interval because farmer identities are absent. Sushi intervals resample whole respondents and condition on the fixed fits. No respondent rankings are distributed. Reproduce with `python run_baseline_replacement.py` in the matching checkout; see [reproduction](../../docs/reproducibility.md).
