# Reproduction and provenance

## Environment and entry points

Run from the project root with Python 3.12. Install `requirements-lock.txt` for
the recorded package versions; `requirements.txt` is the less restrictive
alternative. SciPy supplies HiGHS through `scipy.optimize.milp`; no commercial
solver or R installation is needed. `rdata` reads the bundled R data file.

| Command | Work performed | Needs original Sushi data? |
|---|---|---|
| `python -m pytest -q` | Exhaustive solver, sampler, likelihood, and gradient checks | No |
| `python make_figures.py` | Replot saved primary results | No |
| `python download_data.py` | Download missing inputs, verify SHA256, audit coverage | Downloads it |
| `python download_data.py --verify-only` | Check local inputs and audit coverage | Must already exist |
| `python run_experiments.py --part real` | All 72 real-data paired fits and algorithm benchmarks | Downloads if absent |
| `python run_experiments.py --part synthetic --synthetic-reps 30` | All 360 synthetic paired fits | No |
| `python run_followups.py` | Same-order, year-transfer, and five-fold checks | Downloads if absent |
| `python run_followups.py --cutting-plane` | Also run two 60-second bound audits | Downloads if absent |
| `python run_diagnostics.py --same-center` | All mechanism diagnostics and same-center sensitivity | Downloads if absent |

The follow-up and diagnostic scripts can use the committed fitted parameters
without regenerating undistributed `results/private/` caches. Main experiments
generate these caches locally but no downstream reproduction step requires
their distribution. Dataset byte mismatches are errors, not automatic updates.

Commands overwrite the corresponding result/figure files. Synthetic runs with
fewer than 30 repeats are useful for smoke checks but are **not** the reported
experiment. Full primary real fitting took about 4.2 minutes in the original
environment; other timings depend on hardware. Timed MILP incumbents/bounds
are not guaranteed to be identical across machines. Small-instance DP objective
values, data parsing, and seeded splits should reproduce.

## Shuffling and independent units

Yes, the primary experiment shuffles **report rows**. With seed 20260920, a
permutation supplies the first ceil(0.2M) rows as test and the remainder as the
development pool. Test sizes are 169 for Beans and 1,000 for each Sushi task.
Sushi A/B use aligned indices because they have the same respondents.

For training repetition b starting at zero, the pool is permuted using seed
20260920 + 11 + b. A budget N takes the first N rows, yielding nested budgets.
The first floor(0.8N) of these train the inner fits and the rest tune; final
fits use all N. The same rows are used for both models. Item order within a
ranking is never shuffled, and pairs from a report are never split across folds.

Beans budgets: 20,50,100,200,400,673 (five repetitions).
Sushi A: 20,50,100,300,1000,3000 (five repetitions).
Sushi B: 100,300,1000,3000 (three repetitions).
The exploratory chronological Beans experiment keeps 2015 and 2016 separate;
it only permutes training rows internally.

## Scores and confidence intervals

For test report t and training repetition b, let
$\delta_{tb}=-\log\widehat P_{SM,b}(Y_t\mid S_t)
+\log\widehat P_{PL,b}(Y_t\mid S_t)$.
The real-data estimate is the average of
$\bar\delta_t=B^{-1}\sum_b\delta_{tb}$ over reports. Each of 2,000 bootstrap
draws resamples the report indices with replacement and averages these fixed
paired differences. The percentile interval is conditional on the existing
fits; repeated training fits are not treated as independent datasets.

Simulations have 30 independent data-generation repetitions per setting.
Their CI is $\bar\Delta\pm t_{29,0.975}s_\Delta/\sqrt{30}$.
Five-fold follow-ups report descriptive ranges and pooled loss only, since
their training sets overlap. All reported intervals are pointwise and
exploratory, without multiplicity correction.

## Packaging changes and preserved experiment history

The English repository packages the completed September 2026 experiments.
Original protocols are copied byte-for-byte into `docs/protocols/`; recorded
SHA256 hashes still identify their pre-run content. They are a chronological
record, not an external preregistration. The diagnostic protocol follows the
primary results; its same-center addendum follows the initial diagnostics.

Packaging changes do not change either likelihood, the solver selection,
hyperparameter grid, dataset decoding, or original splits:

- English README, reports, result dictionary, and data documentation.
- Explicit checksum verification and a data-access CLI.
- Download before opening the Sushi archive in diagnostics.
- Reconstruct same-order follow-up splits/losses from saved fits and seeds,
  replacing dependence on local private caches.
- Move protocols under `docs/protocols/` and update file references.
- Bundle the unchanged Beans file with upstream licensing information. The
  original protocol's download-only packaging statement records the earlier
  distribution; Sushi remains download-only.

`results/environment.json` describes the original primary run, not necessarily
the machine viewing this repository. `results/repository_validation.json`
records checks performed on this English packaging. Original CSV tables are
retained, with diagnostic regeneration checked against their numerical values.
The unpublished manuscript and private conversation history are not included.
