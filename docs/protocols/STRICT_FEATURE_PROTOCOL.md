# Strict feature-transition study (frozen before model fits)

Date: 2026-09-25. Seed: 202609251. This protocol responds to the user's requirement to preserve original observations and published estimators. It is a prospective extension, not a replacement for earlier regularized experiments.

## Questions
1. How does changing probability structure, at fixed sample size, display design, and average Kendall noise, change SM versus PL prediction?
2. Do original human ranking datasets exhibit common reliability at equal displayed center gap, approximately uniform probabilities within Kendall shells, or the specific positive context effect predicted by SM?
3. Can a diagnostic calculated on discovery reports predict the winner on separate confirmation reports?

No dataset will be retained or discarded according to which model wins. All screened sources and all failures will be reported.

## Estimator contract
- SM center MLE: manuscript Proposition 4.1, exact subset DP, with a fixed data-independent tie rule. For larger catalogs, a separately cited exact linear-order integer formulation may be used only when the optimum is certified. No insertion heuristic is an MLE in this study.
- Dispersion: Proposition 4.2 on [0,infinity]. Return beta=infinity when training distance is zero and beta=0 at the uniform boundary. No cap, shrinkage, penalty, or probability floor. Zero-probability held-out events produce infinite NLL.
- PL: Hunter (2004), Section 5 / equation (30), the simultaneous unaccelerated MM update for the full ranking likelihood. No ridge, pseudo-comparisons, smoothing, early-stopping estimator, or rank breaking. Check the directed comparison graph first; no unique finite MLE is a reported outcome, not an invitation to drop items. Stop on a prespecified numerical fixed-point tolerance, record convergence and gradient checks.
- Sharp center: literal manuscript Algorithm 2.1 and Lemma 2.11, proof constants, one orientation-independent pair per report/block, fixed lexicographic greedy packing. Refuse exact blocks above size 8; do not substitute MLE.
- Efficient center: literal Algorithm 3.1 only on its specified lambda<=1 schedule domain; no eta cap. The paper's global clipped Borda (3.4) is a separately named baseline outside that domain. Keep all proof constants. Record depth and actual branch. Do not claim minimax validity for misspecified DGPs or nonuniform real displays.
- Real beta0 is set in advance to 0.1 for schedule construction only; its truth is not certified. Synthetic SM beta0=beta=0.8.
- Existing regularized/shrunk/heuristic results remain historical comparisons and cannot establish conclusions about these strict estimators. Section 4 explicitly permits prespecified regularization; it is nevertheless excluded here to answer the user's new scientific question.

## Synthetic designs
Uniform independent r-subsets; generate a whole ranking directly conditional on the subset. Randomize the true center independently of estimator ties. Never obtain SM reports by thinning full Mallows rankings.

A. Matched-noise bridge: P_a(.|S)=(1-a)P_SM(.|S)+a P_PL(.|S), a in {0,.25,.5,.75,1}. Calibrate the PL worth scale so its expected inversion count, averaged over uniform subsets, equals that of SM beta=.8. Use two fixed adjacent log-worth gap shapes: equal gaps and alternating gaps (1,4,1,4,...). Both preserve a strictly ordered center. This bridge changes context dependence and pair heterogeneity together; it is not an isolated causal intervention on one feature.
- n=8, r in {2,3}, N in {8,28,112,448}, 40 independent repetitions.
- n=32, r=3, N in {40,160,640}, a in {0,.5,1}, equal gaps, 40 repetitions. Exact sieve is unavailable here; do not replace it.

B. Within-shell intervention, n=8,r=3: retain exactly the SM mass of EVERY Kendall shell for EVERY displayed set. Inside each shell assign probabilities proportional to P_PL(Y|S)^h, h in {0,.5,1,2,4}. Thus h=0 is SM; larger h favors specific error patterns without changing the inversion-count distribution. The hybrid distribution is a declared simulation mechanism, not a fitted competitor or a modification of real data. Pair marginals may change as a consequence.
- Same two PL gap shapes; N in {28,112,448}; 40 independent repetitions.

Total planned independent training datasets: 4,760. Identical reports go to every applicable estimator. Exact enumeration evaluates population conditional NLL for small n; independently generated test reports (2,000) evaluate n=32. Separate discovery reports (1,000) supply diagnostics/selection and are never used to fit either model. Report that selection has this additional data budget.

Report model existence/convergence frequencies first. Never average only successful runs without disclosing conditioning. If any positive-probability outcome has zero predicted probability, expected NLL is infinite. Finite-run summaries are explicitly conditional. Kendall center risk is separate.

## Original real data: frozen candidate families
- PrefLib 00024 Dots: all four original .soc files.
- PrefLib 00025 Puzzle: all four original .soc files.
Both have n=r=4, externally known objective order, but upstream aggregation removed assessor/trial IDs. They can test shell structure, not selective context variation or lambda<1. Preserve multiplicities; do not pretend recovered anonymous records restore grouping.
- Yoo et al. (Scientific Reports, 2024), official linked repository ryankemmer/simpleRatingRanking. Inspect schema/provenance before selecting canonical exports. Use directly elicited ordinal reports, not rankings induced from numerical ratings. Different report sizes use different image catalogs and remain separate tasks. Keep whole participant blocks together. No outcome-dependent cleaning, outlier deletion, or invented tie breaking. If original encoding or grouping cannot be established, mark the source unusable for the corresponding claim.
- Existing Beans/Sushi remain previously examined benchmarks, not fresh independent confirmation sources.

Split once with the frozen seed: 60% fit / 20% discovery / 20% confirmation, grouped where IDs can be recovered from the original export structure. No searching for favorable split seeds. Preserve each full displayed set and reported order. Catalogs are source-defined; never remove unseen labels to obtain a finite MLE. Source checksums, schema validation, and every exclusion with an outcome-independent reason are saved. New source eligibility details may be added before its first fitted result and are timestamped.

## Diagnostics and selection
Use the training-estimated center, and separately the objective ground truth where genuinely supplied. For r=2 examine pair success heterogeneity. For r>2 compare reliability at the SAME displayed gap; do not impose common reliability on all extracted pairs.
Use the exact shell decomposition for r<=6, treating pairs within a report as dependent. Evaluate a within-pair displayed-gap slope only when at least two gap levels have at least two observations each. PL predicts zero; SM predicts its exact pair marginals on identical displays. Missing variation means unavailable, not zero effect.
A prespecified exploratory selector chooses the model with smaller mean pairwise log loss on discovery reports (whole-report averages); ties choose PL. For r=2 this is ordinary validation log loss, not an independent structural diagnostic. Confirm its whole-ranking performance separately; compare with always-SM/always-PL. An unsupported model or insufficient diagnostic coverage yields abstention, not an imputed score.
Also test a context-only selector where eligible: choose SM if the observed slope is closer to its predicted slope than to zero, otherwise PL. Keep it distinct from the pairwise selector.

## Uncertainty and reporting
Simulation intervals use paired independent-replicate t intervals, with boundary/nonexistence outcomes reported explicitly. Real report-bootstrap intervals use 2,000 draws conditional on fixed fits, grouped by participant if available. Aggregated PrefLib uncertainty is labelled an anonymous-record working calculation, not independent-participant inference. Diagnostics/confirmation for each real task are disjoint; dataset search does not establish external replication. Report all tasks and no universal feature threshold from this one study.
