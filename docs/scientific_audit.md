# Scientific audit and corrections

**26 September 2026 UTC / 25 September New York.** Audited the actual GitHub snapshot 89b21645d5f7eb463cc90c4e982c3a66ce805b41 against the supplied manuscript's Sections 2–4, the cited integer formulation, the implementation and original-data manifests. This is a retrospective audit, not a new independent study.

**Answer to the user's question:** not every earlier experiment met the current standard. The active pipeline now separates original estimators, exact optimization and exploratory diagnostics; earlier modified pipelines are accessible only in Git history. No result is called compliant merely because its filename contains strict.

## Findings and actions

| Audit issue | What was actually done | Correction / consequence |
|---|---|---|
| Early fitting pipeline | beta cap, optional shrinkage, PL ridge, large-center insertion heuristics | Removed from current runnable comparison; Beans/Sushi rerun under a frozen unpenalized protocol |
| Section 4 attribution | Current unpenalized study described too broadly as literal manuscript replication | Algorithm 4.1 explicitly uses prespecified boundary treatment and regularized PL; current study is a declared variant using original estimator definitions and Hunter MM |
| Large-n center MLE | Conitzer integral LP3 with HiGHS, not original CPLEX 9.1 | Retain as certified exact-optimization benchmark; no original solver/runtime reproduction claim; disclose possible tied MLEs |
| Efficient estimator entry point | Shared legacy function capped lambda at 1; strict wrapper already rejected lambda>1 | Removed cap and enforce rejection at both interfaces; recorded successful strict fits unchanged |
| Sharp estimator | Literal pair extraction and exact greedy sieve only up to block size 8 | Retain unavailable status above limit; do not replace by MLE or claim an untested computational implementation |
| PrefLib uncertainty | Anonymous records bootstrapped despite missing assessor identities | Withdraw all associated inferential intervals and significance claims; retain descriptive point comparisons |
| Wheat uncertainty | Missing village IDs pooled into an artificial bootstrap block | Remove that convention, its intervals and village-adjusted inference; keep all records and unadjusted point values |
| Shared helper APIs | Obsolete capped/penalized/heuristic fitters remained callable alongside current fits | Remove obsolete fitting APIs and clipped diagnostic probability helper; one active fitter module |
| Data validation | Integer conversion could silently truncate noninteger labels | Reject noninteger inputs; original datasets already use integer item IDs, so fitted values do not change |
| Repository presentation | Historical and current instructions/reports/results coexisted | One current README, algorithm contract, reproduction guide and result index; old full snapshot linked in History |

Regularization is not intrinsically unscientific: the manuscript itself includes it. The issue is specifying the estimator honestly, following its definition, and not letting undisclosed modifications determine a scientific conclusion. Likewise exact algebraic reformulation and numerical tolerances do not by themselves modify a statistical objective, but do not establish replication of every implementation detail.

## Recomputed and verified

- Refit **all 16 strict real tasks and wheat**, with original data and unchanged membership/seeds. **All centers, beta values, PL worths, fit statuses and NLL point values match** the saved earlier fits to numerical tolerance. The 90 compared result rows include both held-out wheat splits, not 90 independent studies. [Replay comparison](../results/audit/refit_comparison.json).
- Refit **Beans, Sushi A and Sushi B** after [freezing the replacement protocol](protocols/BASELINE_REPLACEMENT.md). All original reports retained. Sushi B now has a certified global MLE with objective 45,149. Its interval and Sushi A's interval span zero; Beans is descriptive only. [Results](baseline_replacement.md).
- Existing **4,760 synthetic training samples** are retained, not rerun or counted again. The mathematical helpers used there are unchanged on admitted inputs. Tests verify noise/shell controls, independent MM optimization, exhaustive small-n center optima, sieve separation/coverage, orientation-independent pair sampling and boundary failures. All successful recorded Section 3 fits have depth zero.
- Full raw source checksum validation and saved-fit prediction replay are included. No source ranks were modified to produce a model advantage. New uncertainty suppression changes reported evidence, not an estimator or a source observation.

See [machine-readable validation](../results/audit/validation.json). It records the actual checks performed, rather than asserting that tests prove every future input correct. Frozen protocols remain unedited historical records; [the audit amendment](protocols/AUDIT_AMENDMENT.md) explicitly supersedes the affected inference provisions.

## Current defensible conclusions

1. Controlled simulations show a model-winner reversal as within-shell error allocation changes with all shell masses fixed.
2. Puzzle 2 remains an SM-favorable **descriptive** example. Its earlier interval-based support is withdrawn. Two identified-participant partial-dots tasks retain PL-favorable conditional intervals; source/task dependence and training uncertainty still limit generalization.
3. The specific positive real-data SM context effect remains unconfirmed. Wheat is too weakly supported and incompletely grouped for such an inference; SP-Rank lacks the targeted objective-gap variation.
4. No claim of MLE minimax optimality, a successful active Section 3 hierarchy comparison, or universally correct feature-based model selection follows.

This audit corrects earlier overly broad assurances of strict replication. [Algorithm details](algorithms.md), [all references](references.md), [historical snapshot](history.md).

Subsequent work is recorded separately in [additional data and mechanism validation](validation_extension.md). It adds three empirical tasks without changing the audited estimators and identifies limits of the context diagnostic. Its PatrasIQ report intervals are supported by newly verified one-report-per-person source metadata; the older Dots/Puzzle interval withdrawal remains in force.
