# Estimator theory and the recorded results

[Models and algorithms](algorithms.md) · [Estimator inventory and references](algorithms.md#estimator-inventory-and-references) · [Findings](findings.md) · [All numerical comparisons](../results/theory_alignment/tables.md) · [Evidence and reproduction](../results/theory_alignment/README.md)

The recorded experiments partly illustrate the manuscript's information and coverage distinctions. They do **not** establish its minimax rates empirically across the stated parameter ranges. The most informative evidence is the center error in correctly specified SM simulations. Empirical held-out NLL answers a different question, and most empirical training designs are outside the intermediate-information region even before checking sampling assumptions.

Theorem 2.17 and Fotakis et al.'s PosEst use the same majority-score idea. Their handling of tied pair counts differs, and their statistical conclusions concern different targets. In the implemented efficient estimator, every recorded hierarchy has depth zero; those observations describe global score sorting, not an active multilevel algorithm.

The manuscript references below refer to the supplied 37-page *Selective Mallows Estimation from Uniform Partial Rankings: Minimax Kendall Risk, Efficient Algorithms, and Likelihood Comparisons*, SHA256 `400563b1789acbeea985e4b4c551162b64c87295ee3a7bf91037c8d4cc49e676`. It is unpublished and is not redistributed. [Source records](../results/theory_alignment/sources.json) identify the tables in the supplementary arithmetic appendix.

## Connection to the primary predictive study

[P0](predictive_comparison.md) implements the finite predictive protocol of Algorithm 4.1, with training-only PL regularization and a fixed finite SM dispersion bound. [L0/S0](predictive_learning.md) hold R=10 fixed: Sushi has r=10 and the controlled N/n curves have r=3. S0's correctly specified SM rows report true-center Kendall error; its PL rows and empirical NLL remain different targets from SM minimax risk.

[B0](sieve_computation.md) adds the global pair-sieve wherever r<=10. Corollary 2.15 additionally requires lambda<=1 and the assumed generating design. Those conditions must be checked per training budget, not inferred from a small r. Sharp has zero pilot depth and one global terminal block in these catalogues, so B0 is an explicit reuse of the same selected pairs and sieve. Such identity supplies an algorithmic connection, not two independent supporting experiments.

[E0](estimator_comparison.md) is the supplementary estimator comparison, distinct from P0's Algorithm 4.1 main experiment. Its Sharp implementation removes the eight-item guard without changing A=256 or W_star. A full-space exact-DP shortcut makes some n=10 and n=12 fits computable, while other radii require complete greedy packing and can exceed time or memory budgets. [Resource receipts](../results/predictive/sieve_resources.json) and [E0 estimator scores](../results/estimator_comparison/summary.csv) distinguish computational availability from theorem applicability. The tables below retain the supplementary P1/G1/S1–S3 comparisons with their frozen implementations; references to an eight-item guard in those rows describe that implementation only.

The same study includes a 30-minute / 4-GiB completion of unavailable fits. Exact ball-cover construction and a parity-constrained DP for radius one recover 100 Sharp fits without changing its candidate packing, selected-pair objective or tie rule. Direct comparison confirms that the original and completion engines produce the same 29,086 ten-item radius-four candidates in the same order. This improves computational availability, not the estimator's statistical definition or theorem assumptions; [remaining limitations](sieve_computation.md#completion-results-and-remaining-limits) stay explicit.

## What the risk theorem measures

For a fixed positive dispersion, the manuscript studies

```math
R_K^\star(N;n,r,\beta)
=\inf_{\widehat\pi}\sup_{\pi^\star\in\mathfrak S_n}
\mathbb E_{\pi^\star,\beta}\,d_K(\widehat\pi,\pi^\star).
```

The loss is unnormalized Kendall distance to the **generating center**. The expectation includes independent reports, independently sampled uniform r-subsets and any estimator randomization. Each report is generated directly on its displayed set. The model has one center and one dispersion. Uniform upper bounds use a supplied positive lower bound on the true dispersion where specified; their constants need not remain bounded as the signal approaches zero.

For this chapter define

```math
\lambda=\frac{Nr(r-1)}{n(n-1)},\qquad
\mu=\frac{Nr}{n},\qquad
\nu=\frac{Nr(r-1)}{n-1}=n\lambda,
```

```math
Q=\frac{n^2(n-1)}{Nr(r-1)}=\frac n\lambda=\frac{n^2}{\nu},\qquad
V_{\rm cov}=-N\log(1-r/n),\qquad
B_{\rm cov}=n^2e^{-V_{\rm cov}}.
```

At r=n use Vcov=∞ and Bcov=0. Under the uniform design, λ and μ are expected pair and item appearances. On nonuniform empirical data they are dimension-derived summaries, not a replacement for actual per-pair counts. **N is the number of training reports**, not the full dataset size, test size or total reports over repeated partitions.

Three different lower-bound mechanisms matter:

| Mechanism | Obstruction and scale | Manuscript location |
|---|---|---|
| Coverage | An unseen item cannot be positioned from its absent comparisons; scale Bcov | Proposition 2.2, pp. 6–7 |
| Local information | Many nearby permutations remain difficult to distinguish; scale Q capped at order n² in the intermediate region | Section 2.3 and Theorem 2.1(i), pp. 5, 9–12 |
| Adjacent-swap testing | Even one neighboring pair has a binary testing error; this matters beyond the intermediate region | Theorem 2.10, pp. 10–12 |

Writing p=r(r−1)/[n(n−1)] and sβ=sech(β/2), the adjacent-swap lower bound has scale

```math
\frac{n}{\sqrt{1+Np}}\bigl[1-p(1-s_\beta)\bigr]^N.
```

This is not a universal Q lower bound for large λ. In particular, at r=n it becomes the full-ranking exponential scale. Constants hidden in order notation are not one, and Q or n² must not be drawn as literal finite-sample lower limits on observed risk. The maximum possible Kendall loss is n(n−1)/2.

## Which bounds match in which region?

Every row below assumes the manuscript's SM observation law and fixed positive signal, in addition to its dimensional conditions.

| Region | Matching estimator / reason | Proved minimax order and its experimental interpretation |
|---|---|---|
| λ≤1 and μ≥C0 log(er) | Sharp Algorithm 2.1; logarithmic item exposure makes the coverage obstruction absorbable | Q, Theorem 2.1(ii). The exposure constant depends on the signal lower bound. Merely checking μ/log(er)>1 does not establish the hypothesis |
| λ≤1, 2≤r≤R for fixed R | Extract one uniform displayed pair per independent report, then apply the global permutation sieve | Q∧n², Corollary 2.15, first part. No additional exposure condition, but the comparison constants depend on R |
| ν≥1 and Vcov≤½ log ν | Global clipped Borda; the coverage term dominates its other upper-bound terms | Bcov, Corollary 2.15, second part |
| ν≤1 | The local-information lower bound is saturated; any order has at most quadratic loss | n², by the lower bound and trivial upper bound. This region cannot distinguish meaningful rate improvements between estimators |
| N=1, any r | Preserve the observed order and insert unobserved items arbitrarily | n(n−r)+n, Proposition 2.16. The missing-label and within-report noise costs are both present |
| r=n, any N | Resolve each pair by majority, form a tournament, and sort its win counts | Theorem 2.17: the exponential order displayed below, not a 1/N extrapolation |

```math
R_K^\star(N;n,n,\beta)\asymp_\beta
\frac{n}{\sqrt{N+1}}\mathrm{sech}(\beta/2)^N.
```

The efficient Algorithm 3.1 has a different upper bound in the same well-covered intermediate region:

```math
\sup_{\pi^\star,\beta\ge\beta_0}
\mathbb E d_K(\widehat\pi_{\rm eff},\pi^\star)
\le \min\!\left\{\binom n2,\ C_{\beta_0}Q\log(e+\nu)\right\}.
```

Thus its guarantee is within one logarithmic factor of the sharp rate, not a statement that it is pointwise worse than Sharp. Proposition 2.14 instead bounds global Borda by a constant times

```math
\bigl[B_{\rm cov}+n^2/\sqrt\nu+Q\bigr]\wedge n^2.
```

For full rankings, global Borda equals sorting average reported positions. Corollary 3.13 gives that estimator an upper bound of order n exp(−cN); it does not identify Theorem 2.17's precise exponential constant or square-root prefactor.

Outside the proved matching regions, the sharp coverage-sensitive order (Bcov+Q)∧n² remains **Conjecture 2.18** in the intermediate regime. Numerical fits must not be described as verification of a proved uniform theorem there. Neither the sparse theorem nor its sieve proof automatically gives exact Kemeny fitting the same uniform risk guarantee; Section 4.4 identifies exact fitting as an optimization benchmark.

## Theorem 2.17 versus Fotakis PosEst

Theorem 2.17 first chooses one orientation for every pair, including ties, then sorts items by decreasing tournament wins. [Fotakis et al., Algorithm 1](https://proceedings.mlr.press/v130/fotakis21a/fotakis21a.pdf) counts an opponent j as preceding i whenever j wins at least half their joint appearances; it sorts those predecessor counts and randomizes final score ties. In the absence of pairwise ties, counting losses upward and wins downward gives the same order, provided the final score-tie rule is aligned.

The exact conventions differ when pair counts tie:

| Detail | Theorem 2.17 | Implemented Fotakis / PosEst |
|---|---|---|
| Pair tied at half its comparisons | Select exactly one direction by a fixed rule | The ≥ condition counts a predecessor in both directions |
| Final score tie | Fixed rule may be used | Seeded random priority |
| Design behind the result | Independent complete Mallows rankings, r=n | Conditional independent selective rankings on a p-frequent sequence; G1 checks every pair is observed |
| Result being invoked | Expected Kendall minimax order, uniform in n,N at fixed β | Primarily high-probability exact recovery with enough comparisons per pair; this is not the same risk statement |

A concrete distinction uses two reports, ABC and BCA. The A–B and A–C counts tie; B beats C twice. Resolving tied edges in favor of earlier labels gives the tournament A→B→C, with A→C, hence ABC. PosEst counts two predecessors for A, one for B and two for C, hence B comes first regardless of the A/C score tie. The methods therefore need not return identical estimates. For complete rankings with odd N, pair ties are impossible, so only the final score-tie convention remains.

Fotakis's Theorem 1 uses sample size of order log(n/δ)/[p(1−exp(−β))²] for exact recovery. Here N denotes that paper's profile length; its use of the symbol r for the number of reports must not be confused with this repository's r items per report. G1's observed positive minimum pair count establishes a structural p value, not the true-model assumption or a numerical high-probability certificate.

The appropriate description is **the same majority-score construction, with different tie conventions and guarantees**. Theorem 2.17 is not the efficient hierarchy, clipped Borda, or the method labelled `sharp` in saved result tables.

## What was actually executed

| Recorded method | Actual operation relevant to the theory | Consequence for interpretation |
|---|---|---|
| `sharp` in the supplementary tables | Algorithm 2.1 with that run's exact sieve guard of eight items. Its recorded small-catalogue grids have no pilot stages and a catalogue-wide terminal block | It reduces to a global one-pair-per-report sieve there. E0/L0/S0 remove the guard through the separate active implementation |
| `efficient` in P1/S1/S2 | Algorithms 3.1/3.2 restricted to λ≤1; all successful depths are zero | Its predictions match global clipped Borda when tie priorities align. No active multilevel comparison was executed |
| `efficient` in S3/L2/T1 | The saved bounded-prediction implementation starts from min(λ,1); all recorded depths are zero | λ>1 rows are an extension of the schedule. At r=n the actual average-position rule can instead be related to Corollary 3.13 |
| `borda` | Global exposure-normalized signed score; the strict implementation applies the manuscript clipping | Relevant to Proposition 2.14 and the coverage-dominated corollary, not automatically the sharp Q rate |
| `mle` | Exact DP or certified integer Kemeny center, then the specified dispersion fit | Training likelihood benchmark. A smaller training objective does not entail lower center error or held-out NLL |
| `sm_fotakis` in G1 | Algorithm 1 predecessor count, with every-pair admission and profiled dispersion | Can be compared empirically with exact SM; the theorem assumptions still require separate assessment |
| `posest` in C1/S3 center benchmarks | Same ≥ predecessor calculation, including zero-exposure ties, without G1's all-pair admission | Missing-pair rows have no p-frequent guarantee. The saved objective gap is not center risk or test NLL |

The zero-depth result follows from the conservative construction, not a data-selected shortcut. A stage requires ηm>A with A=256. With n≤64 and η≤1 in the simulation grids, that condition cannot start a stage. The n=8 Sharp pilot similarly has η=(r−1)/(n−1), and its very wide terminal block contains all items. This identifies the executed estimators without changing their published parameters.

## Correspondence in correctly specified simulations

Use the pure-SM bridge endpoint (mixture weight zero), the shell intervention at tilt zero, and S3 rows generated under SM with β=.8. The independent uniform-display design and true center are known in these rows. PL-generated and mixed/tilted laws remain useful misspecification experiments but cannot validate the SM risk theorem. [Every selected row and its dimensional coordinates](../results/theory_alignment/pure_sm_results.csv) is retained.

### Intermediate information and bounded r

In the S1 n=8, equal-gap pure-SM stream:

| r,N | λ | Exact mean Kendall error | Sharp mean error | Borda / depth-zero efficient | Interpretation |
|---|---:|---:|---:|---:|---|
| 2,8 | .2857 | 11.650 | 13.400 | 11.100 | In the bounded-r intermediate region; no finite-sample ordering of estimators follows from matching rates |
| 2,28 | 1 | 9.100 | 10.575 | 8.325 | Boundary of that region; the three curves need not coincide |
| 3,8 | .8571 | 9.075 | 13.825 | 9.100 | Global pair extraction uses only one of the report's three pairs; constants and sieve resolution matter |
| 3,112 | 12 | .950 | 4.175 | 1.850; efficient unavailable | Outside the intermediate theorem, despite lower errors at the larger N |
| 3,448 | 48 | .075 | .575 | .600; efficient unavailable | Cannot be used to establish a Q rate restricted to λ≤1 |

The local sieve radius is m·binom(m,2)/k. In the one-block n=8, N=8 case, k=8 and the radius is 28, the maximum Kendall distance; the greedy packing contains only one order. This explains why the conservative Sharp implementation can be weak at those finite sample sizes. A minimax-order guarantee with unspecified constants does not imply uniformly best point performance.

The n=32,r=3 coverage grid gives a clearer score-estimation trend:

| N | λ | μ | Borda mean error | Saved 95% t interval | Efficient |
|---:|---:|---:|---:|---|---|
| 40 | .2419 | 3.75 | 153.925 | [146.055,161.795] | Identical point and interval, depth zero |
| 160 | .9677 | 15 | 89.500 | [84.722,94.278] | Identical point and interval, depth zero |
| 640 | 3.8710 | 60 | 45.200 | [42.802,47.598] | Excluded by the strict schedule domain |

These rows show improving global-score estimates and deliberate domain exclusions. They do not compare an active hierarchy with a sharp estimator: neither active localization nor a large-catalogue exact sieve was run. The first two dimensional rows satisfy λ≤1; their coverage ratios do not determine whether the unspecified C0 condition holds.

### Coverage-dominated and one-report examples

Two S3 n=64 global-score rows satisfy the explicit coverage-dominated inequalities:

| r,N | ν | Vcov | ½ log ν | Bcov | Mean Kendall error |
|---|---:|---:|---:|---:|---:|
| 8,2 | 1.7778 | .2671 | .2877 | 3136 | 853.867 |
| 32,1 | 15.7460 | .6931 | 1.3788 | 2048 | 540.900 |

The latter combines 60 saved independent repetitions because two rounded requested budgets gave N=1; the former has 30. These are genuine examples inside the corollary's coverage region under the simulated law. Risk on the scale of Bcov is compatible with that result, but two finite-dimensional observations do not verify a uniform asymptotic order. Bcov is a scale with hidden constants, not a numerical lower bound to compare directly with the mean.

At n=8,N=1, exact SM has mean Kendall error 11.733 for r=4 and 4.767 for r=8. The change is consistent with the disappearance of the missing-item term in Proposition 2.16. It is not by itself evidence for scaling in n. The ν≤1 rows in [the complete table](../results/theory_alignment/pure_sm_results.csv) belong to the quadratic saturation region, where a relative rate advantage is intrinsically hard to demonstrate.

### Complete rankings and the exponential endpoint

The S3 full-ranking slice has n=r=8 and 30 independent repetitions per N:

| N | Exact SM center error | Average-position / depth-zero efficient error | Saved `sharp` error |
|---:|---:|---:|---:|
| 1 | 4.767 | 4.767 | 14.567 |
| 2 | 4.167 | 3.633 | 14.033 |
| 8 | .967 | .967 | 13.433 |
| 32 | .167 | .267 | 6.267 |

The strong decline of the average-position error is consistent with Corollary 3.13's exponential upper bound. These four budgets do not estimate the sharp exponent or the (N+1)^(−1/2) prefactor, and no full-ranking majority-estimator risk curve was saved. The weak `sharp` results are outside its intermediate-information guarantee for N>1 and do not test Theorem 2.17, which uses a different estimator. At N=1, the conservative sieve is also not Proposition 2.16's preserve-the-observed-order construction.

All simulation intervals in [the numerical appendix](../results/theory_alignment/tables.md#pure-sm-center-risk-comparisons) are copied from the saved results. They describe uncertainty in the simulated mean, not a confidence band for a minimax rate. Randomizing the generating center avoids systematically favorable label ties, but the resulting mean does not evaluate a supremum over all centers. Finite Kendall risk also need not imply finite unbounded-profile NLL: the S1 r=2,N=8 exact and Borda rows retain infinite mean predictive loss despite finite center error.

## Correspondence in the real datasets

### P1: dimensional conditions and actual estimator comparisons

[The 23-task training-regime table](../results/theory_alignment/tables.md#p1-training-regimes) uses each partition's training N. Only dots2024 A/B at r=2 have λ≤1: n=30,N=180, λ=.41379, μ=12. All 21 other tasks have λ>1. The nine full-ranking tasks are Sushi A and the eight PrefLib Dots/Puzzle conditions. They have the geometry r=n required by the endpoint, but no verified single-Mallows, independent-report generating law or known latent center.

All-pair coverage and theoretical exposure are different checks. For example, Sushi B has λ=27.27 in P1 but missing pairs; dots2024 and PatrasIQ also have absent pairs. Full item coverage does not repair those gaps. Conversely, seeing every pair does not establish uniform selection or homogeneous preferences. Empirical λ and μ alone cannot certify any of these theorems.

The [complete P1 method inventory](../results/theory_alignment/p1_methods.csv) has all 115 dataset/method combinations. The [paired comparisons](../results/theory_alignment/tables.md#p1-estimator-predictions) show:

- For both dots2024 r=2 tasks, efficient and Borda NLL agree in all 30 partitions. These are the 60 successful efficient fits, all with depth zero; the agreement follows from the executed construction.
- In all eight PrefLib conditions, Borda and exact SM have identical confirmation NLL in every partition and zero distance to the external objective order. That order is not a known latent SM center. These are agreement observations, not a measured exponential risk curve.
- In dots2024 A r=2, Borda has mean NLL .62009 versus .79619 for exact SM; in B r=2 the means are .71569 and .86744. The theorem does not promise that exact likelihood optimization minimizes held-out loss, nor does it promise that a minimax estimator wins each dataset.
- Beans gives Borda NLL 1.79336 versus exact SM 1.80639; PL has 1.79388. The point comparison with PL therefore changes with the SM center procedure. This is a predictive-procedure observation, not a proof of a generating family or a contradiction of the center-risk bounds.
- Sushi A gives Borda minus exact SM NLL +.00363. The true preference center is unknown, so this difference cannot identify which estimator has smaller Kendall risk.

Sushi B has only 8 certified exact fits among 30 partitions. The full paired Borda–exact difference remains NA; its finite-only value and denominator are separate. No missing exact fit is replaced with another center to create a theorem comparison.

### G1 and C1: where Fotakis was actually compared

The C1 center benchmark attached to the S3 n=10,r=3 SM learning design supplies a direct true-center comparison:

| Training N | λ | Borda mean Kendall error | PosEst | Multistart insertion |
|---:|---:|---:|---:|---:|
| 20 | 1.3333 | 9.667 | 10.967 | 9.700 |
| 50 | 3.3333 | 6.467 | 7.633 | 6.533 |
| 100 | 6.6667 | 4.433 | 4.667 | 3.567 |
| 300 | 20 | 2.000 | 1.033 | .267 |

Each mean uses 30 independent streams; budgets are nested within a stream. The ranking of Borda and PosEst changes with N. All four budgets have λ>1, and r=3<n, so neither the intermediate sharp-rate theorem nor the complete-ranking Theorem 2.17 predicts their ordering. Every saved SM multistart result attains the exact DP training objective, but it remains a different algorithm and may choose a different tied optimum. [All four center methods, errors and objective gaps](../results/theory_alignment/tables.md#c1--s3-learning-center-benchmarks-under-sm) are retained; these arithmetic means have no newly constructed interval.

P1 did not fit Fotakis. G1 did. Across all eight Dots/Puzzle tasks, pooled Fotakis and exact SM NLL agree in every recorded pooled partition: the prespecified 70%, the 50%/80% sensitivities and held-out-group allocations. This does not establish algorithmic equivalence for arbitrary data.

At the prespecified 70% within-group allocation, local Fotakis-minus-exact NLL means range from −.02468 to −.00396 across those eight tasks, each using all 100 repetitions. The lower local predictive loss is compatible with finite-sample estimator differences and small local training sets; there is no known true center for a Kendall-risk claim. In Sounds, local Fotakis is unavailable under its pair-coverage gate, while the pooled 70% comparison is −.00597. [All G1 comparison counts and means](../results/theory_alignment/g1_fotakis_vs_exact.csv) preserve the unavailable cases and all allocation schemes.

The C1 Sushi A training-objective benchmark has PosEst and exact DP at D=686 for N=50 and D=45,938 for N=3,000. That is equality of the training Kemeny objective at two contexts, not equality of generating-center risk or a full-ranking exponential-rate experiment. The C1 `posest` comparisons on sparse incomplete data also lack G1's all-pair admission rule. [The saved benchmark](../results/theory_alignment/inputs/c1_algorithm_benchmark.csv) identifies the objective, certification and runtime separately.

## What the existing evidence supports and what remains untested

| Question | Supported reading of the saved results |
|---|---|
| Do more informative samples improve center estimation? | Yes, the pure-SM slices show falling mean Kendall error; coverage-sensitive and complete-ranking cases should be interpreted in their own regimes |
| Do the data exhibit a proved Q rate uniformly in r? | Not established: sparse grids are small, many budgets cross λ=1, and constants and dimensional scaling were not identified |
| Has the efficient hierarchy's logarithmic tradeoff been measured? | No active hierarchy was executed; reported efficient-versus-Borda agreement is a depth-zero comparison |
| Has the sharp full-ranking rate of Theorem 2.17 been tested for its stated estimator? | No saved majority-estimator risk series; existing average-position results relate directly to Corollary 3.13 instead |
| Can a real-data NLL winner confirm or refute a minimax Kendall theorem? | No. The target, population assumptions and available ground truth differ |
| Is the critical coverage transition settled empirically or theoretically here? | No. The manuscript labels its uniform sharp claim a conjecture; the saved finite grids do not resolve it |

A future direct rate study would need deliberately chosen sequences of n,r,N within each claimed region, known SM signal, the actual estimator named in each theorem, active hierarchy stages if that comparison is intended, and true-center Kendall risk with adequate independent repetitions. It would also need to vary coverage separately from pair exposure and audit pairwise/final tie rules for the full-ranking majority estimator. Those are missing tests identified by this analysis, not newly performed experiments.
