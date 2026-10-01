# Trial and assessor heterogeneity

[Experiment G1](experiments.md) · [Data and identities](../data/dots_puzzle.md) · [Criteria](criteria.md#group-comparisons-and-aggregation) · [Uncertainty](uncertainty.md#group-split-percentiles) · [Outputs](../results/group_sensitivity/README.md)

Local fitting can improve Puzzle prediction when the training count is held fixed, for both SM and PL. Full pooled training often offsets that benefit with a larger sample. The relative SM–PL change is not stable across Puzzle conditions. Sounds exposes severe finite-MLE and infinite-prediction limitations for individual fitting; its rare successful cases do not support a population-level model comparison.

## Observations and group identity

The original [author data page](https://www.andrewmao.net/code/) links [voting-results.tar.gz](https://dl.dropboxusercontent.com/s/mf0mm153pe3f12w/voting-results.tar.gz), SHA256 `2906b0ce3fc375813f7fd061e55fd642e6e9ac472a385a56d2b8e36ef838e0d4`. Its 40 files per condition identify repeated physical stimulus sets. All 24 ranking frequencies exactly match each of the eight pinned PrefLib files. Puzzle contributes 3,180 reports; Dots (2013, **not dots2024**) contributes 3,183. Each report ranks all four presented items. The four difficulty conditions in each family are fitted separately.

A local trial uses its fixed four physical stimuli, whereas pooled item labels identify difficulty categories across trials. Actual board layouts, globally unique board IDs and cross-trial assessor IDs remain unavailable. Trial membership does not establish assessor independence or prove that no stimulus was reused elsewhere. Sounds contributes 46 source-identified assessors with 30 pair reports each over 12 items (1,380 reports). The pinned BayesMallows source and download hashes are retained in the data manifests. Other tasks do not provide both reliable group identities and within-task per-person repetitions for this design. Different catalogs/tasks are not combined to manufacture repetitions.

## Pre-fit design and fitting

The [protocol commit](https://github.com/hyj55/mallowsmodel/commit/69541057711c08ff1508f25676bb6abfdd12c27d) predates production fits. Root seed `202609270` uses separate streams by task, fraction, repeat, purpose and group. The primary design repeats 70/30 within-group splits 100 times; budget sensitivities repeat 50/50 and 80/20 20 times each. Every group contributes floor(fraction × count) intact training reports, with the remainder held out. Integer rounding is explicit; no split is rerolled for coverage or fit existence.

For identical test reports, compare (1) pooled training on all groups, (2) local training on the target group, and (3) matched_pool, a uniform without-replacement subsample of pooled training with exactly the local training count. Matched training can contain target-group reports. All methods share each context's training and test memberships. Group labels route local predictions but are not covariates in either ranking law. Local prediction requires known group identity and increases total model capacity.

A separate 100 whole-group 70/30 holdouts evaluates transfer to unseen trials/assessors using pooled fits. It is a different predictive target, not paired report-for-report with within-group evaluation. Within-assessor evaluation predicts additional reports of known people; it is not a new-person split. Trial holdout cannot establish person disjointness without person IDs.

Unchanged conditional likelihoods, unbounded SM profile beta and unpenalized Hunter MM are used. Infinite SM losses and undefined/nonconverged PL fits remain explicit. No beta cap, pseudodata, removed catalog items, test-driven method selection or repaired split is introduced. This is the declared unregularized variant, not a literal implementation of the entirety of manuscript Algorithm 4.1.

- **Exact SM center:** exact subset DP for n=4 and n=12; cardinality batching preserves the recurrence, objective and seeded tie order. No approximate substitute was needed. G1 conservatively excludes fits with unseen catalog items. Full pair coverage is not necessary for a Kemeny minimizer to exist; sparse ties/nonidentifiability remain limitations.
- **Fotakis Algorithm 1 / PosEst:** majority-predecessor counts, counting equal-count pair ties in both directions, fixed seeded random score-tie order. Admit only training sets containing every item pair; record empirical p=min(pair count)/N. This structural check does not certify the paper's true-model or sample-size recovery guarantees. Profile beta is then fitted by the same likelihood.
- **Sharp / efficient:** the pre-fit policy conservatively excludes lambda=N*r*(r−1)/(n*(n−1))>1, outside the manuscript's sparse theorem regime. This is a theorem-domain admission choice, not a claim that Sharp is mechanically undefined outside that regime. Consequently Sharp/efficient are excluded for full four-item trials. Sounds local data can satisfy lambda≤1; n=12 exceeds the size-8 exact sieve guard, so the specified Section 3 fallback is used when every item appears. All successful efficient fits had hierarchy depth zero. Uniform subset sampling, independent reports, true beta≥.1 and the unknown sufficient constant C0 are not verified; mu/log(e*r)>1 is not a certificate.
- **PL:** requires directed strong connectivity and the unchanged numerical convergence checks. An unavailable finite unique MLE is not assigned an invented predictive score.

## Primary results

NLL is in nats/report; delta=SM exact−PL, negative favoring SM. Values are means across 100 70/30 repetitions on each scheme's pairwise finite predictions. Cross-scheme comparisons below use stricter four-way common masks. Whole-group holdout is a separate target.

| Task | Pooled | Local | Matched pool | Whole-group holdout |
| --- | --- | --- | --- | --- |
| puzzle-5 | -0.0571 | -0.0482 | -0.0585 | -0.0572 |
| puzzle-7 | -0.0143 | +0.0113 | +0.0047 | -0.0191 |
| puzzle-9 | -0.0094 | +0.0053 | +0.0004 | -0.0106 |
| puzzle-11 | -0.0110 | -0.0175 | -0.0084 | -0.0123 |
| dots-3 | -0.0129 | -0.0007 | -0.0050 | -0.0147 |
| dots-5 | -0.0167 | +0.0220 | -0.0136 | -0.0182 |
| dots-7 | -0.0126 | -0.0080 | +0.0009 | -0.0128 |
| dots-9 | -0.0313 | -0.0312 | -0.0260 | -0.0364 |

Puzzle-5 pooled delta has a 5th–95th split range [-0.0773, -0.0356]; local [-0.0995, +0.0073]. Puzzle-7/9 have mean sign reversals but ranges spanning zero. These are partition-sensitivity summaries, not confidence intervals or independent samples from a population.

## Training-budget control

Each contrast uses the same test reports with all four predictions finite (SM/PL × local/reference). Negative changes favor local fitting. Coverage is the mean fraction of test reports in the matched four-way mask.

| Task | SM local−pooled | PL local−pooled | SM local−matched | PL local−matched | Matched coverage |
| --- | --- | --- | --- | --- | --- |
| puzzle-5 | +0.0040 | -0.0049 | -0.1285 | -0.1386 | 99.44% |
| puzzle-7 | +0.0187 | -0.0071 | -0.1327 | -0.1391 | 99.38% |
| puzzle-9 | +0.0177 | +0.0030 | -0.1162 | -0.1212 | 99.65% |
| puzzle-11 | +0.0097 | +0.0162 | -0.1212 | -0.1121 | 100.00% |
| dots-3 | +0.0997 | +0.0876 | -0.0392 | -0.0435 | 100.00% |
| dots-5 | +0.0935 | +0.0549 | -0.0459 | -0.0814 | 100.00% |
| dots-7 | +0.1113 | +0.1066 | -0.0354 | -0.0266 | 99.95% |
| dots-9 | +0.0985 | +0.0984 | -0.0349 | -0.0297 | 100.00% |

At equal training counts, all four Puzzle tasks improve for both families by about 0.11–0.14 nats/report. This does not imply that a local model beats the much larger pooled training set. Both families retain negative mean local-minus-matched changes at the 50%, 70% and 80% training budgets. Smaller budgets increase failures and favor full pooled training; some local fits improve at 80%. Dots has smaller equal-budget gains and generally benefits from the full pooled sample.

![Prediction changes](../figures/group_sensitivity/local_prediction_changes.png)

## Relative model sensitivity

Interaction=(SM_local−PL_local)−(SM_reference−PL_reference), evaluated on common four-way finite cases. Negative shifts the comparison toward SM. Ranges are empirical 5th–95th split percentiles, **not population confidence intervals**.

| Task | Vs pooled mean | Split range | Vs matched mean | Split range |
| --- | --- | --- | --- | --- |
| puzzle-5 | +0.0089 | [-0.0432, +0.0642] | +0.0101 | [-0.0777, +0.0867] |
| puzzle-7 | +0.0257 | [-0.0388, +0.0844] | +0.0064 | [-0.0778, +0.0748] |
| puzzle-9 | +0.0147 | [-0.0346, +0.0572] | +0.0050 | [-0.0650, +0.0759] |
| puzzle-11 | -0.0065 | [-0.0481, +0.0398] | -0.0091 | [-0.0701, +0.0488] |
| dots-3 | +0.0122 | [-0.0425, +0.0521] | +0.0043 | [-0.0480, +0.0668] |
| dots-5 | +0.0387 | [+0.0001, +0.0816] | +0.0356 | [-0.0154, +0.0892] |
| dots-7 | +0.0046 | [-0.0449, +0.0498] | -0.0088 | [-0.0732, +0.0622] |
| dots-9 | +0.0001 | [-0.0592, +0.0519] | -0.0052 | [-0.0863, +0.0651] |

Puzzle interactions differ in sign and all ranges span zero. Group identity has predictive value, but no stable differential sensitivity is established. Dots-5 shifts toward PL against full pooled training; the equal-budget range spans zero. These are multiple descriptive comparisons, not a population significance claim. More parameters, assessor composition and unrecorded trial conditions prevent a causal board-identity interpretation.

![Relative advantage](../figures/group_sensitivity/relative_model_changes.png)

## Estimator sensitivity

Local delta values below retain exact as the predeclared primary method; they do not select a method using test results.

| Task | Exact−PL | Fotakis−PL |
| --- | --- | --- |
| puzzle-5 | -0.0482 | -0.0707 |
| puzzle-7 | +0.0113 | -0.0032 |
| puzzle-9 | +0.0053 | +0.0015 |
| puzzle-11 | -0.0175 | -0.0298 |
| dots-3 | -0.0007 | -0.0097 |
| dots-5 | +0.0220 | +0.0087 |
| dots-7 | -0.0080 | -0.0294 |
| dots-9 | -0.0312 | -0.0559 |

Fotakis often predicts better locally despite not maximizing training likelihood. Model-family conclusions should therefore name the center estimator. The per-group output retains every group and candidate, including skipped candidates and finite coverage.

## Sounds and dependent observations

With 21 training and 9 test pairs per assessor, only 28 of 4,600 local PL contexts have a usable finite unique MLE; 4,572 fail strong connectivity. Matched pooled training has only 9 usable contexts. Exact SM excludes 454 contexts with unseen items; among 4,146 admitted contexts, 1,531 have at least one infinite test loss and 2,615 have all finite predictions. Efficient admits the same 4,146, with 420 contexts containing infinite losses, all at depth zero. Local Fotakis fails all-pair coverage everywhere.

These failures are outcomes of the fixed unregularized experiment. The tiny intersection of finite local predictions cannot estimate overall comparative personal predictive risk. Additional regularized or hierarchical modeling would require a separately specified experiment. All pooled primary fits and whole-person holdout fits are available: exact-SM delta=+0.0134 within persons and +0.0090 for new persons, with new-person split range [-0.0060,+0.0275].

Stable latent person characteristics can induce dependence after pooling; including other people does not remove it. Conditional independence given a person's parameters is a modeling assumption. Unknown cross-trial identities remain unresolved. Repeated shuffles do not create independent people, and no independent-splits t-test or standard error divided by sqrt(100) is used.

## Availability, validation and reproduction

Main trial four-way coverage is about 99.4%–100%; unavailable/infinite cases are still reported separately. Finite conditional means are not unconditional finite-risk estimates. Puzzle-5 matched coverage at the 50% budget falls to about 94%, increasing conditional-selection concerns. Sounds local coverage is too low for meaningful overall comparisons.

The run records 104,640 training contexts and 523,200 candidate statuses, including exclusions and cache reuse, across 7,743 original reports. Public outputs have 23,400 repeat-score rows and 18,300 group-score summaries. Figures use medians; tables use means. Micro/report-weighted and macro/equal-group values are both retained.

Focused tests check sampling, ties, exact-DP agreement, coverage admission, likelihoods and unavailable/infinite aggregation. Full local validation reconciles source frequencies, replays stored predictions and split memberships, and recomputes the published tables and four-way masks. See [validation.json](../results/group_sensitivity/validation.json) for the completed validation receipt. Public repository verification checks checksums and repeat aggregation without downloading respondent data.

```bash
python run_group_sensitivity.py --workers 4
python validate_group_sensitivity.py
python validate_group_sensitivity.py --repository-only
python make_group_sensitivity_figures.py
```

Use the pinned dependencies in a separate checkout; the recorded run used Python 3.13.7. Original data, per-report caches and fitted context parameters stay in ignored local directories. Reproduction refits those caches from the verified sources; public artifacts are aggregate results. Full replay requires the caches produced by the runner. Public-only validation does not claim to reconstruct per-report predictions.
