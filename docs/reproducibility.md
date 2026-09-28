# Reproduction and verification

Use Python 3.12 and a separate checkout so recorded results are not overwritten accidentally. Numerical dependencies and solver versions are fixed in requirements-lock.txt. The current source is the single active implementation; historical variants require the pinned checkout in [History](history.md).

**Current repeated real comparison:** use the [30-partition correction](#repeated-estimation-of-the-original-real-comparison) below. The original real-data commands immediately below reproduce their archived single-split studies; they do not produce the newer repeated averages. Existing simulation commands already generate multiple independent training datasets.

```bash
python -m pip install -r requirements-lock.txt
python validation_artifacts.py
python -m pytest -q
python download_strict_data.py
python download_strict_tricot.py
python run_strict_simulations.py --part bridge
python run_strict_simulations.py --part shell
python run_strict_simulations.py --part coverage
python run_strict_real.py
python run_strict_followups.py --part budgets
python run_strict_followups.py --part objective
python run_context_followup.py
python run_baseline_replacement.py
python validate_strict_features.py
python validate_scientific_audit.py
python make_strict_figures.py
python run_validation_synthetic.py --workers 2
python run_validation_real.py
python validate_validation_extension.py
python make_validation_figures.py
```

The strict simulation/real seed is 202609251, wheat seed 202609252, baseline replacement seed 202609253. Dataset, training, diagnostic and estimator randomization streams are fixed separately where specified. All models within a task receive the same reports. Discovery is disjoint from confirmation; neither selects an optimizer after seeing test performance.

The additional validation seed is 202609260. Its 1,400 independent synthetic training datasets are new, separate from the 4,760 earlier datasets. Each has three nested diagnostic budgets; these are not independent replications. Exact synthetic draws are saved in results/validation_extension/synthetic_draws.npz and replayed against the frozen random streams. The three eligible real tasks retain every original report and use the pre-fit source amendment's fixed split indices. Beach is excluded before fitting, not after inspecting performance. See the [extension report](validation_extension.md) and [file dictionary](../results/validation_extension/README.md).

Three large extension outputs are committed as lossless archive parts because the large-file upload did not complete. `python validation_artifacts.py` restores their exact original bytes and verifies file, archive and part SHA256 hashes; it performs no fitting, resampling or numerical alteration. It refuses to overwrite a changed local output. The CSV, JSONL and NPZ names in the result dictionary refer to these restored files. The read-only CI workflow restores and checks them locally before validation. `--pack` is for packaging a deliberately completed new run, not for altering the recorded study.

Extension empirical per-report predictions and unit/split records remain in ignored local caches. They are not published to GitHub. The frozen seed and source-index rules reconstruct the same split; full validation checks aggregate predictions from source reports and saved parameters without requiring these caches. When locally available, the caches receive additional record-level checks. Synthetic archives contain no empirical participant records.

Sharp exact sieve blocks above 8 are unavailable. Section 3 accepts only lambda<=1 and every recorded successful fit uses zero hierarchy stages. Exact subset DP is guarded at n<=18; larger centers use the cited integer formulation with a 120-second certificate requirement. Solver timeout returns unavailable, never a heuristic estimate. Certified ties can have different chosen orders on another solver version; compare the objective certificate and disclose prediction changes rather than forcing a match.

Source downloaders reject a changed checksum. No raw ranking files are copied into new repository outputs. Results contain aggregate losses, actual fitted parameters and anonymous split indices. NaN means unavailable; infinity is a divergent loss. A Python JSON NaN is used in some stored historical/current parameter records and must be read with an appropriate parser.

The complete 4,760-dataset simulation is already recorded. Its earlier GitHub recovery replay is not another independent study. The scientific audit refitted 17 real tasks and ran three replacement tasks; all earlier strict fitted parameter values and predictive point values matched. See results/audit/refit_comparison.json and the [audit](scientific_audit.md). Run only the affected experiment when modifying a method or inference rule; do not reinterpret a rerun as independent evidence.

Uncertainty definitions and withdrawal of unidentified-unit intervals are specified once in [algorithms.md](algorithms.md). Reported real intervals are conditional on fixed training fits. The source/metadata search is exploratory; data-dependent discovery is not population-level evidence about how often a model wins.

The GitHub verification workflow has read-only repository permissions. It checks tests and all repository-only validators; it does not push experiment outputs, change published estimates, or automatically run the full simulation after a documentation edit. Full data checks can be run locally with the commands above.

## Repeated trial/assessor sensitivity

The [group-sensitivity protocol](protocols/GROUP_SENSITIVITY_20260927.md) uses root seed 202609270 and was committed before production fits. Nine tasks use 100 within-group 70/30 splits, 20 splits each at 50/50 and 80/20, and 100 separate whole-group holdouts. The recorded run used Python 3.13.7 with the pinned NumPy/SciPy/pandas versions in the result manifest.

```bash
python run_group_sensitivity.py --workers 4
python validate_group_sensitivity.py
python validate_group_sensitivity.py --repository-only
python make_group_sensitivity_figures.py
```

The runner downloads only missing sources, verifies their hashes, and exactly reconciles original trial frequencies with pinned PrefLib data. Original reports and detailed fit/membership records remain in ignored `data/raw/group_sensitivity/` and `results/private/group_sensitivity/`. Full replay needs the private cache generated by the runner; public-only validation verifies published hashes and aggregation without downloading respondent records. It does not refit or claim record-level reconstruction.

`--quick --datasets puzzle-5 sounds` is an implementation check, saved to a separate private directory and never admitted to published summaries. Full dataset batches can be replayed read-only with `python validate_group_sensitivity.py --datasets puzzle-5 puzzle-7 puzzle-9 puzzle-11`; the recorded validation used two such batches followed by a six-table recomputation, documented in `results/group_sensitivity/validation.json`. No fitted estimates were changed by validation.

On systems where Python does not recognize the local HTTPS certificate chain, repair the local CA configuration or use a trusted HTTPS client to download the manifest's exact URLs into the specified cache paths. The loader still verifies SHA256 and byte size; do not disable certificate verification or accept changed sources.

Repeated-split percentiles are descriptive partition ranges, not independent-person confidence intervals. See the [report](group_sensitivity.md) for finite-mask denominators and the severe Sounds individual-fit limitations.

## Repeated estimation of the original real comparison

The [28 September protocol](protocols/REPEATED_HOLDOUT_20260928.md) was committed before production at [3da7e993](https://github.com/hyj55/mallowsmodel/commit/3da7e993c9ce2ae23a85a418cfa19ac2b138f01d). It corrects 23 earlier single-split real comparisons with 30 new 60/20/20 allocations and full refits per task. It preserves the earlier source decoders, methods, parameter settings and grouping rules, including whole-person Sounds partitions. It does not change the separate group study.

```bash
python download_repeated_data.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python run_repeated_real.py --workers 2
python validate_repeated_holdout.py
python validate_repeated_holdout.py --repository-only
python make_repeated_holdout_figures.py
```

The root seed is 202609280. `SeedSequence([seed, task_split_key, repeat])` separates partition randomization from the fixed original estimator seeds. Sushi A/B share one split key, and each dots2024 arm shares a key across report lengths. The [manifest](../results/repeated_holdout/manifest.json) records all task-specific keys, exact source/code hashes and Python 3.13.7/locked numerical versions used in the completed run. Raw observations and detailed predictor/membership caches remain local. Full verification replays these caches without refitting; read-only CI verifies the public counts, hashes and averages.

The primary outputs are averages of separately trained confirmation losses, with availability and infinity accounting. The partition Monte Carlo SE measures the precision of that average conditional on the fixed dataset, not population sampling uncertainty. It differs from the partition percentile ranges in the group-sensitivity report. See the [result dictionary](../results/repeated_holdout/README.md) for all denominators, resume/batch behavior and quick-check commands. Source acquisition leaves existing source manifests unchanged and rejects mismatched bytes.

The already completed real and synthetic sample-size curves are indexed [here](learning_curves.md). The historical empirical curves used older fitting rules and one fixed outer test set; they are not silently substituted for current-estimator repeated curves.
