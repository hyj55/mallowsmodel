"""Reader-facing E0 comparison generated from the six-method score table."""
import numpy as np
import pandas as pd
from .estimator_comparison import METHODS, borda_comparisons


LABELS = dict(pl='PL', sm_likelihood='Likelihood SM', sm_sharp='Sharp',
              sm_fotakis='Fotakis', sm_efficient='Efficient', sm_global_borda='Global Borda')


def report(summary, scores, table, task_label):
    datasets = sorted(summary.dataset.unique())
    wide = pd.DataFrame({'dataset':datasets})
    wide['task'] = wide.dataset.map(task_label)
    for method in METHODS:
        g = summary[summary.method == method].set_index('dataset')
        wide[method] = wide.dataset.map(g.nll_mean)
    contrasts = borda_comparisons(scores)
    paired = pd.DataFrame({'dataset':datasets})
    paired['task'] = paired.dataset.map(task_label)
    counts = []
    for method in METHODS[:-1]:
        g = contrasts[contrasts.reference == method].set_index('dataset')
        paired[method] = [f'{g.loc[d,"delta_mean"]:+.5f} ({g.loc[d,"delta_mcse"]:.5f})'
                          if g.loc[d,'available'] == 5 else f'NA ({int(g.loc[d,"available"])}/5)'
                          for d in datasets]
        complete = g[g.available == 5]
        counts.append(dict(reference=LABELS[method], complete=len(complete),
            lower=int((complete.delta_mean < -1e-12).sum()),
            equal=int((complete.delta_mean.abs() <= 1e-12).sum()),
            higher=int((complete.delta_mean > 1e-12).sum())))
    admission = []
    for dataset in datasets:
        g = scores[scores.dataset == dataset]
        e = g[g.method == 'sm_efficient']
        row = dict(task=task_label(dataset), lambda_=float(e.lambda_.iloc[0]),
            efficient=f'{int(e.status.eq("ok").sum())}/5',
            depth='0 in 5/5' if e.status.eq('ok').all() and e.depth.eq(0).all()
                  else 'not applicable' if not e.status.eq('ok').any()
                  else ', '.join(map(str,sorted(e.depth.dropna().unique()))),
            borda='5/5', sharp=f'{int(g[g.method == "sm_sharp"].status.eq("ok").sum())}/5',
            fotakis=f'{int(g[g.method == "sm_fotakis"].status.eq("ok").sum())}/5')
        admission.append(row)
    b = summary[summary.method == 'sm_global_borda'].set_index('dataset')
    c = contrasts.set_index(['dataset','reference'])
    def difference(dataset, reference):
        row=c.loc[(dataset,reference)]
        return f'{row.delta_mean:+.5f} (MCSE {row.delta_mcse:.5f})'
    text='''# E0: supplementary center-estimator comparison

[Design and formulas](../../docs/estimator_comparison.md) · [All-method summary](summary.csv) · [Per-partition scores](repeat_scores.csv.gz) · [Borda paired contrasts](borda_comparisons.csv) · [Fitted parameters](predictors.jsonl.gz) · [P0 main results](../main/README.md) · [B0 global sieve](../global_sieve/README.md)

E0 compares Sharp, Fotakis, independently admitted Efficient and global clipped Borda on the same 23 tasks and five development/test allocations. PL and likelihood-center SM are the saved P0 references, included in the same tables. This is one supplementary estimator comparison; no test-selected E0 estimator replaces P0's likelihood center.

## Complete comparison

The table gives whole-ranking test NLL, averaged equally across five allocations; lower is better. All SM centers use the same development-data dispersion fit on [0,10]. A full mean requires all five planned fits. NA is an unavailable full comparison, not zero loss or a mean over the successful subset. The availability table below gives every denominator; conditional subset means remain explicitly labeled in the CSV.

'''
    text += table(wide,[('task','Task')]+[(m,LABELS[m]+' NLL') for m in METHODS])+'\n\n'
    text += '''## Global Borda against every other method

Each cell is **mean(Borda NLL − comparator NLL), with paired partition MCSE in parentheses**. Negative favors Borda. Compute each difference within the same allocation first, then average those five differences; the MCSE is their sample standard deviation divided by sqrt(5). It is not obtained by treating the two methods as independent. It is not a population confidence interval. Full differences and MCSEs require 5/5 paired fits.

'''
    text += table(paired,[('task','Task')]+[(m,'Borda − '+LABELS[m]) for m in METHODS[:-1]])+'\n\n'
    text += 'Descriptive task counts use a 1e-12 nats/report equality tolerance. Tasks share sources and people; these are not independent votes or significance tests.\n\n'
    text += table(pd.DataFrame(counts),[('reference','Comparator'),('complete','Complete task comparisons'),
        ('lower','Borda lower'),('equal','Equal'),('higher','Borda higher')])+'\n\n'
    text += f'''## Interpretation

- Against PL, Borda's five-allocation mean is lower in {int((b.delta_mean < -1e-12).sum())}/23 tasks. This does not identify a universally preferred model family or establish significant winners.
- Against likelihood-center SM, Borda is lower in 11 tasks, equal in eight and higher in four. Likelihood optimization minimizes training disagreement; it need not minimize held-out loss. For example, Dots 2024 B r2 has Borda-minus-likelihood {difference('dots2024_B_r2','sm_likelihood')}, whereas Wheat has {difference('wheat','sm_likelihood')}. P0's three uncertified Sushi B centers retain their original status.
- Among the eleven tasks with complete Sharp fits, Borda is lower in four and equal in seven. This comparison says nothing about Borda versus the twelve unavailable full-catalogue Sharp fits. B0 aliases those Sharp results where their constructions coincide.
- Fotakis has complete five-allocation comparisons on thirteen tasks: Borda is lower in two, equal in eight and higher in three. Partial Fotakis availability on two further tasks is retained without converting it into a five-fit mean.
- Efficient and Borda coincide exactly in both admitted tasks. There is no observed positive-depth hierarchy in E0, so these data do not measure an active hierarchy's advantage over Borda.
- The source objective order is never used to fit these centers. For preference data, no true preference center is observed; the comparison is predictive NLL, not true-center recovery risk.

## Efficient admission, depth and estimator availability

Efficient is assessed independently of Sharp on every allocation. Equation (3.23)'s schedule requires lambda = N r(r−1)/(n(n−1)) <= 1. Only Dots 2024 A/B r2 meet that requirement (10 fits); the other 105 allocations are explicitly outside its domain. Their missing depth is **not** depth zero. Global Borda is fitted on all 115 allocations, including those outside Efficient's schedule domain.

For admitted tasks, eta<=lambda<=1 and n<=100 imply eta*n<=100<256=A. Thus the schedule has zero hierarchy stages and the root is the terminal block. All development reports still score-sort that full catalogue. With the same tie seed 93847, Efficient and Borda have identical order, training distance, fitted beta, every test-report loss and bootstrap endpoints. Both names remain visible for comparison, with alias_of=sm_global_borda on Efficient; they are not independent estimator evidence. If a future admitted configuration has positive depth, its separate Borda fit remains in this same E0 table.

'''
    text += table(pd.DataFrame(admission),[('task','Task'),('lambda_','Development lambda'),
        ('sharp','Sharp'),('fotakis','Fotakis'),('efficient','Efficient'),
        ('depth','Efficient depth'),('borda','Global Borda')])+'\n\n'
    text += '''## Uncertainty, data reuse and scope

The summary saves each estimator's paired delta against PL and its MCSE, plus all five split scores. Within each eligible split, 2,000 paired bootstrap draws resample identified test units while every predictor stays fixed. The same bootstrap draws are used across methods. The 2.5th and 97.5th percentiles are conditional test-sampling intervals; they omit training/tuning uncertainty and are not averaged into a CI for the five-split mean. Beans, Wheat and the anonymous PrefLib tasks have no supported sampling interval. The Borda-versus-method table above uses paired partition MCSE, not a bootstrap CI.

Random allocations, data preprocessing and existing PL/likelihood/Sharp/Fotakis parameters are reused exactly. Global Borda and Efficient use complete development reports and a common fixed tie rule, with no extra validation selection. The global Borda baseline is exposure-normalized clipped scoring, not an unnormalized sum of wins. The [design](../../docs/estimator_comparison.md) gives its formula and references.

Sharp has 60 unavailable E0 fits; the further 15 L0 and 80 S0 contexts give 155 unavailable supplementary fits. These are not missing P0 main results. Numerical admission and completion do not establish uniform displays, independent reports or a true SM law. The [sieve report](../../docs/sieve_computation.md) records those limits.

## Files and reproduction

| File | Contents |
|---|---|
| summary.csv | All six methods on 23 tasks; 138 rows, availability, mean NLL/delta, MCSE and explicitly conditional means |
| repeat_scores.csv.gz | 690 rows: six methods × 23 tasks × five unchanged allocations; depth, status, alias and conditional intervals |
| borda_comparisons.csv | Borda-minus-comparator paired differences, complete/conditional denominators, MCSE and split ranges |
| predictors.jsonl.gz | All six method records per allocation, source hashes, tie rules and Efficient depth/domain metadata |
| manifest.json | Fitting/scoring code, input and output hashes; the report manifest separately verifies generated summaries |

Run `python run_estimator_comparison.py` after acquiring the shared sources to fit the score candidates and replay saved references. Run `python build_study_reports.py` to rebuild E0's tables without fitting. Public verification is `python validate_estimator_comparison.py`; `--sources` additionally reconstructs all 115 partitions, the score estimators, test predictions and conditional bootstrap endpoints. `python build_study_reports.py --check` verifies the generated report. No separate experiment or new split is introduced.
'''
    return text, contrasts
