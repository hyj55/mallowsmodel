"""Construct the expensive shared packings once before parallel predictive fits."""
from concurrent.futures import ProcessPoolExecutor, as_completed
from src.resource_sieve import cached_packing,SieveResourceError


def run_case(case):
    try:
        orders,meta=cached_packing(*case)
        return case,meta
    except SieveResourceError as exc:
        return case,exc.metadata


if __name__=='__main__':
    with ProcessPoolExecutor(max_workers=3) as pool:
        jobs=[pool.submit(run_case,case) for case in ((10,1),(10,4),(10,9),(10,22),(9,9))]
        for job in as_completed(jobs):
            print(job.result(),flush=True)
