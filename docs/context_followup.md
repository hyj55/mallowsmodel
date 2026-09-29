# Original-data follow-up: displayed-set context

**28 September 2026 update:** the real-data point comparisons below retain their original single partition. Use the [30-repeat correction](repeated_holdout.md) ([中文](repeated_holdout_zh.md)) for average predictive performance after repeated full refitting. Original bootstrap intervals stay conditional on the original fits; synthetic results and source-only audits are unchanged.

**Audited 26 September 2026 UTC.** One intact agricultural task and six SP-Rank source-design audits. The positive SM context effect remains unconfirmed. Original reports, centers, dispersion estimates and NLL point values are unchanged by the audit.

## Wheat

The official gosset sample contains **493 strict triples over 16 varieties**, Vaishali, India, 2014 Rabi season. Best and worst among three distinct varieties determine the order without ambiguity. All 493 reports are retained. This is the package sample, not all records in the 2019 PNAS study; no latent true center is supplied. [Source documentation](https://agrdatasci.github.io/gosset/reference/breadwheat.html).

The frozen split is 295 training / 99 discovery / 99 confirmation. Training lambda=7.375, mu=55.3125. All items occur in training. There are **418 distinct displayed sets**. The center algorithms and computational limits are specified in the [method contract](algorithms.md).

| Confirmation method | Conditional NLL | SM minus PL |
|---|---:|---:|
| Hunter MM PL | 1.4794 | — |
| SM exact DP MLE | 1.5801 | +0.1007 |
| SM clipped Borda | 1.4847 | +0.0053 |

These are **descriptive point comparisons**. Sharp is unavailable at this exact sieve size; Section 3 is outside its schedule domain. Neither is replaced by a different estimator. MLE training distance is 216, beta=0.93935; Borda distance is 234, beta=0.84795.

**Correction:** 113 village labels are missing and farmer identities are redacted. The previous extra unknown-village bootstrap block did not identify independent units. Its intervals, including the degenerate village-adjusted interval, are withdrawn. No missing report is deleted or assigned a surrogate village. All CIs are now unavailable; the village-adjusted diagnostic is unavailable as well. A -1 label in the split metadata denotes missing information only. Point estimates do not establish statistical superiority or geographic generalization.

## Specific SM prediction

Freeze the training MLE center. Within each pair, relate its correctly oriented indicator Z to its displayed-center gap h, using pair fixed effects. This exploratory diagnostic does not change either model fit. A pair needs at least two observations at each of two gap levels.

| Split | Eligible pairs | Pair observations | Observed slope | SM prediction | PL prediction |
|---|---:|---:|---:|---:|---:|
| Discovery | 8 | 39 | -0.1043 | 0.1109 | 0 |
| Confirmation | 6 | 30 | +0.0874 | 0.1109 | 0 |

The signs differ between splits and support is sparse. No inferential interval is asserted with unidentified clustering. Thus the confirmation point estimate being closer to SM is **not sufficient evidence** for its mechanism. Arbitrary third-item dependence would not establish the SM gap formula either.

## SP-Rank design audit

The author's public dataset contains repeated participants and several elicitation formats. We retained for the audit actual complete first-order Rank responses (treatments 4/5/6), separately across three domains and the two author-defined cohorts. Top choices, approvals and meta-predictions were not converted to full rankings.

| Cohort | Domains | Strict reports per domain | Distinct displays per domain | Pairs with changing objective displayed gap |
|---|---:|---:|---:|---:|
| Four items | 3 | 1,200 | 20 | 0 in every task |
| Five items | 3 | 576 | 12 | 0 in every task |

All 5,328 audited reports are strict, but each observed pair has a constant gap within the displayed **objective order**. These displays cannot identify the targeted between-versus-outside contrast about that order. No fits were run for this follow-up. This is not a claim about all possible fitted centers or other uses of SP-Rank. Objective order need not equal a latent SM center. [Paper and author release](https://arxiv.org/html/2601.05253v1).

The lesson is about experimental information: total report count, lambda and mu do not measure repeated within-pair context contrasts. We did not alter observations to create those contrasts or continue screening until a favorable result appeared.

## Reproduce and provenance

Run `python run_context_followup.py` with requirements-lock.txt. See [the shared reproduction guide](reproducibility.md), [original frozen protocol](protocols/CONTEXT_FOLLOWUP.md), [retrospective correction](protocols/AUDIT_AMENDMENT.md), [source manifest](../data/context_followup_sources.json), and [outputs](../results/context_followup/README.md).

Sources are pinned at gosset bb5eb75c08fe3ab0f28931c093dcb66dea7c4185 and SP-Rank d9ceab3386ac04aca7791fd83da8508851f87dc9. The original study and metadata amendment preceded fits at commits 7be066c1d951569783acf96aca14f3e8635939e1 and 40be502dc4be5c006fcd6ef7c2f1e5916c24237c. The later audit is retrospective and adds no independent data. [Full references](references.md).
