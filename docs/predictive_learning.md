# Supplementary learning and catalogue-size experiments (L0/S0)

[Primary prediction](predictive_comparison.md) · [Empirical curves](../results/predictive/learning.csv) · [Synthetic curves](../results/predictive/synthetic.csv) · [Supplementary learning controls](learning_curves.md)

**L0 and S0 are supplementary experiments; P0 alone is the Algorithm 4.1 main experiment.** Their likelihood-center SM and PL curves use P0's finite fitting procedures: the fixed SM beta bound 10, inner-selected positive PL ridge, exact small-catalogue likelihood centers, and certified-or-explicitly-approximate integer optimization for larger catalogues. Separate estimator curves additionally attempt Sharp with the resource-accounted exact sieve; this does not make Sharp a P0 main method. Fotakis requires every pair to be observed. Efficient appears only as an admitted fallback after Sharp fails computationally. The global-sieve supplement reuses the identical Sharp fit when the two constructions coincide.

## L0: Sushi A/B with five outer partitions

Both tasks have 5,000 respondent rows and rank ten items per report. A has a fixed ten-item catalogue and display; B has a hundred-item catalogue and varying ten-item displays. This makes the two tasks informative about different exposure regimes, but they are different preference tasks and not a controlled intervention on catalogue size.

Use P0's 5 aligned respondent permutations. Each outer test has 1,000 people. Independently permute the 4,000 development respondents with seed sequence (202610130, task split key, repetition), using the same order for A and B. Take nested prefixes of N=20,50,100,300,1000,3000. An observation in a small prefix remains in all larger prefixes for that repetition. The N=4000 endpoint reuses P0 for likelihood-center SM/PL and E0 for the estimator supplements; it is linked, not fitted or counted twice.

At each N, use the first floor(0.75N) respondents for inner fitting and the rest for PL penalty validation, then refit on all N. Thus N always denotes the final development budget, not the smaller inner-training size. Inner membership can change as a prefix grows, while the outer test remains fixed within the repetition. There is no exchange of training and test respondents as N changes.

The reported curve is

```math
\overline L_M(N)=\frac1{5}\sum_{b=1}^{5}
\frac1{1000}\sum_{t\in\mathcal T_b}
-\log P_M(Y_t\mid S_t;\widehat\vartheta_{M,b,N}),\qquad
\overline\Delta(N)=\frac1{5}\sum_b\left[L_{\mathrm{SM},b}(N)-L_{\mathrm{PL},b}(N)\right].
```

The same-test and nested-training design makes the within-repetition comparisons paired. It does not make the budgets independent. Curves need not improve monotonically in the realized finite sample. Means, partition MCSEs and split quantiles have the same fixed-data interpretation as P0. Per-split respondent-bootstrap intervals remain conditional on their fitted predictors and are not population CIs for the average curve.

Here r=10 and the upper bound R=10 are held fixed for every N, for both catalogue sizes. In Sushi B, many pairs or items can be unseen at small N; these catalogue items are retained. The tables record missing coverage and method admission, rather than rerolling a prefix or silently changing the catalogue.

Sharp has 5/5 fits at every Sushi A budget. Sushi B has no Sharp result at N=300,1000,3000 or the linked N=4000 E0 endpoint. Unavailable points remain absent, with their status and denominator reported.

## S0: independent data with fixed r=3 and R=10

These controls isolate N and n under known generating mechanisms. Draw each displayed set uniformly before generating its reported order. The SM generator has beta=0.8; the PL generator has log-worths linearly decreasing from 1 to −1 along the generating order. Each independent repetition draws a fresh random order, training data, and 4,000 test reports. The model definitions and generator parameters are fixed, not calibrated to a favorable result.

In the PL catalogue-size curve the overall log-worth range stays fixed, so adjacent log-worth gaps decrease as 2/(n−1). In SM the dispersion beta remains fixed. These are explicit families of growing problems, not a claim that every aspect of task difficulty is identical as n changes. Averaging over randomly generated centers is also an average-center risk calculation, not the supremum over centers in a minimax definition.

| Curve | What varies | What remains fixed |
|---|---|---|
| Training size | N=20,100,500 | n=10, r=3, R=10, generating law and noise parameters |
| Catalogue size | n=6,10,16,32 | N=100, r=3, R=10, generating-law parameter rule |

The shared n=10,N=100 cell is used once. With two generators and 20 independent repetitions, there are 240 distinct training/test draws, not 280. Each cell uses a 75/25 inner split of its training reports and refits on all N. Seeds are determined by (202610131, generator index, n, N, repetition); independent child streams supply the generating order, training reports and test reports.

The predictive quantity remains whole-ranking NLL. Also record Kendall distance of each fitted order from the generating order. Under the correctly specified SM generator this is realized center-estimation error. Under the PL generator it is an ordering-error description, not selective-Mallows minimax risk.

For any scalar outcome X, including a paired SM−PL loss difference, the independent-repetition mean and interval are

```math
\overline X=\frac1{20}\sum_{b=1}^{20}X_b,\qquad
\overline X\ \pm\ t_{19,.975}\frac{s_X}{\sqrt{20}}.
```

Fresh independent training **and** test draws make the repetitions independent Monte Carlo observations. Finite test-set noise is part of X_b. The Student-t interval estimates the mean of this specified simulation procedure; with twenty potentially non-Gaussian errors it is approximate, not an exact risk bound. All intervals are pointwise. When an estimator is unavailable for a planned repetition, its full-cell mean and interval are unavailable; the conditional mean and denominator remain explicit.

Fixing R meets one requirement of the bounded-subset corollary. The tables also report lambda: only cells satisfying lambda<=1 can address its first-part regime, and no finite grid establishes an asymptotic minimax theorem. The [theory correspondence](theory_alignment.md) distinguishes prediction, true-center risk, numerical exposure and theorem assumptions.

Both generators have 20/20 Sharp fits at every n=10 sample-size point. At N=100 the n=16 and n=32 Sharp cells remain memory-limited. These are 80 missing independent simulated fits. See the [exact-sieve resource account](sieve_computation.md).

## Complementary curves

[Supplementary L1/L2/S3](learning_curves.md) retain fixed-outer-test curves, very small budgets, dispersion shrinkage, penalty controls and additional exposure designs. Their independent questions and fitting variants remain identifiable. They are not pooled with L0/S0 or displayed as extra repetitions of the same curve. The r=32 exposure design is explicitly outside the R=10 comparison; an r=n curve with growing n is a full-ranking endpoint, not a fixed-R experiment.
