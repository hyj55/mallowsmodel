# Exact sieve computation and bounded-report supplement

[Primary comparison](predictive_comparison.md) · [Resource receipts](../results/predictive/sieve_resources.json) · [Theory correspondence](theory_alignment.md)

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

The active entry points are [resource_sieve.py](../src/resource_sieve.py), [predictive_models.py](../src/predictive_models.py), and the completion engine [sieve_budget_retry.py](../src/sieve_budget_retry.py). The byte-locked eight-item implementation in `manuscript_estimators.py` belongs to the supplementary P1/P2/S1 records and is retained solely so those saved results can still be replayed. It is not called for P0/L0/S0 Sharp fits.

## Exact completion algorithms

For an integer radius d, the greedy construction retains the first uncovered lexicographic order, then excludes every order within Kendall distance d. The completion engine generates the inversion ball around the identity by insertion, relabels that ball by the retained order, and marks the corresponding lexicographic ranks as covered. Relabeling preserves Kendall distance. This gives the same retained orders in the same order as testing every remaining permutation against the retained order. Small-catalogue tests compare entire packings, not just prediction scores, against the original implementation.

The original ten-item radius-four construction was also rerun with the larger budget. It finished in 545.53 seconds, and **all 29,086 orders match the completion engine element for element, in the same order**. The [direct comparison receipt](../results/predictive/packing_crosscheck.json) records both timings and the identical normalized array hashes. `python verify_sieve_packing.py` reproduces this comparison; without a cached original packing it can take several minutes.

At radius one the lexicographic greedy packing consists exactly of the even permutations. Two even permutations cannot be one adjacent swap apart. Every odd permutation has an adjacent descent; swapping it gives an earlier lexicographic even permutation, so that odd permutation is already covered. Induction through lexicographic order proves the claim. A subset DP with an additional parity state therefore minimizes the selected-pair disagreement over this exact packing, preserving lexicographic objective tie-breaking. This is not ordinary unconstrained full-ranking MLE. Tests include tied objectives and comparison with exhaustive enumeration.

## Completion results and remaining limits

All **630** initially unavailable Sharp contexts were retried: **100 recovered, 530 remain unavailable**. Global-sieve aliases share these statuses and are not counted twice. Existing PL, likelihood-center SM and Fotakis parameters, source reports, train/test memberships, selected-pair seeds, beta fitting and bootstrap streams are preserved. Only unavailable Sharp/global-sieve fits and the resulting fallback-availability labels are updated. Both code fingerprints and the original Sharp failure are retained in each retried predictor record. [Per-repetition completion status](../results/predictive/resource_retries.csv) and the combined learning/simulation tables are the authoritative outputs.

| Component | Newly completed Sharp fits | Remaining unavailable Sharp fits |
|---|---:|---:|
| P0, 23 empirical tasks | 0 | 360: Dots2024 A/B at r=2,3,5,6; PatrasIQ cost/population; Sushi B; Wheat |
| L0, Sushi learning | 60: Sushi A N=100 and N=300, each 30/30 | 90: Sushi B N=300,1000,3000, each 0/30 |
| S0, independent simulations | 40: n=10,N=100 under both generators, each 20/20 | 80: n=16 and n=32 at N=100 under both generators |

L0 also displays the P0 N=4000 endpoints by reference; the unavailable Sushi B endpoint is included in P0's 360, not counted again. All Sushi A learning points and all n=10 synthetic sample-size points now have complete Sharp results.

The remaining attempts fail the enlarged memory admission check, before allocating arrays. The new general packing engine still has factorial storage in its current representation, even though it avoids the previous repeated distance scans. These failures do not prove that a different implicit exact solver is impossible, and no additional completed real-data P0 Sharp task is claimed. Increasing a runtime limit cannot resolve this particular pre-allocation memory failure. Existing approximate Sushi B whole-ranking likelihood centers are a separate optimization problem and are not refitted by this Sharp completion pass.

A covering-count calculation also explains why some larger cases need more than a modest budget increase. A maximal radius-d packing must cover all n! orders with balls of size B(n,d), so it contains at least ceil(n!/B(n,d)) orders. For Wheat, n=16 and d=4, B=3,723 and that lower bound is **5,619,873,728 orders**: at least 179.84 GB just for the retained orders in the current int16 representation. For Dots2024, n=30,d=54, the corresponding storage lower bound is 3.48 TB. These are lower bounds for an explicitly stored packing, not for every possible implicit optimization algorithm. Other cases have weaker bounds, and must not be declared intrinsically impossible from this argument. [Exact counts for the remaining radii](../results/predictive/sieve_cover_bounds.json) are saved separately from measured resource receipts.

## B0: global pair-sieve for bounded report sizes

Every P0 empirical task has r<=10 and therefore receives the global-sieve supplement with the fixed constant **R=10**. The global version selects one uniform pair from every development report and applies the same sieve to the entire catalogue. In these designs Sharp has no consumed pilot reports and exactly one global block. With the same retained-pair seed, the two procedures are identical. Accordingly, `sm_global_sieve` is an explicit alias of `sm_sharp`, including its resource status, rather than another independent fitted result.

Corollary 2.15's first part concerns fixed beta, uniform independent r-subsets, lambda<=1 and r<=R for a constant R, giving the Q∧n² Kendall-risk scale with constants allowed to depend on beta and R. **r<=10 alone does not establish those assumptions.** The empirical rows record numerical exposure but cannot certify a true SM law or uniform assignment. The result concerns center Kendall risk; real-data NLL measures a different quantity.

R does not change when N or n changes. The Sushi learning curves hold r=10; the synthetic sample-size and catalogue-size curves hold r=3. The separate supplementary exposure grid containing r=32, and full-ranking limits where r=n grows, are not used as fixed-R evidence. Computational failure is also not a statistical failure of the corollary: the literal global sieve is a statistical construction without a general efficient-computation guarantee.
