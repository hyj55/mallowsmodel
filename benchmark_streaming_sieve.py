"""Retry the shared exact packings needed by the remaining Sharp contexts.

This is a computation audit, not another statistical experiment. No partial
packing is scored. The saved predictive results are opened read-only.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np

from src.streaming_sieve import (streamed_packing, SieveResourceError, ROOT, CACHE,
                                 SECONDS, MEMORY, file_hash)

PUBLIC = ROOT/'results/predictive/streaming'
CODE = ('src/streaming_sieve.cpp', 'src/streaming_sieve.py',
        'benchmark_streaming_sieve.py')
INPUTS = tuple('results/predictive/'+name for name in (
    'predictors.jsonl.gz','manifest.json','primary.csv','learning.csv',
    'synthetic.csv','repeat_scores.csv.gz','packing_crosscheck.json'))


def contexts():
    with gzip.open(ROOT/INPUTS[0], 'rt') as stream:
        records=[json.loads(line) for line in stream]
    rows=[]
    for r in records:
        fit=r['models']['sm_sharp']
        if fit['status']!='sieve_resource_budget':continue
        meta=fit['metadata']; n=r['n']
        assert meta['depth']==0 and meta['actual_block_items']==n
        assert meta['global_sieve_identical'] and meta['pilot_reports']==0
        assert meta['A']==256 and meta['W_star']>=n
        # Every complete report has at least two items in this global block,
        # hence exactly one retained pair per development report, k=N.
        assert r['r']>=2
        radius=n*(n*(n-1)//2)//r['N']
        rows.append(dict(study=r['study'],dataset=r['dataset'],n=n,r=r['r'],N=r['N'],
            repeat=r['repeat'],estimator_seed=r['estimator_seed'],integer_radius=radius,
            case=f'{n}:{radius}',status_before=fit['status']))
    return rows


def construction(case, seconds, cache, resume):
    n,radius=case
    try:
        _,meta=streamed_packing(n,radius,cache=cache,seconds=seconds,
                               memory_bytes=MEMORY,resume=resume)
    except SieveResourceError as exc:
        meta=exc.metadata
    print(f'n={n} d={radius}: complete={meta["complete"]}; '
          f'retained={meta["packing_so_far"]}; '
          f'working bytes={meta["allocated_working_bytes"]}; '
          f'seconds={meta["total_elapsed_seconds"]:.3f}',flush=True)
    return meta


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seconds',type=float,default=SECONDS)
    parser.add_argument('--workers',type=int,default=1,
        help='Concurrent distinct packings; each has a separate 4-GiB array budget')
    parser.add_argument('--resume',action='store_true')
    parser.add_argument('--cache',type=Path,default=CACHE)
    parser.add_argument('--cases',nargs='*',help='Optional n:radius subset to extend')
    args=parser.parse_args()
    if args.workers<1 or args.seconds<0:parser.error('Invalid resource budget')
    rows=contexts(); cases=sorted({(r['n'],r['integer_radius']) for r in rows})
    selected=set(tuple(map(int,x.split(':'))) for x in args.cases) if args.cases else set(cases)
    if not selected<=set(cases):parser.error('Requested case is not a missing-fit packing')
    frozen={p:file_hash(ROOT/p) for p in INPUTS}
    def run(case):
        # A subset extension leaves other verified checkpoint budgets intact.
        return construction(case,args.seconds if case in selected else 0,args.cache,
                            args.resume and case in selected)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        receipts=list(pool.map(run,cases))
    benchmarks=[]
    for n,d in ((10,4),(12,40),(16,100)):
        orders,meta=streamed_packing(n,d,cache=args.cache,seconds=120)
        meta=dict(meta,role='computational_check_not_experiment')
        if (n,d)==(10,4):
            check=json.loads((ROOT/'results/predictive/packing_crosscheck.json').read_text())
            digest=hashlib.sha256(orders.astype('<i2').tobytes()).hexdigest()
            assert digest==check['original_orders_sha256']
            meta['matches_original_complete_packing']=True
        benchmarks.append(meta)
    # A deliberately tiny cache exercises actual eviction/reloading. This is
    # an implementation check, not an experimental tuning parameter.
    from src.resource_sieve import build_packing
    orders,meta=streamed_packing(9,4,cache=args.cache/'forced-spill',seconds=120,memory_bytes=2108000)
    original,_=build_packing(9,4)
    np.testing.assert_array_equal(orders,original)
    assert meta['disk_block_writes']>0 and meta['disk_block_reads']>0
    benchmarks.append(dict(meta,role='forced_disk_spill_check_not_experiment',
        matches_original_complete_packing=True,
        original_orders_sha256=hashlib.sha256(original.astype('<i2').tobytes()).hexdigest()))
    assert frozen=={p:file_hash(ROOT/p) for p in INPUTS}
    PUBLIC.mkdir(parents=True,exist_ok=True)
    (PUBLIC/'packings.json').write_text(json.dumps(receipts,indent=2)+'\n')
    (PUBLIC/'benchmarks.json').write_text(json.dumps(benchmarks,indent=2)+'\n')
    index={(m['m'],m['integer_radius']):m for m in receipts}
    for row in rows:
        meta=index[row['n'],row['integer_radius']]
        row.update(packing_complete=meta['complete'],packing_so_far=meta['packing_so_far'],
            reason=meta['reason'],status_after=row['status_before'],
            fit_published=False)
    with (PUBLIC/'contexts.csv').open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    manifest=dict(code_sha256={p:file_hash(ROOT/p) for p in CODE},inputs_sha256=frozen,
        missing_contexts=len(rows),shared_packings=len(cases),
        complete_packings=sum(m['complete'] for m in receipts),
        recovered_fits=0,statistical_definition_changed=False,
        note='A shared prerequisite construction is attempted once per (n, radius), not once per split. '
             'No predictor or score is published by this computational audit. Completed packings, '
             'if any, must still be scored on each unchanged extracted-pair sample before fits are published.',
        outputs_sha256={p:file_hash(PUBLIC/p) for p in ('packings.json','benchmarks.json','contexts.csv')})
    (PUBLIC/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('AUDITED',len(rows),'contexts sharing',len(cases),'packings; predictions unchanged',flush=True)


if __name__=='__main__':main()
