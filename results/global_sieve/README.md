# B0: supplementary global pair-sieve comparison

[Construction and theorem scope](../../docs/sieve_computation.md#b0-global-pair-sieve-for-bounded-report-sizes) · [Empirical B0 summary](summary.csv) · [E0 Sharp results](../estimator_comparison/README.md) · [P0 main experiment](../main/README.md)

B0 concerns the exact global pair-sieve and the bounded-report-size theory with fixed R=10. It is not Algorithm 4.1's main experiment. Its empirical summary has 23 tasks, with `raw_study=P0` preserving their shared allocation-family key and `study=B0` naming this supplementary comparison.

In every recorded empirical configuration, Sharp has zero pilot depth and a single catalogue-wide terminal block. With the same selected pairs and tie rule, global sieve and Sharp are identical. The 330 available empirical B0 rows and 360 unavailable rows therefore alias E0 Sharp; they are not another 690 independent fits. The same alias rule is recorded in the L0/S0 raw tables. An unavailable Sharp/global-sieve pair is counted only once in the 530 outstanding computations.

The report-size bound alone does not verify uniform displays, independence, a true SM law, or the corollary's lambda condition. Empirical predictive NLL is a different target from minimax center Kendall risk. Full details and resource limits are in the linked construction chapter.
