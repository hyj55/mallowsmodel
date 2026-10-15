"""Separate model-producer fingerprints from current report/replay code."""
import hashlib
import json


def validate_producer(root, manifest, records=None):
    producer=json.loads((root/manifest['fit_producer']).read_text())
    saved=hashlib.sha256(json.dumps(producer['code_sha256'],sort_keys=True).encode()).hexdigest()
    current=hashlib.sha256(json.dumps(manifest['code_sha256'],sort_keys=True).encode()).hexdigest()
    assert set(manifest['record_code_signatures']) <= {saved,current}
    if 'code_signature' in producer:
        assert saved==producer['code_signature']
    if records is not None:
        assert {r['code_signature'] for r in records} == set(manifest['record_code_signatures'])
