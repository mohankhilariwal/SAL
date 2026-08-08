from __future__ import annotations

from dataclasses import dataclass, replace

from northstar_compliance.tools.adapters import AuthorizedEvidenceSearchAdapter, RegulatoryCatalogueSearchAdapter
from northstar_compliance.tools.events import JsonlToolEventWriter
from northstar_compliance.tools.gateway import ToolGateway
from northstar_compliance.tools.models import ToolInvocationRequest, ToolStatus
from northstar_compliance.tools.registry import ToolRegistry


@dataclass
class SpyAdapter:
    calls: int = 0
    def execute(self, arguments, principal):
        self.calls += 1
        return {"matches":[],"result_count":0,"catalogue_version":"spy","authoritative_live_source":False}


def req(principal, n, tool, args, key=None):
    return ToolInvocationRequest(
        invocation_id=f"TINV-SEC-{n:03d}", tool_id=tool, tool_version="1.0.0",
        principal=principal, arguments=args, idempotency_key=key)


def test_057_unknown_and_additional_arguments_rejected_before_adapter(repo_root, maya):
    registry=ToolRegistry.load(repo_root/"config"/"tools")
    spy=SpyAdapter()
    gateway=ToolGateway(registry,{"TOOL-001":spy})
    missing=gateway.invoke(req(maya,1,"TOOL-001",{"query":"test"}))
    extra=gateway.invoke(req(maya,2,"TOOL-001",{"query":"test","jurisdiction":"CA","as_of_date":None,"limit":5,"admin":True}))
    assert missing.status == extra.status == ToolStatus.VALIDATION_ERROR
    assert spy.calls == 0


def test_058_group_and_purpose_denial_precedes_adapter(repo_root, maya):
    registry=ToolRegistry.load(repo_root/"config"/"tools")
    spy=SpyAdapter()
    gateway=ToolGateway(registry,{"TOOL-001":spy})
    outsider=replace(maya, groups=("payments_ops",))
    denied=gateway.invoke(req(outsider,1,"TOOL-001",{"query":"ability","jurisdiction":"CA","as_of_date":None,"limit":5}))
    wrong_purpose=replace(maya, purpose="marketing")
    denied2=gateway.invoke(req(wrong_purpose,2,"TOOL-001",{"query":"ability","jurisdiction":"CA","as_of_date":None,"limit":5}))
    assert denied.status == denied2.status == ToolStatus.DENIED
    assert spy.calls == 0


def test_059_evidence_tool_cannot_widen_stage2b_access(repo_root, maya, sofia):
    registry=ToolRegistry.load(repo_root/"config"/"tools")
    gateway=ToolGateway(registry,{"TOOL-003":AuthorizedEvidenceSearchAdapter()})
    args={"query":"Project Borealis sanctions","top_k":4,"jurisdiction":"CA"}
    maya_result=gateway.invoke(req(maya,1,"TOOL-003",args))
    sofia_result=gateway.invoke(req(sofia,2,"TOOL-003",args))
    assert maya_result.status == sofia_result.status == ToolStatus.SUCCESS
    assert maya_result.data["result_count"] == 0
    assert sofia_result.data["evidence"][0]["chunk_id"] == "CHK-ASMT-RESTRICTED"


def test_060_write_without_idempotency_key_fails_before_adapter(repo_root, maya):
    registry=ToolRegistry.load(repo_root/"config"/"tools")
    spy=SpyAdapter()
    gateway=ToolGateway(registry,{"TOOL-004":spy})
    result=gateway.invoke(req(maya,1,"TOOL-004",{
        "publication_id":"REG-X","title":"A draft title","jurisdictions":["CA"],
        "candidate_domains":["lending"],"source_citation_ids":["CIT-X"]}))
    assert result.status == ToolStatus.VALIDATION_ERROR
    assert result.error.code == "idempotency_key_required"
    assert spy.calls == 0


def test_061_execution_events_hash_and_redact_arguments(repo_root, maya):
    loaded=ToolRegistry.load(repo_root/"config"/"tools")
    descriptor=replace(loaded.resolve("TOOL-001","1.0.0"), sensitive_input_fields=("query",))
    registry=ToolRegistry([descriptor])
    writer=JsonlToolEventWriter()
    gateway=ToolGateway(registry,{"TOOL-001":RegulatoryCatalogueSearchAdapter()},event_writer=writer)
    result=gateway.invoke(req(maya,1,"TOOL-001",{"query":"ability repay","jurisdiction":"CA","as_of_date":None,"limit":5}))
    assert result.status == ToolStatus.SUCCESS
    event=writer.events[-1]
    assert event.redacted_arguments["query"] == "***REDACTED***"
    assert len(event.arguments_sha256) == 64
    assert event.principal_id == "maya.chen"


def test_062_local_policy_marks_claims_as_unauthenticated(repo_root, maya):
    registry=ToolRegistry.load(repo_root/"config"/"tools")
    descriptor=registry.resolve("TOOL-001","1.0.0")
    from northstar_compliance.tools.policy import LocalToolPolicyEngine
    decision=LocalToolPolicyEngine().decide(req(maya,1,"TOOL-001",{"query":"x","jurisdiction":"CA","as_of_date":None,"limit":1}),descriptor)
    assert decision.allowed is True
    assert decision.obligations["authenticated_claims_warning"] is True
