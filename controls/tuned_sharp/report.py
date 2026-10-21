"""Render one self-contained Markdown report from the completed supplement."""
import argparse
import gzip
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import numpy as np
import pandas as pd

P=ROOT/'results/tuned_block_sieve'
DOC=ROOT/'docs/tuned_block_sieve.md'


def label(record):
    name=record['dataset'].replace('dots2024_','Dots ').replace('_r',' r=').replace('_',' ')
    if record['source_study']=='L0': name+=f" (N={record['N']})"
    if record['source_study']=='S0': name+=f" (n={record['n']})"
    return name


def table(rows,columns):
    out=['| '+' | '.join(title for _,title in columns)+' |',
         '|'+'|'.join('---' for _ in columns)+'|']
    for row in rows:
        values=[]
        for key,_ in columns:
            value=row.get(key)
            values.append('—' if value is None or isinstance(value,float) and not np.isfinite(value)
                          else f'{value:.5f}' if isinstance(value,(float,np.floating)) else str(value))
        out.append('| '+' | '.join(values)+' |')
    return '\n'.join(out)


def artifacts():
    with gzip.open(P/'models.jsonl.gz','rt') as stream: records=[json.loads(line) for line in stream]
    records=sorted(records,key=lambda r:({'P0':0,'L0':1,'S0':2}[r['source_study']],r['dataset'],r['n'],r['N']))
    empirical=[r for r in records if r['source_study']=='P0']
    candidates=pd.read_csv(P/'candidates.csv')
    summary=[];supports=[]; designs=[]; intervals=[]; truth=[]; resources=[]; other=[]
    for r in records:
        fits={s['method']:s for s in r['scores']};comparison={c['reference']:c for c in r['comparisons']}
        own=fits.get('borda_block_sieve',{})
        row=dict(task=label(r),blocks=r['selected_blocks'],variant=own.get('nll'),
            pl=fits['pl']['nll'],likelihood=fits['sm_likelihood']['nll'],
            borda=fits['global_borda']['nll'],pilot=fits['pilot_borda']['nll'],
            delta=own.get('delta_vs_pl'),kind=r['source_study'])
        summary.append(row)
        designs.append(dict(task=label(r),n=r['n'],r=r['r'],
            counts=f"{r['train_count']} / {r['validation_count']} / {r['test_count']}",
            units=r['unit_description']))
        if r['status']=='ok':
            meta=r['models']['borda_block_sieve']['metadata'];b=meta['blocks']
            supports.append(dict(task=label(r),pilot=meta['pilot_reports'],sieve=meta['terminal_reports'],
                blocks=r['selected_blocks'],sizes='/'.join(map(str,[x['m'] for x in b])),
                pairs=f"{min(x['pairs'] for x in b)}–{max(x['pairs'] for x in b)}",
                singletons=sum(x['solver'].get('sieve_size')==1 for x in b),
                empty=sum(x['pairs']==0 for x in b),beta=own['beta']))
        cirow=dict(task=label(r))
        for method,short in [('pl','pl'),('sm_likelihood','likelihood'),('global_borda','borda'),('pilot_borda','pilot')]:
            c=comparison.get(method)
            if c:
                interval='unavailable' if c['ci_low'] is None else f"[{c['ci_low']:.5f}, {c['ci_high']:.5f}]"
                cirow[short]=f"{c['delta']:+.5f}; {interval}"
        intervals.append(cirow)
        if own.get('kendall') is not None:
            truth.append(dict(task=label(r),variant=own['kendall'],likelihood=fits['sm_likelihood']['kendall'],
                borda=fits['global_borda']['kendall'],pilot=fits['pilot_borda']['kendall'],pl=fits['pl']['kendall']))
        resources.append(dict(task=label(r),grid='/'.join(map(str,r['grid'])),
            completed='/'.join(str(c['blocks']) for c in r['candidates'] if c['status']=='ok'),
            failed='/'.join(str(c['blocks']) for c in r['candidates'] if c['status']!='ok') or 'none',
            refits='/'.join(f"{c['blocks']}:{c['status']}" for c in r['refits'])))
        for method in ('sm_fotakis','sm_efficient_fallback'):
            if fits[method]['status']=='ok':
                c=comparison[method]
                other.append(dict(task=label(r),method=method,nll=fits[method]['nll'],delta=c['delta'],
                    interval=f"[{c['ci_low']:.5f}, {c['ci_high']:.5f}]" if c['ci_low'] is not None else 'unavailable'))
    def wins(reference, subset=empirical):
        values=[next(c for c in r['comparisons'] if c['reference']==reference)['delta'] for r in subset]
        return sum(v<0 for v in values),sum(v>0 for v in values),sum(v==0 for v in values)
    counts={ref:wins(ref) for ref in ['pl','sm_likelihood','global_borda','pilot_borda']}
    best=min(empirical,key=lambda r:next(c['delta'] for c in r['comparisons'] if c['reference']=='pl'))
    worst=max(empirical,key=lambda r:next(c['delta'] for c in r['comparisons'] if c['reference']=='pl'))
    plgap=lambda r:next(c['delta'] for c in r['comparisons'] if c['reference']=='pl')
    ci_lower=sum(next(c for c in r['comparisons'] if c['reference']=='pl')['ci_high'] is not None and
        next(c for c in r['comparisons'] if c['reference']=='pl')['ci_high']<0 for r in empirical)
    ci_upper=sum(next(c for c in r['comparisons'] if c['reference']=='pl')['ci_low'] is not None and
        next(c for c in r['comparisons'] if c['reference']=='pl')['ci_low']>0 for r in empirical)
    all_ok=sum(r['status']=='ok' for r in records)
    successes=int(candidates.status.eq('ok').sum())
    by_name={r['case']:r for r in records}
    def gap(case,ref):
        return next(c['delta'] for c in by_name[case]['comparisons'] if c['reference']==ref)
    text=fr'''# Borda-pilot tuned block sieve: a single-allocation supplement

[Study guide](../README.md) · [Original Sharp computation](sieve_computation.md) · [Main Algorithm 4.1 results](../results/main/README.md) · [Protocol](../results/tuned_block_sieve/protocol.json) · [Scores](../results/tuned_block_sieve/scores.csv) · [Validation candidates](../results/tuned_block_sieve/candidates.csv) · [Paired comparisons](../results/tuned_block_sieve/comparisons.csv)

## Question and result

Can a global Borda pilot and validation-selected small blocks produce a usable predictor for the catalogue/budget settings where the literal Sharp estimator could not be computed? The answer here is computationally yes in **{all_ok}/19 settings**. This is a **Borda-pilot block-sieve variant**, not a completion of manuscript Sharp and not the main experiment. The original Sharp's unavailable entries remain unchanged.

Across the twelve empirical full-budget tasks, the variant has lower test NLL than PL in **{counts['pl'][0]}/12**, likelihood-center SM in **{counts['sm_likelihood'][0]}/12**, full-development Borda in **{counts['global_borda'][0]}/12**, and its own pilot-only Borda in **{counts['pilot_borda'][0]}/12**. These are descriptive counts of tasks, not independent votes or a significance test. Zero differences, if any, are not counted as wins. Every comparison uses identical held-out reports within a setting.

The most negative empirical SM-variant-minus-PL gap is **{label(best)}: {plgap(best):+.5f} nats/report**; the most positive is **{label(worst)}: {plgap(worst):+.5f}**. Conditional 95% intervals lie wholly below zero in {ci_lower} empirical tasks and wholly above zero in {ci_upper}; this is exploratory, with no multiplicity correction. Test sets were also used by existing repository experiments, so this is not a fresh confirmatory study.

## Scope, data and the single allocation

The target list is frozen from the active E0/L0/S0 Sharp resource failures at repository commit `80e246692d741eba54b06f380614f3396cb8d9f9`. The 155 unavailable contexts correspond to 19 distinct task/budget/generator cells: 12 empirical tasks × 5 allocations, 3 Sushi B budgets × 5 allocations, and 4 simulated cells × 20 independent draws. This supplement uses **ID 0 once in each cell**, without searching across IDs. Global-sieve B0 aliases are not counted again. The separate P1/P2 implementation-size guards are not new unresolved cells in this resource audit; their unpenalized fitting protocol is not silently replaced.

The data and preprocessing are unchanged. [Wheat](../data/wheat.md) consists of strict three-variety orders reconstructed from best/worst reports; [Sushi B](../data/sushi.md) contains ten-item displayed-set orders; [Dots 2024](../data/dots2024.md) separates arm and report size; [PatrasIQ](../data/patras.md) has separate cost and population tasks. The [S0 design](predictive_learning.md) generates fixed-r=3 rankings under SM or PL. No items, ties, displays or individual ranking orders are modified to improve computational feasibility.

| Component | Allocation used | What is independent |
|---|---|---|
| Empirical E0 cells | Existing ID-0 allocation: 60% of units train, next 20% validation, final 20% test | Sushi respondent; reconstructed dots2024 participant; documented one-report Patras volunteer; Wheat anonymous report |
| L0 Sushi B | Existing ID-0 nested budget N=300/1000/3000: 75% train, 25% validation inside development; same 1,000-person outer test | Respondent rows; budgets share their outer test |
| S0 | Existing simulated draw 0: N=100 development reports, 75 train and 25 validation, 4,000 independently generated test reports | Simulated reports; one draw per generating cell |

No repeated outer shuffle is added. Whole allocation units stay together. Within a dots2024 arm, source allocation is aligned across report sizes. No season/geography stratification is introduced. Wheat's missing assessor identity remains unresolved. For the source unit permutation, the root seed is 202609280, with the existing task key and repetition 0; L0 and S0 retain their original streams. Saved array hashes verify exact agreement with the source records.

{table(designs,[('task','Setting'),('n','n'),('r','r'),('counts','Train / validation / test reports'),('units','Allocation unit')])}

## Estimator definition and references

The starting points are manuscript Algorithm 2.1's pilot/local-sieve structure, equation (3.4)'s clipped normalized Borda score, and Lemma 2.11's permutation sieve. The [reference registry](references.md#supplied-manuscript-m) identifies the supplied manuscript; [the estimator chapter](algorithms.md) and [exact-sieve chapter](sieve_computation.md) give its original construction. This repository defines the following variant; no theorem or published algorithm is claimed for the combined procedure.

1. **Fresh pilot/sieve pools.** For any fitting pool, permute its distinct allocation units with a fixed stream and give the first floor(U/2) units to the pilot, the rest to the sieve. Every report of a unit follows it. This happens inside the training pool during selection, and inside train+validation during final refitting. It is not an additional outer train/test shuffle. Both stages therefore use disjoint reports/known people. Unknown Wheat dependence cannot be removed by this rule.
2. **Global Borda pilot.** On the pilot pool, let K_i count reports containing item i. Sum +1 for every displayed item below i and −1 for every displayed item above i; multiply by (n−1)/((r−1)K_i), and clip to [−n,n]. An unobserved item has score zero. Sort descending, breaking ties with a fixed seeded label priority. This is the full-catalogue form of equation (3.4), not unnormalized total wins.
3. **Tuned actual blocks.** Cut the pilot order into k consecutive blocks whose sizes differ by at most one. Blocks are **disjoint and unpadded**. Candidate k values are the sorted unique set {{2,3,4,ceil(n/10),ceil(n/8)}}. Thus n=100 uses {{2,3,4,10,13}}; n=48 uses {{2,3,4,5,6}}. The extra choices are declared before fitting so large catalogues have genuinely smaller blocks. Ten/eight are grid-design targets, not solver item-count limits: every candidate is attempted and admitted by its actual algorithm/resource requirement.
4. **Exact local pair sieve.** For a block B of m labels, each sieve-pool report containing at least two B items supplies one uniformly selected unordered pair; selection uses displayed labels, never the observed direction. Then retain its reported orientation. A report may contribute once in several blocks. With q retained pairs, use radius floor(m·binom(m,2)/q), form the complete lexicographic greedy Kendall packing, and minimize selected-pair disagreement on it. Enumeration uses canonical source item labels, independently of the Borda order. The existing exact solver handles singleton, full-space and parity cases without changing this definition. q=0 returns the canonical first order. Empty or weakly informed blocks are reported, not silently replaced by Borda.
5. **Assemble and fit dispersion.** Concatenate the fitted block orders in pilot-block order. Sieve cannot reverse cross-block relationships. Fit a single SM dispersion by whole-ranking maximum likelihood on [0,10], using all reports in the current fitting pool. The predictive law remains the displayed-set SM law; the center estimator changes.

The exact local objective and greedy packing are unchanged, but **the Borda pilot, tuned partition geometry, absence of padding and cross-block ordering differ from Algorithm 2.1**. The original W_star formula is not used. In particular, this procedure is not entitled to Sharp's minimax risk bound. It does retain independent pilot/sieve pools where identities permit them, instead of reusing the same reports to choose blocks and fit their local orders.

## Validation, refitting and evaluation

Each candidate is fitted using train only. Its score is the mean negative log likelihood of complete validation reports under their observed displays:

```math
V_k = -\frac{{1}}{{|V|}}\sum_{{t\in V}}\log P_{{\widehat\pi_k,\widehat\beta_k}}(Y_t\mid S_t).
```

Choose the completed candidate with smallest V_k; exact validation ties prefer fewer blocks. Refit that block count from scratch on train+validation, including a new Borda pilot and new local fits. If the refit exceeds the fixed computational budget, attempt the next candidate in validation order; all such attempts are saved. No test loss chooses a candidate or rescues an unavailable fit. The per-call exact-solver budget is 120 seconds and 4 GiB estimated working arrays; incomplete packings are never used. Exact packings are cached by size/radius/budget.

For each final method a, compute the same whole-ranking test loss:

```math
L_a = -\frac{{1}}{{|T|}}\sum_{{t\in T}}\log P_a(Y_t\mid S_t),
\qquad \Delta_{{a,b}}=L_a-L_b.
```

Negative delta favors the variant when it is method a. Different r values have different loss scales; there is no pooled raw-NLL average across tasks.

**Paired existing comparators.** Saved PL, likelihood-center SM, eligible Fotakis, and eligible Efficient models are replayed on the identical ID-0 test data. Their training budget is the same final development pool. PL's positive ridge is selected on the original inner validation set; SM likelihood-center dispersion uses the same [0,10] bound. Exactness certificates remain attached to the likelihood-center fit; an approximate center is not relabeled exact. Existing five-allocation means are context, not substituted for paired ID-0 scores.

**Two Borda controls.** Full-development Borda uses all development reports to estimate its order. Pilot-only Borda uses exactly the half-pool pilot order fed into the selected block procedure. Both fit bounded dispersion on all development reports. Comparison with pilot-only Borda isolates the effect of replacing within-block order by sieve results, including the resulting dispersion refit. Comparison with full-development Borda asks whether the more involved procedure is preferable to spending all available reports on a simple score estimator. These controls are not validation candidates.

## Whole-ranking test results

{table(summary,[('task','Setting'),('blocks','Selected k'),('variant','Variant NLL'),('pl','PL NLL'),('likelihood','Likelihood SM NLL'),('borda','Full Borda NLL'),('pilot','Pilot Borda NLL'),('delta','Variant − PL')])}

All twelve empirical full-budget likelihood centers in this particular ID-0 comparison are certified exact. The three smaller-budget Sushi B likelihood centers are approximate and retain their source optimization gaps; the four S0 centers are exact. These statuses concern the comparator, not the exactness of the variant's local sieve.

The additional existing estimator comparisons below are included wherever their original admission rules allowed a fit. A missing Fotakis or Efficient fit is not replaced by an invented result. Full Borda and an existing depth-zero Efficient fit can differ in tied scores because they retain different declared tie priorities.

{table(other,[('task','Setting'),('method','Saved comparator'),('nll','Comparator NLL'),('delta','Variant − comparator'),('interval','Conditional 95% interval')])}

![Paired test NLL differences](../figures/tuned_block_sieve/comparisons.png)

The figure shows paired differences and, where supported, conditional 95% test-unit bootstrap intervals. A point without an interval is not a zero-width CI. These are the single saved allocation/draw results, not means over multiple shuffles.

## Exact-solver availability and information retained

{successes}/{len(candidates)} training-stage candidates completed. Unavailable candidates are excluded by validation-stage feasibility, never by test performance. A completed variant does not certify that the original global sieve could be computed.

{table(resources,[('task','Setting'),('grid','Candidate k'),('completed','Completed on train'),('failed','Unavailable on train'),('refits','Refit attempts')])}

For the selected final fit, the following table distinguishes catalogue block size from statistical support. A singleton sieve can arise even with observed pairs when its radius covers the entire permutation space. It is computationally exact but supplies no choice among competing local orders. Because enumeration uses source labels, its first order need not preserve the pilot order. Splitting more finely reduces computation but also reduces within-block pair support and fixes more cross-block decisions.

{table(supports,[('task','Setting'),('pilot','Pilot reports'),('sieve','Sieve reports'),('sizes','Block sizes'),('pairs','Retained pairs/block'),('singletons','Singleton sieves'),('empty','Blocks with zero pairs'),('beta','Final beta')])}

**Label-order effect.** Dots A r=2 has q=(10,10,9) in three ten-item blocks, so all three sieves contain only their canonical first order. Dots source labels are increasing dot counts, also the objective reference order. Its within-block refinement therefore benefits from this label/reference alignment without learning the local orientation from the retained outcomes. The resulting objective Kendall distance drops from 110 for its pilot to 53, while test NLL rises from 0.56354 to 0.65118. This is a concrete reason not to interpret the smaller reference-order error as evidence that sieve learned more accurately. No labels were changed for this supplement: the exact source-label enumeration was preserved and its finite-sample effect is disclosed. In the PL-generated n=32 cell all four blocks are likewise singleton sieves, but the generating worth order was independently randomized and has no analogous canonical-label alignment.

## Interpretation by dataset family

**Dots 2024.** The variant is below PL for A r=2, A r=3, A r=6 and B r=2, but all four paired intervals include zero. B r=5 has a positive gap of {gap('E0-dots2024_B_r5-n30-N240','pl'):+.5f} with interval [0.02088, 0.36205], favoring PL conditional on this split. Only A r=6 and B r=2 beat full-development Borda. B r=3 improves on pilot-only Borda by {gap('E0-dots2024_B_r3-n30-N240','pilot_borda'):+.5f}, with interval [−0.15334, −0.00253], but still loses to full-development Borda. Thus local refinement can help a half-data pilot without improving on a simple estimator using the entire training budget. The r=2 singleton/label effect above further limits an estimator-learning interpretation.

**PatrasIQ.** Cost strongly favors PL in this allocation: variant-minus-PL is {gap('E0-patras_cost-n36-N313','pl'):+.5f}, interval [0.29255, 0.72452]. The variant also loses to the likelihood-center SM and both Borda controls on cost. Population reverses the point comparison with PL ({gap('E0-patras_population-n48-N313','pl'):+.5f}), but its interval [−0.48484, 0.09642] includes zero and full-development Borda is still lower. The two tasks therefore do not establish one common family-wide advantage for this variant.

**Wheat.** Selected k=4 gives four four-item blocks, each with a full 24-order sieve (integer radius zero). The local empirical objectives are exactly minimized over every local permutation, yet its test NLL 1.59426 is higher than PL 1.45400, likelihood-center SM 1.56653, full Borda 1.56805, pilot Borda 1.57468 and eligible Fotakis 1.55694. Here solver incompleteness cannot explain the result; data division, sampled-pair objectives and frozen cross-block order are possible causes. One split does not identify which cause dominates, and unknown farmer dependence prevents a justified person-level CI.

**Sushi B.** The full-budget fit selects 13 blocks of seven/eight items. Its NLL 14.28603 is slightly higher than PL 14.26039 and full Borda 14.27745; both paired intervals include zero. At N=300/1000/3000 the selected counts are 10/10/13. Every budget has higher variant NLL than PL and full Borda. At N=300 both differences have positive conditional intervals; the larger-budget differences do not. Pair support is highly uneven even at N=4000: selected blocks retain between 8 and 1,043 pairs. Small blocks make fitting possible without guaranteeing adequate information for every part of the order. These NLLs decrease as the budget grows in this one allocation, but that is not a replicated learning-curve conclusion.

**Simulations.** Under PL generation the variant loses to PL in both n=16 and n=32 draws, as might be expected, although model correctness alone does not force a finite-sample loss ordering. Under SM generation it beats PL for n=16 (delta −0.01874) and loses for n=32 (+0.04726). The n=32 failure despite SM generation illustrates estimation error and weak local support rather than disproving the generating law. Full-development Borda is lower than the variant in all four cells. None of these four draw-0 observations estimates a minimax rate or an average over training datasets.

## Uncertainty: what the intervals do and do not mean

For an identified test unit u, let c_u be its report count and D_u the sum of paired per-report NLL differences. Each of 2,000 bootstrap samples draws U unit IDs with replacement and computes

```math
\Delta^* = \frac{{\sum_{{j=1}}^U D_{{u_j^*}}}}{{\sum_{{j=1}}^U c_{{u_j^*}}}}.
```

The interval endpoints are empirical 2.5% and 97.5% quantiles. The same sampled units are used for both models, preserving pairing. This approximates test-sample uncertainty under exchangeable independent units, conditional on the fitted models and selected k. It does not include training uncertainty, hyperparameter-selection variability or variation between splits. The denominator preserves a report-weighted target when unit sizes differ. For S0 the unit is an independent generated test report; this CI still conditions on a single training draw.

No CI is supplied for Wheat because anonymous report rows do not establish independent farmers. This supplement has only one outer split/draw per setting, so it reports **no partition MCSE**, no between-training-draw risk CI, and no averaged-split population CI. Unadjusted intervals across many correlated tasks/comparators are descriptive.

Each cell below gives delta followed by its conditional 95% interval. Negative favors the variant.

{table(intervals,[('task','Setting'),('pl','Against PL'),('likelihood','Against likelihood SM'),('borda','Against full Borda'),('pilot','Against pilot-only Borda')])}

## Reference-order errors where an order is available

Kendall distance counts discordant unordered item pairs. Dots and Patras reference orders are objective task-category orders; they do not prove that the subjective/reporting population has that SM center. S0 SM has a known generating center. S0 PL's generating worth order is a ranking reference, not an SM true center. Wheat/Sushi have no supplied true order and are omitted here.

{table(truth,[('task','Setting'),('variant','Variant Kendall'),('likelihood','Likelihood SM Kendall'),('borda','Full Borda Kendall'),('pilot','Pilot Borda Kendall'),('pl','PL worth-order Kendall')])}

## Interpretation and limits

- **Computational recovery and predictive improvement are different.** All reported local fits use the exact sieve for their declared blocks. Whether their assembled center predicts better is answered by the held-out table, not by completion status. The twelve empirical tasks favor the variant over full Borda in {counts['global_borda'][0]} cases and favor full Borda in {counts['global_borda'][1]}; therefore merely making sieve computation feasible does not establish an across-task improvement.
- **Pilot errors can be locked in.** With disjoint blocks, a wrongly placed item cannot cross a boundary. Smaller blocks trade optimization freedom for computational tractability. The pilot-only comparison separates this limitation from errors introduced by sparse local sieve fitting.
- **Sparse local pairs matter.** Only terminal-pool reports containing at least two items from a block contribute to its center objective. This can leave very little local information even when the overall dataset is large. The support table exposes this cost rather than interpreting every computed block as well estimated.
- **Model-family conclusions remain separate.** Likelihood-center SM and the variant share the same SM probability law but differ in center estimation. A variant-versus-PL loss difference combines model mismatch and estimation error. Disagreement with likelihood-center SM is evidence about the fitting procedure, not a new SM-versus-PL law.
- **Learning-budget and synthetic rows are limited comparisons.** Sushi B uses nested budgets and a shared test set; one allocation cannot establish a smooth learning curve. The four S0 rows are paired illustrations from draw 0; the existing twenty-draw S0 summaries remain the source for simulation-average conclusions. No single simulated training sample is presented as a minimax-risk test.
- **The test data are reused research data.** The new grid, sample pools and tie rules were fixed before these new test scores were computed, but the datasets/test sets already appear in the repository. A strong confirmatory claim would require an additional untouched evaluation source.

## Reproduction and files

Run `python controls/tuned_sharp/run.py` after restoring the documented source data. The runner verifies source arrays against existing predictor hashes before fitting and saves private split/unit/loss details locally. It does not modify any existing model or result table. The fixed protocol is saved separately from the results.

Run `python controls/tuned_sharp/validate.py` for public-artifact, selection and comparator checks; add `--replay` to reconstruct source data and verify every saved validation/test score, sampled-pair objective and bootstrap interval. Run `python controls/tuned_sharp/report.py` to regenerate this report and figure. The tests in `tests/test_tuned_block_sieve.py` independently check whole-unit separation, orientation-blind pair extraction, exact local objectives, boundary preservation and test-independent selection.

Public files under `results/tuned_block_sieve/` contain all candidate statuses, final scores, paired contrasts, fitted models, source/code hashes and the protocol. Per-person reports and allocations remain in the ignored private cache. The [main P0 analysis](../results/main/README.md), [E0 comparisons](../results/estimator_comparison/README.md) and [L0/S0 curves](predictive_learning.md) retain their original meanings and results.
'''
    return text,records


def figure(records):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,3,figsize=(14,9),sharey=True)
    for ax,ref,title in zip(axes,['pl','sm_likelihood','global_borda'],['vs PL','vs likelihood-center SM','vs full-development Borda']):
        for i,r in enumerate(records):
            c=next((c for c in r['comparisons'] if c['reference']==ref),None)
            if c is None: continue
            color={'P0':'#146b8c','L0':'#ba6418','S0':'#7761a8'}[r['source_study']]
            ax.plot(c['delta'],i,'o',color=color,ms=4)
            if c['ci_low'] is not None:
                ax.hlines(i,c['ci_low'],c['ci_high'],color=color,alpha=.8)
        ax.axvline(0,color='#777777',lw=.8)
        ax.grid(axis='x',alpha=.15);ax.set_title(title);ax.set_xlabel('Variant minus comparator NLL (nats/report)')
        for boundary in (11.5,14.5):ax.axhline(boundary,color='#cccccc',lw=.8)
    axes[0].set_yticks(range(len(records)),[label(r) for r in records],fontsize=8)
    axes[0].invert_yaxis()
    fig.suptitle('Borda-pilot block sieve: one allocation/draw per setting\nNegative favors variant; intervals condition on fitted models',fontsize=12)
    fig.tight_layout()
    out=ROOT/'figures/tuned_block_sieve';out.mkdir(parents=True,exist_ok=True)
    fig.savefig(out/'comparisons.png',dpi=170)
    fig.savefig(out/'comparisons.pdf')
    plt.close(fig)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    text,records=artifacts()
    if args.check:
        assert DOC.read_text()==text
        print('PASS generated report matches saved results')
    else:
        DOC.write_text(text);figure(records);print('WROTE',DOC)


if __name__=='__main__':main()
