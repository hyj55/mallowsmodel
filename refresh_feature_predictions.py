"""Join saved full-data characteristics to current prediction summaries, without refitting."""
import json
import pandas as pd
from describe_pair_features import ROOT, OUT, digest, prediction_comparison


def run():
    pair = prediction_comparison(pd.read_csv(OUT/'summary.csv'))
    pair.to_csv(OUT/'nll_comparison.csv', index=False, float_format='%.15g')
    manifest = json.loads((OUT/'manifest.json').read_text())
    for path in manifest['nll_input_sha256']:
        manifest['nll_input_sha256'][path] = digest(ROOT/path)
    manifest['code_sha256']['describe_pair_features.py'] = digest(ROOT/'describe_pair_features.py')
    manifest['code_sha256']['refresh_feature_predictions.py'] = digest(ROOT/'refresh_feature_predictions.py')
    manifest['output_sha256']['nll_comparison.csv'] = digest(OUT/'nll_comparison.csv')
    (OUT/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    columns = ['dataset','nll_study','sm_method','pl_method','nll_target','nll_source',
        'sm_nll','pl_nll','delta','delta_status','paired_repetitions','planned_repetitions',
        'conditional_delta','delta_partition_mcse','delta_per_pair_scale','center_method','center_certified']
    summary = pd.read_csv(OUT/'structure/summary.csv')
    full = summary.loc[summary.reference.eq('full_data')].copy()
    # Center metadata belongs to the descriptive table when already present.
    keep = ['dataset'] + [c for c in columns[1:] if c not in full.columns]
    joined = full.merge(pair[keep], on='dataset', validate='one_to_one')
    joined.to_csv(OUT/'structure/nll_comparison.csv', index=False, float_format='%.15g')
    manifest = json.loads((OUT/'structure/manifest.json').read_text())
    for path in manifest['inputs']:
        manifest['inputs'][path] = digest(ROOT/path)
    manifest['output_sha256']['nll_comparison.csv'] = digest(OUT/'structure/nll_comparison.csv')
    manifest['code_sha256']['refresh_feature_predictions.py'] = digest(ROOT/'refresh_feature_predictions.py')
    (OUT/'structure/manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    from make_feature_summary import run as render
    render()


if __name__ == '__main__':
    run()
