# E0: supplementary center-estimator comparison

[E0 results](../results/estimator_comparison/README.md) · [P0 main experiment](predictive_comparison.md) · [Global sieve B0](sieve_computation.md) · [Experiment map](experiments.md)

E0 asks how replacing the SM center-estimation procedure changes prediction on the same 23 empirical tasks. **It is a supplementary estimator comparison, not the main experiment.** The main experiment is exclusively P0, the Algorithm 4.1 comparison of whole-ranking likelihood-center SM and tuned ridge PL. Sharp is not a replacement required by Algorithm 4.1, and no E0 winner is selected using the outer test to become P0's SM predictor.

## Shared observations and separate estimators

E0 reuses P0's 30 grouped 80/20 outer allocations, development rankings, test reports and tuned/refitted PL reference. Each SM center uses the same dispersion fit on the fixed interval [0,10]. This makes the estimator comparisons paired. It does not create independent replications of the model-family comparison.

| E0 estimator | Construction and reference | Admission |
|---|---|---|
| Sharp | Manuscript Algorithm 2.1, with Lemma 2.11 pair-sieve and the supplied proof-constant width; [reference locator](references.md#supplied-manuscript-m) | A=256 and W_star unchanged; no eight-item guard in this implementation; only a complete exact construction is accepted |
| Fotakis / PosEst | Fotakis et al. (2021), Algorithm 1; [paper](https://proceedings.mlr.press/v130/fotakis21a.html) | Every unordered pair must appear in development data; checked again in each partition |
| Efficient fallback | Manuscript Algorithms 3.1/3.2; [estimator references](algorithms.md#estimator-inventory-and-references) | Only after a recorded Sharp resource failure and only in the lambda<=1 schedule domain; retains its own method name |

The linked [complete estimator map](algorithms.md) gives the manuscript page, formula and implementation for each method. Coverage admission, computational completion and theoretical applicability are different questions. An empirical lambda value or small r does not verify uniform displays, independent reports, a true SM law or all sufficient constants in a theorem.

## Evaluation and uncertainty

For each available estimator and split, evaluate the complete held-out ranking conditional on its displayed set. Compute its mean NLL and its paired difference from the same PL predictor. Average all 30 split values only when the planned set is complete. Report the partition MCSE, split quantiles and explicit availability; a finite-only conditional mean is not substituted for the full comparison. Supported per-split test-unit bootstrap intervals retain the same conditional target as P0 and are not averaged into a CI for the 30-split mean.

The main P0 likelihood-center result is a fixed reference, not a test-selected member of this candidate list. E0 does not assess true-center minimax risk on real data. [S0](predictive_learning.md#s0-independent-data-with-fixed-r3-and-r10) supplies the separately named known-generator curves, with twenty independent draws per cell.

## Global-sieve identity and missing fits

All recorded E0 Sharp schedules have zero pilot depth and a single terminal block covering the catalogue. With the same selected-pair seed, their terminal problem is identical to **B0's global pair-sieve**. B0 aliases the Sharp result; it is not another independent fit. Whole-ranking likelihood-center optimization in P0 is a different objective and does not require this sieve.

Sharp is available for 330 E0 contexts: eleven tasks, each 30/30. The other 360 E0 contexts cover Wheat, Sushi B, both PatrasIQ tasks and the eight dots2024 arm/size tasks. Together with 90 L0 and 80 S0 Sharp fits, these form the 530 outstanding computations. **P0's 690 main paired predictions are already available; none of these sieve failures is a missing main comparison.** [Resource details](sieve_computation.md#completion-results-and-remaining-limits).

## Reading name versus stored key

The frozen runner evaluated several methods under `study=P0`, the common empirical allocation-family key, and exported them to `results/predictive/primary.csv`. These raw identifiers are retained for hashes and replay. Reader-facing names are unambiguous:

| Raw selection | Named result |
|---|---|
| `study=P0`, method `pl` or `sm_likelihood` | **P0 main experiment**, Algorithm 4.1 |
| `study=P0`, method `sm_sharp`, `sm_fotakis` or `sm_efficient_fallback` | **E0 supplementary estimator comparison** |
| `study=P0`, method `sm_global_sieve` | **B0 supplementary global sieve** |

The E0/B0 CSV views include both `raw_study` and `study` to make this mapping explicit. Creating named reports changes no estimator, observation, split, fit, loss or uncertainty calculation. Frozen protocols preserve what was specified before fitting; they do not override this reading nomenclature.
