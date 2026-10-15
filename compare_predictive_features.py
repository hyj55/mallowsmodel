"""Join the three unchanged whole-data characteristics to primary predictive NLL."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
from summarize_predictive_study import markdown_table

ROOT=Path(__file__).resolve().parent


def main():
    features=pd.read_csv(ROOT/'data/features/all_features.csv')
    primary=pd.read_csv(ROOT/'results/predictive/primary.csv')
    sm=primary[primary.method.eq('sm_likelihood')].set_index('dataset')
    pl=primary[primary.method.eq('pl')].set_index('dataset')
    rows=[]
    for _,r in features.iterrows():
        if r.reference!='full_data':
            continue
        out=r.to_dict()
        if r.dataset in sm.index:
            s=sm.loc[r.dataset]
            out.update(primary_study='P0',primary_sm_nll=s.nll_mean,
                primary_pl_nll=pl.loc[r.dataset].nll_mean,primary_delta=s.delta_mean,
                primary_delta_mcse=s.delta_mcse,primary_available=s.available,
                primary_certified=s.certified_centers,primary_N=s.N)
        else:
            assert r.dataset.startswith('atp_') or str(r.nll_study)=='T1',r.dataset
            out.update(primary_study='T1_chronological',primary_sm_nll=r.sm_nll,
                primary_pl_nll=r.pl_nll,primary_delta=r.delta,primary_delta_mcse=np.nan,
                primary_available=r.paired_repetitions,primary_certified=np.nan,primary_N=np.nan)
        rows.append(out)
    frame=pd.DataFrame(rows)
    assert len(frame)==33 and (frame.primary_study=='P0').sum()==23
    path=ROOT/'data/features/predictive_comparison.csv'
    frame.to_csv(path,index=False,float_format='%.12g')
    for source,target in [('context_display_sd','C_percentage_points'),('swap_gap_effect','R_percentage_points')]:
        frame[target]=100*frame[source]
    text='# Three full-data characteristics beside predictive performance\n\n'
    text+='[Feature definitions and support](README.md) · [Combined CSV](predictive_comparison.csv) · [Primary fitting design](../../docs/predictive_comparison.md) · [Unpenalized and detailed feature tables](comparison.md)\n\n'
    text+='All three characteristics use every eligible report and the same saved full-data reference center. They are unchanged data descriptions. P0 NLL uses separately trained predictors and outer-test reports; none of these full-data characteristics selects its center, penalty or training split. Negative delta favors SM. The comparison is descriptive, not a causal explanation or an independent model test.\n\n'
    text+='H is equal-gap pair-rate dispersion; T−b is within-display/shell TV minus a nominal iid-uniform sampling reference; C is within-pair variation across displays; gamma is its gap slope; R is the one-item replacement effect (distinct from the report-size upper bound also denoted R). H, C and R are in percentage points. Undefined contrasts remain NA. The nominal shell reference is not a calibrated significance test. Sparse single-report cells can produce large apparent dispersion.\n\n'
    text+=markdown_table(frame,[('dataset','Task'),('primary_study','NLL target'),
        ('heterogeneity_percentage_points','H (pp)'),('shell_excess_tv','T−b'),
        ('C_percentage_points','C (pp)'),('context_gap_slope','gamma'),
        ('R_percentage_points','R (pp)'),('primary_delta','SM−PL NLL')])+'\n\n'
    text+='The CSV preserves all support counts, feature statuses and supplementary NLL fields, alongside clearly prefixed `primary_*` columns. P0 averages five 80/20 fits; ATP retains T1’s chronological target and is not added to P0. Raw NLL gaps have different scales across r. Shared respondents, task mixtures and unmeasured season/assessor composition prevent an interpretation as independent causal evidence.\n'
    (path.parent/'predictive_comparison.md').write_text(text)
    manifest=dict(inputs={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
        [ROOT/'data/features/all_features.csv',ROOT/'results/predictive/primary.csv']},
        outputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [path,path.with_suffix('.md')]},
        feature_recalculation=False,predictive_refitting=False)
    (path.parent/'predictive_comparison_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Joined three unchanged features to 23 primary and 10 temporal comparisons')


if __name__=='__main__':
    main()
