"""Direct full-packing equality check; original engine may take several minutes."""
import hashlib
import json
from pathlib import Path
import numpy as np
from src.resource_sieve import cached_packing
from src.sieve_budget_retry import cached_ball_packing,SECONDS,MEMORY


def main():
    new,new_meta=cached_ball_packing(10,4)
    old,old_meta=cached_packing(10,4,seconds=SECONDS,memory_bytes=MEMORY)
    np.testing.assert_array_equal(new,old)
    digest=lambda a:hashlib.sha256(a.astype('<i2').tobytes()).hexdigest()
    result=dict(n=10,integer_radius=4,orders=len(new),complete_ordered_arrays_equal=True,
        original_orders_sha256=digest(old),completion_orders_sha256=digest(new),
        original_construction_seconds=old_meta['elapsed_seconds'],
        completion_construction_seconds=new_meta['elapsed_seconds'],
        seconds_limit=SECONDS,memory_bytes=MEMORY,
        verifier_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    target=Path(__file__).resolve().parent/'results/predictive/packing_crosscheck.json'
    target.write_text(json.dumps(result,indent=2)+'\n')
    print('Identical complete ordered packings:',len(new),'orders',flush=True)


if __name__=='__main__':main()
