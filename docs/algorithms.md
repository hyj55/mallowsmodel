# Algorithm and inference contract

This is the authoritative method specification for the current repository. Historical variants are documented through [History](history.md), not exposed as alternative defaults.

## Relation to the supplied manuscript

The current study fits the direct subset law P(Y|S). It never obtains selective Mallows observations by deleting items from a sampled full ranking. Pair counts are sufficient for the center objective; using them does not assume the induced pairs are independent.

The manuscript's **Algorithm 4.1 is a regularized predictive protocol**: step 2 prespecifies a dispersion bound/penalty, step 3 uses Proposition 4.3's regularized listwise PL objective. Its Proposition 4.2 also describes the unbounded profile MLE. Therefore the present unbounded-SM/unpenalized-PL study is an explicitly chosen experimental variant using original estimators, not a claim to replicate all of Algorithm 4.1. Regularization is not inherently unscientific or contrary to that manuscript; undisclosed estimator changes would be.

## Published estimator mapping

| Method | Source and implementation | Limitations |
|---|---|---|
| SM exact center DP | Manuscript Proposition 4.1: F(A)=min_i[F(A minus i)+sum_{j in A minus i} W_ij], backtrack last items | n<=18 computational guard; data-independent tie priority |
| Larger exact center | Conitzer, Davenport & Kalagnanam (2006), integer version of LP3, objective equal to total Kendall disagreement | HiGHS replaces their CPLEX 9.1 backend; certified optimum only; no original-runtime/solver-trajectory replication |
| SM dispersion | Manuscript Proposition 4.2 on [0,infinity]; solve expected inversions=observed mean | beta=infinity and infinite test loss retained; no cap or shrinkage |
| Sharp | Algorithm 2.1, Lemma 2.11, equations (3.22–3.23) | Literal constants and schedule; exact sieve limited to block size 8; no substitution |
| Efficient | Algorithms 3.1/3.2, equations (3.4), (3.22–3.23) | lambda<=1 schedule domain; direct entry point now rejects larger lambda; all recorded successful fits have depth zero |
| Clipped Borda | Equation (3.4) with the full catalog | Separate score estimator, not an MLE or a renamed hierarchy outside its domain |
| PL | Hunter (2004), Section 5, simultaneous unaccelerated MM equation (30) | Requires a unique finite MLE; no penalty, pseudo-comparison, component deletion or rank breaking |

Sharp pair extraction selects one uniform unordered pair from each displayed block intersection using randomness independent of orientation. Its sieve uses phi=m*choose(m,2)/k and a fixed lexicographic greedy packing at distance greater than phi; disagreements are minimized **over that sieve**, not all permutations. Pilot reports and subsequent reports are disjoint. Arbitrary choices permitted by the manuscript are fixed before outcomes; they are not tuned to improve test loss.

The score hierarchy uses original whole reports, batch-local appearance denominators, padded cores and accumulated offsets. The test with manually supplied small hierarchy stages checks bookkeeping only; it is **not** an experiment with changed proof constants and supplies no multilevel statistical evidence.

For PL, if W_i counts reports placing i above last, each simultaneous update is

\[
 w_i^{new}=\frac{W_i}{\sum_t\sum_{k<r:\ i\in R_{tk}}1/\sum_{j\in R_{tk}}w_j},
\]

followed only by normalization of the unidentified common worth scale. R_tk is the remaining set at choice stage k. Fixed log-worth change tolerance=1e-10, gradient/report threshold=1e-8, maximum=100000 iterations. Nonconvergence is unavailable, not a new early-stopping estimator. The published update is also checked against an independent likelihood optimizer; that optimizer is a test oracle, not the fitted PL algorithm.

The integer formulation eliminates antisymmetric variables algebraically: x_ij=1 means i precedes j for i<j, objective=sum_{i<j}[W_ij+(W_ji-W_ij)x_ij], and 0<=x_ij+x_jk-x_ik<=1. Feasible integer solutions are total orders. The backend's numerical lower bound and a verified feasible upper bound must certify the same integer objective; an incumbent alone is never used. Different solvers can choose different tied optima, so a stored fit is **one** certified MLE, not proof all MLEs predict identically. We report the actual center and do not compare runtime with the original paper.

## Conditions and what cannot be claimed

Training lambda=Nr(r-1)/(n(n-1)); mu=Nr/n. Numeric lambda<=1 alone establishes neither the sufficient mu condition nor uniform independent displayed sets. The manuscript's sufficient constants are used without finite-sample retuning. On real data beta0=.1 is a fixed schedule input, not an established lower bound on the true signal. Simulations use beta0=.8. No true latent center is supplied for preference datasets; objective dot/puzzle answers are a different reference.

Exact likelihood maximization does not establish minimax Kendall risk. Sharp is not an approximate MLE. Infinite SM predictive loss and nonfinite/nonunique PL MLEs are substantive outcomes. Finite-run averages condition on finiteness when applicable; they do not establish finite unconditional expected plug-in log loss.

## Data and uncertainty

Keep full original reports and catalogs. Preserve ties as ties; do not turn them into strict rankings. Sources requiring invalid-report deletion fail whole-task eligibility. Lossless decoding and one fixed train/discovery/test partition do not alter within-report preferences. Simulated bridges and shell tilts are declared generating laws, never transformations of real data.

Synthetic intervals use independent training repetitions. Identified real respondent units use paired bootstrap sampling of whole units, conditional on training. Anonymous PrefLib and Beans data receive no inferential intervals. Missing wheat village IDs are not imputed or grouped into a fabricated village. Its NLL and unadjusted context slope are descriptive only; the village-adjusted diagnostic is unavailable. Unavailable results are not zeros.

The within-pair slope and shell decomposition are our exploratory diagnostics, not estimators proposed in the manuscript. They help interpret a particular fitted comparison; they establish neither causal effects nor a universally valid selection rule.

## References

[Manuscript and published algorithm references](references.md). The private manuscript is not redistributed. This code is a mathematical implementation, not an author-supplied implementation or a certification of the paper's theorems.
