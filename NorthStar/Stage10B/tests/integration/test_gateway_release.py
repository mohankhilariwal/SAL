import pytest

from northstar_compliance.agentops.release import GateResult, ReleaseManager
from northstar_compliance.audit.port import AuditUnavailable, InMemoryAuditPort
from northstar_compliance.deployment.plan import DeploymentPlanner
from northstar_compliance.integration.gateway import EnterpriseIntegrationGateway, InvalidGrant


def grant(op="write", valid=True):
    return {"issuer": "CMP-007", "operation": op, "valid": valid, "grant_id": "G"}


def test_protected_effect_has_intent_and_outcome():
    audit = InMemoryAuditPort(); gw = EnterpriseIntegrationGateway(audit)
    gw.protected_write(operation="write", payload={}, idempotency_key="K", grant=grant())
    assert [e["event_type"] for e in audit.events] == ["protected_effect_intent", "protected_effect_outcome"]


def test_duplicate_effect_is_deduplicated():
    audit = InMemoryAuditPort(); gw = EnterpriseIntegrationGateway(audit)
    first = gw.protected_write(operation="write", payload={}, idempotency_key="K", grant=grant())
    second = gw.protected_write(operation="write", payload={}, idempotency_key="K", grant=grant())
    assert not first["deduplicated"] and second["deduplicated"] and len(audit.events) == 2


def test_invalid_grant_blocks():
    with pytest.raises(InvalidGrant):
        EnterpriseIntegrationGateway(InMemoryAuditPort()).protected_write(operation="write", payload={}, idempotency_key="K", grant=grant(valid=False))


def test_audit_failure_blocks_effect():
    audit = InMemoryAuditPort(fail=True); gw = EnterpriseIntegrationGateway(audit)
    with pytest.raises(AuditUnavailable): gw.protected_write(operation="write", payload={}, idempotency_key="K", grant=grant())
    assert "K" not in gw.applied


def test_reconciliation_by_idempotency_key():
    gw = EnterpriseIntegrationGateway(InMemoryAuditPort())
    assert not gw.reconcile("K")["found"]
    gw.protected_write(operation="write", payload={}, idempotency_key="K", grant=grant())
    assert gw.reconcile("K")["found"]


def test_nonproduction_promotion_can_pass():
    rm = ReleaseManager(); m = rm.build_manifest(release_id="R", environment="test", source_files={}, config={}, test_report={})
    d = rm.evaluate_promotion(m, [GateResult("unit", True, "D")], human_release_approval=True)
    assert d.allowed


def test_production_promotion_denied_even_when_tests_pass():
    rm = ReleaseManager(); m = rm.build_manifest(release_id="R", environment="production", source_files={}, config={}, test_report={})
    d = rm.evaluate_promotion(m, [GateResult("unit", True, "D")], human_release_approval=True)
    assert not d.allowed and len(d.reasons) >= 3


def test_failed_gate_denies_promotion():
    rm = ReleaseManager(); m = rm.build_manifest(release_id="R", environment="test", source_files={}, config={}, test_report={})
    assert not rm.evaluate_promotion(m, [GateResult("unit", False, "D")], human_release_approval=True).allowed


def test_human_release_approval_required():
    rm = ReleaseManager(); m = rm.build_manifest(release_id="R", environment="test", source_files={}, config={}, test_report={})
    assert not rm.evaluate_promotion(m, [GateResult("unit", True, "D")], human_release_approval=False).allowed


def test_deployment_planner_denies_production_route():
    p = DeploymentPlanner().prepare("production")
    assert not p.route_activation_allowed and p.strategy == "none"


def test_deployment_planner_reference_only():
    p = DeploymentPlanner().prepare("pre-production")
    assert not p.route_activation_allowed and p.rollback_required
