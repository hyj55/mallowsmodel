"""Complete E0 Efficient/global-Borda candidates on all five saved allocations."""
import pandas as pd
from src.estimator_comparison import source_records, execute, export, ROOT
from src.repeated_holdout import load_tasks


def main():
    tasks = {t.name:t for t in load_tasks()}
    scores = pd.read_csv(ROOT/'results/predictive/repeat_scores.csv.gz')
    scores = scores[scores.study == 'P0']
    records = []
    for source in source_records():
        record = execute(source, tasks[source['dataset']], scores)
        records.append(record)
        efficient = record['models']['sm_efficient']
        print(source['dataset'], source['repeat'], 'Borda complete;',
              'Efficient', efficient['status'], 'depth', efficient['metadata'].get('depth'), flush=True)
    export(records)
    print('Published E0: 23 tasks, 115 allocations, 690 method scores', flush=True)


if __name__ == '__main__':
    main()
