from __future__ import annotations

from northstar_compliance.tools.models import ToolInvocationRequest, ToolStatus


def invoke(gateway, principal, n, tool, args, key=None):
    return gateway.invoke(ToolInvocationRequest(
        invocation_id=f"TINV-EVALUATION-{n:03d}", tool_id=tool, tool_version="1.0.0",
        principal=principal, arguments=args, idempotency_key=key,
    ))


def test_070_eval_014_all_registered_contracts_are_valid(gateway_store):
    gateway, _ = gateway_store
    assert len(gateway.registry.all()) == 6
    assert all(len(d.descriptor_hash) == 64 for d in gateway.registry.all())


def test_071_eval_015_end_to_end_gateway_preserves_draft_semantics(gateway_store, maya):
    gateway, store = gateway_store
    args={"publication_id":"REG-EVAL","title":"Evaluation case","jurisdictions":["CA"],"candidate_domains":["lending"],"source_citation_ids":["CIT-EVAL"]}
    first=invoke(gateway,maya,1,"TOOL-004",args,"EVAL-K1")
    replay=invoke(gateway,maya,2,"TOOL-004",args,"EVAL-K1")
    assert first.status == ToolStatus.SUCCESS
    assert first.data["status"] == "DRAFT_UNAPPROVED"
    assert first.data["human_review_required"] is True
    assert replay.status == ToolStatus.REPLAYED
    assert store.write_counts["cases"] == 1


def test_072_eval_016_permission_boundary_has_zero_forbidden_hits(gateway_store, maya, sofia):
    gateway, _ = gateway_store
    args={"query":"Project Borealis sanctions","top_k":4,"jurisdiction":"CA"}
    maya_result=invoke(gateway,maya,1,"TOOL-003",args)
    sofia_result=invoke(gateway,sofia,2,"TOOL-003",args)
    assert maya_result.data["result_count"] == 0
    assert sofia_result.data["result_count"] == 1


def test_073_eval_017_no_agent_or_irreversible_authority(gateway_store):
    gateway, _ = gateway_store
    assert all(d.impact_class.value in {"read_only", "reversible_write"} for d in gateway.registry.all())
    assert not any(d.approval_required for d in gateway.registry.all())
