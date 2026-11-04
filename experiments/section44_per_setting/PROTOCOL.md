# S4-T: per-setting constant selection

This additional experiment preserves S4 and tests whether choosing constants separately for each `(n,r,N)` improves on global Borda. It reuses the unchanged S4 candidate definitions and center algorithms. It does not implement the proposed adaptive-resolution algorithm.

The scope is all 90 eligible partial-ranking signal settings from S4, forming 82 distinct `(n,r,N)` groups. Each group receives one fixed configuration per estimator family, shared by all repetitions and by all signal/lower-bound controls with that same group key. There is no per-test-draw or per-signal choice.

## Training, validation and test separation

`N` remains the number of training reports, so training information matches the original S4 coordinate. Independently generated validation and test sets each have `ceil(N/3)` reports, at least one. For a common center this corresponds to approximately 60/20/20 information roles; rounding for tiny N is explicit, and N is not the combined sample size.

Selection uses 20 independent training/validation draws per signal setting. Each candidate estimates its center from training only, then profiles beta on `[0,10]` on those same training reports. Validation mean whole-ranking NLL chooses the candidate. Centers are random in each draw; each validation set shares its training set's true center and signal, but has independently sampled displays and rankings.

After the choices are locked, 100 completely fresh training/test draws per signal setting evaluate them. Each test set shares the generating center with its own fresh training set. No test reports or true-center errors enter selection. There is no refit on train plus validation: the center's fitting budget stays N. Additional independent draws for selection are part of the simulation design, so this is a group-level calibration procedure, not a tuning recipe based on only one observed dataset.

## Selection and comparators

Use the original 25 Efficient and 35 Sharp candidate configurations. Rank eligible candidates by mean validation NLL, giving each signal setting within a group equal weight; exact ties use candidate name. A candidate is eligible only if every planned calibration fit completes. Unlike S4's active-hierarchy search, zero-depth configurations and the original algorithm's explicitly recorded Borda fallback are allowed. No minimum positive-depth fraction is imposed. A resource failure is not converted to Borda.

Compare per-setting choices with full-training global Borda, the proof configurations, and S4's already locked configurations, all on the same new training/test draws and estimator tie seeds. The old S4 tables remain distinct because their selection target was known-center risk and their eligibility rule required activity; the new primary selection target is validation NLL.

## Outcomes and uncertainty

Report held-out whole-ranking NLL and Kendall distance to the known center separately. Better prediction does not necessarily mean smaller center error. Save fitted beta, depth, branch, candidate identity and availability. Also report NLL differences divided by `log(r!)` and Kendall distances divided by `n(n-1)/2`.

Compute mean paired differences across 100 independent confirmation draws, MCSE and approximate pointwise 95% Student-t intervals. Apply Holm correction separately for each outcome and per-setting family across complete comparisons with Borda. These intervals condition on the selected constants. Do not treat reports/pairs within a draw as independent repetitions or treat descriptive configuration counts as independent votes. If any confirmation fit fails, its full-setting result is unavailable; successful-subset means cannot replace it.

## Computation and preservation

Keep S4's 512 MiB per exact-sieve admission, 30-second packing limit and 120-second terminal-sieve limit. Use three processes, one numerical-library thread each. Identical computational plans may reuse the exact same fit within a draw, with the equivalence recorded; failed packings retain their resource receipts. All random streams, data hashes, fitted orders and selection receipts are saved or reproducibly regenerated. Original S4 code, reports, results and figures are not edited.

The root seed is 202611040. The design is recorded before outcome generation. Definitions are in `design.py` and the machine-readable protocol.
