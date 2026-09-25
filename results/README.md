# Result files

All scores are in natural-log units unless labeled otherwise. Positive `delta`
means SM has larger loss and PL predicts better. Files are aggregate statistics
or fitted parameters, not respondent ranking records.

| File(s) | Contents |
|---|---|
| `real_summary.csv` | Primary means, paired report-bootstrap intervals, shrinkage/near-MLE sensitivities |
| `real_replicates.csv` | Per-training-fit scores, selected penalties, optimizer status, gaps, unseen-item counts |
| `synthetic_summary.csv` | Means and independent-repeat t intervals; true-center errors |
| `synthetic_replicates.csv` | All 360 synthetic comparisons |
| `synthetic_settings.json` | DGP parameters and expected-inversion matching |
| `algorithm_benchmark.csv`, `synthetic_algorithms.csv` | Training Kemeny objectives and algorithm checks |
| `fitted_parameters.json` | Saved SM centers/β, PL log-worths, tuning selections, solver metadata |
| `same_order_*.csv` | Exploratory comparisons constrained to a common fitted order |
| `beans_transfer_*` | 2015-to-2016 transfer |
| `outer_fold_*.csv` | Five-fold descriptive stability, without independent-fold CIs |
| `cutting_plane_pilot.json` | Large-instance lower/upper-bound audit |
| `shell_decomposition.csv` | Exact additive whole-ranking loss decomposition |
| `shell_same_center_sensitivity.csv` | Post-diagnostic constrained-order decomposition |
| `pair_diagnostics.csv` | Pair binary log loss and Brier loss, averaged within reports |
| `adjacent_pair_bins.csv`, `diagnostic_bin_cutoffs.csv` | h = 1 reliability bins and training-defined cutoffs |
| `context_effects.csv`, `context_replicates.csv` | Within-pair gap slopes, intervals, eligibility counts |
| `diagnostic_coverage.csv`, `diagnostic_controls.csv` | Test-set repetition and known-parameter controls |
| `data_manifest.json`, `data_audit.json` | Source hashes and parsed dataset coverage |
| `environment.json`, `validation.json` | Original primary environment and validation |
| `diagnostic*_manifest.json` | Diagnostic seeds, protocol hashes, and checks |
| `repository_validation.json` | Validation of the English repository packaging |

`SM_calibrated_nll` is a historical column name for **validation-selected β
shrinkage**, not a certification of probability calibration. `PL_near_mle_nll`
uses ridge 1e−6 and is not an existence-guaranteed unpenalized MLE.
`SM_center_error`/`PL_center_error` in simulations are unnormalized Kendall
distances to the known truth (maximum 45 at n = 10).

`sm_certified`/`reference_certified` indicate global optimization certificates.
At n = 100, `excess_over_best` refers to the listed feasible reference objective,
not a proven optimum; use the lower bound and certification flag as well.
Solver times and time-limited bounds are machine-dependent.

Primary real CIs condition on fitted models; synthetic CIs use independent
dataset repetitions. Diagnostic intervals use another fixed bootstrap seed
and may differ slightly from primary endpoints. Missing context estimates mean
insufficient within-pair gap variation, not a zero effect.

`private/` is ignored by Git. Full experiment reruns create per-report loss
caches there; do not redistribute Sushi-derived respondent-level files.
