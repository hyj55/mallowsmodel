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

The predeclared limits are 1 GiB of working arrays and 120 seconds per distinct packing construction. Arrays are checked before allocation. Complete packings and explicit resource failures are cached by size, integer radius and resource configuration. Exact full-space DP has the same resource limits. No incomplete packing or uncertified minimizer is reported as Sharp.

The packing benchmark completed m=9, radius=9 with 185 candidates, and m=10, radius=9 with 1,049 candidates. A ten-item radius-22 packing has only eight candidates. In contrast, the ten-item radius-1 and radius-4 constructions reached the two-minute limit. This is why item count alone is a poor feasibility rule: even at the same m, the radius matters substantially. Timings and incomplete-construction progress are saved in the [machine-readable receipts](../results/predictive/sieve_resources.json); timing depends on hardware and concurrent load.

For larger catalogues at intermediate radii, factorial array requirements can exceed the budget before construction starts. This records a limitation of this exact enumeration implementation, not a proof that every possible exact algorithm is infeasible. A resource rejection leaves the fit unavailable and retains its actual block size, radius and reason. The finite primary likelihood-center predictor is still evaluated independently. Efficient is used only under its explicitly stated fallback policy.

The active entry points are [resource_sieve.py](../src/resource_sieve.py) and [predictive_models.py](../src/predictive_models.py). The byte-locked eight-item implementation in `manuscript_estimators.py` belongs to the supplementary P1/P2/S1 records and is retained solely so those saved results can still be replayed. It is not called for P0/L0/S0 Sharp fits.

## B0: global pair-sieve for bounded report sizes

Every P0 empirical task has r<=10 and therefore receives the global-sieve supplement with the fixed constant **R=10**. The global version selects one uniform pair from every development report and applies the same sieve to the entire catalogue. In these designs Sharp has no consumed pilot reports and exactly one global block. With the same retained-pair seed, the two procedures are identical. Accordingly, `sm_global_sieve` is an explicit alias of `sm_sharp`, including its resource status, rather than another independent fitted result.

Corollary 2.15's first part concerns fixed beta, uniform independent r-subsets, lambda<=1 and r<=R for a constant R, giving the Q∧n² Kendall-risk scale with constants allowed to depend on beta and R. **r<=10 alone does not establish those assumptions.** The empirical rows record numerical exposure but cannot certify a true SM law or uniform assignment. The result concerns center Kendall risk; real-data NLL measures a different quantity.

R does not change when N or n changes. The Sushi learning curves hold r=10; the synthetic sample-size and catalogue-size curves hold r=3. The separate supplementary exposure grid containing r=32, and full-ranking limits where r=n grows, are not used as fixed-R evidence. Computational failure is also not a statistical failure of the corollary: the literal global sieve is a statistical construction without a general efficient-computation guarantee.
