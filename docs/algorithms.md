# Algorithms and assumption checks

The supplied manuscript, *Selective Mallows Estimation from Uniform Partial
Rankings*, defines a Mallows law **directly on each displayed subset** (§1.1).
The SM center likelihood objective is to minimize

`D(pi) = sum_t Kendall(Y_t, pi restricted to S_t)`.

Exact DP solves this objective globally. Greedy and insertion are heuristics
for it; Borda and PosEst are score-based center estimators and initializers,
not direct global minimizers. Their comparison in the appendix is an
optimization audit, not six different probability models.

## Original predictive benchmark

- Beans, Sushi A, and the n=10 simulations: exact subset DP only for the main
  SM fit. There is no reason to substitute a less accurate optimizer here.
- Sushi B: retain eight-start insertion plus a time-limited MILP bound audit.
  Count this as one approximate fitting pipeline; report its residual gap.
  Borda, PosEst, greedy and random orders supply the starts, and are not
  separate SM-versus-PL competitors in the main results.
- Existing baseline results remain for reproducibility in the appendix.
  No algorithm is selected by held-out predictive performance.
- The [exposure extension](exposure_analysis.md) now implements the literal
  sharp sieve and score hierarchy, with explicit computational limitations.
  No minimax claim follows from these finite experiments.

Pair counts are sufficient for this objective; using them is not an assumption
that the pairs within a report are independent. Likelihood evaluation,
train/test splitting and bootstrap all use whole reports.

| Method | Compatible with the conditional likelihood? | Exact center MLE? | Decision |
|---|---|---|---|
| Subset DP, supplied manuscript §4.1 | Yes; arbitrary observed subsets | Yes, all permutations considered implicitly | Main method for n=10 |
| Linear-order MILP | Yes; same weighted Kemeny objective | Only with matching lower/upper bounds | Optimization audit for n=100 |
| Cutting-plane LP/MILP | Yes; same constraints added on demand | Only with certificate | Follow-up improved the large-sample Sushi B bound |
| FKS PosEst, Algorithm 1 | Yes as a center estimator | No | Benchmark; frequent-pair recovery guarantees do not apply automatically to sparse real data |
| Exposure-normalized Borda | Yes as a center estimator | No | Manuscript's global score baseline; uniform-design statistical guarantees stay separate |
| Equal-reliability greedy MAL | Yes for strict subset orders, with common reliability | No general exactness guarantee | Benchmark specialization of Raman & Joachims |
| Eight-start insertion search | Yes; optimizes the correct objective | No | Our generic heuristic implementation, not a new theoretical estimator |
| FKS localization + bounded-displacement DP | Same selective model | Conditional on the localization event | Reviewed, not implemented; small n permits an unconditional exact DP |
| Manuscript efficient hierarchy | Uniform independent subsets, supplied signal lower bound | No | Implemented in exposure extension; all executed fits have depth zero |
| Manuscript sharp estimator | Uniform selective design; local pair extraction and permutation sieve | No | Exact greedy sieve implemented for blocks up to eight items; larger exact blocks unavailable |

FKS's literal `>=` majority rule counts a missing pair as an empirical tie.
We retain this published convention and use seeded random final tie-breaking;
we do not silently invent a sparse-data variant. The number of items seen in
training and test reports containing unseen items are recorded.

## Why the sharp estimator does not compute “the most accurate MLE”

The sharp statement concerns the worst-case expected **Kendall error relative
to the unknown truth**. The MLE concerns the **likelihood of the observed
sample**. These are different objectives. The sieve estimator restricts the
candidate permutations and uses extracted pairs; it need not minimize D over
all permutations. The manuscript explicitly does not transfer its sharp risk
guarantee to unrestricted Kemeny fitting (§2.5, following Lemma 2.11).

For a fixed positive beta, exact DP gives a global center MLE. Profiling beta
gives the joint MLE when the dispersion solution is interior. Our preset
[0,10] bound also defines finite predictions at boundary cases. No original primary real-data
fit reached 10; the new tiny-sample extension often reaches this cap. A validation multiplier below 1 changes the fitted dispersion,
so that calibrated predictor is explicitly **not the joint MLE**.

Small sample size N does not make the n! search space small. DP costs
O(n*2^n) time and storage after counts, and is easy at n=10; we guard it at
n<=18. The code includes faster heuristics and integer-program bounds for
larger n. Exact optimization does not imply the smallest finite-sample
estimation or prediction error.

## Large-instance certificate

Use one variable x_ij for each i<j, with x_ij=1 when i precedes j. The objective
is `sum_{i<j} W_ij + (W_ji-W_ij)*x_ij`. For each i<j<k impose
`0 <= x_ij + x_jk - x_ik <= 1`. Integral feasible solutions are total orders.
Deleting constraints yields a valid lower bound; cutting planes reintroduce
violations. Timed-out bounds and incumbents are logged rather than relabeled
as exact fits. The first large-sample Sushi B fit has feasible D=44736 and a
follow-up lower bound 44724: its optimization gap is at most 12, not zero.
This is a training-objective bound, not a bound on test NLL.

## Sources

- Supplied manuscript: Proposition 1.1, Lemma 2.11, Algorithm 3.1,
  Propositions 4.1-4.3. The unpublished manuscript itself is not redistributed.
- [Fotakis, Kalavasis & Stavropoulos (2021), Aggregating Incomplete and Noisy Rankings](https://proceedings.mlr.press/v130/fotakis21a.html).
- [Raman & Joachims (2014), Methods for Ordinal Peer Grading](https://www.cs.cornell.edu/people/tj/publications/raman_joachims_14a.pdf), Algorithm 2. Its title uses MLE terminology; the greedy implementation is treated here as a heuristic.
- [Conitzer, Davenport & Kalagnanam (2006), Improved Bounds for Computing Kemeny Rankings](https://cdn.aaai.org/AAAI/2006/AAAI06-099.pdf), linear-order optimization and bounds.
- [Mao, Weed & Rigollet (2018), Minimax Rates and Efficient Algorithms for Noisy Sorting](https://proceedings.mlr.press/v83/mao18a.html), independent-pair minimax/sieve antecedent; not applied directly to dependent report pairs.
- [SciPy `milp` documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html), HiGHS solver status and dual bounds.

Generic Mallows software for a latent full ranking with missing positions is
not automatically an implementation of this direct subset law. This project
does not claim an exhaustive survey of every partial-ranking algorithm.

## Manuscript estimators in the exposure extension

src/manuscript_estimators.py implements Algorithms 2.1, 3.1 and 3.2,
including proof constants, fresh batches, accumulated offsets, and exact
Lemma 2.11 sieve packing. It refuses unavailable exact blocks above eight
items. Every executed Section 3 fit has depth zero and equals Borda; this
is reported rather than described as active hierarchy refinement. See the
[extension report](exposure_analysis.md) and [protocol](protocols/EXPOSURE_PROTOCOL.md).
