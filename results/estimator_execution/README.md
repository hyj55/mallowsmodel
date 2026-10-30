# Sharp and Efficient: execution, depth and stopping reasons

[Results map](../README.md) · [Estimator definitions](../../docs/algorithms.md) · [S4](../../experiments/section44/README.md)

This is an audit of the saved experiments, not a new experiment. It does not change an estimator, fit, train/test split, loss, confidence interval or computation budget. Every table separates **normal root stopping**, **global-Borda fallback**, **admission exclusions**, and **terminal-sieve failures**. Depth zero is not a failure by itself. An unattempted fit has depth NA, not zero.

## Reading a row

- `n`: full catalogue size; `r`: items in each report; `N`: reports supplied to this particular fit. Inner fits use their own smaller N. G1 fits use their own group training size.
- `m0=n`: initial schedule cap. Later `m` is a block-size cap, not the number of reports. `M1` is the first-round report budget; `floor(N/2)` is the producer's pilot budget limit.
- `alpha=(r-1)/(n-1)`, `lambda=N*r*(r-1)/(n*(n-1))`, `mu=N*r/n`. Sharp starts at eta=alpha. Efficient searches a decreasing sequence starting at lambda (the explicitly identified exposure producer starts at min(lambda,1)).
- The recorded depth is preserved separately from executed/reconstructed depth. Formula reconstruction is identified in `depth_basis`. A gated method never acquires an invented execution depth. Full-data feature computations and MLE/PL fits do not acquire Sharp/Efficient labels.
- When a root already satisfies eta*m0 <= A, **no first pilot round is executed**. Its w1 and M1 are counterfactual formula diagnostics. Efficient still scores the whole catalogue using global clipped Borda. Sharp still attempts its terminal pair-sieve; its pilot is not an additional global-Borda fit.
- If an Efficient resolution is rejected, a smaller resolution can be chosen. Initial and selected eta are both shown. The exact selected w1/M1 and every attempted stage (m, width, cap, batch) are in the CSV and plan archive. A failed complete schedule may exceed the budget in round two even when M1 alone fits.
- Resource limits and estimates come from receipts. Blank limits were not retained; they are not unlimited budgets. A fitted center with infinite unpenalized dispersion is not an algorithm execution failure; this audit uses center status rather than silently relabeling a nonfinite held-out loss.

## Formulas and meanings

With the configuration's width coefficient cW (normally 1), the first-round diagnostics are

```math
w_1=\left\lceil c_W\left(\sqrt{n/\eta}+1/\eta\right)\right\rceil,\qquad
m_1=\min(n,8w_1),\qquad
M_1=\left\lceil K\eta\{\log C_T+\log8+\log(1+\lambda n)\}\frac{n(n-1)}{r(r-1)}\right\rceil.
```

S4 clamps w1 to at least 1. With rho=tanh(beta0/2), c*=2+2048/beta0^2, t*=min(1/8,beta0/64), b0=min(1/(8c*),t*/8), the proof configuration uses K=max(8,4/(b0*rho^2)) and CT=12/rho. S4 can explicitly replace K, cW, A and the terminal coefficient. The exact constants used are stored per plan. Sharp's terminal width is W*=ceil(c_terminal*A/alpha), normally c_terminal=8; it is distinct from the pilot w1. Padding gives an upper cap 8W*, clipped by actual items. The tuned disjoint-block variant has neither this W* nor this hierarchical depth.

The A test is the producer's stopping rule, not a statement that A is the only possible obstruction. `8w1 >= m0` is a separate geometry check. `M1 > floor(N/2)` is an immediate budget obstruction only for a round the schedule actually proposes; a counterfactual large M1 cannot be called the cause of a root A-stop.

## Coverage and provenance

E0 includes the independently assessed Efficient result for every empirical allocation. P0 contains only the main likelihood-center SM/PL comparison and needs no Sharp/Efficient table. B0 is the global-sieve alias of E0 Sharp, and L0's N=4000 endpoint reuses E0; aliases do not add fits. L0/S0 retain their actual conditional Efficient-fallback policy. D1 reuses S1/S2 model fits. D2, L1 and the C1 center benchmark contain no literal Sharp/Efficient fits; a standalone Borda or insertion method is not renamed Efficient.

P2 covers all fixed-allocation sources, plus the explicit Beaches screening exclusion. G1's public receipt projection contains every Sharp/Efficient fit context at repetition IDs 0–4, including each group and equal-budget control, without report indices or participant identities. The inputs manifest identifies the originating receipts. G1's unseen-item, lambda and item-count gates are study-specific admission rules, not universal impossibility claims about the estimator.

S3 exposure, L2 and T1 retain their recorded producer from the [implementation snapshot](https://github.com/hyj55/mallowsmodel/tree/89b21645d5f7eb463cc90c4e982c3a66ce805b41). That producer caps Efficient's initial resolution at 1 even for lambda>1. Those executed extension fits are explicitly distinguished from the outside-domain exclusions in other studies. L2/S3 inner dispersion-selection schedules use the runner's documented floor(0.8N), and are reconstructed, not saved inner-fit receipts. Their shrunk predictions reuse the same center and are not counted again. Insertion's deterministic Efficient starting order reuses the same schedule; it is not an additional estimator comparison. T1's final yearly fit parameters are available, but its inner chronological sample counts and inner center metadata are not retained in the linked receipts; their exact first-round parameters are unavailable and are not guessed. The separate schedule-feasibility CSV in the snapshot is a theoretical preflight, not a fitted dataset or an observed depth.

S4 calibration, confirmation and fresh-process resource profiles have separate tables. Resource profiles rerun existing datasets and are not independent simulation repetitions. Proof and calibrated configurations remain separate. The Borda-pilot tuned block-sieve table includes every validation candidate and development refit, including unsuccessful candidates; its Efficient reference table identifies reused predictors.

The [CSV](fits.csv.gz) is the fit-level index with source locators and exact numeric values. [Plans](plans.jsonl.gz) contain all attempted resolutions and stages without storing ranks or losses. [Inputs](inputs/sources.json) identify immutable snapshot blobs and sanitized G1 receipts. Decimal display rounding and resource ranges apply only to Markdown; no averaging changes schedule parameters. Rebuild or verify with `python build_estimator_execution.py` or `python build_estimator_execution.py --check`. Neither runs a scientific fit. The verifier checks every published byte against its manifest; schedule replay allows relative/absolute tolerance 1e-14 only for floating-point fields (such as logarithms), while integer widths, report budgets, depths, branches and status decisions must agree exactly across platforms.

## Tables by result family

| Result family | Contexts | Audited zero/excluded/fallback/unavailable | Parameter rows | Successful positive-depth contexts |
|---|---|---|---|---|
| [E0](E0.md) | 230 | 230 | 46 | 0 |
| [G1](G1.md) | 22320 | 22320 | 420 | 0 |
| [L0](L0.md) | 120 | 120 | 24 | 0 |
| [L2](L2.md) | 115 | 115 | 23 | 0 |
| [P1](P1.md) | 230 | 230 | 46 | 0 |
| [P2](P2.md) | 48 | 48 | 48 | 0 |
| [S0](S0.md) | 480 | 480 | 24 | 0 |
| [S1](S1.md) | 6400 | 6400 | 160 | 0 |
| [S2](S2.md) | 2760 | 2760 | 69 | 0 |
| [S3](S3.md) | 4440 | 4440 | 146 | 0 |
| [S4-calibration](S4-calibration.md) | 4800 | 2820 | 141 | 1980 |
| [S4-confirmation](S4-confirmation.md) | 36000 | 30928 | 312 | 5072 |
| [S4-resources](S4-resources.md) | 360 | 309 | 309 | 51 |
| [T1](T1.md) | 10 | 10 | 10 | 0 |
| [Tuned-block](Tuned-block.md) | 87 | 87 | 87 | 0 |
| [Tuned-reference](Tuned-reference.md) | 19 | 19 | 19 | 0 |
