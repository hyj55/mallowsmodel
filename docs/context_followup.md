# Observation design and context identifiability

[Experiment map](experiments.md) · [Context criterion](criteria.md#context-slope) · [Data catalogue](../data/README.md) · [Calibration](validation_extension.md)

A ranking dataset may be suitable for predictive comparison without identifying a changing-display mechanism. The context diagnostic needs the **same pair** observed at different gaps in a fixed reference order, with enough observations at each gap. More reports, larger average item coverage, or several nominal display sizes do not automatically provide this contrast.

## What the data can identify

| Observation design | Predictive comparison | Changing-gap diagnostic |
|---|---|---|
| Complete fixed display, such as Sushi A or a four-category PrefLib task | Whole-ranking probabilities can be compared | No within-pair display-gap variation |
| Varying assigned subsets, such as Sushi B or PatrasIQ | Conditional probabilities can be compared on the observed display distribution | Possible, subject to repeated-pair overlap and the chosen reference |
| One pair per report, such as Sounds or ATP | Direct pair prediction | Displayed gap is always one; no such context contrast |
| Top-k responses from a larger display | Requires a censored likelihood | Cannot replace the original display by the recorded top-k items |
| Pair seen at different gaps by different participant mixtures | Pooled prediction remains a defined target | A slope may reflect mixture changes rather than a homogeneous SM mechanism |

The model input is only the ordering and displayed set. Metadata can still be essential for identifying dependence, defining a split or explaining a diagnostic. The [D2 control](validation_extension.md) gives an exact heterogeneous-PL counterexample with a nonzero pooled context effect.

## Wheat: predictive data with limited inferential metadata

[Wheat](../data/wheat.md) has 493 intact triples over 16 varieties and 418 distinct displays. P2 uses 295 training, 99 discovery and 99 confirmation reports. Exact-center SM has confirmation NLL 1.5801, PL 1.4794 and clipped-Borda SM 1.4847. These are descriptive point comparisons; [P1](repeated_holdout.md) also averages 30 complete refits.

The fitted-center context calculation has the following support:

| Held-out sample | Eligible pairs | Pair occurrences | Observed slope | SM predicted slope | PL predicted slope |
|---|---:|---:|---:|---:|---:|
| Discovery | 8 | 39 | −.1043 | .1109 | 0 |
| Confirmation | 6 | 30 | +.0874 | .1109 | 0 |

The signs differ and support is sparse. Participant names are redacted and 113 village labels are missing. Missing villages are not assigned one artificial inferential cluster. Neither a village-adjusted estimate nor a sampling-unit-justified CI is available. Closeness of one slope point estimate to SM's prediction does not establish an SM mechanism.

## SP-Rank: many reports but no targeted objective-gap contrast

The [source audit](../data/screening.md#sp-rank) uses actual complete first-order Rank treatments 4/5/6, separately by domain and the two study cohorts. It retains 1,200 four-item reports per domain and 576 five-item reports per domain: 5,328 total. Top choices, approvals and meta-predictions are not converted into full rankings.

Each of the three four-item tasks has 20 distinct displays and each five-item task has 12. In every audited task, each observed pair has a constant gap in the **objective** reference order. There are zero pairs with the changing objective-gap contrast. No SM or PL fits are made for this screen. This does not exclude other uses of SP-Rank or prove absence of variation around every possible fitted center.

## Trial identity and physical identity

[Puzzle/Dots trial recovery](../data/dots_puzzle.md) restores which reports concerned the same four-stimulus set. It does not recover individual puzzle layouts, globally unique board IDs or worker identities across trials. Pooled category labels and local physical sets therefore define different prediction tasks. [G1](group_sensitivity.md) quantifies that difference with matched training budgets; it does not equate solution-step count with a universal latent human difficulty.

Source and observation checks are recorded in [A1 outputs](../results/context_followup/README.md). Their scope is eligibility and identifiability, not a search-unadjusted claim about how often either model wins.
