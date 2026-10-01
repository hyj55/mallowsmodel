# Models, estimators and admission rules

[Experiment map](experiments.md) · [Evaluation](criteria.md) · [Uncertainty](uncertainty.md) · [References](references.md)

## Observation law

A report is a strict complete ordering Y=(y₁,…,yᵣ) of its displayed set S. The selective Mallows model is

```math
P_{SM}(Y\mid S;\pi,\beta)=\frac{e^{-\beta d_K(Y,\pi|_S)}}{Z_r(\beta)},\qquad
Z_r(\beta)=\prod_{j=1}^{r}\sum_{v=0}^{j-1}e^{-\beta v},\quad \beta\ge0.
```

π is one catalogue-wide center; π restricted to S orders only that display. β=0 is uniform and large β concentrates around the center. The law is defined directly on S. Sampling a full n-item Mallows ranking and deleting unshown items is a different observation mechanism and is not the selective generator used here.

With worths wᵢ=e^θᵢ>0, PL gives

```math
P_{PL}(Y\mid S;\theta)=\prod_{k=1}^{r}\frac{e^{\theta_{y_k}}}{\sum_{j=k}^{r}e^{\theta_{y_j}}}.
```

A common shift of θ is unidentified; scale normalization changes no probabilities. Both laws can evaluate complete orders of different display sizes, but the reported experiments use separate fixed-r tasks, preserving each physical catalogue. A censored top-k report would require the full original display and summation over unseen tails, not these likelihoods on the retained k items alone.

The private manuscript *Selective Mallows Estimation from Uniform Partial Rankings: Minimax Kendall Risk, Efficient Algorithms, and Likelihood Comparisons* supplies the SM construction and estimators. Its Section 4 also specifies regularized prediction in Algorithm 4.1. The study therefore labels its unpenalized and bounded/regularized procedures explicitly; sharing the SM law is not a claim that every experiment reproduces every step of that algorithm.

## Exact center and dispersion

Let Wᵢⱼ count training reports putting i ahead of j. Then

```math
\hat\pi\in\arg\min_{\pi}D(\pi),\qquad D(\pi)=\sum_{t=1}^{N}d_K(Y_t,\pi|_{S_t}).
```

Pair counts are sufficient for this optimization; no pair independence assumption is introduced. For a set A, exact subset DP uses

```math
F(A)=\min_{i\in A}\left\{F(A\setminus\{i\})+\sum_{j\in A\setminus\{i\}}W_{ij}\right\},\quad F(\varnothing)=0,
```

with i placed last. The computational guard is n≤18. G1 batches the same recurrence and preserves its fixed tie priority.

For larger catalogues, a binary linear-order formulation uses xᵢⱼ=1 when i precedes j, minimizes Σᵢ<ⱼ[Wᵢⱼ+(Wⱼᵢ−Wᵢⱼ)xᵢⱼ], and imposes 0≤xᵢⱼ+xⱼₖ−xᵢₖ≤1 for i<j<k. P1/P2 accept an exact center only when an independently checked feasible objective and integer lower bound coincide within the declared numerical rules. The time budget is 120 seconds. HiGHS solves the integral formulation of [Conitzer et al.](references.md), not their original CPLEX runtime experiment. An uncertified incumbent is unavailable for the exact comparison; tied optima may choose different centers.

Given any selected SM center, profile β by minimizing βD+N log Zᵣ(β). With d̄=D/N, the unbounded profile solves Eβ[dK]=d̄, with β=∞ when d̄=0 and β=0 when d̄≥r(r−1)/4. Finite roots use tolerance 10⁻¹². The same profile is used after exact, Sharp, efficient, Fotakis and clipped-Borda centers in the unpenalized experiments. Infinite predictive losses remain recorded.

## Score, sieve and majority estimators

| Estimator | Construction and role | Scope/admission |
|---|---|---|
| Sharp | Manuscript Algorithm 2.1: proof-constant localization/pilot, one orientation-independent uniformly selected pair per report/block, exact greedy permutation sieve and disagreement minimization | Exact terminal blocks limited to eight items; larger required blocks return unavailable. Fresh pilot and terminal reports are disjoint |
| Efficient | Algorithms 3.1/3.2: clipped block scores, fresh batches, padded blocks and accumulated offsets, then terminal ordering | Unpenalized entry point requires λ≤1; insufficient feasible schedule falls back as specified to global scores. Every recorded successful fit has depth zero |
| Clipped Borda | Full-catalogue version of manuscript equation (3.4), sorted by normalized score | A scalable separate center baseline; no silent relabeling as an active multilevel hierarchy |
| Fotakis / PosEst | Algorithm 1 of Fotakis et al. (2021): majority-predecessor counts, ascending score order, seeded final ties | G1 requires every unordered pair observed; records p̂=min Cᵢⱼ/N. Equality counts as a predecessor in both directions |
| Insertion | Local moves minimizing the same D objective from specified starts | A declared approximation in L1/L2/T1/C1; not used to fill missing exact results in P1/P2 |
| Greedy MAL specialization | Equal-reliability ordinal aggregation heuristic | C1 center-objective benchmark; not a separate probability law |

For a block B, qₜᵢ=(|B∩Sₜ|+1−2 rank of i within Yₜ restricted to B)1{i∈B∩Sₜ}. With Aᵢ its batch appearance count, the block score is

```math
s_i(B)=\mathrm{clip}_{[-|B|,|B|]}\left[\frac{n-1}{(r-1)A_i}\sum_tq_{ti}\right],
```

using zero when Aᵢ=0. Larger scores precede smaller scores. Sharp's exact terminal packing radius is φ=m·choose(m,2)/k for a block of m items and k extracted pairs; lexicographic greedy packing and seeded choices make permitted arbitrary choices reproducible.

The proof constants and schedule are not tuned to test performance. β₀=.1 is a real-data schedule input, not an established lower bound on a real population signal; simulations use .8. Numerical λ≤1, full item coverage or μ/log(er)>1 do not verify the sufficient unknown constant, independent reports, uniform displays or a true SM law.

## Unpenalized PL

P1/P2, G1, S1/S2 and D2 use Hunter's simultaneous, unaccelerated MM equation (30). If Vᵢ counts reports in which i is not last and Rₜₖ is the remaining set at stage k<r,

```math
w_i^{new}=\frac{V_i}{\sum_t\sum_{k<r:i\in R_{tk}}\left(\sum_{j\in R_{tk}}w_j\right)^{-1}}.
```

Updates normalize the common worth scale only. The observed directed win graph must support a unique finite MLE; disconnected or one-way-separated data are not repaired with pseudo-comparisons or item deletion. The fixed convergence criteria are maximum log-worth change <10⁻¹⁰ and gradient per report <10⁻⁸, with at most 100,000 iterations. Nonconvergence and failed existence checks remain unavailable. An independent optimizer used in tests verifies the likelihood, not an extra competing fitted method.

## Bounded and regularized predictive procedures

L1/L2/S3/T1 and related C1 controls use explicit variants stored with their implementation snapshot. SM profiles β on [0,10]. A separate predictor uses αβ, with α selected on inner validation from {0,.25,.5,.75,1}, holding the final center fixed. Both unshrunk and shrunk results are recorded.

Ridge PL minimizes the summed listwise NLL plus (τ/2)Σᵢθᵢ², under the implementation's worth normalization. L1 tunes τ over {.01,.1,1,10,100}, refits on all N development reports, and records a τ=10⁻⁶ sensitivity separately. L2/S3 exposure/T1 use {.1,1,10}; fixed τ=1 and 10 sensitivities are separately identified. When N<5 in the exposure procedure, no validation is attempted: τ=1 and α=.5 are fixed. These variants assess predictive regularization and do not supply an unpenalized MLE comparison.

The efficient-center variant in the regularized exposure implementation starts the schedule at min(λ,1), including λ>1 designs. Those rows are an empirical extension outside the manuscript schedule domain; their labels do not establish theorem applicability. All its executed hierarchies are also depth zero. C1's ordering constraints on PL and the converse SM-on-PL-order fit are specified [with those controls](structural_controls.md).

## Which methods are admitted where?

[The empirical allocation table](experiments.md#estimator-allocation-by-empirical-dataset) gives every dataset family. The simulation grids specify methods in [S1/S2](strict_feature_analysis.md), [S3](learning_curves.md#simulation-learning-and-exposure-grids), and [D2](validation_extension.md).

G1 applies additional training-only checks: every SM candidate needs all catalogue items observed; Fotakis needs every pair observed; Sharp/efficient are excluded for λ>1; n≤8 uses Sharp where admitted and does not duplicate an efficient fallback; n>8 records Sharp unavailable and permits the efficient fallback where its domain holds. Exact DP needs no full-pair-coverage assumption, but G1 conservatively excludes unseen items. PL retains its own directed-connectivity rule.

P1/P2 mechanically attempt Sharp where its sieve can be computed, including dense n=4 tasks; those rows do not claim a sparse-theorem guarantee. This deliberate policy difference is part of the experiment specification. No estimator is selected because it won on the confirmation data.

## Status and reference conventions

Read algorithm, branch/depth, solver certificate, boundary status and availability alongside the method label. A fallback is identified by its actual branch. External dot counts, solution steps and city answers are used only for reference diagnostics, not supplied as the fitted latent center. The study provides neither an active-hierarchy performance result nor a theorem certificate for arbitrary real-data sampling designs.
