"""Run the predeclared 30-partition correction without changing previous artifacts."""
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import gzip
import hashlib
import json
import time

from src.repeated_holdout import (ROOT, REPETITIONS, load_tasks, split_task, fit_all,
    evaluate, save_fit, json_value, source_inventory, code_hashes)
from src.repeated_holdout_summary import publish

TASKS = {}


def initialize(tasks):
    global TASKS
    TASKS = {t.name:t for t in tasks}


def run_one(name, repeat, directory, signature):
    task = TASKS[name]
    path = directory / name / f'repeat-{repeat:03d}.json.gz'
    if path.exists():
        with gzip.open(path, 'rt') as f:
            record = json.load(f)
        if record.get('code_signature') != signature:
            raise ValueError('Cached code differs; use a separate output directory: '+str(path))
        return name, repeat, 'cached'
    started = time.perf_counter()
    parts = split_task(task, repeat)
    fitted = fit_all(task, task.y[parts['fit']])
    outputs = evaluate(task, repeat, parts, fitted)
    record = json_value(dict(dataset=name, repeat=repeat, code_signature=signature,
        parts=parts, models={m:save_fit(f) for m,f in fitted.items()},
        elapsed_seconds=time.perf_counter()-started, **outputs))
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix('.temporary')
    with gzip.open(temp, 'wt') as f:
        json.dump(record, f, allow_nan=False)
    temp.replace(path)
    return name, repeat, {m:f.status for m,f in fitted.items()}


def read_records(directory):
    records = []
    for path in sorted(directory.glob('*/repeat-*.json.gz')):
        with gzip.open(path, 'rt') as f:
            record = json.load(f)
        # JSON stores nonfinite values as strings; data frames need numeric metrics.
        for key in ('scores', 'diagnostics', 'selections'):
            for row in record[key]:
                for name, value in row.items():
                    if value in ('nan', 'inf', '-inf'):
                        row[name] = float(value)
        records.append(record)
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workers', type=int, default=2)
    parser.add_argument('--datasets', nargs='*')
    parser.add_argument('--quick', action='store_true')
    parser.add_argument('--summarize-only', action='store_true')
    args = parser.parse_args()
    directory = ROOT / ('results/private/repeated_holdout_quick' if args.quick else 'results/private/repeated_holdout')
    tasks = load_tasks()
    selected = tasks if not args.datasets else [t for t in tasks if t.name in args.datasets]
    if args.datasets and len(selected) != len(set(args.datasets)):
        raise ValueError('Unknown dataset requested')
    signature = hashlib.sha256(json.dumps(code_hashes(), sort_keys=True).encode()).hexdigest()
    if not args.summarize_only:
        repetitions = 2 if args.quick else REPETITIONS
        # Interleave tasks across repetitions; heavy large-catalog solves can overlap.
        order = sorted(selected, key=lambda t:-t.n)
        jobs = [(t.name, rep) for rep in range(repetitions) for t in order]
        with ProcessPoolExecutor(max_workers=args.workers, initializer=initialize, initargs=(tasks,)) as pool:
            pending = [pool.submit(run_one, name, repeat, directory, signature) for name,repeat in jobs]
            for number,future in enumerate(as_completed(pending), 1):
                name, rep, status = future.result()
                print(number, '/', len(jobs), name, rep, status, flush=True)
    if not args.quick and not args.datasets:
        publish(read_records(directory), tasks, source_inventory(), ROOT / 'results/repeated_holdout')


if __name__ == '__main__':
    main()
