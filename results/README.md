# Current results index

| Directory | Study | Current status |
|---|---|---|
| [repeated_holdout](repeated_holdout/README.md) | 23 original real tasks, 30 new partitions and full refits per task | Current average predictive comparison; retains failures and distinguishes partition precision from population uncertainty |
| [group_sensitivity](group_sensitivity/README.md) | Nine real tasks; trial/person strata, 100 primary splits, equal-budget controls and new-group transfer | Completed; group information helps both models at equal Puzzle training budgets; Sounds personal comparison limited by fit existence and infinite losses |
| [validation_extension](validation_extension/README.md) | Three new real tasks and 1,400 new independent synthetic training datasets | Completed; no clear new primary real winner; center-error and confounding effects plus diagnostic failure retained |
| [strict_features](strict_features/README.md) | 4,760 synthetic training samples, 16 real tasks, frozen follow-ups | Retained; PrefLib intervals withdrawn; method attribution clarified |
| [context_followup](context_followup/README.md) | Wheat fit and six SP-Rank design audits | Point results retained; unidentified-cluster inference withdrawn |
| [baseline_replacement](baseline_replacement/README.md) | Intact Beans/Sushi rerun with original estimators | Completed; all three centers exact/certified |
| [audit](audit/README.md) | Refitting, source integrity, mathematical and structural checks | Evidence for corrections; not independent scientific replications |

The real point results in baseline_replacement, strict_features, context_followup and validation_extension retain their original single partitions. Use repeated_holdout for their updated average predictive estimates; synthetic studies and the separate group_sensitivity study remain distinct. The [learning-curve index](../docs/learning_curves.md) locates the historical Beans/Sushi size experiments and explains their different fitting protocol.

No current result uses the removed historical capped, shrunk or heuristic fitting pipeline. All prior outputs remain at the snapshot linked in [History](../docs/history.md). See [the scientific audit](../docs/scientific_audit.md) before comparing old and new values.
