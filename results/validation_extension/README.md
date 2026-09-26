# Additional-source and mechanism validation outputs

Read [the English report](../../docs/validation_extension.md) first. This directory adds three original real tasks and 1,400 independent synthetic training datasets. It does not overwrite earlier studies. Both design commits preceded fitting; see the manifests and [protocols](../../docs/protocols/README.md).

Run `python validation_artifacts.py` from the repository root to restore the three large files below. They are stored in `artifacts/` as lossless ZIP parts to avoid the stalled large-file upload. The manifest checks every part and the exact original file bytes; no data or numerical result changes. Other tables are directly readable on GitHub.

| File | Contents |
|---|---|
| `source_screen.csv` | Entire declared candidate scope, inclusion/exclusion rationale and source links |
| `real_datasets.csv` | Original and split sizes, sampling units, lambda/mu and coverage |
| `real_scores.csv` | All five method statuses per included/excluded task; confirmation NLL, SM-minus-PL delta and paired unit-bootstrap interval |
| `real_parameters.json` | Actual fitted centers, dispersion/worth, status and optimum certificates; no raw responses |
| `real_splits.csv` | Every included source-record index and its unit/split; no within-report changes |
| `real_predictions.csv` | Confirmation per-report loss for each method, including unavailable values |
| `real_pair_profiles.csv` | Sounds agreement and predictions in three training-defined signed log-worth-gap bins |
| `real_shells.csv` | Exact NLL decomposition into shell mass and within-shell allocation, both held-out splits |
| `real_context.csv` | Fitted/objective-reference within-pair gap slopes, eligibility and exploratory intervals |
| `synthetic_fits.csv` | 2,800 fitted-model rows: exact population NLL, Kendall error, status and coverage |
| `synthetic_parameters.jsonl` | One record per independent training dataset, including both fits and randomized truth |
| `synthetic_draws.npz` | Actual synthetic reports: concatenated `train`, `training_offsets`, 1,000 `diagnostic` rows per repetition, diagnostic `groups`, and `cell_rep` identifiers |
| `synthetic_diagnostics.csv` | All 8,400 budget/reference/adjustment outcomes; unavailable cells retained |
| `synthetic_diagnostic_summary.csv` | Rates, Wilson intervals and separate denominators; conditional on metric availability |
| `synthetic_paired.csv` | Paired exact-population delta for every training repetition |
| `synthetic_prediction_summary.csv` | Per-cell mean and Monte Carlo t interval when all comparisons are finite; separately labeled finite-conditional summaries |
| `confounding_population_controls.csv` | Exact focal-pair marginal contrast and zero within-group contrast |
| `real_manifest.json`, `synthetic_manifest.json` | Frozen seed, scope, protocol hash and execution metadata |
| `validation.json` | Checks actually executed: source hashes, lossless source decoding, unchanged method modules, saved fits/predictions and exact draw replay |
| `artifacts/manifest.json`, `artifacts/part-*.bin` | Exact compressed storage of the large diagnostic CSV, parameter JSONL and draw NPZ; restore with the root helper |

Delta = NLL(SM) − NLL(PL); negative favors SM. Synthetic setting 0/1 in the calibration family means SM/PL. Confounding setting means rho. Training N is distinct from diagnostic budget M. Each independent training dataset has six diagnostic rows (three nested budgets, two reference/adjustment choices), not six independent datasets. The saved `correct` measure selects the better fitted population-NLL predictor, not the generator label. `reject_zero` is two-sided; `positive` means the lower 95% interval endpoint exceeds zero. Both are conditional on their recorded availability denominator. The confounding family's `reject_sm` uses the fixed beta=0.8 diagnostic reference, not its trained SM fit; it is not a primary claim in the report.

Synthetic summaries contain 21 unavailable PL comparisons at N=28. The unconditional cell means are left missing. In the severe-confounding small-budget cell, many adjusted diagnostics are unavailable and the remaining nominal intervals are poorly calibrated. Neither failure is repaired or excluded from reporting.

Reproduce in a separate checkout:

```bash
python validation_artifacts.py
python run_validation_synthetic.py --workers 2
python run_validation_real.py
python validate_validation_extension.py
python make_validation_figures.py
```

Real sources are downloaded and checksum-verified automatically; original responses are not redistributed. `--summarize-only` and `--archive-only` on the synthetic runner recompute summaries or replay exact frozen draws from saved parameters, without fitting. The committed archive was created by that exact replay after the initial fit run and verified against every frozen stream; it is not a second experiment. The original manifest elapsed time refers to fitting and summary generation, excluding the later archive replay. `python validate_validation_extension.py --repository-only` is read-only and requires no external source downloads.
