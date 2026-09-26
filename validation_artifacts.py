"""Lossless storage of large recorded outputs; no statistical computation.

Default: restore exact CSV/JSONL/NPZ bytes from the committed archive parts.
--pack: package an already completed run, with hashes for every file and part.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'results/validation_extension'
ARCHIVE = OUT/'artifacts'
FILES = ('synthetic_diagnostics.csv', 'synthetic_parameters.jsonl', 'synthetic_draws.npz')
PART_BYTES = 180000


def digest(payload):
    return hashlib.sha256(payload).hexdigest()


def pack():
    buffer = io.BytesIO()
    records = []
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in FILES:
            payload = (OUT/name).read_bytes()
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, payload, compresslevel=9)
            records.append(dict(file=name, bytes=len(payload), sha256=digest(payload)))
    payload = buffer.getvalue()
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    parts = []
    for index, start in enumerate(range(0, len(payload), PART_BYTES)):
        name = f'part-{index:03d}.bin'
        part = payload[start:start+PART_BYTES]
        (ARCHIVE/name).write_bytes(part)
        parts.append(dict(file=name, bytes=len(part), sha256=digest(part)))
    keep = {item['file'] for item in parts}
    for path in ARCHIVE.glob('part-*.bin'):
        if path.name not in keep:
            path.unlink()
    manifest = dict(format='zip-parts-v1', archive_bytes=len(payload),
                    archive_sha256=digest(payload), files=records, parts=parts,
                    purpose='Lossless transport only; no modified reports, fits or statistics')
    (ARCHIVE/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps(dict(operation='pack', parts=len(parts), original_files=len(records),
                         archive_bytes=len(payload))))


def restore():
    manifest = json.loads((ARCHIVE/'manifest.json').read_text())
    assert manifest['format'] == 'zip-parts-v1'
    pieces = []
    for index, item in enumerate(manifest['parts']):
        assert item['file'] == f'part-{index:03d}.bin'
        payload = (ARCHIVE/item['file']).read_bytes()
        assert len(payload) == item['bytes'] and digest(payload) == item['sha256']
        pieces.append(payload)
    payload = b''.join(pieces)
    assert len(payload) == manifest['archive_bytes']
    assert digest(payload) == manifest['archive_sha256']
    records = {item['file']: item for item in manifest['files']}
    assert set(records) == set(FILES)
    restored = {}
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        assert sorted(archive.namelist()) == sorted(FILES)
        for name in FILES:
            raw = archive.read(name)
            item = records[name]
            assert len(raw) == item['bytes'] and digest(raw) == item['sha256']
            path = OUT/name
            if path.exists() and path.read_bytes() != raw:
                raise ValueError(f'Refusing to overwrite changed local result: {path}')
            restored[name] = raw
    for name, raw in restored.items():
        if not (OUT/name).exists():
            (OUT/name).write_bytes(raw)
    print(json.dumps(dict(operation='restore', exact_files_verified=len(restored),
                         parts_verified=len(pieces), status='passed')))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pack', action='store_true')
    args = parser.parse_args()
    pack() if args.pack else restore()
