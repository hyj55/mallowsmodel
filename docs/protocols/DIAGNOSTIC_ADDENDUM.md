# Same-center sensitivity added after inspecting the diagnostic outputs

The Sushi A within-shell advantage could partly reflect different fitted center
orders. Extend the already implemented same-order sensitivity from run_followups:
fit PL on the original training data subject to the fitted SM ordering, allowing
ties, with the original ridge coefficient. Do not optimize any quantity on test.
Repeat the shell decomposition across all five original fits with the same
2,000 report-bootstrap resamples. This is explicitly a post-diagnostic check,
not part of the frozen initial diagnostic protocol.

This addresses fitted-order disagreement. It does not make the fitted SM center
equal to the unknown true center or remove all model misspecification.
