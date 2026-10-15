# Fit and report provenance

The published empirical repeated-allocation summaries use fixed repetition IDs **0–4**. This is a reporting-budget choice, not a prospective preregistration and not an outcome-selected subset. The current execution specifications, summaries and validators describe this five-allocation design. Independent simulated datasets and bootstrap draws have separate budgets.

Model construction and report generation have separate fingerprints. The three JSON files here record the producer code maps and protocol versions for cached predictive, unpenalized and group fits. Their source commit is immutable. Public manifests record current replay/summary code and the actual code signatures attached to saved predictors. A producer signature is checked against the hash of its complete recorded code map; it is not silently replaced with the current source hash. Retried exact sieves retain an additional producer fingerprint and original failure state.

Reaggregating fixed IDs does not require fitting those same parameters again. Full validation reconstructs memberships and replays their losses against verified source reports. Fresh runs in a clean cache use the current code fingerprint. L1's five-permutation fixed-test control has its own current runner, fitted parameters and [manifest](../regularized_learning/manifest.json).

- [Predictive fit producer](predictive_fit_producer.json)
- [Unpenalized fit producer](repeated_holdout_fit_producer.json)
- [Group fit producer](group_sensitivity_fit_producer.json)

These records are technical provenance, not competing result versions. Reader-facing conclusions and numerical tables use the current reporting design.
