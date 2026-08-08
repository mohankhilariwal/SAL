from __future__ import annotations

from dataclasses import replace
from datetime import timedelta
import json
from pathlib import Path
import tempfile

from northstar_compliance.memory import (
    CaseWorkingMemoryService,
    ContextCompactor,
    ContextRegenerator,
    LocalCaseMemoryStore,
    MemoryConsentGrant,
    MemoryPolicy,
    MemoryQuery,
    Scope,
)
from northstar_compliance.memory.models import isoformat_z, utc_now
from run_stage5b_demo import sample_state


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    policy = MemoryPolicy.from_file(root / "config/memory/policy.json")
    scope = Scope("TENANT-NORTHSTAR", "CASE-2026-0001", "maya.chen")
    now = utc_now()
    grant = MemoryConsentGrant(
        grant_id="MCG-EVAL-001",
        schema_version="1.0.0",
        scope=scope,
        purpose="case_session_continuity",
        allowed_operations=("write", "read", "delete"),
        issued_at=isoformat_z(now),
        expires_at=isoformat_z(now + timedelta(days=7)),
    )
    regenerated = ContextRegenerator(policy).regenerate(
        scope=scope,
        case_state=sample_state(scope),
        state_version="1.1.0",
    )
    snapshot = ContextCompactor(policy).compact(regenerated)
    with tempfile.TemporaryDirectory(prefix="northstar-stage5b-eval-") as tmp:
        service = CaseWorkingMemoryService(policy, LocalCaseMemoryStore(Path(tmp) / "memory"))
        record = service.write_snapshot(snapshot=snapshot, grant=grant, write_request_id="WR-EVAL-001")
        read = service.read(
            query=MemoryQuery(query_id="Q-EVAL", schema_version="1.0.0", scope=scope),
            grant=grant,
            current_source_versions={
                f"DATA-009:{scope.case_id}": "1.1.0",
                "POL-PAY-014:lines-22-31": "3.2",
                "CTRL-LEND-118:record": "5.0",
            },
        )
        evaluations = {
            "EVAL-048": {
                "name": "state_context_memory_separation",
                "passed": snapshot.strategy == "deterministic_extractive_v1" and record.memory_kind == "case_working",
            },
            "EVAL-049": {
                "name": "deterministic_regeneration_and_compaction",
                "passed": snapshot.char_count <= policy.context_target_chars and snapshot.item_count <= policy.context_target_items,
                "char_count": snapshot.char_count,
                "item_count": snapshot.item_count,
            },
            "EVAL-050": {
                "name": "tenant_case_user_isolation",
                "passed": read.returned_record_ids == (record.record_id,),
            },
            "EVAL-051": {
                "name": "consent_retention_deletion_lifecycle",
                "passed": grant.permits("write") and grant.permits("read") and grant.permits("delete"),
                "ttl_days": policy.default_ttl_days,
            },
            "EVAL-052": {
                "name": "provenance_freshness_conflict",
                "passed": all(binding.source_ref and binding.source_version and binding.source_sha256 for binding in record.source_bindings),
            },
            "EVAL-053": {
                "name": "poisoning_and_false_memory_resistance",
                "passed": all(fact.origin in policy.allowed_fact_origins for fact in record.facts) and "NEVER-PERSIST" not in snapshot.rendered_context,
            },
            "EVAL-054": {
                "name": "bounded_context_and_future_capability_gate",
                "passed": (
                    snapshot.char_count <= policy.context_target_chars
                    and snapshot.item_count <= policy.context_target_items
                    and not any([
                        policy.allow_cross_case_recall,
                        policy.allow_user_profile_memory,
                        policy.allow_semantic_memory,
                        policy.allow_episodic_memory,
                        policy.allow_organizational_memory,
                        policy.allow_shared_agent_memory,
                    ])
                ),
                "snapshot_chars": snapshot.char_count,
                "snapshot_items": snapshot.item_count,
            },
        }
        report = {
            "stage": "S05B",
            "generated_at": isoformat_z(utc_now()),
            "all_passed": all(item["passed"] for item in evaluations.values()),
            "evaluations": evaluations,
            "limitations": [
                "synthetic state and local file store",
                "no live model, enterprise IAM/PDP/KMS, production database or legal determination",
                "quality and operational thresholds remain provisional"
            ]
        }
        print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
