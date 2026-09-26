# Reproduction and verification

Use Python 3.12 and a separate checkout so recorded results are not overwritten accidentally. Numerical dependencies and solver versions are fixed in requirements-lock.txt. The current source is the single active implementation; historical variants require the pinned checkout in [History](history.md).

```bash
python -m pip install -r requirements-lock.txt
python -m pytest -q
python download_strict_data.py
python download_strict_tricot.py
python run_strict_simulations.py --part bridge
python run_strict_simulations.py --part shell
python run_strict_simulations.py --part coverage
python run_strict_real.py
python run_strict_followups.py --part budgets
python run_strict_followups.py --part objective
python run_context_followup.py
python run_baseline_replacement.py
python validate_strict_features.py
python validate_scientific_audit.py
python make_strict_figures.py
```

The strict simulation/real seed is 202609251, wheat seed 202609252, baseline replacement seed 202609253. Dataset, training, diagnostic and estimator randomization streams are fixed separately where specified. All models within a task receive the same reports. Discovery is disjoint from confirmation; neither selects an optimizer after seeing test performance.

Sharp exact sieve blocks above 8 are unavailable. Section 3 accepts only lambda<=1 and every recorded successful fit uses zero hierarchy stages. Exact subset DP is guarded at n<=18; larger centers use the cited integer formulation with a 120-second certificate requirement. Solver timeout returns unavailable, never a heuristic estimate. Certified ties can have different chosen orders on another solver version; compare the objective certificate and disclose prediction changes rather than forcing a match.

Source downloaders reject a changed checksum. No raw ranking files are copied into new repository outputs. Results contain aggregate losses, actual fitted parameters and anonymous split indices. NaN means unavailable; infinity is a divergent loss. A Python JSON NaN is used in some stored historical/current parameter records and must be read with an appropriate parser.

The complete 4,760-dataset simulation is already recorded. Its earlier GitHub recovery replay is not another independent study. The scientific audit refitted 17 real tasks and ran three replacement tasks; all earlier strict fitted parameter values and predictive point values matched. See results/audit/refit_comparison.json and the [audit](scientific_audit.md). Run only the affected experiment when modifying a method or inference rule; do not reinterpret a rerun as independent evidence.

Uncertainty definitions and withdrawal of unidentified-unit intervals are specified once in [algorithms.md](algorithms.md). Reported real intervals are conditional on fixed training fits. The source/metadata search is exploratory; data-dependent discovery is not population-level evidence about how often a model wins.

The GitHub verification workflow has read-only repository permissions. It checks tests and structural consistency; it does not push experiment outputs, change published estimates, or automatically run the full simulation after a documentation edit. Full data checks can be run locally with the commands above.
