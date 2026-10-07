"""Calculate characteristics 2 and 3 from every report, reusing saved centers.

Public outputs aggregate shell and pair summaries. Frequency tables that can
reconstruct source rankings remain in the ignored results/private directory.
"""
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

from describe_pair_features import ROOT, OUT as PAIR_OUT, array_digest, digest, tennis_tasks
from src.repeated_holdout import load_tasks,source_inventory
from src.structure_features import describe_structure

OUT=PAIR_OUT/'structure'
PRIVATE=ROOT/'results/private/structure_features'


def save_frame(frame,path):
    path.parent.mkdir(parents=True,exist_ok=True)
    frame.to_csv(path,index=False,float_format='%.15g',
        compression={'method':'gzip','mtime':0} if str(path).endswith('.gz') else None)


def run():
    centers=json.loads((PAIR_OUT/'centers.json').read_text())
    tasks=[dict(name=t.name,y=t.y,n=t.n,truth=t.truth) for t in load_tasks()]+tennis_tasks()
    summaries=[]; outputs=[]; private_hashes={}
    for task in tasks:
        name,y=task['name'],task['y']
        assert array_digest(y)==centers[name]['reports_sha256']
        refs=[('full_data',np.asarray(centers[name]['order']))]
        if task['truth'] is not None:
            refs.append(('objective',np.asarray(task['truth'])))
        shells=[]; pairs=[]
        for ref,order in refs:
            print('DESCRIBE',name,ref,flush=True)
            result=describe_structure(y,order)
            summaries.append(dict(dataset=name,reference=ref,**result['summary']))
            # Public summaries omit actual displayed items, individual ranking
            # identities, and pair-by-exact-display outcomes.
            shells.append(result['shells'].assign(dataset=name,reference=ref))
            pairs.append(result['pairs'].assign(dataset=name,reference=ref))
            for kind in ['displays','rankings','context_cells','swaps']:
                path=PRIVATE/name/f'{ref}_{kind}.csv.gz'
                save_frame(result[kind],path)
                private_hashes[str(path.relative_to(ROOT))]=digest(path)
        for kind,frames in [('shells',shells),('pairs',pairs)]:
            path=OUT/kind/(name+'.csv')
            save_frame(pd.concat(frames,ignore_index=True),path)
            outputs.append(str(path.relative_to(OUT)))
    summary=pd.DataFrame(summaries)
    save_frame(summary,OUT/'summary.csv'); outputs.append('summary.csv')
    comparison=pd.read_csv(PAIR_OUT/'nll_comparison.csv')
    columns=['dataset','nll_study','sm_method','pl_method','nll_target','nll_source','sm_nll','pl_nll',
             'delta','delta_status','paired_repetitions','planned_repetitions','conditional_delta',
             'delta_partition_mcse','delta_per_pair_scale','center_method','center_certified']
    comparison=summary.loc[summary.reference.eq('full_data')].merge(comparison[columns],on='dataset',validate='one_to_one')
    assert len(comparison)==33
    save_frame(comparison,OUT/'nll_comparison.csv'); outputs.append('nll_comparison.csv')
    source_inventory()
    manifest=dict(purpose='Full-data descriptive characteristics 2 and 3; not prediction experiments',
        source_main_commit='1265f2815bb0436514843abf0a8ed9d7519dd076',tasks=33,references=len(summary),
        inputs={str(p.relative_to(ROOT)):digest(p) for p in [PAIR_OUT/'centers.json',PAIR_OUT/'manifest.json',
            PAIR_OUT/'nll_comparison.csv',ROOT/'results/repeated_holdout/scores.csv',PAIR_OUT/'tennis_nll_source.csv']},
        code_sha256={p:digest(ROOT/p) for p in ['src/structure_features.py','describe_structure_features.py']},
        output_sha256={p:digest(OUT/p) for p in outputs},private_output_sha256=private_hashes,
        private_scope='Exact ranking frequencies, displays, pair-by-display counts and individual replacement contrasts stay local to avoid redistributing source reports',
        limitations=['Full-data reference order estimated from these reports',
            'Conditional shell TV includes all zero-count possible rankings',
            'IID-uniform expected TV is a nominal sampling reference, not a corrected population estimate or significance test',
            'Exact-display pair variation includes sampling noise and assessor/display mixtures',
            'No context contrast for a pair observed in only one displayed set',
            'All comparisons use full eligible tasks; unavailable structure is NA, not zero'])
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(comparison[['dataset','shell_tv','shell_iid_uniform_expected_tv','context_display_sd',
                      'context_gap_slope','swap_gap_effect','swap_gap_edges','delta']].to_string(index=False),flush=True)


if __name__=='__main__':
    run()
