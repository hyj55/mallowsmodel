"""Fresh-process resource measurements, separate from Monte Carlo risk."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import tracemalloc

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import numpy as np
from experiments.section44.core import fit
from experiments.section44.design import confirmation_cells
from experiments.section44.run import (OUTPUT,PRIVATE,data,methods,write_json,sha)


def worker(index,method):
    c=confirmation_cells()[index]
    selected=json.loads((OUTPUT/'selection.json').read_text())
    choices={name:(family,cfg) for name,family,cfg in methods(c,1,selected)}
    family,cfg=choices[method]
    truth,y,seed=data(c,1,index,0)
    cache=PRIVATE/'resource_packing'/c['id']/method
    # A unique empty directory makes this a cold packing run, not a reused fit.
    if cache.exists():
        raise RuntimeError('Cold profile cache exists; preserve the receipt or use a new profile directory')
    tracemalloc.start(); start=time.perf_counter()
    order,meta=fit(y,c['n'],family,cfg,c['beta0'],seed,cache)
    seconds=time.perf_counter()-start
    current,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    path=PRIVATE/'resource_receipts'/c['id']/(method+'.json')
    write_json(path,dict(cell=c['id'],method=method,n=c['n'],r=c['r'],N=c['N'],Nr=c['N']*c['r'],
        status=meta['status'],depth=meta.get('depth'),branch=meta.get('branch'),
        fit_seconds_with_tracing=seconds,peak_traced_working_bytes=peak,
        input_bytes=y.nbytes,peak_including_input_bytes=peak+y.nbytes,
        fresh_process=True,cold_packing=True,repeat=0,resource_limits=meta.get('failed_block'),
        selection_sha256=sha(OUTPUT/'selection.json')))


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--index',type=int)
    parser.add_argument('--method');parser.add_argument('--shard',type=int,default=0)
    parser.add_argument('--shards',type=int,default=1)
    args=parser.parse_args()
    if args.index is not None:
        worker(args.index,args.method);return
    selected=json.loads((OUTPUT/'selection.json').read_text())
    # Resource curves span n,N,r and methods; each uses repetition zero only.
    for index,c in enumerate(confirmation_cells()):
        if index%args.shards!=args.shard:continue
        for name,_,_ in methods(c,1,selected):
            path=PRIVATE/'resource_receipts'/c['id']/(name+'.json')
            if path.exists():continue
            result=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--index',str(index),'--method',name],
                                  text=True,capture_output=True,env=os.environ)
            if result.returncode:
                raise RuntimeError(result.stderr)
        print('PROFILE',c['id'],flush=True)


if __name__=='__main__':main()
