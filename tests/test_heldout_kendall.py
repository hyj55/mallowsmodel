import numpy as np
from src.heldout_kendall import report_loss,beta_audit,mean_nll


def test_display_restriction_and_report_denominator():
    y=np.array([[3,0,2],[0,3,1]])
    result=report_loss(y,[0,1,2,3])
    assert result['test_kendall_sum']==3
    assert result['test_kendall_mean']==1.5
    assert result['evaluation_count']==2


def test_population_mass_is_not_support_size():
    y=np.array([[0,1],[1,0]])
    assert report_loss(y,[0,1],[.8,.2])['test_kendall_mean']==.2
    assert report_loss(y,[0,1])['test_kendall_mean']==.5


def test_infinite_nll_still_has_finite_order_loss():
    y=np.array([[1,0]])
    assert np.isinf(mean_nll(y,dict(order=[0,1],beta=np.inf)))
    assert report_loss(y,[0,1])['test_kendall_mean']==1


def test_estimated_beta_is_not_truth_assumption():
    a=beta_audit(.3,.8,.8,dict(A=4,c_width=1/16,K=.1,c_terminal=1/512))
    assert a['beta_fit_below_beta0']
    assert not a['true_beta_below_beta0']
    assert a['constant_beta0_status']=='no_common_proof_inverse'


def test_noise_does_not_change_order_loss():
    y=np.array([[0,2,1],[2,1,0]])
    values=[mean_nll(y,dict(order=[0,1,2],beta=b)) for b in [.2,2]]
    assert values[0]!=values[1]
    assert report_loss(y,[0,1,2])['test_kendall_mean']==2
