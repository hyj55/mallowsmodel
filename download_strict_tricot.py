"""Reproduce the frozen candidate rule and schema eligibility audit.

No report is repaired. Raw demographics remain in ignored downloaded sources;
only provenance and aggregate eligibility counts enter the repository.
"""
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen
import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW = ROOT/'data/raw/strict_features/tricot'
COMMIT = '169edfaba947b5afee52c1e217e0ff275fb71e34'


def run():
    RAW.mkdir(parents=True, exist_ok=True)
    candidates = json.loads((ROOT/'data/strict_tricot_candidates.json').read_text())
    manifest = ROOT/'data/strict_tricot_sources.json'
    previous = {x['file']: x for x in json.loads(manifest.read_text())} if manifest.exists() else {}
    def one(candidate):
        path = RAW/candidate['file']
        url = f'https://raw.githubusercontent.com/AgrDataSci/tricot-data/{COMMIT}/data/'+path.name
        if not path.exists():
            path.write_bytes(urlopen(url, timeout=60).read())
        data = path.read_bytes()
        sha = hashlib.sha256(data).hexdigest()
        if path.name in previous:
            assert sha == previous[path.name]['sha256'], path.name
        d = json.loads(data)
        return dict(**candidate, url=url, bytes=len(data), sha256=sha,
                    genotypes=len(d['metadata']['genotypes']), variables=d['metadata']['variables'])
    with ThreadPoolExecutor(max_workers=4) as pool:
        sources = list(pool.map(one, candidates))
    manifest.write_text(json.dumps(sources, indent=2)+'\n')
    audit = []
    for source in sources:
        d = json.loads((RAW/source['file']).read_text())
        traits = [x['variable_name'] for x in d['metadata']['variables']
                  if x['value_type'] == 'rank' and 'overall' in x['description'].lower()]
        common = {k: source[k] for k in ['file', 'crop', 'country', 'participants', 'genotypes']}
        if not traits:
            audit.append(dict(**common, status='no_overall_ranking_trait', eligible=False))
        for trait in traits:
            rows = [x for x in d['plot_data'] if x['trait'] == trait]
            for moment in sorted(set(x['collection_moment'] for x in rows)):
                reports = defaultdict(list)
                for x in rows:
                    if x['collection_moment'] == moment:
                        reports[x['block_id']].append(x)
                valid = 0
                patterns = Counter()
                for report in reports.values():
                    values = sorted(str(x['value']) for x in report)
                    patterns['|'.join(values)] += 1
                    valid += (len(report) == 3 and len(set(x['genotype_name'] for x in report)) == 3
                        and values == ['1', '2', '3'] and all(x['value_type'] == 'rank' for x in report))
                eligible = valid == len(reports) and valid > 0
                audit.append(dict(**common, trait=trait, moment=moment,
                    reported_assessments=len(reports), strict_complete_reports=valid,
                    non_strict_or_incomplete_reports=len(reports)-valid,
                    absent_assessments=len(d['block_data'])-len(reports),
                    rank_patterns=json.dumps(dict(patterns), sort_keys=True),
                    eligible=eligible, status='eligible' if eligible else 'non_strict_reports_present'))
    out = ROOT/'results/strict_features/tricot_eligibility.csv'
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(audit).to_csv(out, index=False)
    print(pd.DataFrame(audit)[['file', 'eligible', 'status']].to_string(index=False))
    print('Eligible tasks:', sum(x['eligible'] for x in audit), '; model fits: 0')


if __name__ == '__main__':
    run()
