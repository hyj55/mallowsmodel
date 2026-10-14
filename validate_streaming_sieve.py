"""Read-only validation of the exact-sieve computation audit; no new search."""
import csv
import json

from benchmark_streaming_sieve import PUBLIC, ROOT, CODE, INPUTS, contexts
from src.streaming_sieve import file_hash, ENGINE


def main():
    manifest=json.loads((PUBLIC/'manifest.json').read_text())
    assert manifest['code_sha256']=={p:file_hash(ROOT/p) for p in CODE}
    assert manifest['inputs_sha256']=={p:file_hash(ROOT/p) for p in INPUTS}
    for p,digest in manifest['outputs_sha256'].items():
        assert file_hash(PUBLIC/p)==digest,p
    receipts=json.loads((PUBLIC/'packings.json').read_text())
    index={(m['m'],m['integer_radius']):m for m in receipts}
    expected=contexts()
    assert len(index)==len(receipts)==manifest['shared_packings']
    assert set(index)=={(r['n'],r['integer_radius']) for r in expected}
    with (PUBLIC/'contexts.csv').open(newline='') as stream:rows=list(csv.DictReader(stream))
    assert len(rows)==len(expected)==manifest['missing_contexts']
    assert manifest['complete_packings']==sum(m['complete'] for m in receipts)
    assert manifest['recovered_fits']==0 and not manifest['statistical_definition_changed']
    for actual,want in zip(rows,expected):
        for key,value in want.items():assert actual[key]==str(value),(key,actual,want)
        meta=index[want['n'],want['integer_radius']]
        assert actual['packing_complete']==str(meta['complete'])
        assert actual['packing_so_far']==str(meta['packing_so_far'])
        assert actual['status_after']==actual['status_before'] and actual['fit_published']=='False'
        assert actual['reason']==meta['reason']
    for meta in receipts+json.loads((PUBLIC/'benchmarks.json').read_text()):
        assert meta['engine']==ENGINE
        assert meta['implementation_sha256']==dict(native=file_hash(ROOT/CODE[0]),wrapper=file_hash(ROOT/CODE[1]))
        assert meta['allocated_working_bytes']<=meta['memory_bytes']
        assert 0<=meta['resolved_permutations']<=meta['total_permutations']
        assert abs(meta['total_elapsed_seconds']-sum(s['elapsed_seconds'] for s in meta['sessions']))<1e-6
        assert meta['sessions'][-1]['retained_after']==meta['packing_so_far']
        if meta['complete']:
            assert meta['sieve_size']==meta['packing_so_far'] and meta['exact']
            assert meta['resolved_permutations']==meta['total_permutations']
        else:
            assert 'sieve_size' not in meta and meta['reason'] in (
                'packing_wall_time_budget','working_array_memory_budget')
    check=json.loads((ROOT/'results/predictive/packing_crosscheck.json').read_text())
    benchmark=json.loads((PUBLIC/'benchmarks.json').read_text())[0]
    assert benchmark['m']==10 and benchmark['integer_radius']==4
    assert benchmark['sieve_size']==check['orders']==29086
    assert benchmark['matches_original_complete_packing']
    assert benchmark['orders_sha256']==check['original_orders_sha256']
    spill=json.loads((PUBLIC/'benchmarks.json').read_text())[-1]
    assert spill['matches_original_complete_packing'] and spill['complete']
    assert spill['disk_block_writes']>0 and spill['disk_block_reads']>0
    assert spill['orders_sha256']==spill['original_orders_sha256']
    print(f'STREAMING: {len(rows)} contexts, {len(receipts)} shared packing attempts; '
          'code, exact reference sequence, status mapping, and unchanged predictions verified')


if __name__=='__main__':main()
