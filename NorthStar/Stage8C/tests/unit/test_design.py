import pytest
from northstar_compliance.evaluation.judge_bias.design import counterbalanced_order, stable_trial_id, canonical_digest

# TEST-619..625

def test_counterbalance_even(): assert counterbalanced_order(0,0)==("control","treatment")
def test_counterbalance_odd(): assert counterbalanced_order(1,0)==("treatment","control")
def test_counterbalance_repetition(): assert counterbalanced_order(0,1)==("treatment","control")
def test_counterbalance_rejects_negative():
    with pytest.raises(ValueError): counterbalanced_order(-1,0)
def test_trial_id_stable(): assert stable_trial_id("J","P","X","control",0)==stable_trial_id("J","P","X","control",0)
def test_trial_id_changes(): assert stable_trial_id("J","P","X","control",0)!=stable_trial_id("J","P","X","treatment",0)
def test_digest_order_independent(): assert canonical_digest({"a":1,"b":2})==canonical_digest({"b":2,"a":1})
