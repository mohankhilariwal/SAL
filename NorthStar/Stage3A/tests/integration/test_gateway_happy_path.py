from __future__ import annotations

from northstar_compliance.tools.models import ToolInvocationRequest, ToolStatus


def invoke(gateway, principal, n, tool, args, key=None, dry_run=False):
    return gateway.invoke(
        ToolInvocationRequest(
            invocation_id=f"TINV-HAPPY-{n:03d}",
            tool_id=tool,
            tool_version="1.0.0",
            principal=principal,
            arguments=args,
            idempotency_key=key,
            dry_run=dry_run,
        )
    )


def test_052_read_tools_return_typed_results(gateway_store, maya):
    gateway, _ = gateway_store
    regulatory = invoke(gateway, maya, 1, "TOOL-001", {"query":"ability repay","jurisdiction":"CA","as_of_date":"2026-07-31","limit":5})
    controls = invoke(gateway, maya, 2, "TOOL-002", {"control_id":None,"domain":"lending"})
    evidence = invoke(gateway, maya, 3, "TOOL-003", {"query":"ability repay","top_k":4,"jurisdiction":"CA"})
    assert regulatory.status == controls.status == evidence.status == ToolStatus.SUCCESS
    assert regulatory.data["result_count"] == 1
    assert controls.data["controls"][0]["control_id"] == "CTL-LEND-017"
    assert evidence.data["evidence"][0]["citation_id"].startswith("CIT-")


def test_053_create_mapping_and_queue_preserve_unapproved_semantics(gateway_store, maya):
    gateway, store = gateway_store
    case = invoke(gateway, maya, 1, "TOOL-004", {
        "publication_id":"REG-FCAC-2026-009","title":"Consumer lending disclosure review",
        "jurisdictions":["CA"],"candidate_domains":["lending"],
        "source_citation_ids":["CIT-A2C5075B64B4E443"]}, key="CASE-K1")
    mapping = invoke(gateway, maya, 2, "TOOL-005", {
        "case_id":case.data["case_id"],"policy_id":"POL-LEND-004",
        "control_ids":["CTL-LEND-017"],"source_citation_ids":["CIT-A2C5075B64B4E443"],
        "rationale":"The evidence creates a candidate relationship for human review."}, key="MAP-K1")
    review = invoke(gateway, maya, 3, "TOOL-006", {
        "case_id":case.data["case_id"],"mapping_ids":[mapping.data["mapping_id"]],
        "reviewer_group":"compliance_reviewers"}, key="REV-K1")
    assert case.data["status"] == "DRAFT_UNAPPROVED"
    assert case.data["disposition"] == "preliminary_unapproved"
    assert mapping.data["accepted"] is False
    assert review.data["approval_granted"] is False
    assert review.data["external_notification_sent"] is False
    assert store.write_counts == {"cases":1,"mappings":1,"reviews":1}


def test_054_dry_run_has_no_side_effect(gateway_store, maya):
    gateway, store = gateway_store
    result = invoke(gateway, maya, 1, "TOOL-004", {
        "publication_id":"REG-1","title":"Dry run publication",
        "jurisdictions":["CA"],"candidate_domains":["lending"],
        "source_citation_ids":["CIT-DRYRUN"]}, key="DRY-1", dry_run=True)
    assert result.status == ToolStatus.DRY_RUN
    assert result.data["side_effect_performed"] is False
    assert store.write_counts["cases"] == 0


def test_055_same_idempotency_key_replays_one_write(gateway_store, maya):
    gateway, store = gateway_store
    args={"publication_id":"REG-2","title":"Idempotent publication","jurisdictions":["CA"],"candidate_domains":["lending"],"source_citation_ids":["CIT-IDEM"]}
    first=invoke(gateway,maya,1,"TOOL-004",args,key="IDEM-1")
    second=invoke(gateway,maya,2,"TOOL-004",args,key="IDEM-1")
    assert first.status == ToolStatus.SUCCESS
    assert second.status == ToolStatus.REPLAYED
    assert second.data == first.data
    assert store.write_counts["cases"] == 1


def test_056_idempotency_key_conflict_is_rejected(gateway_store, maya):
    gateway, store = gateway_store
    base={"publication_id":"REG-3","title":"First title","jurisdictions":["CA"],"candidate_domains":["lending"],"source_citation_ids":["CIT-IDEM"]}
    invoke(gateway,maya,1,"TOOL-004",base,key="IDEM-CONFLICT")
    changed={**base,"title":"Different title"}
    result=invoke(gateway,maya,2,"TOOL-004",changed,key="IDEM-CONFLICT")
    assert result.status == ToolStatus.IDEMPOTENCY_CONFLICT
    assert store.write_counts["cases"] == 1
