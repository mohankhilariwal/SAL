import copy
import pytest
from northstar_compliance.security.threat_model.models import ValidationError
from .helpers import make_engine

def test_692_validation_clean(): assert make_engine().validate() == []
def test_693_digest_stable():
    e=make_engine(); assert e.canonical_digest(e.snapshot)==e.canonical_digest(copy.deepcopy(e.snapshot))
def test_694_digest_changes():
    e=make_engine(); x=copy.deepcopy(e.snapshot); x['architecture_version']='x'; assert e.canonical_digest(e.snapshot)!=e.canonical_digest(x)
@pytest.mark.parametrize('score,band',[(1,'low'),(4,'low'),(5,'moderate'),(9,'moderate'),(10,'high'),(15,'high'),(16,'critical'),(25,'critical')])
def test_695_risk_bands(score,band): assert make_engine().risk_band(score)==band
def test_696_unknown_score():
    with pytest.raises(ValidationError): make_engine().risk_band(26)
def test_697_report_counts():
    r=make_engine().report(); assert r['counts']=={'threats':36,'attack_trees':3,'misuse_cases':6,'assets':12,'flows':20,'boundaries':8}
def test_698_report_authority_none(): assert make_engine().report()['authority_effect']=='none'
def test_699_recommendations_all_none(): assert all(x['authority_effect']=='none' for x in make_engine().report()['recommendations'])
def test_700_current_treatment_present(): assert any(x['action']=='treat_before_production' for x in make_engine().report()['recommendations'])
def test_701_future_design_gate_present(): assert any(x['action']=='design_gate_before_activation' for x in make_engine().report()['recommendations'])
