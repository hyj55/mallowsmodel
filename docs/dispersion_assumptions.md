# Fitted dispersion, algorithm bounds and calibrated constants

[Estimator comparison](estimator_comparison.md) · [NLL and report Kendall results](../results/heldout_kendall/README.md) · [Audit summary](../results/heldout_kendall/beta_summary.csv) · [Every audited score](../results/heldout_kendall/beta_audit.csv.gz)

Three quantities have different roles:

| Quantity | Meaning | What the audit can establish |
|---|---|---|
| beta_true | Dispersion of a correctly specified generating SM law | Known in pure-SM simulations; usually unknown and potentially nonexistent as one common parameter in real data or mixtures |
| beta0 | Positive lower bound supplied to the center algorithm's construction | The theorem assumes beta_true >= beta0, in addition to its other design and parameter conditions |
| beta_hat | Dispersion fitted around the particular estimated center for probability prediction | May fall below beta0, even when the true simulation dispersion satisfies the bound |

The saved predictors do not feed beta_hat back into Sharp/Efficient's center construction. E0 uses beta0=0.1, estimates each center on development data, then profiles dispersion on the same development data over [0,10]. Methods with different centers may obtain different beta_hat values. Each fitted value is then held fixed for test scoring. Test data never determine beta or beta0.

## Why beta below beta0 needs to be reported

A prediction using beta_hat < beta0 is outside the dispersion subfamily described by that supplied lower bound. It must not be described as a fitted predictor constrained to beta >= beta0. The audit explicitly flags that case. It does **not** convert the flag into proof that beta_true < beta0: sampling error, center error, and misspecification can all lower the fitted dispersion. Nor does beta_hat >= beta0 verify the theorem's other assumptions.

For a fixed estimated center, manuscript M's Proposition 4.2, equation (4.5), pp. 33–34 defines the dispersion profile; it does not require that the supplied center was obtained by Kemeny MLE. This makes the predictive calibration a well-defined optimization for any center. It does not give a non-MLE center the joint-MLE label, or extend its center-risk theorem to an estimated-dispersion predictor. See the [versioned manuscript reference](references.md#supplied-manuscript-m).

In E0, **1 of 55 completed Sharp fits** has beta_hat below 0.1: Beans, allocation 0, development N=673, beta_hat=0.072187008020347. None of the **10 completed Efficient fits** does. Unavailable fits have no beta estimate and do not count as passed checks. B0's matching Sharp/global-sieve entry is an alias, not an independent violation. P1 discovery and confirmation reuse the same fitted beta, so their repeated audit rows are also not independent fits.

The audit covers the other predictive studies as well. For example, L0 has 9 below-bound Sharp fits among 45 completed fits. Calibration/shrinkage controls retain their actual prediction beta; a separate shrinkage rule can also move it below the center algorithm's input. These counts describe recorded predictors, not significance tests or estimates of the probability that a theorem assumption is false.

## What tuning constants does and does not imply

The explicit construction implemented from M's proof uses

```math
\rho=\tanh(\beta_0/2),\qquad
c_*=2+2048/\beta_0^2,\qquad
t_*=\min\{1/8,\beta_0/64\},
```

```math
b_0=\min\{1/(8c_*),t_*/8\},\qquad
K=\max\{8,4/(b_0\rho^2)\},\qquad C_T=12/\rho.
```

The same construction fixes A=256, the width multiplier at 1, and the terminal multiplier at 8. Those three constants are not functions that can be inverted to recover beta0. See [the constant implementation](../src/manuscript_estimators.py) and [S4's explicit modifications](../experiments/section44/README.md).

Because b0 <= 1/64 and rho < 1 for every finite positive beta0, this map gives **K > 256**, with limiting infimum 256. Therefore, independently selecting K=0.003, 0.01, 0.1 or 1 cannot be represented as merely choosing another beta0 under this map. Changing A or either multiplier likewise prevents exact agreement with this particular map. The audit calls this `no_common_proof_inverse`. It does not claim that a different proof could never justify smaller constants.

S4-T supplies beta0 to each construction, varies declared constants, chooses candidates by validation NLL, and evaluates the locked choice on independent test reports. Its calibrated variants retain that supplied beta0 as an input; their tuned constants do not establish a new theoretically certified lower bound. `supplied_input_not_inferred` means precisely that no beta0 has been inferred from the constants; it is not a proof-admission verdict. Known pure-SM beta_true is checked separately in the machine table. Mixture controls and real data do not receive an invented true beta.

## Evaluation policy

Original centers, fitted dispersions, candidate choices, and NLLs are retained alongside the new report-level Kendall distance and audit flags. No failed or below-bound fit is removed to improve a mean. No test outcome selects constants or revises beta0. These tables evaluate the recorded procedures; they do not claim that the calibrated constructions inherit the proof's guarantees.

An alternative predictive procedure can explicitly profile beta over [beta0,10] when beta0 <= 10. For the same fixed-center convex profile, this clips an existing [0,10] optimum up to beta0. That changes NLL but leaves report Kendall distance unchanged. In a validation-selected study it would also require rescoring **all validation candidates**, locking the resulting choices, and evaluating those choices independently; clipping only the reported test predictor does not constitute retuning. The present audit does not silently replace the original selection by that different procedure.
