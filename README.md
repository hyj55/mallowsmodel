# Selective Mallows versus Plackett–Luce

Numerical research on how pair reliability, error allocation within Kendall-distance shells, and displayed-set effects relate to prediction. Python implementations preserve original ranking reports and distinguish published estimators from optimization and diagnostic choices.

**Current status:** repeated trial/assessor sensitivity is complete across nine tasks. At the same training count, fitting the same Puzzle trial improves both SM and PL; larger pooled samples often offset that benefit, and relative model sensitivity varies by condition. Sounds individual fits frequently lack a finite PL MLE or incur infinite SM prediction loss, preventing an overall personal-model winner claim. The earlier three-task and 1,400-dataset mechanism validation remains separate; the specific positive real SM context mechanism is still unconfirmed.

## Start here

1. [Trial/assessor sensitivity](docs/group_sensitivity.md) · [中文详细结果](docs/group_sensitivity_zh.md) — 100 primary shuffles, training-budget controls, group holdout and estimator admission.
2. [Additional data and mechanism validation](docs/validation_extension.md) — Sounds, two PatrasIQ tasks, center uncertainty and assessor/display confounding.
3. [Scientific audit and corrections](docs/scientific_audit.md) — what complied, what did not, and what was withdrawn.
4. [Feature-transition experiments](docs/strict_feature_analysis.md) — 4,760 earlier independent synthetic training samples and 16 original real tasks.
5. [Wheat and SP-Rank follow-up](docs/context_followup.md) and [historical Beans/Sushi replacement](docs/baseline_replacement.md).
6. [Canonical algorithms and assumptions](docs/algorithms.md), [data provenance](data/README.md), [reproduction](docs/reproducibility.md), [references](docs/references.md).

## Interpretation

The primary criterion is conditional whole-ranking NLL, averaged over the same test reports. Delta = NLL(SM) − NLL(PL); negative favors SM. No joint-probability comparison. Raw NLLs across different report lengths are not comparable.

The current unpenalized experiment is **not a literal replication of the manuscript's complete Algorithm 4.1**, which explicitly permits/requires prespecified boundary handling and regularized PL fitting. It uses the manuscript's center/dispersion definitions and Hunter's original MM algorithm under a separately recorded protocol. See the algorithm contract before attributing a result to the paper.

The larger SM MLE uses Conitzer et al.'s integral LP3 formulation with a different solver backend and an optimum certificate. This is an exact-optimization comparison, **not a reproduction of the original CPLEX implementation or its runtime**. Uncertified fits are unavailable. Unavailable sharp sieves are not replaced by MLE; Section 3 is not extended by capping lambda.

No unsupported inference is repaired by inventing sampling identities: earlier PrefLib Dots/Puzzle, Beans and wheat results remain descriptive where the independent units cannot be established. The new PatrasIQ source documents one report per person per task, permitting per-task report intervals despite anonymization; its two tasks are not independent studies. Sounds uses whole-assessor resampling. All real intervals are conditional on frozen fits. Source search and related tasks limit generalization; sparse context intervals are exploratory and not uniformly calibrated.

## Run

```bash
python -m pip install -r requirements-lock.txt
python validation_artifacts.py
python -m pytest -q
```

Experiment commands are maintained in the [reproduction guide](docs/reproducibility.md).

The restoration command verifies and unpacks three large recorded outputs from lossless archive parts. It changes only their storage representation, with no statistical computation.

The extension publishes aggregate empirical results and fitted model parameters. Per-report empirical predictions and sampling-unit/split records are generated locally and are not included in GitHub. The synthetic archive contains only generated observations.

Python 3.12 for the earlier experiments; the group-sensitivity run used Python 3.13.7 with the same pinned packages. Run in a separate checkout to preserve committed results. The n=100 exact-optimization attempt can exhaust its fixed 120-second budget; this is an outcome, not a fallback trigger. See [reproduction details](docs/reproducibility.md).

## Structure

| Path | Purpose |
|---|---|
| `src/strict_models.py` | Single active fitting interface: exact SM, published centers, unpenalized Hunter MM |
| `src/manuscript_estimators.py` | Sharp sieve, score hierarchy, clipped Borda |
| `src/models.py` | Likelihood mathematics, exact subset DP, direct-subset samplers |
| `src/diagnostics.py`, `src/strict_features.py` | Descriptive diagnostics and declared synthetic laws |
| `src/group_sensitivity.py`, `src/group_sensitivity_summary.py` | Recovered groups, repeated splits, coverage admission and paired summaries |
| `src/validation_extension.py` | New source acquisition, lossless decoding and declared heterogeneous PL law |
| `src/data.py`, `download_*.py` | Original-source acquisition and validation |
| `run_*.py` | Current experiments only |
| `docs/protocols/` | Dated original designs and explicit audit amendments |
| `results/strict_features/`, `results/context_followup/`, `results/baseline_replacement/` | Distinct experiments, all outcomes retained |
| `results/validation_extension/` | New real comparisons, all synthetic draws, parameters, statuses and validation |
| `results/group_sensitivity/` | Repeated split and per-group aggregates, availability, source/code hashes and validation |
| `results/audit/` | Refit and repository validation evidence |
| `figures/strict_features/`, `figures/validation_extension/`, `figures/group_sensitivity/` | Scientific figures, PNG for reading and SVG for export |
| `tests/` | Mathematical, boundary and sampling-unit checks |

Historical regularized, shrunk and heuristic experiments are accessible at the pinned commit in [History](docs/history.md). They are no longer mixed into the runnable current pipeline. Git history is preserved; the private manuscript and respondent ranking data are not newly redistributed. [Third-party notices](THIRD_PARTY_NOTICES.md).
