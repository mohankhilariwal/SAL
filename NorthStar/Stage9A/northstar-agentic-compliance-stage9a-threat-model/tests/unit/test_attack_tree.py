from northstar_compliance.security.threat_model.attack_tree import leaf_risks, evaluate_boolean
from .helpers import make_engine

def test_702_attack_tree_leaves_known():
    e=make_engine(); known={t.risk_id for t in e.threats}; assert all(leaf_risks(t)<=known for t in e.trees['trees'])
def test_703_exfiltration_or_path():
    t=make_engine().trees['trees'][0]; assert evaluate_boolean(t, {'RSK-317'}) is True
def test_704_and_path_requires_both():
    t=make_engine().trees['trees'][0]; assert evaluate_boolean(t, {'RSK-311'}) is False; assert evaluate_boolean(t, {'RSK-311','RSK-321'}) is True
def test_705_tree_ids_unique():
    ids=[t['tree_id'] for t in make_engine().trees['trees']]; assert len(ids)==len(set(ids))
