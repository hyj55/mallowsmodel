# Evaluation criteria

[Experiment map](experiments.md) · [Models](algorithms.md) · [Uncertainty](uncertainty.md)

## Whole-ranking predictive loss

For a fitted model f, test report t has loss

```math
\ell_{f,t}=-\log P_f(Y_t\mid S_t),\qquad
L_f=\frac1T\sum_{t=1}^{T}\ell_{f,t}.
```

Natural logarithms give nats per report. Each complete report has equal weight within a task. The paired comparison is

```math
d_t=\ell_{\mathrm{SM},t}-\ell_{\mathrm{PL},t},\qquad \Delta=\frac1T\sum_t d_t.
```

Negative Δ favors SM. This score is used in every fitted empirical and simulation comparison. Different r values have different outcome spaces; raw loss or Δ magnitude is not a universal ranking of dataset suitability. The uniform-ranking reference has loss $`\log(r!)`$. No likelihood of the display-selection mechanism is included.

Expected log loss is appropriate for probability prediction because, for a true conditional law p and candidate q,

```math
\mathbb E_p[-\log q(Y\mid S)]=H(p(\cdot\mid S))+\mathrm{KL}(p(\cdot\mid S)\Vert q(\cdot\mid S)).
```

Thus differences compare predictive distributions under the evaluation population. Winning does not establish that the winning family generated the data. A zero probability assigned to a possible test observation gives infinite loss and cannot be replaced by a finite score without changing the procedure.

## Exact population loss and empirical test loss

S1 and D2 enumerate the finite support of displayed sets and their orderings. For each fitted predictor,

```math
L_f^{\mathrm{pop}}=\sum_S p(S)\sum_{Y\in\mathfrak S(S)}p(Y\mid S)[-\log P_f(Y\mid S)].
```

This is exact finite-state summation, subject to numerical precision. Training fits still vary across independent repetitions. S2 instead averages 2,000 independently generated test reports per repetition. S3 uses 2,000 test reports in the n=8/n=10 grids and 1,000 in the n=64 grid. Empirical tasks use their specified held-out reports. A diagnostic sample is not substituted for the exact population test distribution.

## Center recovery and optimization

With a known generating order $`\pi_0`$, the center error is

```math
d_K(\hat\pi,\pi_0)=\sum_{i\lt j}\mathbf1\{\hat\pi\text{ and }\pi_0\text{ disagree on }i,j\}.
```

PL's estimated order sorts its worths. Some tables normalize by the maximum $`n(n-1)/2`$. Exposure tables also divide by the reference scale $`\min\{n(n-1)/2,n/\lambda\}`$; this is a descriptive normalization, not a verified minimax constant. Center risk is averaged over independent simulated training draws.

For human objective-ordering tasks, distance to the external dot-count, puzzle-step, or city-answer order is an **objective-reference error**, not error relative to a known population SM center. Preference datasets have no observed true center.

The training objective is $`D(\pi)=\sum_{t=1}^{N}d_K(Y_t,\pi|_{S_t})`$. Benchmark excess objective is $`D(\mathrm{method})-D(\mathrm{exact\ optimum})`$. A certified integer solver reports matching integer lower and upper bounds. An optimization gap bounds training D, not test NLL. Runtime is measured for the recorded implementation and platform, not inferred from a cited paper's implementation.

## Item and pair coverage

For training data, define item appearances and pair co-occurrences as

```math
A_i=\sum_{t=1}^{N}\mathbf1\{i\in S_t\},\qquad C_{ij}=\sum_{t=1}^{N}\mathbf1\{i,j\in S_t\}.
```

Report unseen items, observed pairs, minima/maxima, and

```math
\mu=\frac{Nr}{n},\qquad \lambda=\frac{Nr(r-1)}{n(n-1)},\qquad
\hat p=\min_{i\lt j}\frac{C_{ij}}N.
```

For fixed r, μ and λ are the actual catalogue-wide averages of appearance and pair counts. Under independent uniform subset sampling they also equal each item's/pair's expected count. They need not describe any particular item in nonuniform real data. Full item coverage, full pair coverage, and directed strong connectivity are different properties.

Coverage simulations additionally report $`\mu/\log(er)`$, the uniform-design unseen expectation $`n(1-r/n)^N`$, the scaled unseen term $`n^2(1-r/n)^N`$, and $`V_{\mathrm{cov}}=-N\log(1-r/n)`$, with $`V_{\mathrm{cov}}=\infty`$ at r=n. These design summaries do not establish theorem conditions in empirical data.

## Pair probabilities, log loss and Brier loss

Orient a pair (i,j) according to a chosen reference center, and let $`z=1`$ if the report agrees. Let h be their position difference **within that center restricted to the displayed set**, not their gap in the entire catalogue. Then

```math
p_{\mathrm{SM}}(h,\beta)=\frac{h+1}{1-e^{-(h+1)\beta}}-\frac{h}{1-e^{-h\beta}},\qquad
p_{\mathrm{PL}}(i,j)=\frac{e^{\theta_i}}{e^{\theta_i}+e^{\theta_j}}.
```

At $`\beta=0`$, $`p_{\mathrm{SM}}=1/2`$; for $`h=1`$ it equals $`\mathrm{logistic}(\beta)`$. A pair extracted from a longer ranking may have $`h>1`$. For each pair, binary log loss is $`-z\log p-(1-z)\log(1-p)`$; Brier loss is $`(z-p)^2`$. Average pairs **within each report** before averaging reports. The fitting likelihood remains listwise; these scores are diagnostics and discovery criteria.

At r=2, pair log loss is whole-ranking NLL. ATP Brier scores use a consistent player-ID orientation for outcomes and probabilities, so a row recorded as winner–loser is not incorrectly treated as an always-positive event. Pair-profile bins are defined by training PL log-worth gaps; their held-out observed rates and model probabilities are means over the selected occurrences. Profile entries do not all have confidence intervals.

ATP's strength profile bins $`\lvert\theta_i-\theta_j\rvert`$ into $`[0,0.5)`$, $`[0.5,1)`$, $`[1,1.5)`$ and $`[1.5,\infty)`$, using fitted training worths. Exclude exact worth ties from favorite-win rates, and record their count. A separate calibration plot sorts seen-player predictions by fitted probability within each method and divides them into ten nearly equal-count bins. Each point compares the bin's average predicted probability with its observed frequency. These are descriptive calibration summaries, not an independent test of the ranking model.

For the separate **full-data descriptive characteristic**, [equal-gap pair frequencies](../data/features/README.md) count actual wins for every pair × h cell across the entire task, rather than grouping held-out outcomes by fitted PL worth. Its h-specific dispersions and full-task H summarize the observed frequencies; they are not prediction scores, confidence intervals, or goodness-of-fit tests. The [dataset comparison](../data/features/comparison.md) joins these features to already recorded NLL gaps.

## Decomposition by Kendall-distance shell

For the separate **full-data frequency characteristic**, [characteristic 2](../data/features/structure/README.md#characteristic-2-uniform-frequencies-within-the-same-display-and-shell) fixes both S and d and counts actual orders across the entire task, including zero-count possible orders. It reports empirical total variation from uniformity and the nominal finite-sample uniform reference. The saved-fit likelihood decomposition below answers a different question and does not replace those frequency counts.

Fix the training SM center. Let $`d=D(Y)=d_K(Y,\pi|_S)`$, and let $`a_r(d)`$ count permutations at distance d. Define the PL shell probability $`Q_{\mathrm{PL}}(d\mid S)`$ by summing PL probabilities within the shell. The distribution

```math
Q_{\mathrm{sym}}(Y\mid S)=Q_{\mathrm{PL}}(D(Y)\mid S)/a_r(D(Y))
```

keeps PL's shell masses but makes its within-shell probabilities uniform. The exact identity is

```math
\ell_{\mathrm{SM}}-\ell_{\mathrm{PL}}
=\underbrace{\ell_{\mathrm{SM}}-\ell_{\mathrm{sym}}}_{\text{shell-mass contribution}}
+\underbrace{\ell_{\mathrm{sym}}-\ell_{\mathrm{PL}}}_{\text{within-shell contribution}}.
```

PL shell masses are computed by finite-state subset/polynomial recursion, not a frequency estimate from sparse test permutations. The two components are paired contributions to one loss difference, not independent causal effects. A positive within-shell component means PL's differentiated probabilities helped on those reports. This diagnostic is used for P2 PrefLib/dots2024 and PatrasIQ, P1 averages of those diagnostics, and the Beans/Sushi structural analyses under their specified regularized fits.

## Context slope

[Full-data characteristic 3](../data/features/structure/README.md#characteristic-3-a-fixed-pair-across-exact-displayed-sets) retains exact pair × display counts before aggregation, uses all reports without the diagnostic's repetition threshold, and includes matched contrasts that replace one nonfocal item. Its descriptive C, γ and replacement effect are joined to existing NLLs in [the data comparison](../data/features/structure/comparison.md). The following held-out diagnostic has its own eligibility and uncertainty procedure.

For a fixed pair, SM's marginal probability can change when its displayed-center gap changes; a single homogeneous PL model's pair probability does not. Define a cell c as a pair, or pair × recorded stratum. Keep cells with at least two distinct gaps each occurring at least twice. With within-cell means $`\bar h_c`$ and $`\bar z_c`$,

```math
\hat\gamma=\frac{\sum_c\sum_{a\in c}(h_a-\bar h_c)(z_a-\bar z_c)}
{\sum_c\sum_{a\in c}(h_a-\bar h_c)^2}.
```

The index a refers to a pair occurrence inside a report. Replacing z by $`p_{\mathrm{SM}}`$ or $`p_{\mathrm{PL}}`$ gives the predicted slope under the same exposures. The residuals are $`\gamma_{\mathrm{observed}}-\gamma_{\mathrm{SM}}`$ and $`\gamma_{\mathrm{observed}}-\gamma_{\mathrm{PL}}`$. These are descriptive slopes, not parameters added to either ranking model.

P2 examines fitted-center and, where supplied, external-objective references. In the PrefLib/dots2024 objective-reference analysis, β is profiled on training rankings around that reference. PatrasIQ's objective-reference diagnostic retains the fitted SM β. P1 repeats those conventions. Beans season and Sushi B region controls use pair × stratum cells; D2 uses known synthetic groups. Wheat's village-adjusted diagnostic is unavailable because missing labels are not assigned an invented group.

Full fixed displays have no changing h within a pair. A missing or zero-variance contrast is unavailable, not a zero observed effect. Even a nonzero pooled slope need not imply an SM mechanism: participant composition and reference-center error can produce it. [D2](validation_extension.md) tests these explanations directly.

## Population structure summaries

S1 records exact structural summaries using the finite support. For each pair/display occurrence let $`p_a`$ be its true agreement probability and $`h_a`$ its gap. Equal-gap heterogeneity is the root mean square of $`p_a-\mathrm{mean}(p\mid h_a)`$; context heterogeneity is the root mean square of $`p_a-\mathrm{mean}(p\mid\mathrm{pair}_a)`$. The population context slope uses the same within-pair centering as above, without empirical eligibility thresholds. All support occurrences receive the weighting implemented by the uniform-set design.

Within-shell nonuniformity is the display-averaged quantity

```math
\sum_d P(D=d\mid S)\,\mathrm{KL}\big(P(Y\mid D=d,S)\Vert\mathrm{Uniform}(a_r(d))\big).
```

Mean inversions is $`\mathbb E[D]`$. The shell intervention holds the full distribution of D fixed, not only this mean.

## Discovery selection and regret

The pair selector chooses the fitted model with smaller mean discovery pair log loss. The context selector chooses SM when $`\lvert\gamma_{\mathrm{observed}}-\gamma_{\mathrm{SM}}\rvert\lt\lvert\gamma_{\mathrm{observed}}\rvert`$, otherwise PL; it abstains if the required contrast or fit is unavailable. Neither is an omnibus goodness-of-fit test. The selected model is evaluated on independent confirmation data or the known population distribution.

Regret is $`L_{\mathrm{selected}}-\min(L_{\mathrm{SM}},L_{\mathrm{PL}})`$, comparing the two fitted candidates. Simulation correctness is whether the selected loss equals the better candidate's loss, with the implementation's $`10^{-12}`$ tolerance where specified. D2 excludes true ties/unavailable winners for its correctness rate. Unavailable selections are counted, not changed into successes or zeros. Comparing a choice with an empirical confirmation point winner is weaker than knowing the population winner.

## Group comparisons and aggregation

G1 reports both report-weighted (micro) and equal-group (macro) means. If group g has $`T^g`$ scored reports and summed loss $`A^g`$, micro loss is $`\frac{\sum_g A^g}{\sum_g T^g}`$; macro loss is the mean of $`A^g/T^g`$ across contributing groups. These targets can differ when group sizes differ.

The local-versus-reference change for a family is $`L_{\mathrm{local}}-L_{\mathrm{reference}}`$. Relative sensitivity is

```math
I=(L_{\mathrm{SM},\mathrm{local}}-L_{\mathrm{PL},\mathrm{local}})-(L_{\mathrm{SM},\mathrm{reference}}-L_{\mathrm{PL},\mathrm{reference}}).
```

The four losses use exactly the same test reports with all four predictions finite. Negative I shifts the comparison toward SM; it need not mean either local model improves absolutely. Pooled and equal-budget matched-pool references answer different questions. Group-transfer tests use different held-out groups and are not report-paired with within-group tests.

## Availability is part of every comparison

`NaN` means no defined fitted result; `+inf` means a defined model assigned zero probability to a scored report. P1's full mean requires all repetitions defined and retains infinite losses. Separately named finite-conditional summaries exclude nonfinite repetition metrics. Finite-report summaries exclude nonfinite reports within a repetition; this is a different denominator. G1 explicitly reports finite common masks and coverage. Neither kind of conditioning estimates unconditional performance when failures matter. See [uncertainty and denominator rules](uncertainty.md#nonfinite-results-and-denominators).
