# Supplementary exact sieve computation: E0/L0/S0 and B0

[Primary comparison](predictive_comparison.md) · [Resource receipts](../results/predictive/sieve_resources.json) · [Theory correspondence](theory_alignment.md)

**This chapter concerns supplementary estimators, not the main experiment.** P0 is exclusively Algorithm 4.1's likelihood-center SM versus PL comparison, with [115 available paired predictions](../results/main/README.md). E0 names the empirical Sharp/Fotakis/Efficient comparison. L0/S0 are separate curve experiments and B0 is the global-sieve alias. A failed sieve is not a missing P0 main result.

## Width is a statistical construction, not a computational cutoff

Sharp's terminal width remains

```math
W_\star=\left\lceil8A\frac{n-1}{r-1}\right\rceil,\qquad A=256.
```

A core has at most 2W_star items, with 3W_star padding on each side, clipped at the catalogue boundary. Thus a padded block has at most min(n,8W_star) items. The factor eight in this geometry is retained. The unrelated implementation rule rejecting a block merely because it contains more than eight items is absent from the active predictor.

For the present empirical catalogues n<=100, these conservative widths cover the catalogue and the pilot has depth zero. The actual terminal block has n items, not W_star or 8W_star items. Width is not tuned using test loss or shrunk to make the sieve fit in memory. A and the width rule come from the proof construction; the computational budgets below are implementation choices.

## What the exact pair-sieve computes

Within a block of m labels, choose one unordered pair uniformly from each eligible report's displayed items in that block, without using the reported orientation to choose it. Retain the observed direction afterward. With k retained pairs, define J=binom(m,2) and phi=mJ/k.

Traverse all m! orders in a fixed lexicographic order. Keep an order if its Kendall distance from every previously retained order exceeds phi. Since distance is an integer, this is equivalent to exceeding floor(phi). Minimize the retained-pair disagreement count over this complete greedy packing, breaking objective ties by its enumeration order. A partial packing after a timeout is not an exact sieve.

The implementation uses exact shortcuts that preserve this construction:

| Case | Exact computation |
|---|---|
| No retained pairs | Return the specified first order |
| phi>=J | Every order is within the radius of the first; the packing contains one order |
| phi<1 | Distinct orders are all separated, so the packing is all m! orders; solve its empirical objective by exact DP, with **lexicographic optimum tie-breaking** |
| Other radii | Construct the complete greedy packing from packed pair orientations and score its candidates |

The full-space shortcut uses the selected-pair objective, with exactly the same first minimizing permutation as enumeration. It does not replace the Sharp calculation by fitting a different objective. Multiple 64-bit words support catalogues with more than 64 unordered pairs; simply deleting the former eight-item check would not have fixed that representation issue.

## Resource budgets and measured feasibility

The initial pass uses 1 GiB of working arrays and 120 seconds per distinct packing construction. Every unavailable Sharp context then receives a **30-minute / 4-GiB completion attempt** using the same selected pairs, A, W_star, lexicographic packing and objective tie rule. This completes existing experiment cells rather than adding a new statistical experiment. Arrays are checked before allocation. Complete packings and explicit resource failures are cached by engine, size, integer radius and resource configuration. No incomplete packing or uncertified minimizer is reported as Sharp.

The packing benchmark completed m=9, radius=9 with 185 candidates, and m=10, radius=9 with 1,049 candidates. A ten-item radius-22 packing has only eight candidates. Ten-item radius-1 and radius-4 constructions initially reached the two-minute limit. The completion engine constructs the entire radius-4 packing of **29,086 candidates in about 6.06 seconds**, using a radius-four ball containing 649 permutations and estimated working arrays of 76,495,552 bytes. Radius one uses the exact parity DP described below. Timing depends on hardware and concurrent load; the speedup reflects an equivalent algorithm, not merely a larger cutoff. [Machine-readable receipts](../results/predictive/sieve_resources.json) retain unsuccessful attempts as well as completed constructions.

For larger catalogues at intermediate radii, factorial array requirements can exceed the budget before construction starts. This records a limitation of this exact enumeration implementation, not a proof that every possible exact algorithm is infeasible. A resource rejection leaves the fit unavailable and retains its actual block size, radius and reason. The finite primary likelihood-center predictor is still evaluated independently. Efficient is used only under its explicitly stated fallback policy.

The active entry points are [resource_sieve.py](../src/resource_sieve.py), [predictive_models.py](../src/predictive_models.py), and the completion engine [sieve_budget_retry.py](../src/sieve_budget_retry.py). The byte-locked eight-item implementation in `manuscript_estimators.py` belongs to the supplementary P1/P2/S1 records and is retained solely so those saved results can still be replayed. It is not called for E0/L0/S0 Sharp fits.

## Exact completion algorithms

For an integer radius d, the greedy construction retains the first uncovered lexicographic order, then excludes every order within Kendall distance d. The completion engine generates the inversion ball around the identity by insertion, relabels that ball by the retained order, and marks the corresponding lexicographic ranks as covered. Relabeling preserves Kendall distance. This gives the same retained orders in the same order as testing every remaining permutation against the retained order. Small-catalogue tests compare entire packings, not just prediction scores, against the original implementation.

The original ten-item radius-four construction was also rerun with the larger budget. It finished in 545.53 seconds, and **all 29,086 orders match the completion engine element for element, in the same order**. The [direct comparison receipt](../results/predictive/packing_crosscheck.json) records both timings and the identical normalized array hashes. `python verify_sieve_packing.py` reproduces this comparison; without a cached original packing it can take several minutes.

At radius one the lexicographic greedy packing consists exactly of the even permutations. Two even permutations cannot be one adjacent swap apart. Every odd permutation has an adjacent descent; swapping it gives an earlier lexicographic even permutation, so that odd permutation is already covered. Induction through lexicographic order proves the claim. A subset DP with an additional parity state therefore minimizes the selected-pair disagreement over this exact packing, preserving lexicographic objective tie-breaking. This is not ordinary unconstrained full-ranking MLE. Tests include tied objectives and comparison with exhaustive enumeration.

## Completion results and remaining limits

The current results contain **155 unavailable Sharp contexts**. Global-sieve aliases share their status and are not counted twice.

| Component | Available Sharp fits | Unavailable Sharp fits |
|---|---:|---|
| E0 empirical supplement | 55: eleven tasks × five allocations | 60: Wheat, Sushi B, both PatrasIQ tasks, eight dots2024 tasks |
| L0 Sushi learning | 45: every Sushi A budget, and Sushi B N=20,50,100 | 15: Sushi B N=300,1000,3000 |
| S0 independent simulations | 160 | 80: n=16 and n=32, N=100, both generators |

L0's N=4000 endpoint links to P0/E0 and is not counted twice. Every active n≤10 Sharp/global-sieve fit is available. The smallest missing catalogue is n=16. A separate [Borda-pilot tuned block-sieve supplement](tuned_block_sieve.md) uses one allocation/draw for each of these 19 unresolved task/budget/generator cells. It changes the pilot and block geometry, so its completed fits do not replace these original Sharp failures or inherit Sharp's risk guarantee. The distinct P1/P2 unpenalized controls retain their explicitly documented candidate guard; these are not the resource-accounted E0/L0/S0 fits above.

[Per-context resource status](../results/predictive/resource_retries.csv) identifies the 205 budgeted exact-sieve attempts: 50 complete and 155 fail the enlarged memory admission check. Their predictor records retain original fit-producer and retry fingerprints. These are exact-solver paths for the same estimator, not additional statistical replications. No partial packing or approximate optimum is labeled Sharp. The separate [streaming solver work](https://github.com/hyj55/mallowsmodel/pull/14) remains outside these published fit results.

A covering-count calculation also explains why some larger cases need more than a modest budget increase. A maximal radius-d packing must cover all n! orders with balls of size B(n,d), so it contains at least ceil(n!/B(n,d)) orders. For Wheat, n=16 and d=4, B=3,723 and that lower bound is **5,619,873,728 orders**: at least 179.84 GB just for the retained orders in the current int16 representation. For Dots2024, n=30,d=54, the corresponding storage lower bound is 3.48 TB. These are lower bounds for an explicitly stored packing, not for every possible implicit optimization algorithm. Other cases have weaker bounds, and must not be declared intrinsically impossible from this argument. [Exact counts for the remaining radii](../results/predictive/sieve_cover_bounds.json) are saved separately from measured resource receipts.

## B0: global pair-sieve for bounded report sizes

Every empirical task shared by P0/E0 has r<=10 and therefore enters the separately named B0 global-sieve supplement with the fixed constant **R=10**. The global version selects one uniform pair from every development report and applies the same sieve to the entire catalogue. In these designs Sharp has no consumed pilot reports and exactly one global block. With the same retained-pair seed, the two procedures are identical. Accordingly, `sm_global_sieve` is an explicit alias of `sm_sharp`, including its resource status, rather than another independent fitted result.

Corollary 2.15's first part concerns fixed beta, uniform independent r-subsets, lambda<=1 and r<=R for a constant R, giving the Q∧n² Kendall-risk scale with constants allowed to depend on beta and R. **r<=10 alone does not establish those assumptions.** The empirical rows record numerical exposure but cannot certify a true SM law or uniform assignment. The result concerns center Kendall risk; real-data NLL measures a different quantity.

R does not change when N or n changes. The Sushi learning curves hold r=10; the synthetic sample-size and catalogue-size curves hold r=3. The separate supplementary exposure grid containing r=32, and full-ranking limits where r=n grows, are not used as fixed-R evidence. Computational failure is also not a statistical failure of the corollary: the literal global sieve is a statistical construction without a general efficient-computation guarantee.
