# Reproduction and verification

[Study guide](../README.md) · [Experiment map](experiments.md) · [Implementation registry](implementation_registry.md) · [Result dictionaries](../results/README.md)

Choose the experiment and its matching implementation before running a command. Verification checks recorded evidence; fitting creates or replaces outputs. Use a separate checkout for a reproduction run. The published figures and tables are already computed, and editing their explanation does not require rerunning experiments.

## Verify saved public artifacts

The read-only GitHub workflow uses Python 3.12. Numerical dependencies are pinned in [requirements-lock.txt](../requirements-lock.txt); recorded P1/G1 production runs used Python 3.13.7, with versions preserved in their manifests.

```bash
python -m pip install -r requirements-lock.txt
python validation_artifacts.py
python -m pytest -q
python validate_scientific_audit.py --repository-only
python validate_validation_extension.py --repository-only
python validate_group_sensitivity.py --repository-only
python validate_repeated_holdout.py --repository-only
```

The restoration command verifies ZIP parts and reconstructs the exact recorded D2 diagnostic CSV, parameter JSONL and synthetic-draw NPZ. It performs no fitting or resampling and refuses to overwrite altered local outputs. Repository-only validators check public hashes, counts, arithmetic and stated status rules without downloading participant data. They do not claim to replay private respondent predictions.

## Recompute full-data descriptive characteristics

These commands calculate data features and reuse saved NLLs; they do not run a prediction experiment:

```bash
python download_repeated_data.py
python describe_pair_features.py
python make_pair_feature_summary.py
python validate_pair_features.py --sources
python describe_structure_features.py
python make_structure_feature_summary.py
python validate_structure_features.py --sources
```

The descriptor verifies sources and replays saved full-data reference centers by default. Missing ATP annual files are acquired from the pinned manifest. `--refresh-centers` explicitly requests center recomputation. Public-only validation is `python validate_pair_features.py`; it checks the counts, within-h summaries, hashes and NLL join without downloading raw data. [Definitions and file dictionary](../data/features/README.md).

The structure descriptor reuses those references and counts every report for characteristics 2 and 3. It writes public shell/pair summaries to `data/features/structure/` and exact ranking/display tables to ignored `results/private/structure_features/`, respecting source redistribution terms. `python validate_structure_features.py` checks public hashes, aggregation identities, structural availability and the unchanged NLL join. Adding `--sources` independently reconstructs every exact ranking and pair/display count, checks zero-count shell contributions, and verifies each one-item replacement against the original reports. [Definitions, local frequency-table dictionary and limitations](../data/features/structure/README.md).

## Reproduce P1: repeated empirical prediction

```bash
python download_repeated_data.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python run_repeated_real.py --workers 2
python validate_repeated_holdout.py
python make_repeated_holdout_figures.py
```

Root seed 202609280 and `SeedSequence([seed, task_split_key, repeat])` define 30 independent partition randomizations per task. Estimator seeds retain their specified values. Sushi A/B share one split key, and each dots2024 arm shares a key across r values. All methods share the same reports within a repetition. The manifest records exact keys, unit rules, source/core hashes and numerical versions.

The runner retains detailed membership/predictor caches locally. Full validation replays those caches without refitting. `--datasets` supports complete task batches; `--summarize-only` recomputes public aggregates after every task finishes. `--quick` writes implementation-check repetitions to a separate ignored directory; they are not publication repetitions. Certificate availability can vary with platform or load under the fixed 120-second budget; an uncertified solution remains unavailable.

## Reproduce P2: fixed empirical prediction and diagnostics

| Scope | Command | Root seed / outputs |
|---|---|---|
| Beans, Sushi A/B | `python run_baseline_replacement.py` | 202609253; `results/baseline_replacement/` |
| Dots/Puzzle and dots2024 | `python download_strict_data.py`, then `python run_strict_real.py` | 202609251; `results/strict_features/real_*` |
| Objective-reference diagnostics | `python run_strict_followups.py --part objective` | Same strict-feature seed; no confirmation-driven center selection |
| Wheat and SP-Rank screen | `python run_context_followup.py` | 202609252; `results/context_followup/` |
| Sounds, PatrasIQ and Beaches screen | `python run_validation_real.py` | 202609260 with task-index rules; `results/validation_extension/real_*` |

These runners retain one specified 60/20/20 partition per task. Their detailed conditional intervals accompany those fitted models; they are not intervals around P1 averages. The real validation runner automatically acquires missing pinned sources. Full saved-parameter/source verification uses `python validate_scientific_audit.py`, `python validate_strict_features.py`, and `python validate_validation_extension.py`; these may write verification receipts but do not supply extra independent fits.

## Reproduce G1: trial/person heterogeneity

```bash
python run_group_sensitivity.py --workers 4
python validate_group_sensitivity.py
python make_group_sensitivity_figures.py
```

Root seed 202609270 separates task, fraction, repetition, purpose and group streams. Nine tasks use 100 within-group 70/30 splits, 20 each at 50/50 and 80/20, and 100 whole-group holdouts. The loader verifies the original voting archive against every PrefLib frequency. Detailed fits and memberships stay in ignored `results/private/group_sensitivity/`; full validation requires that runner-generated cache. Public verification instead recomputes aggregate tables from published repeat rows.

`--quick --datasets puzzle-5 sounds` is an isolated implementation check. `--datasets` can partition a full run or read-only replay by task. A completed run's [validation receipt](../results/group_sensitivity/validation.json) records which batches and tables were checked.

## Reproduce S1/S2/D1: controlled laws, coverage and discovery

```bash
python run_strict_simulations.py --part bridge
python run_strict_simulations.py --part shell
python run_strict_simulations.py --part coverage
python run_strict_followups.py --part budgets
python validate_strict_features.py
python make_strict_figures.py
```

Root seed 202609251 supplies 40 independent training draws per cell: 3,200 bridge, 1,200 fixed-shell and 360 coverage datasets. Diagnostic-budget analyses reuse 200 bridge fits with nested discovery prefixes; they do not generate additional training replications. The [design](strict_feature_analysis.md) specifies exact population versus fresh-test scoring and all nonfinite rules.

## Reproduce D2: diagnostic calibration and confounding

```bash
python run_validation_synthetic.py --workers 2
python validate_validation_extension.py
python make_validation_figures.py
```

Root seed 202609260 gives seven settings × 200 independent training datasets. Diagnostic budgets 60/200/1,000 are nested within each repetition. `--summarize-only` rebuilds aggregates; `--archive-only` reconstructs exact generated draws from the frozen streams and saved parameters without fitting. Neither operation creates another experiment. The archive and parameter log must contain exactly the same complete repetition identifier set.

## Reproduce L1/L2/S3/T1/C1: bounded and regularized procedures

Use the [matching implementation snapshot](https://github.com/hyj55/mallowsmodel/tree/89b21645d5f7eb463cc90c4e982c3a66ce805b41) in a separate directory. Its helper APIs implement the declared bounded/shrunk SM and ridge-PL variants. Mixing its runners with the unpenalized implementation changes the procedure or fails outright.

| Experiment | Commands in that snapshot | Seed and dependencies |
|---|---|---|
| L1 empirical curves, C1 center benchmark | `python run_experiments.py --part real` | 20260920; downloads verified Beans/Sushi sources |
| S3 n=10 learning grid | `python run_experiments.py --part synthetic` | 20260920; 30 independent streams per law, nested N |
| L2 small empirical budgets | `python run_exposure.py --part real` | 20260925; same outer split rule as L1 |
| S3 n=8 exposure | `python run_exposure.py --part small` | 20260925; 30 repetitions per cell |
| S3 n=64 exposure | `python run_exposure.py --part coverage` | 20260925; separate streams per requested design |
| T1 ATP | `python run_exposure.py --part tennis` | 20260925; chronological allocation, pinned 2009–2019 source files |
| T1 Beans, C1 same order/five folds | `python run_followups.py` | Uses L1 saved parameters; add `--cutting-plane` for the two objective-bound pilots |
| C1 pair/shell/context diagnostics | `python run_diagnostics.py`, then `python run_diagnostics.py --same-center` | 20260925; uses L1 saved parameters |
| C1 ATP common order, L2 fixed penalties | `python run_exposure_followup.py` | Uses saved tennis and empirical exposure parameters |

Install that snapshot's recorded dependencies and follow its source manifests. [Learning curves](learning_curves.md), [temporal design](temporal_prediction.md), and [controls](structural_controls.md) specify the statistical targets. Snapshot result files can be inspected directly without rerunning these commands. Interval limitations in [the shared uncertainty chapter](uncertainty.md) apply even where an immutable table contains unsupported sampling-interval columns.

## Reproduce source-only screening

`python download_strict_tricot.py` applies the declared nine-project eligibility audit. The wheat/context and validation-real runners include SP-Rank and Beaches checks. [Screening records](../data/screening.md) distinguish acquired-and-audited sources from metadata-only leads. Excluded sources receive no fitted SM–PL result.

## Integrity, formats and numerical limits

Source acquisition rejects changed byte counts or SHA256 hashes. Repair a local HTTPS trust-chain problem through the local CA configuration or a trusted client; do not disable certificate verification or accept substituted data. Raw third-party rankings and detailed participant caches are generally ignored by Git. Generated synthetic archives contain no empirical responses.

Sharp's exact terminal sieve is guarded at eight items; exact subset DP at 18. Larger exact centers need a certificate within 120 seconds. All successful efficient fits in the saved study have zero hierarchy depth. Tied exact optima may yield different chosen orders on another solver version: compare objective certificates and disclose prediction differences rather than forcing agreement.

CSV blanks/NaN denote unavailable quantities; infinity denotes divergent loss. Some saved JSON parameter records use Python-compatible NaN/Infinity tokens, so a strict JSON reader may need explicit handling. Verification of stored values is not a new independent experiment. The [protocol index](protocols/README.md) and [result dictionaries](../results/README.md) identify the evidence supporting each run.
