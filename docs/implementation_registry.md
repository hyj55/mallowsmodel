# Implementation and evidence registry

[Experiment map](experiments.md) · [Reproduction](reproducibility.md) · [Frozen protocols](protocols/README.md)

The scientific organization is by research question. This page maps each component to the implementation and evidence that generated its results. Repository paths are technical identifiers; they do not divide the study into separate narratives.

| Component | Matching implementation and outputs | Procedure identity |
|---|---|---|
| Full-data characteristics | `describe_pair_features.py`, `src/pair_features.py`, `data/features/` | Every report; pair frequencies compared within exact h; saved NLLs joined without refitting prediction models |
| P1 repeated prediction | `run_repeated_real.py`, `src/repeated_holdout.py`, `results/repeated_holdout/` | 30 unpenalized full refits per task |
| P2 fixed prediction | Baseline, strict-real, context and validation-real runners and result directories | Fixed training/discovery/confirmation allocation; supported unit-bootstrap inference |
| G1 group heterogeneity | `run_group_sensitivity.py`, `results/group_sensitivity/` | Exact/Fotakis plus admitted Sharp/efficient; unpenalized PL; equal-budget controls |
| S1/S2/D1 | Strict simulation/follow-up runners, `results/strict_features/` | Independent controlled draws, discovery rules and diagnostic budgets |
| D2 | Validation synthetic runner, `results/validation_extension/` | 200 draws per setting, exact population loss and diagnostic calibration |
| L1 and S3 n=10 | [run_experiments.py](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/run_experiments.py), [results](https://github.com/hyj55/mallowsmodel/tree/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results) | Bounded/shrunk SM, ridge PL, specified center approximations |
| L2, S3 exposure and T1 ATP | [run_exposure.py](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/run_exposure.py), [exposure outputs](https://github.com/hyj55/mallowsmodel/tree/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results/exposure) | Exposure variants, fixed penalty controls and chronological forecasts |
| T1 Beans and C1 | [run_followups.py](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/run_followups.py), [run_diagnostics.py](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/run_diagnostics.py), [run_exposure_followup.py](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/run_exposure_followup.py) | Common-order, objective, temporal and diagnostic controls |

The linked implementation snapshot is `89b21645d5f7eb463cc90c4e982c3a66ce805b41`. Use it in a separate checkout to reproduce those exact bounded/regularized procedures; do not copy its scripts into a checkout with incompatible unpenalized helper APIs. Its executable code, output tables, source manifests and protocol records are immutable references. Its prose is not the study's reading guide; the mathematical descriptions and inference qualifications are centralized here.

## Protocol and evidence provenance

Pre-fit design records and amendments are indexed in [protocols](protocols/README.md). The retrospective uncertainty correction is explicitly identified there; it is not presented as a prospective decision. Protocol contents remain fixed because their hashes are part of run manifests. Explanatory documents describe the full study without rewriting those records.

The audit's `retired_paths.json` is a compatibility and integrity list for files absent from this checkout. It is not a scientific exclusion list: learning curves, regularized controls and ATP remain study components through the references above. Numerical outcomes are not pooled across incompatible estimators, and withdrawn inferential claims are not reinstated by including the corresponding point results.

Generated datasets, saved fits, fixed-data repartitions, source recovery and replay have different roles. Replaying a source or an archived random stream adds no independent evidence. Public result dictionaries identify whether an artifact is a scientific output, a storage receipt or a verification record.
