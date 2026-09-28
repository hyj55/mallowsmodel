"""Acquire only the pinned sources needed for the repeated old comparisons."""
import argparse
import hashlib
import json
from urllib.request import Request, urlopen

from src.repeated_holdout import ROOT, source_inventory


def download():
    for manifest, folder in [('data/sources.json', 'data/raw'),
            ('data/strict_feature_sources.json', 'data/raw/strict_features'),
            ('data/validation_extension_sources.json', 'data/raw/validation_extension'),
            ('data/context_followup_sources.json', 'data/raw/context_followup')]:
        for source in json.loads((ROOT / manifest).read_text()):
            if manifest.endswith('context_followup_sources.json') and source['file'] != 'breadwheat.rda':
                continue
            path = ROOT / folder / source['file']
            if not path.exists():
                request = Request(source['url'], headers={'User-Agent':'RankingResearch/1.0'})
                with urlopen(request, timeout=90) as response:
                    payload = response.read()
                assert hashlib.sha256(payload).hexdigest() == source['sha256'], source['file']
                assert 'bytes' not in source or len(payload) == source['bytes'], source['file']
                path.parent.mkdir(parents=True, exist_ok=True)
                temporary = path.with_suffix(path.suffix+'.part')
                temporary.write_bytes(payload)
                temporary.replace(path)
    return source_inventory()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    entries = source_inventory() if args.verify_only else download()
    print('VERIFIED', len(entries), 'PINNED SOURCE FILES')
