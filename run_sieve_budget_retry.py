"""Retry only previously unavailable Sharp fits; preserve all allocation streams."""
import gzip
import hashlib
import json
from pathlib import Path
import time

from src.predictive_study import (PRIVATE,empirical_context,synthetic_context,
    load_tasks,array_hash,evaluate,signature)
from src.predictive_models import sm_fit
from src.repeated_holdout import restore_fit,save_fit,json_value
from src.strict_models import StrictFit
from src.sieve_budget_retry import retry_sharp_center,SieveResourceError

BASE_COMMIT='cb3807c4930c76d3b35369164ec6c9e009d0872f'
ROOT=Path(__file__).resolve().parent
RETRIES=ROOT/'results/private/predictive_retry'
RETRY_CODE=('src/sieve_budget_retry.py','run_sieve_budget_retry.py')


def retry_hashes():
    return {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in RETRY_CODE}


def apply_saved_retries(records):
    indexed={(r['study'],r['dataset'],r['n'],r['N'],r['repeat']):r for r in records}
    for path in sorted(RETRIES.glob('*/*.json.gz')):
        with gzip.open(path,'rt') as stream:r=json.load(stream)
        assert r['resource_retry']['code_sha256']==retry_hashes()
        key=(r['study'],r['dataset'],r['n'],r['N'],r['repeat'])
        assert key in indexed and indexed[key]['models']['sm_sharp']['status']=='sieve_resource_budget'
        for method in ('pl','sm_likelihood','sm_fotakis'):
            assert indexed[key]['models'][method]==r['models'][method]
        assert indexed[key]['data_sha256']==r['data_sha256']
        for row in r['scores']:
            for field,value in row.items():
                if value in ('nan','inf','-inf'):row[field]=float(value)
        indexed[key]=r
    return list(indexed.values())


def main():
    tasks={t.name:t for t in load_tasks()}; hashes=retry_hashes(); completed=0; recovered=0
    for path in sorted(PRIVATE.glob('*/*.json.gz')):
        with gzip.open(path,'rt') as stream:record=json.load(stream)
        if record['models']['sm_sharp']['status']!='sieve_resource_budget':continue
        target=RETRIES/path.relative_to(PRIVATE)
        if target.exists():
            with gzip.open(target,'rt') as stream:existing=json.load(stream)
            assert existing['resource_retry']['code_sha256']==hashes
            completed+=1;recovered+=existing['models']['sm_sharp']['status']=='ok'
            continue
        if record['study']=='S0':
            context=synthetic_context(record['generator'],record['n'],record['N'],record['repeat'])
        else:
            context=empirical_context(tasks[record['dataset']],record['repeat'],
                                      None if record['study']=='P0' else record['N'])
        assert {k:array_hash(v) for k,v in context['data'].items()}==record['data_sha256']
        assert record['code_signature']==signature()
        started=time.perf_counter();y=context['data']['development']
        before=record['models']['sm_sharp']
        try:
            order,meta=retry_sharp_center(y,record['n'],record['estimator_seed'])
            sharp=sm_fit('sm_sharp',y,order,meta)
        except SieveResourceError as exc:
            sharp=sm_fit('sm_sharp',y,None,dict(exc.metadata,status='sieve_resource_budget'))
        fits={m:restore_fit(f) for m,f in record['models'].items()}
        fits['sm_sharp']=sharp
        fits['sm_global_sieve']=StrictFit('sm_global_sieve',sharp.order,beta=sharp.beta,
            status=sharp.status,metadata=dict(sharp.metadata,alias_of='sm_sharp',R_bound=10))
        if sharp.status=='ok':
            # Newly recovered contexts all have lambda>1, so no existing
            # efficient prediction is deleted by the fallback status change.
            assert fits['sm_efficient_fallback'].status!='ok'
            fits['sm_efficient_fallback']=sm_fit('sm_efficient_fallback',y,None,dict(status='sharp_available'))
            scores,losses=evaluate(context,fits)
            record.update(scores=scores,losses=losses)
            recovered+=1
        else:
            # Losses remain unavailable, but the computation path now belongs
            # to the enlarged-budget engine and must match saved metadata.
            for row in record['scores']:
                if row['method'] in ('sm_sharp','sm_global_sieve'):
                    row['branch']=sharp.metadata.get('branch',sharp.metadata.get('path',''))
        record['models']={m:save_fit(f) for m,f in fits.items()}
        record['resource_retry']=dict(base_commit=BASE_COMMIT,code_sha256=hashes,
            base_record_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            original_sharp=before,seconds=time.perf_counter()-started,
            statistical_definition_changed=False)
        target.parent.mkdir(parents=True,exist_ok=True)
        temporary=target.with_suffix('.temporary')
        with gzip.open(temporary,'wt') as stream:json.dump(json_value(record),stream,allow_nan=False)
        temporary.replace(target);completed+=1
        if completed%25==0:print('RETRIED',completed,'RECOVERED',recovered,flush=True)
    print('COMPLETE retries=',completed,'recovered=',recovered,flush=True)


if __name__=='__main__':main()
