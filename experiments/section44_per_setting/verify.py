"""Read-only verification of preserved S4, selection and independent test results."""
import csv
import gzip
import json
import math
from pathlib import Path
import sys

sys.set_int_max_str_digits(0)

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import numpy as np

from experiments.section44.core import digest_array,kendall_fast
from experiments.section44_per_setting.run import OUT,HERE,sha,select_records
from experiments.section44_per_setting.engine import generate,score
from experiments.section44_per_setting.report import ci,adjusted


def records(phase):
    archive=json.loads((OUT/'draw_archives.json').read_text())
    for part in archive:
        if not Path(part['path']).name.startswith(phase+'-'):continue
        path=OUT/part['path']
        assert sha(path)==part['sha256']
        count=0
        with gzip.open(path,'rt') as f:
            for line in f:
                count+=1;yield json.loads(line)
        assert count==part['records']


def main():
    for name,digest in json.loads((OUT/'manifest.json').read_text()).items():
        assert sha(HERE/name)==digest,name
    old=json.loads((OUT/'original_s4_hashes.json').read_text())
    for name,digest in old.items():assert sha(ROOT/name)==digest,name
    selected=json.loads((OUT/'selection.json').read_text())
    signature=json.loads((OUT/'producer.json').read_text())['signature']
    for name,digest in signature['code'].items():assert sha(ROOT/name)==digest,name
    assert sha(OUT/'protocol.json')==signature['protocol']
    slim=[];seen=set()
    for rec in records('calibration'):
        assert rec['signature']==signature and rec['selection_sha256'] is None
        assert (rec['cell']['id'],rec['repeat']) not in seen
        seen.add((rec['cell']['id'],rec['repeat']))
        slim.append(dict(cell=rec['cell'],group=rec['group'],repeat=rec['repeat'],
                         models={k:{j:v[j] for j in ('fit_key','depth','branch')} for k,v in rec['models'].items()},
                         fits={k:{j:v.get(j) for j in ('status','holdout_nll')} for k,v in rec['fits'].items()}))
    assert len(seen)==1800
    replay,audit=select_records(slim)
    assert replay==selected
    assert audit==json.loads((OUT/'calibration_candidates.json').read_text())
    del slim
    seen=set();draws={};replayed=0
    for rec in records('confirmation'):
        assert rec['signature']==signature and rec['selection_sha256']==sha(OUT/'selection.json')
        key=(rec['cell']['id'],rec['repeat'])
        assert key not in seen;seen.add(key)
        assert len(rec['models'])==7
        draws[key]={name:rec['fits'][m['fit_key']] for name,m in rec['models'].items()}
        # Keep only numerical scores after verification to bound memory.
        for family in ('efficient','sharp'):
            m=rec['models'][family+'_per_setting']
            assert m['config']==selected[rec['group']][family]['config']
        for f in rec['fits'].values():
            if f['status']=='ok':
                assert sorted(f['order'])==list(range(rec['cell']['n']))
                assert f['kendall']==kendall_fast(f['order'],rec['truth'])
        if rec['repeat']==0 and rec['index']%7==0:
            truth,train,test,seed=generate(rec['cell'],1,rec['index'],0)
            assert digest_array(train)==rec['train_sha256']
            assert digest_array(test)==rec['holdout_sha256']
            assert digest_array(truth)==rec['truth_sha256'] and seed==rec['estimator_seed']
            for f in rec['fits'].values():
                if f['status']=='ok':
                    scores=score(train,test,np.asarray(f['order']))
                    for name,v in scores.items():
                        np.testing.assert_allclose(v,f[name],rtol=1e-11,atol=1e-10)
            replayed+=1
        draws[key]={name:{k:f.get(k) for k in ('status','holdout_nll','kendall')} for name,f in draws[key].items()}
    assert len(seen)==9000
    verified=[]
    with (OUT/'paired_comparisons.csv').open() as f:
        reported=list(csv.DictReader(f))
        assert len(reported)==1800
        for row in reported:
            paired=[rep for rep in range(100)
                    if draws[(row['cell'],rep)][row['method']]['status']=='ok'
                    and draws[(row['cell'],rep)][row['reference']]['status']=='ok']
            assert int(row['available'])==len(paired)
            assert (row['complete']=='True')==(len(paired)==100)
            if row['complete']!='True':continue
            metric='holdout_nll' if row['metric']=='nll' else 'kendall'
            values=[draws[(row['cell'],rep)][row['method']][metric]-
                    draws[(row['cell'],rep)][row['reference']][metric] for rep in range(100)]
            stats=ci(values)
            for k,v in stats.items():np.testing.assert_allclose(v,float(row[k]),rtol=1e-11,atol=1e-10)
            scale=math.lgamma(int(row['r'])+1) if metric=='holdout_nll' else int(row['n'])*(int(row['n'])-1)/2
            np.testing.assert_allclose(stats['mean']/scale,float(row['scaled_mean']),rtol=1e-11,atol=1e-10)
            verified.append(dict(row,complete=True,**stats))
    adjusted(verified)
    for row in verified:
        if row['method'].endswith('_per_setting') and row['reference']=='global_borda':
            original=next(r for r in reported if all(r[k]==row[k] for k in ('cell','method','reference','metric')))
            np.testing.assert_allclose(row['holm_p'],float(original['holm_p']),rtol=1e-11,atol=1e-10)
    print(f'PASS: {len(old)} original S4 files unchanged; 1800 selection draws replayed; '
          f'9000 confirmation draws; all paired intervals; {replayed} report-stream replays.')


if __name__=='__main__':main()
