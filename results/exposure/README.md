# Exposure extension outputs

See ../../docs/exposure_analysis.md for interpretation and the numerical report.
The recovery workflow regenerates:

- small_replicates.csv and small_summary.csv: 1020 datasets; n=8 exact sieve,
  Section 3, exact center MLE and PL.
- coverage_replicates.csv and coverage_summary.csv: 720 datasets; n=64 with
  changing lambda/mu and report length.
- real_replicates.csv, real_summary.csv, real_exposure.csv,
  real_parameters.json: 60 Beans/Sushi B fits and saved split indices.
- tennis_audit.json, tennis_parameters.json, tennis_by_year.csv,
  tennis_summary.csv: catalogs, exclusions, ten chronological seasons,
  seen-player and all-catalog targets.
- tennis_same_order_*.csv, tennis_strength_bins.csv, tennis_calibration.csv:
  exploratory probability-structure and calibration diagnostics.
- real_penalty_sensitivity.csv: fixed PL penalties and the uniform baseline.
- schedule_feasibility.csv: proof-constant budget audit, not measured active
  hierarchy performance.
- validation.json and run/followup manifests: regeneration checks/provenance.

Positive NLL differences favor PL. Synthetic uncertainty uses independent
replicates; real uncertainty conditions on the fitted models. Read the report
for the distinct tournament and year aggregation conventions. The n=64,r=32,N=1
actual cell pools two rounded targets and has 60 replicates per DGP.

The per-match tennis_predictions.csv is regenerated and excluded from Git.
Raw Sushi files and respondent observations are never committed. ATP CSVs are
downloaded separately under Jeff Sackmann's CC BY-NC-SA 4.0 terms.

To reproduce from the repository root:

~~~bash
python -m pip install -r requirements-lock.txt
python -m pytest -q
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python run_exposure.py --part all
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python run_exposure_followup.py
python make_exposure_figures.py
python validate_exposure.py
~~~
