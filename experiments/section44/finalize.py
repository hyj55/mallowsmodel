"""Write the public artifact manifest after reporting and verification."""
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from experiments.section44.run import HERE,OUTPUT,sha,write_json


def main():
    files={str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob('*'))
           if p.is_file() and '__pycache__' not in p.parts and '.pytest_cache' not in p.parts
           and p!=OUTPUT/'manifest.json'}
    write_json(OUTPUT/'manifest.json',dict(files=files,experiment='S4',
        runtime_options=dict(PYTHONINTMAXSTRDIGITS=0,OPENBLAS_NUM_THREADS=1,OMP_NUM_THREADS=1),
        execution=dict(risk_worker_limit=3,resource_worker_limit=2,
            resource_profiles_overlapped_the_last_risk_worker=True,
            timing_interpretation='Descriptive wall time on a shared workstation; tracing overhead is included in resource profiles'),
        source_provenance='Producer hashes identify estimator code before calibration; the manifest also covers reporting code',
        independent_of=['P0','E0','B0','L0','S0','S1','S2','S3','tuned_block_sieve']))
    print(f'Manifest covers {len(files)} S4 files')


if __name__=='__main__':main()
