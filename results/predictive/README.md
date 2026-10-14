# Finite predictive comparison and learning results

[Primary tables](tables.md) · [Design and formulas](../../docs/predictive_comparison.md) · [Learning design](../../docs/predictive_learning.md) · [Exact sieve](../../docs/sieve_computation.md)

These outputs cover 690 empirical P0 training contexts, 360 Sushi learning contexts (L0), and 240 independent synthetic contexts (S0). Six method rows per context include all unavailable states and an explicitly reused global-sieve row. They do **not** represent 7,740 independent fits. P0 supplies L0's full-development endpoint without another fit; the intersecting S0 curve cell is fitted once.

| File | Contents |
|---|---|
| [primary.csv](primary.csv) | All 23 tasks and six methods, averaged over 30 outer allocations |
| [learning.csv](learning.csv) | Sushi A/B at N=20,50,100,300,1000,3000, plus P0's N=4000 endpoint; 30 allocations each |
| [synthetic.csv](synthetic.csv) | Fixed-r sample-size and catalogue-size curves, two generators and 20 independent repetitions per cell |
| [repeat_scores.csv.gz](repeat_scores.csv.gz) | Every per-repetition score, paired difference, coverage measure, conditional bootstrap interval and availability flag |
| [predictors.jsonl.gz](predictors.jsonl.gz) | Fitted orders, dispersion, log-worths, selected ridge, inner-validation scores, seeds, data fingerprints and solver/resource metadata; no raw empirical reports |
| [sieve_resources.json](sieve_resources.json) | Complete cached packing receipts and explicit memory/time failures |
| [resource_retries.csv](resource_retries.csv) | All 630 enlarged-budget completion attempts; 100 recoveries and 530 remaining failures |
| [sieve_cover_bounds.json](sieve_cover_bounds.json) | Covering-count lower bounds on explicit packing size for remaining cases; not universal solver memory bounds |
| [packing_crosscheck.json](packing_crosscheck.json) | Direct equality of all 29,086 ordered radius-four candidates from the original and completion engines |
| [streaming/](streaming/README.md) | Bounded-memory exact search, disk-spill checks, and actual search attempts for the 530 remaining contexts; no partial-packing predictions |
| [manifest.json](manifest.json) | Protocol commit, code/source SHA256, exact task inventory and public-output hashes |
| [tables.md](tables.md) | Readable primary and Sharp comparisons |

Standard Python reads the compressed CSV with `pandas.read_csv(path)` and JSONL with `gzip.open(path, 'rt')`. Each JSONL line is one training context, containing its method parameters. Nonfinite unavailable parameters are represented by the strings `nan`, `inf` or `-inf`; successful primary prediction losses are finite.

## Keys and method identity

The score key is `(study,dataset,n,N,repeat,method)`. `r` is report size and `N` is final development reports, including the inner-validation subset used for PL tuning. `n_test` counts complete ranking reports, and `test_units` counts the units available for cluster resampling. `repeat` starts at zero.

| Method | Meaning |
|---|---|
| `pl` | Inner-selected positive ridge PL, refitted on all development reports |
| `sm_likelihood` | Whole-ranking likelihood center, exact DP when small and certificate/gap-labeled integer optimization otherwise; beta in [0,10] |
| `sm_sharp` | Literal Sharp with resource-accounted exact pair-sieve; beta in [0,10] |
| `sm_fotakis` | Published majority-predecessor estimator, admitted only with every pair observed; same beta bound |
| `sm_efficient_fallback` | Algorithm 3.1 only after Sharp resource failure and when lambda<=1; never relabeled Sharp |
| `sm_global_sieve` | B0 global pair-sieve, with `alias_of=sm_sharp` whenever construction and retained pairs coincide |

`certified` and `certified_centers` refer specifically to a **whole-ranking likelihood-center** optimality certificate, not to whether a Sharp packing was computed exactly. Sharp's exact construction is described by `blocks`, `path`, `complete` and `exact` in its parameter metadata. `objective_gap` is an integer Kendall-objective upper bound minus lower bound; an uncertified predictor remains explicitly approximate.

## Score and interval fields

`nll` is mean whole-ranking NLL in nats per report. `delta` is that method's NLL minus the paired PL NLL, on identical reports. PL's delta is zero. `kendall` is distance to a supplied source objective order on empirical tasks where one exists, or to the generating order in S0; these targets must not be conflated.

For each summary cell:

- `available/planned_repetitions` gives the denominator. `*_mean` and its uncertainty are unavailable unless every planned fit is available. `*_conditional_mean` is separately retained and must not substitute for a complete comparison.
- `*_mcse` is the SD across available complete repetitions divided by their square root. On P0/L0 it measures conditional partition precision, not population uncertainty.
- `*_split_q025/q975` are empirical outcome quantiles, not CI endpoints.
- `*_ci_low/high` in the **summary** are Student-t 95% intervals only for S0's independent-repetition mean; they are empty for P0/L0.
- `nll_ci_low/high` and `delta_ci_low/high` in **repeat_scores** are 2,000-draw paired test-unit percentile intervals, only where identities support that resampling unit. They condition on fitted predictors and do not refit. `ci_kind` disambiguates the target.

`lambda_min/max` and `mu` describe exposure, while `missing_pairs` and `unseen_items` describe realized coverage. None verifies uniform random displays or a true model. `R_bound=10` is constant in every row; S0 holds r=3 and L0 r=10.

## Availability states

`sieve_resource_budget` preserves the exact failure reason and actual block size/radius. `not_p_frequent` means a pair is unobserved, so Fotakis is not admitted. `sharp_available` means no efficient fallback is needed; `outside_schedule_domain` means efficient's lambda<=1 domain does not hold. These are not zero losses. An identical unavailable Sharp/global-sieve pair is still an alias, not two unrelated failures.

The tables and figures include the [30-minute / 4-GiB completion pass](../../docs/sieve_computation.md#completion-results-and-remaining-limits). The 100 recovered Sharp fits fill existing L0/S0 cells; repetitions are not added. Predictor records retain each initial failure and the separate completion code fingerprint. All PL and likelihood-center parameters are unchanged.

Use `python validate_predictive_study.py --repository-only` to verify public records and arithmetic. Full local replay additionally requires the source acquisition and private membership/loss caches described in the [reproduction guide](../../docs/reproducibility.md). Source reports and memberships are not redistributed in this directory.
