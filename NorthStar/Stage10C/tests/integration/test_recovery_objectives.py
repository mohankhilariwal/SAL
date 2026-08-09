import pytest
from northstar_compliance.readiness.recovery import ImpactTier, RecoveryObjectiveProposal

def test_1054_recovery_proposal_is_unapproved_and_non_authorizing():
    p=RecoveryObjectiveProposal('ROP',ImpactTier.TIER_A_CRITICAL_CONTROL,60,0,'Aisha','Liam','Marcus','Sofia')
    assert not p.approved and not p.tested and p.authority_effect=='none'

def test_1055_invalid_rpo_rejected():
    with pytest.raises(ValueError): RecoveryObjectiveProposal('ROP',ImpactTier.TIER_A_CRITICAL_CONTROL,60,-1,'A','L','M','S')
