# Models, estimators and admission rules

[Experiment map](experiments.md) · [Theory and results](theory_alignment.md) · [Evaluation](criteria.md) · [Uncertainty](uncertainty.md) · [References](references.md)

## Observation law

A report is a strict complete ordering $`Y=(y_1,\ldots,y_r)`$ of its displayed set S. The selective Mallows model is

```math
P_{\mathrm{SM}}(Y\mid S;\pi,\beta)=\frac{e^{-\beta d_K(Y,\pi|_S)}}{Z_r(\beta)},\qquad
Z_r(\beta)=\prod_{j=1}^{r}\sum_{v=0}^{j-1}e^{-\beta v},\quad \beta\ge0.
```

π is one catalogue-wide center; π restricted to S orders only that display. $`\beta=0`$ is uniform and large β concentrates around the center. The law is defined directly on S. Sampling a full n-item Mallows ranking and deleting unshown items is a different observation mechanism and is not the selective generator used here.

With worths $`w_i=e^{\theta_i}>0`$, PL gives

```math
P_{\mathrm{PL}}(Y\mid S;\theta)=\prod_{k=1}^{r}\frac{e^{\theta_{y_k}}}{\sum_{j=k}^{r}e^{\theta_{y_j}}}.
```

A common shift of θ is unidentified; scale normalization changes no probabilities. Both laws can evaluate complete orders of different display sizes, but the reported experiments use separate fixed-r tasks, preserving each physical catalogue. A censored top-k report would require the full original display and summation over unseen tails, not these likelihoods on the retained k items alone.

The private manuscript *Selective Mallows Estimation from Uniform Partial Rankings: Minimax Kendall Risk, Efficient Algorithms, and Likelihood Comparisons* supplies the SM construction and estimators. Its Section 4 also specifies regularized prediction in Algorithm 4.1. The study therefore labels its unpenalized and bounded/regularized procedures explicitly; sharing the SM law is not a claim that every experiment reproduces every step of that algorithm.

**P0 is the only main experiment: Algorithm 4.1, with likelihood-center SM and tuned ridge PL.** Its active implementation is `predictive_models.py`, with finite beta in [0,10], training-only ridge selection, refitting on 80% development data and paired outer evaluation. The separately named E0 estimator comparison uses Sharp via `resource_sieve.py` and the equivalent enlarged-budget completion in `sieve_budget_retry.py`, with no eight-item admission limit. [Primary fitting details](predictive_comparison.md#prespecified-fitting-procedures) and [sieve computation](sieve_computation.md) take precedence over the separately identified supplementary P1/P2 rules below.

## Estimator inventory and references

The inventory below covers the fitted methods and center-optimization procedures used across the study. They are not all separate statistical estimators: DP and integer programming solve the same center objective; insertion is a numerical approximation; dispersion fitting completes an SM predictor after a center has been chosen. Dataset-specific allocation remains in the [experiment map](experiments.md#estimator-allocation-by-empirical-dataset).

**M** denotes the [supplied 37-page manuscript](references.md#supplied-manuscript-m), identified there by title and SHA256. Page numbers and algorithm numbers below refer to that version. A paper's theorem applies only under its stated assumptions; identifying an algorithm's source does not establish those assumptions for empirical data.

### Center estimators and solvers

| Method / saved label | Reference and precise location | Construction, implementation and study role |
|---|---|---|
| Exact SM likelihood center: subset DP (`mle`, `exact_dp`, or `sm_likelihood` with the DP path) | **M**, Section 4.1, Proposition 4.1, equation (4.4), p. 33 | Globally minimizes the whole-report Kendall objective. Implemented in [models.py](../src/models.py) and the batched recurrence in [group_sensitivity.py](../src/group_sensitivity.py); used through n=18. These are implementations of the same recurrence, not different estimators. |
| Exact SM likelihood center: certified integer program | [Conitzer, Davenport & Kalagnanam (2006)](https://cdn.aaai.org/AAAI/2006/AAAI06-099.pdf), integral version of LP3, p. 623; the SM objective is **M**, Section 4.1 | [strict_models.py](../src/strict_models.py), `exact_integer_center`, eliminates reverse-direction variables and uses HiGHS. A center is called exact only with a matching feasible objective and lower bound. |
| Primary likelihood-center procedure (`sm_likelihood`) | **M**, Algorithm 4.1 and Proposition 4.1, pp. 32–33; [Conitzer et al. (2006)](https://cdn.aaai.org/AAAI/2006/AAAI06-099.pdf), LP3; [repository-defined solver policy](references.md#repository-defined-procedures) | [predictive_models.py](../src/predictive_models.py), `likelihood_center`: DP through n=18, otherwise five-start insertion plus a 30-second integer attempt. Used in P0/L0/S0. An uncertified result is an explicitly approximate likelihood center, not an exact MLE. |
| Sharp (`sharp`, `sm_sharp`) | **M**, Algorithm 2.1, p. 5; Lemma 2.11, pp. 12–13; Lemma 2.12 and Proposition 2.13, pp. 13–15; pilot Algorithm 3.2, pp. 24–25 | Localization/pilot, one orientation-independent random pair per eligible report/block, then permutation-sieve disagreement minimization. Active [resource_sieve.py](../src/resource_sieve.py) and [sieve_budget_retry.py](../src/sieve_budget_retry.py) have no item-count guard; budgets can still prevent completion. The [frozen supplementary implementation](../src/manuscript_estimators.py) retains its eight-item guard for replay. |
| Global pair-sieve (`sm_global_sieve`, B0) | **M**, Lemma 2.11, pp. 12–13, and the first-part proof of Corollary 2.15, p. 16 | One randomly selected displayed pair per report, with the sieve on the full catalogue. [resource_sieve.py](../src/resource_sieve.py), `global_sieve_center`; included for r≤R=10. In the recorded E0/L0/S0 catalogues, Sharp has the same global terminal problem, so B0 explicitly reuses that fit. The bounded-r rate also requires the corollary's other assumptions. |
| Efficient (`efficient`, `sm_efficient_fallback`) | **M**, Algorithms 3.1/3.2, pp. 19 and 24–25; scores in equation (3.4), p. 19; risk bound in Theorem 3.1 | [manuscript_estimators.py](../src/manuscript_estimators.py), `efficient_center`: fresh stage batches, padded blocks, offsets and terminal score sorting, with the specified global-score fallback. Recorded successful hierarchies have depth zero. The supplementary E0/L0/S0 comparisons attempt it only after Sharp is unavailable and λ≤1. |
| Global clipped Borda (`borda`; exposure-normalized `borda` in C1) | **M**, equation (3.4), pp. 19–20 with B equal to the full catalogue; Proposition 2.14, p. 15 | [manuscript_estimators.py](../src/manuscript_estimators.py), `score_order`, and C1's [pinned `borda`](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/src/models.py#L62). For fixed r the C1 score differs by the positive factor n−1; full-catalogue clipping is inactive, so the score orders agree under a common tie rule. It is also a component/fallback of the hierarchical algorithms. |
| Fotakis / PosEst (`fotakis`, `posest`, `sm_fotakis`) | [Fotakis, Kalavasis & Stavropoulos (2021)](https://proceedings.mlr.press/v130/fotakis21a.html), Section 3, Algorithm 1, proceedings p. 2281 | Counts opponents that precede an item in at least half their joint reports; sorts these counts, using seeded final ties. [group_sensitivity.py](../src/group_sensitivity.py), `fotakis_center`, requires every pair observed in G1 and E0/L0/S0. C1's pinned `posest` mechanically permits missing pairs and has no corresponding full-pair admission guarantee. |
| Insertion / multistart insertion (`insertion`, `multistart`) | [Martí & Reinelt (2011)](https://doi.org/10.1007/978-3-642-16729-4), Section 2.3.1, p. 26 (insertion and best-improvement rule), and Section 2.4, pp. 30–31 (multistart); [source details](references.md#insertion-local-search-references) | Standard insertion-neighborhood local search: repeatedly take the best strictly improving remove-and-reinsert move for the Kendall objective. Starts and tie rules are experiment-specific. Used in supplementary L1/L2/S3/T1/C1, the primary large-catalogue solver, and full-data descriptive reference centers. The search principle is established in the literature; it is not a new estimator proposed by this repository. |
| Greedy MAL specialization (`greedy`) | [Raman & Joachims (2014)](https://www.cs.cornell.edu/people/tj/publications/raman_joachims_14a.pdf), Section 3.1.1, Algorithm 2, PDF pp. 3–4 | C1's [pinned `greedy`](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/src/models.py#L86) sets every assessor reliability to one and greedily selects the next item by net wins among remaining items. This is their greedy center heuristic specialized to equal reliability; it neither estimates individual reliabilities nor guarantees a Kemeny optimum. |

### Dispersion, PL and fitted control variants

| Fitted quantity or variant | Reference and precise location | Role and implementation distinction |
|---|---|---|
| SM profile dispersion, unbounded or capped | **M**, Proposition 4.2, equation (4.5), pp. 33–34 | Unbounded `profile_beta_unbounded` in [strict_models.py](../src/strict_models.py); capped `bounded_beta` in [predictive_models.py](../src/predictive_models.py), with [0,10] in P0/L0/S0. These estimate β conditional on the chosen center. |
| Unpenalized PL MLE by MM | [Hunter (2004)](https://doi.org/10.1214/aos/1079120141), Section 5, equation (30) | [strict_models.py](../src/strict_models.py), `pl_mm_step` and `fit_pl_mm`: simultaneous, unaccelerated MM, subject to finite-MLE existence and convergence checks. Used in the unpenalized supplementary comparisons. |
| Ridge PL (`pl` in P0/L0/S0 and the explicitly regularized controls) | **M**, Algorithm 4.1, p. 32, and Proposition 4.3, equation (4.6), p. 34 | [predictive_models.py](../src/predictive_models.py), `ridge_pl` and `tune_and_refit_pl`, use [SciPy L-BFGS-B](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-lbfgsb.html) plus checked Newton refinement. The objective comes from M; the ridge grid, solver tolerances and refinement policy are specified by this repository. This is not Hunter's unpenalized MM fit. |
| Validation-shrunk SM (`beta_shrinkage`, calibrated SM variants) | **M**, Proposition 4.2 for the base β fit; [repository-defined calibration](references.md#repository-defined-procedures) for the multiplier | Supplementary L1/L2/S3/T1 fit bounded β and choose an additional multiplier on inner validation data. The multiplier grid is not a separate estimator proposed in M. |
| Order-constrained PL and SM on the PL order | [Repository-defined common-order controls](references.md#repository-defined-procedures), built from **M**, Propositions 4.2/4.3 | C1 constrains ridge PL worths to the fitted SM order, or fixes the SM center to the fitted PL order and profiles β. T1 also has a shrunk SM-on-PL-order control. [Control specification](structural_controls.md#holding-the-fitted-order-common) and the pinned code define these variants. |

**Constructions discussed but not separately fitted:** M's Theorem 2.17 majority tournament (p. 16) differs from PosEst in its treatment of tied pair votes; the saved PosEst rows are not a separate implementation of that theorem. The one-report construction in Proposition 2.16 is a theoretical endpoint, not an additional fitted method. Likewise, Fotakis et al.'s localized MLE is not implemented here. See the [theory comparison](theory_alignment.md#theorem-217-versus-fotakis-posest).

## Exact center and dispersion

Let $`W_{ij}`$ count training reports putting i ahead of j. Then

```math
\hat\pi\in\arg\min_{\pi}D(\pi),\qquad D(\pi)=\sum_{t=1}^{N}d_K(Y_t,\pi|_{S_t}).
```

Pair counts are sufficient for this optimization; no pair independence assumption is introduced. For a set A, exact subset DP uses

```math
F(A)=\min_{i\in A}\left\{F(A\setminus\{i\})+\sum_{j\in A\setminus\{i\}}W_{ij}\right\},\quad F(\varnothing)=0,
```

with i placed last. The computational guard is $`n\le18`$. G1 batches the same recurrence and preserves its fixed tie priority.

For larger catalogues, a binary linear-order formulation sets $`x_{ij}=1`$ when item $`i`$ precedes item $`j`$. Its objective is

```math
\min_x\sum_{1\le i\lt j\le n}\left[W_{ij}+(W_{ji}-W_{ij})x_{ij}\right],\qquad x_{ij}\in\{0,1\}.
```

The transitivity constraints are

```math
0\le x_{ij}+x_{jk}-x_{ik}\le1,\qquad 1\le i\lt j\lt k\le n.
```

P1/P2 accept an exact center only when an independently checked feasible objective and integer lower bound coincide within the declared numerical rules. The time budget is 120 seconds. HiGHS solves the integral formulation of [Conitzer et al.](references.md), not their original CPLEX runtime experiment. An uncertified incumbent is unavailable for the exact comparison; tied optima may choose different centers.

P0/L0/S0 use the same subset DP through n=18. Larger catalogues use a 30-second integer attempt plus a deterministic five-start insertion incumbent. Both bounds and the achieved objective are recorded; unequal bounds explicitly identify an approximate center. This provides a finite predictive procedure while retaining a separate exact-center benchmark. It does not establish an exact MLE when certification fails.

Given any selected SM center, profile $`\beta`$ by minimizing

```math
\beta D+N\log Z_r(\beta).
```

With $`\bar d=D/N`$, the unbounded profile solves $`\mathbb E_\beta[d_K]=\bar d`$. The boundary solutions are $`\beta=\infty`$ when $`\bar d=0`$ and $`\beta=0`$ when $`\bar d\ge r(r-1)/4`$. Finite roots use tolerance $`10^{-12}`$. The same profile is used after exact, Sharp, efficient, Fotakis and clipped-Borda centers in the unpenalized experiments. Infinite predictive losses remain recorded.

## Score, sieve and majority estimators

The [theory comparison](theory_alignment.md#which-bounds-match-in-which-region) gives the manuscript's matching risk regimes and relates each to saved runs. Its [Theorem 2.17 comparison](theory_alignment.md#theorem-217-versus-fotakis-posest) explains the shared majority-score construction and the pair-tie difference from Fotakis; neither should be confused with the saved `sharp` sieve or the efficient hierarchy.

The [study-wide inventory](#estimator-inventory-and-references) provides a source for each method. For Sharp, pilot reports and terminal reports are disjoint; the unpenalized efficient entry point requires λ≤1. Fotakis's equality rule counts an opponent as a predecessor in both directions when their observed pair vote is tied. None of the approximate center methods fills a missing exact result in P1/P2.

For a block $`B`$, let $`R_{ti}(B)`$ be the one-based rank of item $`i`$ in report $`Y_t`$ restricted to $`B`$. Define

```math
q_{ti}=\begin{cases}|B\cap S_t|+1-2R_{ti}(B),&i\in B\cap S_t,\\0,&i\notin B\cap S_t.\end{cases}
```

With $`A_i`$ its batch appearance count, the block score is

```math
s_i(B)=\mathrm{clip}_{[-|B|,|B|]}\left[\frac{n-1}{(r-1)A_i}\sum_tq_{ti}\right],
```

using zero when $`A_i=0`$. Larger scores precede smaller scores. Sharp's exact terminal packing radius is $`\phi=m\binom{m}{2}/k`$ for a block of m items and k extracted pairs; lexicographic greedy packing and seeded choices make permitted arbitrary choices reproducible.

The proof constants and schedule are not tuned to test performance. E0/L0/S0 use $`\beta_0=0.1`$; it is a schedule input, not an established lower bound on a real population signal. Supplementary SM simulations use .8 where specified. Numerical $`\lambda\le1`$, full item coverage or $`\mu/\log(er)>1`$ do not verify the sufficient unknown constant, independent reports, uniform displays or a true SM law.

## Insertion and greedy MAL: what the names mean

**Insertion** implements standard insertion-neighborhood local search, with the best-improvement rule described in [Martí & Reinelt (2011), Section 2.3.1, p. 26](https://doi.org/10.1007/978-3-642-16729-4). Starting from a complete order, it evaluates every single-item remove-and-reinsert move, chooses the move with the largest strict reduction in D, and repeats until no such move improves D. Multiple starts retain the best final objective. This only establishes a local optimum unless a separate lower bound certifies it. The [implementation references](references.md#repository-defined-procedures) distinguish C1's eight starts, the primary solver's five starts, and the other declared variants. These settings are repository choices; the underlying search principle is not original to this study. This optimizer is unrelated to the insertion sampling construction used to generate Mallows rankings.

The connection to the linear ordering literature is exact at the objective level: with pair counts W as weights, maximizing agreements $`\sum_{a<b}W_{\pi_a\pi_b}`$ is equivalent to minimizing D, because agreements plus disagreements equal the fixed total number of observed pair occurrences. The repository implements the full-neighborhood best-improvement rule; it does not claim to reproduce the book's separate sequential-scan pseudocode or the first-improvement variants in Schiavinotto & Stützle (2004). [Reference distinctions](references.md#insertion-local-search-references) state precisely which parts correspond.

**Greedy MAL** comes from [Raman & Joachims (2014), Section 3.1.1, Algorithm 2](https://www.cs.cornell.edu/people/tj/publications/raman_joachims_14a.pdf). With all assessor reliabilities set to one, its next item maximizes the following score over the remaining catalogue C:

```math
g_C(i)=\sum_{j\in C\setminus\{i\}}(W_{ij}-W_{ji}).
```

Place that item next, remove it from C, and recalculate the remaining scores. The paper writes the equivalent minimization of losses minus wins. C1 adds a seeded tie rule and uses strict reports. The paper's accompanying text identifies this as a greedy approximation even though the algorithm caption refers to computing an MLE. C1 does not implement their grader-reliability estimation, score-weighted MALS model, or MALBC alternative.

## Unpenalized PL

P1/P2, G1, S1/S2 and D2 use Hunter's simultaneous, unaccelerated MM equation (30). If $`V_i`$ counts reports in which i is not last and $`R_{tk}`$ is the remaining set at stage $`k\lt r`$,

```math
w_i^{\mathrm{new}}=\frac{V_i}{\sum_t\sum_{k\lt r:i\in R_{tk}}\left(\sum_{j\in R_{tk}}w_j\right)^{-1}}.
```

Updates normalize the common worth scale only. The observed directed win graph must support a unique finite MLE; disconnected or one-way-separated data are not repaired with pseudo-comparisons or item deletion. The fixed convergence criteria are maximum log-worth change $`\lt 10^{-10}`$ and gradient per report $`\lt 10^{-8}`$, with at most 100,000 iterations. Nonconvergence and failed existence checks remain unavailable. An independent optimizer used in tests verifies the likelihood, not an extra competing fitted method.

## Bounded and regularized predictive procedures

P0/L0/S0 profile beta on [0,10], without a validation-selected multiplier. PL selects tau from {.01,.1,1,10,100} on the inner split and refits on all development reports. The penalty is applied to summed NLL; positive ridge supports finite fits with disconnected comparisons. [The primary chapter](predictive_comparison.md) specifies objective, numerical checks, allocation and intervals. The following additional variants are supplementary controls.

L1/L2/S3/T1 and related C1 controls use explicit variants stored with their implementation snapshot. SM profiles β on [0,10]. A separate predictor uses $`\alpha\beta`$, with α selected on inner validation from {0,.25,.5,.75,1}, holding the final center fixed. Both unshrunk and shrunk results are recorded.

Ridge PL minimizes the summed listwise NLL plus $`\frac{\tau}{2}\sum_i\theta_i^2`$, under the implementation's worth normalization. L1 tunes τ over {.01,.1,1,10,100}, refits on all N development reports, and records a $`\tau=10^{-6}`$ sensitivity separately. L2/S3 exposure/T1 use {.1,1,10}; fixed $`\tau=1`$ and 10 sensitivities are separately identified. When $`N\lt5`$ in the exposure procedure, no validation is attempted: $`\tau=1`$ and $`\alpha=0.5`$ are fixed. These variants assess predictive regularization and do not supply an unpenalized MLE comparison.

The efficient-center variant in the regularized exposure implementation starts the schedule at $`\min(\lambda,1)`$, including $`\lambda>1`$ designs. Those rows are an empirical extension outside the manuscript schedule domain; their labels do not establish theorem applicability. All its executed hierarchies are also depth zero. C1's ordering constraints on PL and the converse SM-on-PL-order fit are specified [with those controls](structural_controls.md).

## Which methods are admitted where?

[The empirical allocation table](experiments.md#estimator-allocation-by-empirical-dataset) gives every dataset family. The simulation grids specify methods in [S1/S2](strict_feature_analysis.md), [S3](learning_curves.md#simulation-learning-and-exposure-grids), and [D2](validation_extension.md).

G1 applies additional training-only checks: every SM candidate needs all catalogue items observed; Fotakis needs every pair observed; Sharp/efficient are excluded for $`\lambda>1`$; $`n\le8`$ uses Sharp where admitted and does not duplicate an efficient fallback; $`n>8`$ records Sharp unavailable and permits the efficient fallback where its domain holds. Exact DP needs no full-pair-coverage assumption, but G1 conservatively excludes unseen items. PL retains its own directed-connectivity rule.

P1/P2 mechanically attempt Sharp where its sieve can be computed, including dense n=4 tasks; those rows do not claim a sparse-theorem guarantee. This deliberate policy difference is part of the experiment specification. No estimator is selected because it won on the confirmation data.

## Status and reference conventions

Read algorithm, branch/depth, solver certificate, boundary status and availability alongside the method label. A fallback is identified by its actual branch. External dot counts, solution steps and city answers are used only for reference diagnostics, not supplied as the fitted latent center. The study provides neither an active-hierarchy performance result nor a theorem certificate for arbitrary real-data sampling designs.
