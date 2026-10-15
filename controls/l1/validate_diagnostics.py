"""Read-only consistency checks for the five-fit C1 diagnostic collection."""
import argparse,hashlib,json
import numpy as np
import pandas as pd
from run import ROOT
OUT=ROOT/'results/regularized_diagnostics'
CODE=['controls/l1/diagnostics.py','controls/l1/src/diagnostics.py','controls/l1/validate_diagnostics.py']
FILES=['shell_decomposition.csv','pair_diagnostics.csv','context_effects.csv','context_replicates.csv','adjacent_pair_bins.csv','diagnostic_coverage.csv','diagnostic_bin_cutoffs.csv','diagnostic_manifest.json']
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def manifest():return dict(repetitions=5,bootstrap_draws=2000,code={p:digest(ROOT/p) for p in CODE},inputs={'results/regularized_learning/fitted_parameters.json':digest(ROOT/'results/regularized_learning/fitted_parameters.json')},outputs={p:digest(OUT/p) for p in FILES})
def main(write=False):
    if write:(OUT/'manifest.json').write_text(json.dumps(manifest(),indent=2)+'\n')
    assert json.loads((OUT/'manifest.json').read_text())==manifest()
    shell=pd.read_csv(OUT/'shell_decomposition.csv');learning=pd.read_csv(ROOT/'results/regularized_learning/real_summary.csv')
    assert len(shell)==24 and shell.repetitions.eq(5).all()
    for (dataset,N,fit),g in shell.groupby(['dataset','N','fit']):
        v=g.set_index('component').value
        np.testing.assert_allclose(v['total'],v['shell_mass']+v['within_shell'],atol=1e-11)
        target=learning.query('dataset==@dataset and N==@N').iloc[0]
        np.testing.assert_allclose(v['total'],target['delta' if fit=='main' else 'calibrated_delta'],atol=1e-11)
    context=pd.read_csv(OUT/'context_replicates.csv')
    assert len(context)==25
    for _,g in context.groupby(['dataset','stratification']):assert set(g.replicate)==set(range(5)) and len(g)==5
    from diagnostics import verify
    verify()
    print('C1: five fits per task/stratum, shell identity and L1 loss agreement, and exhaustive likelihood identities verified')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write-manifest',action='store_true');main(p.parse_args().write_manifest)
