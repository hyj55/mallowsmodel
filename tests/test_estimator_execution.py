"""Audit semantics: scheduling is not execution, and missing depth is not zero."""
import math
import pytest

import build_estimator_execution as audit
from experiments.section44.core import Calibration, plan


def setup_function():
    audit.ROWS.clear()
    audit.PLANS.clear()


def test_root_stop_keeps_counterfactual_batch_separate():
    audit.add('test','small','',0,'sharp',10,3,673,
              {'status':'ok','metadata':{'depth':0,'branch':'exact_sieve'}},'receipt')
    row=audit.ROWS[-1]
    assert row['actual_depth']==0 and row['used_pilot_reports']==0
    assert row['M1']>row['half_sample']
    assert row['reason_code']=='root_A_stop' # Large *hypothetical* M1 did not cause the stop.
    assert 'hypothetical' in row['parameter_role']
    assert row['terminal_block_items']==10


def test_gate_does_not_invent_depth_zero():
    audit.add('test','excluded','',0,'efficient',4,4,636,
              {'status':'outside_schedule_domain'},'receipt')
    row=audit.ROWS[-1]
    assert row['actual_depth'] is None and row['eta_selected'] is None
    assert row['depth_basis']=='not attempted'


def test_failed_second_round_is_not_an_executed_first_round():
    cfg=Calibration(A=4,c_width=1/16,K=.1,c_terminal=1/512)
    p=plan(512,128,16,.8,cfg,'sharp')
    assert p['status']=='sample_budget' and [s['batch'] for s in p['stages']]==[5,5]
    audit.add('test','budget','',0,'sharp',512,128,16,
              {'status':'ok','depth':0,'branch':'borda_fallback','schedule':p},'receipt',beta0=.8,cfg=cfg.asdict(),mode='s4')
    row=audit.ROWS[-1]
    assert row['M1']==5 and row['half_sample']==8
    assert row['actual_depth']==0 and row['used_pilot_reports']==0
    assert row['reason_code']=='sample_budget'


def test_resolution_rejection_before_zero_depth_selection():
    cfg=Calibration();p=plan(512,128,16,.8,cfg,'efficient')
    audit.add('test','search','',0,'efficient',512,128,16,
              {'status':'ok','depth':0,'branch':'hierarchy','schedule':p},'receipt',beta0=.8,cfg=cfg.asdict(),mode='s4')
    row=audit.ROWS[-1]
    assert row['eta_initial']>row['eta_selected']
    assert 'earlier_candidates_rejected' in row['reason_code']
    assert row['selected_eta_m0']<=256<row['eta_initial_m0']


def test_empty_resolution_set_has_no_selected_eta():
    audit.add('test','sparse','',0,'efficient',64,8,2,
              {'status':'ok','depth':0,'branch':'borda_fallback'},'receipt',beta0=.8,mode='capped')
    row=audit.ROWS[-1]
    assert row['eta_selected'] is None and row['reason_code']=='no_admissible_eta'
    assert row['mu']<1 and row['candidate_count']==0


def test_terminal_resource_failure_is_distinct_from_pilot_stop():
    audit.add('test','large','',0,'sharp',30,2,240,
              {'status':'sieve_resource_budget','metadata':{'depth':0,'reason':'working_array_memory_budget',
               'm':30,'estimated_bytes':10**40,'memory_bytes':2**32}},'receipt')
    row=audit.ROWS[-1]
    assert row['actual_depth']==0 and row['status']=='sieve_resource_budget'
    assert row['resource_estimated_bytes']==10**40
    assert 'root_A_stop' in row['reason_code'] and 'sieve_resource_budget' in row['reason_code']


def test_exposure_extension_not_relabelled_domain_exclusion():
    audit.add('test','extension','',0,'efficient',64,2,6048,
              {'status':'ok','depth':0,'branch':'hierarchy'},'receipt',beta0=.8,mode='capped')
    row=audit.ROWS[-1]
    assert row['lambda_']==3 and row['eta_initial']==1
    assert 'capped_lambda_extension' in row['reason_code']
    assert row['actual_depth']==0


def test_small_calibrated_width_can_fail_contraction():
    cfg=Calibration(A=4,c_width=1,K=.1)
    pid,p=audit.make_plan(64,16,8,.8,cfg.asdict(),'sharp','s4')
    assert p['attempts'][0]['status']=='noncontracting'
    assert p['first']['eight_w1']>=64
    assert p['attempts'][0]['used']==0


def test_sharp_pilot_leaf_size_is_not_terminal_sieve_size():
    cfg=Calibration(A=4,c_width=1/16,K=.1,c_terminal=1/512)
    p=plan(128,8,58,.8,cfg,'sharp')
    audit.add('test','blocks','',0,'sharp',128,8,58,
              {'status':'ok','depth':1,'branch':'exact_sieve','schedule':p,
               'terminal_max_items':40,'blocks':[{'items':5},{'items':8}]},'receipt',
              beta0=.8,cfg=cfg.asdict(),mode='s4')
    row=audit.ROWS[-1]
    assert row['pilot_terminal_block_max']==40
    assert row['terminal_block_items']==8


def test_cross_platform_plan_check_keeps_integer_decisions_exact():
    audit.compare_plan_values({'ell':2.,'batch':10},{'ell':math.nextafter(2.,3.),'batch':10})
    with pytest.raises(AssertionError):
        audit.compare_plan_values({'ell':2.,'batch':10},{'ell':2.,'batch':11})
    with pytest.raises(AssertionError):
        audit.compare_plan_values({'ell':2.},{'ell':2.001})
