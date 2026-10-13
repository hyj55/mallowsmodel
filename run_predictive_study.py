"""Reproduce the predeclared finite predictive comparison; restartable local fits."""
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing as mp

from src.predictive_study import (load_tasks,empirical_context,synthetic_context,
    execute,signature,PRIVATE,BUDGETS,SIMULATION_CELLS)

TASKS = {}


def initialize(tasks):
    global TASKS
    TASKS = {t.name:t for t in tasks}


def run_one(job,code_signature):
    study,name,repeat,budget,n = job
    if study == 'S0':
        context = synthetic_context(name,n,budget,repeat)
        path = PRIVATE/'S0'/f'{name}-n{n}-N{budget}-rep{repeat:03d}.json.gz'
    else:
        context = empirical_context(TASKS[name],repeat,budget)
        path = PRIVATE/study/f'{name}-N{context["N"]}-rep{repeat:03d}.json.gz'
    return job,execute(context,code_signature,path)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--study',nargs='+',choices=['P0','L0','S0'],default=['P0','L0','S0'])
    p.add_argument('--workers',type=int,default=3)
    p.add_argument('--datasets',nargs='*')
    p.add_argument('--repetitions',type=int)
    args = p.parse_args()
    tasks=load_tasks(); code_signature=signature(); jobs=[]
    for repeat in range(args.repetitions or 30):
        if 'P0' in args.study:
            for task in sorted(tasks,key=lambda t:-t.n):
                if not args.datasets or task.name in args.datasets:
                    jobs.append(('P0',task.name,repeat,None,task.n))
        if 'L0' in args.study:
            for budget in BUDGETS:
                for name in ('sushi_a','sushi_b'):
                    if not args.datasets or name in args.datasets:
                        jobs.append(('L0',name,repeat,budget,10 if name=='sushi_a' else 100))
        if 'S0' in args.study and repeat < 20:
            for n,budget in SIMULATION_CELLS:
                for generator in ('sm','pl'):
                    jobs.append(('S0',generator,repeat,budget,n))
    # Spawn isolates solvers and preserves deterministic per-job random streams.
    with ProcessPoolExecutor(max_workers=args.workers,mp_context=mp.get_context('spawn'),
                             initializer=initialize,initargs=(tasks,)) as pool:
        pending=[pool.submit(run_one,job,code_signature) for job in jobs]
        for count,future in enumerate(as_completed(pending),1):
            job,status=future.result()
            print(count,'/',len(jobs),job,status,flush=True)


if __name__=='__main__':
    main()
