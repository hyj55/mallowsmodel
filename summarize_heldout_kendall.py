"""Unified NLL / held-out Kendall views and dispersion-assumption diagnostics."""
import argparse
import gzip
import hashlib
import json
import math
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results/heldout_kendall'
SECTIONS={}


def fmt(x):
    if isinstance(x,(float,np.floating)):
        return 'NA' if np.isnan(x) else '∞' if np.isposinf(x) else f'{x:.6g}'
    return str(x)


def table(frame,cols):
    lines=['| '+' | '.join(label for _,label in cols)+' |','|'+'|'.join('---' for _ in cols)+'|']
    for _,row in frame.iterrows():lines.append('| '+' | '.join(fmt(row[k]) for k,_ in cols)+' |')
    return '\n'.join(lines)+'\n'


def integrate(path,body):
    p=ROOT/path
    text=p.read_text();start='<!-- heldout-kendall:start -->';end='<!-- heldout-kendall:end -->'
    block=start+'\n'+body.rstrip()+'\n'+end
    SECTIONS[str(path)]=block+'\n'
    if start in text:
        a=text.index(start);b=text.index(end,a)+len(end);text=text[:a]+block+text[b:]
    else:text=text.rstrip()+'\n\n'+block+'\n'
    p.write_text(text)


def main(do_integrate=False):
    sources=sorted(OUT.glob('*_fits.csv.gz'))
    full=pd.concat([pd.read_csv(p,low_memory=False).assign(score_file=p.name) for p in sources],ignore_index=True)
    full['setting']=full.setting.fillna('')
    assert ((full.test_kendall_mean.dropna()>=-1e-7)).all()
    defined=full.test_kendall_mean.notna()
    assert (full.loc[defined,'test_kendall_mean'] <= full.loc[defined,'r']*(full.loc[defined,'r']-1)/2+1e-7).all()
    keys=['study','dataset','setting','method','split','evaluation_target']
    reps=[]
    for key,g in full.groupby(keys+['repeat'],dropna=False,sort=False):
        row=dict(zip(keys+['repeat'],key));counts=g.evaluation_count.to_numpy(float)
        # G1 local/matched models predict disjoint groups. Report weighting is
        # performed inside each allocation, before averaging allocations.
        defined=g.test_kendall_mean.notna().to_numpy();weight=counts/counts.sum()
        row.update(n=int(g.n.iloc[0]),r=int(g.r.iloc[0]),N_min=g.N.min(),N_max=g.N.max(),
                   evaluation_count=counts.sum(),available_reports=counts[defined].sum(),
                   complete=bool(defined.all()),models=len(g),available_models=int(defined.sum()),
                   test_kendall_mean=float(weight@g.test_kendall_mean.to_numpy()) if defined.all() else math.nan,
                   available_subset_kendall=float(counts[defined]@g.test_kendall_mean.to_numpy()[defined]/counts[defined].sum()) if defined.any() else math.nan,
                   nll_mean=float(weight@g.nll.to_numpy()) if g.nll.notna().all() else math.nan)
        reps.append(row)
    rep=pd.DataFrame(reps)
    (OUT/'allocation_scores.csv.gz').write_bytes(gzip.compress(rep.to_csv(index=False,float_format='%.15g').encode(),mtime=0))
    summaries=[]
    for key,g in rep.groupby(keys,dropna=False,sort=False):
        row=dict(zip(keys,key));x=g.test_kendall_mean.to_numpy();v=g.nll_mean.to_numpy()
        row.update(n=int(g.n.iloc[0]),r=int(g.r.iloc[0]),N_min=g.N_min.min(),N_max=g.N_max.max(),
                   repetitions=len(g),complete_repetitions=int(g.complete.sum()),
                   test_count_min=g.evaluation_count.min(),test_count_max=g.evaluation_count.max(),
                   test_kendall_mean=float(x.mean()) if np.isfinite(x).all() else math.nan,
                   test_kendall_mcse=float(x.std(ddof=1)/np.sqrt(len(x))) if len(x)>1 and np.isfinite(x).all() else math.nan,
                   nll_mean=float(v.mean()) if not np.isnan(v).any() else math.nan,
                   available_subset_kendall=float(g.available_subset_kendall.mean()) if g.available_subset_kendall.notna().any() else math.nan)
        summaries.append(row)
    summary=pd.DataFrame(summaries)
    summary.to_csv(OUT/'summary.csv',index=False,float_format='%.15g')
    beta=full[full.algorithm_beta0.notna()].copy()
    beta['beta_fit_below_beta0']=(beta.beta_fit<beta.algorithm_beta0).astype('boolean')
    beta['beta_estimate_available']=beta.beta_fit.notna()
    # Explicitly retain unavailable fits: they are not zero beta or a passed check.
    beta.loc[~beta.beta_estimate_available,'beta_fit_below_beta0']=pd.NA
    bcols=keys+['repeat','status','beta_fit','algorithm_beta0','beta_estimate_available',
                'beta_fit_below_beta0','true_beta_below_beta0','constant_beta0_status','source']
    (OUT/'beta_audit.csv.gz').write_bytes(gzip.compress(beta[bcols].to_csv(index=False,float_format='%.15g').encode(),mtime=0))
    bsummary=[]
    for key,g in beta.groupby(['study','split','method']):
        x=g[g.beta_estimate_available]
        bsummary.append(dict(zip(['study','split','method'],key),records=len(g),available_beta=len(x),
                            below_beta0=int(x.beta_fit_below_beta0.eq(True).sum()),
                            beta_min=x.beta_fit.min(),beta_max=x.beta_fit.max(),
                            no_common_proof_inverse=int(g.constant_beta0_status.eq('no_common_proof_inverse').sum())))
    bs=pd.DataFrame(bsummary);bs.to_csv(OUT/'beta_summary.csv',index=False,float_format='%.15g')
    counts=full.groupby('study').agg(score_records=('status','size'),defined_distances=('test_kendall_mean','count')).reset_index()
    counts.to_csv(OUT/'coverage.csv',index=False)
    cols=[('dataset','Task / generator'),('setting','Setting'),('split','Evaluation'),('method','Method'),
          ('nll_mean','Mean NLL'),('test_kendall_mean','Mean report Kendall'),
          ('test_kendall_mcse','Kendall MCSE'),('complete_repetitions','Complete repetitions'),('repetitions','Planned repetitions')]
    groups={
        'P0':['P0'],'E0':['E0'],'B0':['B0'],'L0_S0':['L0','S0'],
        'P1':['P1','P1_selection'],'P2':['P2','P2_selection'],
        'G1':['G1'],'L1':['L1'],'L2':['L2','L2_penalty'],
        'S1_S2_D1':['S1','S2','D1','D1_budget'],'S3':['S3'],'D2':['D2'],
        'T1_C1':['T1_Beans','T1_ATP','C1_ATP','C1_outer','C1_same_order','C1_cutting_plane'],
        'tuned_blocks':['Tuned_blocks'],'S4-T':['S4-T']}
    for name,studies in groups.items():
        s=summary[summary.study.isin(studies)].copy()
        # All candidate-validation rows remain in CSV; the readable S4-T page
        # focuses on locked models on independent confirmation data.
        if name=='S4-T':s=s[s.split=='test']
        if name=='S1_S2_D1':s=s[s.study.isin(['S1','S2'])]
        notes=''
        if name=='S1_S2_D1':
            notes='The table shows fitted candidates. The numeric summaries also include every D1 and D1-budget selected predictor, inherited from its recorded discovery choice.\n\n'
        if name=='S4-T':
            wide=s.pivot(index='dataset',columns='method',values='test_kendall_mean')
            comparisons=[]
            for method in ('sharp_per_setting','efficient_per_setting'):
                d=wide[method]-wide.global_borda
                comparisons.append(dict(method=method,lower=int((d < -1e-10).sum()),same=int((d.abs()<=1e-10).sum()),higher=int((d > 1e-10).sum())))
            notes=('Across the 90 signal settings, compare each selected method with Global Borda on mean test-report Kendall distance. '
                   'These are descriptive signs of cell means, not significance counts. Same uses an absolute tolerance of 1e-10. '
                   'The source report separately gives error to the true generating center.\n\n'+
                   table(pd.DataFrame(comparisons),[('method','Selected method'),('lower','Lower distance'),('same','Same distance'),('higher','Higher distance')])+'\n')
        (OUT/(name+'.md')).write_text(f'# {name}: NLL and report-level Kendall distance\n\n'
            '[Definition and coverage](README.md) · [Every summary](summary.csv) · [Dispersion assumptions](../../docs/dispersion_assumptions.md)\n\n'
            'Distances average inversions **per evaluation report**, after restricting the saved catalogue order to its displayed items. '
            'Population rows use the original probability masses, not an unweighted support average. '
            'This is distinct from error relative to a simulation true center. Lower is better. '
            'Each repetition is scored first; repetitions then receive equal weight. MCSE uses the original repetition unit '
            '(random allocation for empirical studies, independent dataset for simulations). It is not a population confidence interval. '
            'NA retains unavailable complete comparisons; the CSV separately labels available-subset means.\n\n'+notes+table(s,cols))
    index='\n'.join(f'- [{name}]({name}.md)' for name in groups)
    (OUT/'README.md').write_text(r'''# Held-out report Kendall distance alongside NLL

[Experiment map](../../docs/experiments.md) · [All summaries](summary.csv) · [Every allocation](allocation_scores.csv.gz) · [Beta audit](beta_summary.csv) · [Dispersion assumptions](../../docs/dispersion_assumptions.md)

For each fitted catalogue order, restrict it to the items shown in each test report, count discordant pairs, sum across reports, and **divide by the number of test reports**. Do not divide an already averaged loss again. Report size r is retained because the range is 0 to r(r-1)/2. No further pair-count normalization is applied.

```math
L_{K,\mathrm{test}}(\widehat\pi)
=\frac{1}{N_{\mathrm{test}}}\sum_{t\in\mathrm{test}}
d_K(Y_t,\widehat\pi|_{S_t}).
```

This measures agreement with noisy held-out reports. It is not d_K(pi_hat, pi_true), nor a distance to an order fitted on the test set. It needs no beta and does not change if a predictor's dispersion changes while its center stays fixed. SM uses its saved center; PL uses its saved descending-worth order and original tie rule. Common-order controls retain their imposed common order. A uniform reference law alone has no identified fitted center, so its NLL reference is not assigned an arbitrary center error.

The exact-population NLLs in S1 and D2 have no finite test sample. Their companion distance is the corresponding probability-weighted expectation for one new report. S2 retains its sampled test reports. Test losses with an infinite NLL can still have a finite Kendall distance; those distances remain included. A failed estimator with no admitted center remains unavailable.

G1 local/matched predictors first pool discordance sums and report counts across their disjoint evaluation groups within a split. An unavailable group leaves the complete split score unavailable; the separately labeled subset mean is not substituted. Across splits, means give each original allocation equal weight. Selector results inherit the **already selected** model's distance; no selector is rerun on Kendall outcomes and aliases are not additional fits.

## Results

'''+index+'\n\n'+table(counts,[('study','Study'),('score_records','Score records, including unavailable and validation'),('defined_distances','Defined distances')])+'''
S4 itself reports true-center risk and has no predictive NLL/test-set evaluation to supplement. S4-T includes both selection-validation and independent confirmation scores in the machine tables; its readable page shows confirmation. Full-data feature/NLL joins, shell decompositions, and diagnostic subgroups reuse the originating predictors rather than creating additional center fits.

## Calculation and provenance

The original fits, allocations, NLLs, and selected constants are preserved. Saved orders are replayed against the original evaluation reports. S4-T already saves integer held-out distance sums, which are divided by its saved holdout count. Where a positive finite beta and an SM NLL were saved but the order was not, the identity `(NLL - log Z_r(beta)) / beta` recovers the same mean distance; integer totals are checked for sampled tests. This algebra is not used at beta=0 or infinity. Those boundaries and missing PL orders use deterministic source-version replays, checked against the original NLL (and original true-center error where saved). Recovered orders are retained in witness archives.

`inputs/legacy/` pins the source and selected outputs at commit 89b21645; Git blob hashes are verified by `inputs/legacy_tree.json`. These files are provenance, not alternate active experiments. P1/G1 parameter archives omit raw reports and participant membership lists; source-based allocation reconstruction supplies the evaluation sets. Raw licensed datasets remain outside the repository.

Rebuild with `build_heldout_kendall.py` (predictive, repeated, fixed_real, groups, learning, tuned_blocks, validation_simulations, s4t); `replay_strict_kendall.py` (bridge, shell, coverage); `replay_legacy_kendall.py` (small, coverage, synthetic, real, tennis, controls); then `build_kendall_selectors.py` and `summarize_heldout_kendall.py --integrate`. The read-only `verify_heldout_kendall.py` checks saved-score coverage, identities and source hashes. Existing estimation producers are unchanged.
''')
    if do_integrate:
        targets={
            'results/main/README.md':'P0','results/estimator_comparison/README.md':'E0',
            'results/global_sieve/README.md':'B0','results/predictive/README.md':'L0_S0',
            'results/predictive/scaled_curves.md':'L0_S0',
            'results/repeated_holdout/README.md':'P1','results/baseline_replacement/README.md':'P2',
            'results/context_followup/README.md':'P2','results/validation_extension/README.md':'D2',
            'results/group_sensitivity/README.md':'G1','results/regularized_learning/README.md':'L1',
            'results/regularized_diagnostics/README.md':'T1_C1','results/strict_features/README.md':'S1_S2_D1'}
        for path,name in targets.items():
            body=f'## Held-out Kendall distance\n\nThe [joint NLL / mean test-report Kendall table](../heldout_kendall/{name}.md) and [all numeric summaries](../heldout_kendall/summary.csv) report both outcomes for these fitted predictors. Distances are divided by the number of evaluation reports and do not depend on the fitted beta. [Beta/beta0 diagnostics](../../docs/dispersion_assumptions.md) distinguish estimated dispersion from the algorithm input.\n'
            if name in ('P0','E0'):
                s=summary[(summary.study==name)&(summary.split=='test')]
                pivot=s.pivot(index='dataset',columns='method',values='test_kendall_mean').reset_index()
                from summarize_predictive_study import task_label
                pivot['task']=pivot.dataset.map(task_label)
                methods=['pl','sm_likelihood'] if name=='P0' else ['pl','sm_likelihood','sm_sharp','sm_fotakis','sm_efficient','sm_global_borda']
                body+='\nEach entry below is the mean test-report Kendall distance across the five allocations. NA means the full five-fit comparison is unavailable.\n\n'+table(pivot,[('task','Task')]+[(m,m) for m in methods])
            integrate(path,body)
        integrate('experiments/section44_per_setting/README.md','''## Held-out report distance and beta0 checks

The [joint confirmation table](../../results/heldout_kendall/S4-T.md) adds mean Kendall distance to the **noisy test reports**, separately from the true-center Kendall error above. It uses each saved integer holdout distance sum divided by ceil(N/3). Every validation candidate is also covered in the [numeric summaries](../../results/heldout_kendall/summary.csv).

The [dispersion audit](../../docs/dispersion_assumptions.md) reports whether beta_hat is below the supplied beta0 and distinguishes this from the known simulation condition beta_true>=beta0. Calibrated A, K and window coefficients generally have no common inverse under the manuscript's explicit constant map; they do not establish a newly inferred beta0. The recorded validation selection used the declared [0,10] profile, not a beta0-constrained profile. These diagnostics do not retroactively change selection or remove unfavorable fits.
''')
        for path,name in [('docs/tuned_block_sieve.md','tuned_blocks'),('docs/learning_curves.md','L2'),('docs/temporal_prediction.md','T1_C1'),('docs/structural_controls.md','T1_C1')]:
            integrate(path,f'## Mean held-out Kendall distance\n\nThe [joint NLL / report-distance table](../results/heldout_kendall/{name}.md) evaluates the same fitted orders on the same held-out reports. Each distance is divided by the number of evaluation reports. See the [metric definition](../results/heldout_kendall/README.md) and [dispersion audit](dispersion_assumptions.md).')
        integrate('results/README.md','## Held-out report distance\n\n[All NLL experiments: companion Kendall distances and coverage](heldout_kendall/README.md). The P0/E0 reports also display the five-allocation distances directly. [Dispersion assumptions and fitted-beta checks](../docs/dispersion_assumptions.md) accompany these results.')
        integrate('README.md','## Test-report agreement and dispersion assumptions\n\nAll predictive components also report [mean Kendall distance from the fitted order to held-out reports](results/heldout_kendall/README.md), alongside NLL. The metric is report-normalized and separate from simulated true-center error. [Beta and beta0 checks](docs/dispersion_assumptions.md) explain the distinction between fitted dispersion, supplied algorithm bounds, and empirically calibrated constants.')
        (OUT/'report_sections.json').write_text(json.dumps(SECTIONS,indent=2,sort_keys=True)+'\n')
    print('Summarized',len(full),'score records;',len(summary),'setting/method/evaluation summaries',flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--integrate',action='store_true');a=p.parse_args();main(a.integrate)
