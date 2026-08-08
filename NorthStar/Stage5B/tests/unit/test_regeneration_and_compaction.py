from __future__ import annotations

from dataclasses import replace

import pytest

from northstar_compliance.memory import ContextCompactor, ContextRegenerator, MemoryPolicy, Scope


def test_213_regenerates_only_from_authoritative_state(regenerator, scope, case_state):
    result = regenerator.regenerate(scope=scope, case_state=case_state, state_version="1.1.0")
    assert result.plan.strategy == "authoritative_regeneration_v1"
    assert all(f.origin in {"authoritative_state", "human_decision_reference"} for f in result.facts)


def test_214_regeneration_is_deterministic_except_timestamp(regenerator, scope, case_state):
    first = regenerator.regenerate(scope=scope, case_state=case_state, state_version="1.1.0")
    second = regenerator.regenerate(scope=scope, case_state=case_state, state_version="1.1.0")
    assert first.plan.plan_id == second.plan.plan_id
    assert first.items == second.items
    assert first.facts == second.facts


def test_215_compaction_respects_budget(compactor, regenerator, scope, case_state):
    regenerated = regenerator.regenerate(scope=scope, case_state=case_state, state_version="1.1.0")
    snapshot = compactor.compact(regenerated, target_items=4, target_chars=4000)
    assert snapshot.item_count <= 4
    assert snapshot.char_count <= 4000


def test_216_compaction_preserves_critical_state(compactor, regenerator, scope, case_state):
    regenerated = regenerator.regenerate(scope=scope, case_state=case_state, state_version="1.1.0")
    snapshot = compactor.compact(regenerated, target_items=2, target_chars=4000)
    assert "CTX-CASE-STATE" in snapshot.included_item_ids
    assert "CTX-APPROVAL-STATE" in snapshot.included_item_ids


def test_217_compaction_records_omissions(compactor, regenerator, scope, case_state):
    regenerated = regenerator.regenerate(scope=scope, case_state=case_state, state_version="1.1.0")
    snapshot = compactor.compact(regenerated, target_items=2, target_chars=4000)
    assert snapshot.omitted_item_refs
    assert any(ref.startswith("budget:") or ref.startswith("unauthorized:") for ref in snapshot.omitted_item_refs)


def test_218_unauthorized_evidence_never_enters_context(compactor, regenerator, scope, case_state):
    regenerated = regenerator.regenerate(scope=scope, case_state=case_state, state_version="1.1.0")
    snapshot = compactor.compact(regenerated)
    assert "CASE-OTHER-SECRET" not in snapshot.rendered_context
    assert any("CASE-OTHER-SECRET" in ref for ref in snapshot.omitted_item_refs)


def test_219_callback_token_is_removed(regenerator, scope, case_state):
    result = regenerator.regenerate(scope=scope, case_state=case_state, state_version="1.1.0")
    approval = next(item for item in result.items if item.kind == "approval_state")
    assert "MUST-NOT-PERSIST" not in approval.text
    assert "callback_token" not in approval.text


def test_220_scope_mismatch_fails_closed(regenerator, scope, case_state):
    other = replace(scope, case_id="CASE-OTHER")
    with pytest.raises(PermissionError, match="case_scope_mismatch"):
        regenerator.regenerate(scope=other, case_state=case_state, state_version="1.1.0")


def test_221_stage5a_hard_budget_cannot_expand(policy_path):
    import json
    raw = json.loads(policy_path.read_text())
    raw["hard_max_items"] = 9
    from tempfile import NamedTemporaryFile
    with NamedTemporaryFile("w+", suffix=".json") as handle:
        json.dump(raw, handle)
        handle.flush()
        policy = MemoryPolicy.from_file(handle.name)
        with pytest.raises(ValueError, match="stage5a_context_budget_expanded"):
            policy.validate_boundary()


def test_222_required_item_overflow_fails_closed(compactor, regenerator, scope, case_state):
    huge = dict(case_state)
    huge["jurisdictions"] = ["X" * 9000]
    regenerated = regenerator.regenerate(scope=scope, case_state=huge, state_version="1.1.0")
    with pytest.raises(ValueError, match="required_context_item_exceeds_budget"):
        compactor.compact(regenerated, target_items=2, target_chars=100)
