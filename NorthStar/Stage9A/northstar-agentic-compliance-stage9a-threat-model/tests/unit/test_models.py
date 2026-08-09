import copy
import pytest
from northstar_compliance.security.threat_model.models import Score, Threat, ValidationError
from .helpers import make_engine

def test_685_score_value(): assert Score(4,5).value == 20
@pytest.mark.parametrize('l,i',[(0,1),(6,1),(1,0),(1,6)])
def test_686_invalid_score(l,i):
    with pytest.raises(ValidationError): Score(l,i).validate()
def test_687_all_threats_parse(): assert len(make_engine().threats) == 36
def test_688_authority_effect_none(): assert all(t.authority_effect == 'none' for t in make_engine().threats)
def test_689_stride_valid(): assert all(t.stride for t in make_engine().threats)
def test_690_owasp_valid(): assert all(t.owasp.startswith('ASI') for t in make_engine().threats)
def test_691_scope_counts():
    ts=make_engine().threats; assert sum(t.scope=='current' for t in ts)==28; assert sum(t.scope=='future' for t in ts)==8
