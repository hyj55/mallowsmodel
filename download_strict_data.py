"""Retrieve unchanged, pinned source bytes; no outcome-dependent cleaning."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
RAW = ROOT/'data/raw/strict_features'
PREFLIB_COMMIT = '1a8e9a9d0ad02a2a2d7473e813d1ac3057264f80'
DOTS_A_COMMIT = '8bc1331abea2fdbfb4ce75cd453565bda83f4dc7'
DOTS_B_COMMIT = 'e133bec2eb766cef2f0741d4e7d175f89a4719f4'


def sources():
    rows = []
    for code, name in [('00024', 'dots'), ('00025', 'puzzle')]:
        for i in range(1, 5):
            filename = f'{code}-{i:08d}.soc'
            path = f'datasets/{code} - {name}/{filename}'
            rows.append(dict(file=filename, repository='PrefLib/PrefLib-Data',
                             commit=PREFLIB_COMMIT, path=path, role='data'))
    for arm, commit in [('A', DOTS_A_COMMIT), ('B', DOTS_B_COMMIT)]:
        for i in range(1, 6):
            date = '06-14-2021' if arm == 'B' and i in [3, 4] else '06-08-2021'
            filename = f'{date}ratingsrankings{arm}{i}.json'
            rows.append(dict(file=filename, repository='ryankemmer/simpleRatingRanking',
                             commit=commit, path='dataOperations/'+filename, role='data'))
        for path in ['dataOperations/data_to_json.py', 'public/javascripts/rankings.js']:
            rows.append(dict(file=arm+'_'+path.replace('/', '_'),
                             repository='ryankemmer/simpleRatingRanking', commit=commit,
                             path=path, role='encoding_provenance'))
    return rows


def download():
    RAW.mkdir(parents=True, exist_ok=True)
    manifest_path = ROOT/'data/strict_feature_sources.json'
    old = {x['file']: x for x in json.loads(manifest_path.read_text())} if manifest_path.exists() else {}
    def one(row):
        row = dict(row)
        url = f"https://raw.githubusercontent.com/{row['repository']}/{row['commit']}/"+quote(row['path'])
        path = RAW/row['file']
        if not path.exists():
            path.write_bytes(urlopen(url, timeout=45).read())
        data = path.read_bytes()
        row.update(url=url, bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        if row['file'] in old and row['sha256'] != old[row['file']]['sha256']:
            raise ValueError('Source checksum changed: '+row['file'])
        return row
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(one, sources()))
    manifest_path.write_text(json.dumps(rows, indent=2)+'\n')
    print(f'Verified {len(rows)} source files, {sum(x["bytes"] for x in rows)} bytes')
    return rows


if __name__ == '__main__':
    download()
