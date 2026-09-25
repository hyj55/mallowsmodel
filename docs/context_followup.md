# Original-data follow-up: can we identify the SM context effect?

**Completed 25 September 2026.** This exploratory extension adds one intact agricultural task and audits six SP-Rank tasks. It does **not** establish a real SM context effect. No original rankings or estimator algorithms were changed.

## What was added

The official gosset breadwheat sample [1] contains **493 assessments, 16 varieties, and strict triples**, from Vaishali, India, in the 2014 Rabi season. Best and worst among three distinct varieties determine the complete order exactly. All overall-performance assessments are usable; no report or item was removed. This is the package's public sample, not the entire replication dataset of van Etten et al. (2019) [2]. There is no known population central ranking. The source describes randomized incomplete blocks; that does not by itself verify every uniform-sampling assumption in the manuscript.

We fixed 295 training / 99 discovery / 99 confirmation reports. Training **lambda=7.375, mu=55.3125**: this is outside the sparse-pair regime. All 16 varieties appear in training. The 493 reports span **418 different displayed sets**; a moderate total sample need not supply many repeated pair/context contrasts.

Protocol [commit 7be066c](https://github.com/hyj55/mallowsmodel/commit/7be066c1d951569783acf96aca14f3e8635939e1) preceded fitting. The first execution stopped before any fit because **113 village labels were missing**. A [pre-fit amendment](https://github.com/hyj55/mallowsmodel/commit/40be502dc4be5c006fcd6ef7c2f1e5916c24237c) retained every record and explicitly defined missing metadata as one unknown bootstrap block. There are 14 known villages, and 22 missing labels in each held-out split. This is a bookkeeping block, not an imputed village. See the [full protocol](protocols/CONTEXT_FOLLOWUP.md).

## Model comparison

Unchanged estimators from the strict study: SM center MLE by exact subset dynamic programming; uncapped profile dispersion; separately named manuscript clipped Borda; PL by Hunter's simultaneous MM equation (30) [3]. Sharp is **unavailable** because its literal exact sieve exceeds the implemented size limit. Section 3 is **outside its schedule domain**, not silently replaced by Borda. Neither absence is evidence of poor statistical performance.

Lower conditional whole-ranking NLL is better; delta = SM minus PL, in nats per report.

| Confirmation method | NLL | Delta versus PL | Working 95% interval for delta |
|---|---:|---:|---:|
| PL MM | 1.4794 | — | — |
| SM exact MLE | 1.5801 | +0.1007 | [-0.0766, +0.2179] |
| SM clipped Borda | 1.4847 | +0.0053 | [-0.1854, +0.1172] |

**PL has the better point estimate, but confirmation does not resolve the difference.** Discovery favored PL more strongly: MLE delta +0.2153 [0.0136, 0.3797]. That exploratory split cannot replace the unresolved confirmation result. Borda's better test point estimate than SM MLE here is a finite-sample observation, not a general estimator ranking or a minimax result.

SM MLE has training Kendall objective 216 and beta=0.93935; Borda has objective 234 and beta=0.84795. PL converged in 147 simultaneous updates with gradient/report about 2.15e-11. No regularization, floors, heuristic center replacement or deletion was used.

Intervals use 2,000 paired bootstrap samples of entire recorded-village blocks, conditional on fixed training fits. Confirmation has 13 blocks. **These are working intervals:** unknown village membership can link records across blocks; train/test records can share villages; training and source-selection uncertainty are excluded. The target is reports in this sampled region/season, not out-of-region transport. Redacted participant identities also prevent independent verification of repeated farmers.

## The targeted context diagnostic

For a pair oriented by the training SM center, let Z indicate agreement and h be its rank distance *inside the displayed set*. Estimate

\[
Z_{t,ij}=a_{ij}+\gamma h_{t,ij}+\varepsilon_{t,ij}.
\]

This is a descriptive fixed-effect slope, not a new ranking estimator. Each eligible pair must have at least two observations at each of two gap levels. Apply the same slope operator to model probabilities: PL gives zero; the fitted r=3 SM gives **0.11089**. Center and parameters are frozen before either held-out split.

| Split | Eligible pairs | Pair observations | Observed gamma [working interval] |
|---|---:|---:|---:|
| Discovery | 8 | 39 | -0.1043 [-0.3499, 0.0884] |
| Confirmation | 6 | 30 | +0.0874 [-0.4733, 0.4484] |

Confirmation is compatible with both predictions. Discovery's residual relative to SM is negative, but it does not replicate in confirmation. Therefore this dataset **does not verify the positive SM gap mechanism**. Arbitrary third-item effects would not suffice either.

The prespecified pair-by-recorded-village sensitivity has no eligible discovery cells. Confirmation has only two cells / nine pair observations, all contributing within **one metadata block**. Its numerical bootstrap interval collapses to a point whenever that block is drawn; 708/2,000 draws are undefined. **That collapse is a lack of between-cluster information, not high precision, and supports no inference.** Raw outputs retain the diagnostic warning. The unstratified confirmation bootstrap has 1,996 valid draws.

## Why SP-Rank did not solve the coverage problem

The author dataset [4] contains multiple elicitation formats and repeated participants. We audited only actual first-order complete Rank responses (treatments 4/5/6), separately across all three domains and the two author-defined cohorts. Top choices, approvals and meta-predictions were not converted into ranking observations.

| Cohort | Domains | Strict reports per domain | Display sets per domain | Pairs with changing objective displayed gap |
|---|---:|---:|---:|---:|
| Four alternatives | 3 | 1,200 | 20 | 0 in every domain |
| Five alternatives | 3 | 576 | 12 | 0 in every domain |

All **5,328** audited reports are strict. Nevertheless, each observed pair always has the same distance within the displayed **objective order**. More repeated responses to these displays cannot identify the specific between-versus-outside contrast about that order. No fits were run for this targeted follow-up. This does not imply that arbitrary fitted centers have no variation, that the objective order is a latent SM center, or that SP-Rank is unsuitable for other model comparisons. The four-item cohort also only shows 41 of its 50 catalog items; deleting the other items would change a full-catalog estimand.

## Scientific implication

The earlier controlled experiment establishes that within-shell error allocation can reverse the model winner; its real examples remain tentative. The present search adds **no convincing real context example**. What is missing is repeated observation of the same pairs at distinct displayed-center gaps, with adequate assessor/context control. Counts of reports, lambda and mu alone do not measure that diagnostic information.

This bounded follow-up is complete. We did not search further until a favorable result appeared, refit after seeing confirmation, or modify observations to produce the expected effect.

## Reproduce and inspect

From the repository root, using the strict study's Python 3.12 environment:

```bash
pip install -r requirements-lock.txt
pip install rdata==1.0.0
python run_context_followup.py
python -m pytest tests/test_context_followup.py
```

The downloader pins immutable source commits and verifies the saved SHA256 manifest on rerun. Raw data stay ignored and are not redistributed. Results: [scores](../results/context_followup/scores.csv), [context diagnostics](../results/context_followup/context.csv), [coverage](../results/context_followup/coverage.json), [SP-Rank audit](../results/context_followup/sprank_audit.csv), [parameters](../results/context_followup/parameters.json), [source hashes](../data/context_followup_sources.json), [validation](../results/context_followup/validation.json). Splits contain anonymous row and metadata-block indices only. NaN in the Python JSON/CSV convention denotes unavailable quantities.

Two focused checks passed: the new cluster diagnostic exactly reduces to the previous report bootstrap when every report is its own cluster, and each cluster is resampled intact. Both checks were also run directly as Python functions; no new estimator implementation was introduced.

## References

1. AgrDataSci **gosset**, [breadwheat documentation](https://agrdatasci.github.io/gosset/reference/breadwheat.html), [source](https://github.com/AgrDataSci/gosset/tree/bb5eb75c08fe3ab0f28931c093dcb66dea7c4185). Source documentation also cites van Etten et al., *Experimental Agriculture*, DOI [10.1017/S0014479716000739](https://doi.org/10.1017/S0014479716000739).
2. van Etten et al. (2019). **Crop variety management for climate adaptation supported by citizen science.** PNAS 116, 4194–4199. [DOI](https://doi.org/10.1073/pnas.1813720116). Package documentation supplies provenance; this experiment uses its 493-record sample.
3. Hunter (2004). **MM algorithms for generalized Bradley–Terry models.** Annals of Statistics 32, 384–406, Section 5, equation (30). [DOI](https://doi.org/10.1214/aos/1079120141). SM algorithms follow the supplied private manuscript; see [the existing algorithm contract](strict_feature_analysis.md#2-exact-estimator-contract).
4. Hosseini, Mandal & Puhan. **SP-Rank: A Dataset for Ranked Preferences with Secondary Information.** [arXiv:2601.05253v1](https://arxiv.org/html/2601.05253v1), [author source at the audited commit](https://github.com/amrit19/SP-Rank-Dataset/tree/d9ceab3386ac04aca7791fd83da8508851f87dc9).
