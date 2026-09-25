# Exploratory exposure follow-up

Added after inspecting the completed local run, 2026-09-25. These are
explanatory sensitivities, not prespecified winner-selection rules.

1. Give tennis SM the exact same order as fitted training PL worths.
Profile beta and select its shrinkage on the chronological inner split,
then refit using the full training PL order. Compare with saved PL on the
same seen-player test matches. This is not Algorithm 2.1/3.1 or SM MLE.
2. Bin absolute training log-worth gaps into [0,.5), [.5,1), [1,1.5), [1.5,infinity).
Compare actual favored-player win frequencies with model probabilities.
Exclude exact fitted ties and count them. Bootstrap tournament-year groups.
Also report ten equal-count reliability bins for main models.
3. On the saved small real training sets, refit PL at fixed penalties 1 and 10,
and add the uniform log(r!) predictor. Compare previously selected shrunk SM
with all comparators; do not choose a main winner retrospectively.

The first local simulation pass reused a seed for truth and estimator tie
breaking. It was discarded and completely rerun with an independent estimator
stream. A no-information regression check guards against this error.
Real-data fits were unaffected. The report and recovery use only corrected
simulation findings.

The workspace disconnected during upload. The restored code is being rerun
in GitHub Actions to recover complete result files. The archival source commit,
seeds, splits, fitted objectives and simulation designs remain the same;
runtime and serialization can differ across environments.
