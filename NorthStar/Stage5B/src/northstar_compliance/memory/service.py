from __future__ import annotations

from dataclasses import replace
from datetime import timedelta
from pathlib import Path
from typing import Mapping

from .canonical import sha256_hex
from .models import (
    CaseWorkingMemoryRecord,
    ContextSnapshot,
    MemoryConsentGrant,
    MemoryDeletionRequest,
    MemoryLifecycleResult,
    MemoryQuery,
    MemoryReadResult,
    Scope,
    isoformat_z,
    parse_datetime,
    utc_now,
)
from .policy import MemoryPolicy
from .store import LocalCaseMemoryStore


class CaseWorkingMemoryService:
    def __init__(self, policy: MemoryPolicy, store: LocalCaseMemoryStore):
        self.policy = policy
        self.store = store
        self.policy.validate_boundary()

    def write_snapshot(
        self,
        *,
        snapshot: ContextSnapshot,
        grant: MemoryConsentGrant,
        write_request_id: str,
        authorized_user_ids: tuple[str, ...] | None = None,
        ttl_days: int | None = None,
    ) -> CaseWorkingMemoryRecord:
        self._validate_grant(grant, snapshot.scope, "write")
        if snapshot.strategy != "deterministic_extractive_v1":
            raise ValueError("only_deterministic_extractive_snapshot_may_be_persisted")
        ttl = ttl_days or self.policy.default_ttl_days
        if ttl <= 0 or ttl > self.policy.max_ttl_days:
            raise ValueError("memory_ttl_out_of_policy")
        if len(snapshot.facts) > self.policy.max_facts_per_record:
            raise ValueError("too_many_memory_facts")
        for fact in snapshot.facts:
            if fact.origin not in self.policy.allowed_fact_origins:
                raise ValueError("model_generated_or_unapproved_memory_origin")
            if len(str(fact.value)) > self.policy.max_value_chars:
                raise ValueError("memory_fact_value_too_large")
            if not fact.source.source_ref or not fact.source.source_version or not fact.source.source_sha256:
                raise ValueError("memory_fact_missing_provenance")
            self._reject_forbidden_fields(fact.field_name, fact.value)

        existing = self.store.find_by_write_request(snapshot.scope, write_request_id)
        proposed_fingerprint = sha256_hex(
            {
                "snapshot": snapshot.content_sha256,
                "grant": grant.grant_id,
                "users": list(authorized_user_ids or (snapshot.scope.user_id,)),
                "ttl": ttl,
            }
        )
        if existing is not None:
            existing_fingerprint = sha256_hex(
                {
                    "snapshot": next((b.source_sha256 for b in existing.source_bindings if b.source_ref == f"DATA-080:{existing.source_snapshot_id}"), snapshot.content_sha256),
                    "grant": existing.consent_grant_id,
                    "users": list(existing.authorized_user_ids),
                    "ttl": (parse_datetime(existing.expires_at) - parse_datetime(existing.created_at)).days,
                }
            )
            if existing_fingerprint != proposed_fingerprint:
                raise ValueError("idempotency_key_reused_with_different_memory_content")
            return existing

        now = utc_now()
        users = tuple(sorted(set(authorized_user_ids or (snapshot.scope.user_id,))))
        if snapshot.scope.user_id not in users:
            raise PermissionError("memory_owner_must_remain_authorized")
        record_seed = {
            "scope": snapshot.scope.__dict__,
            "snapshot": snapshot.snapshot_id,
            "request": write_request_id,
        }
        record_id = f"MWR-{sha256_hex(record_seed)[:16].upper()}"
        supersedes = self.store.supersede_active(snapshot.scope, except_record_id=record_id)
        unresolved = tuple(
            str(fact.value)
            for fact in snapshot.facts
            if fact.field_name.startswith("unresolved_question.")
        )
        snapshot_binding = {
            "source_ref": f"DATA-080:{snapshot.snapshot_id}",
            "source_version": snapshot.schema_version,
            "source_sha256": snapshot.content_sha256,
            "classification": "confidential",
        }
        from .models import SourceBinding

        record = CaseWorkingMemoryRecord(
            record_id=record_id,
            schema_version="1.0.0",
            memory_kind="case_working",
            scope=snapshot.scope,
            authorized_user_ids=users,
            purpose="case_session_continuity",
            consent_grant_id=grant.grant_id,
            source_snapshot_id=snapshot.snapshot_id,
            source_bindings=(SourceBinding(**snapshot_binding),) + snapshot.source_bindings,
            facts=snapshot.facts,
            unresolved_questions=unresolved,
            created_at=isoformat_z(now),
            expires_at=isoformat_z(now + timedelta(days=ttl)),
            status="active",
            write_request_id=write_request_id,
            supersedes_record_id=supersedes,
            content_sha256="",
        )
        record = replace(record, content_sha256=self.store.compute_record_digest(record))
        self.store.save_record(record)
        return record

    def read(self, *, query: MemoryQuery, grant: MemoryConsentGrant, current_source_versions: Mapping[str, str]) -> MemoryReadResult:
        self._validate_grant(grant, query.scope, "read")
        returned = []
        stale_ids = []
        denied_ids = []
        now = utc_now()
        for record in self.store.list_records(query.scope):
            if query.scope.user_id not in record.authorized_user_ids:
                denied_ids.append(record.record_id)
                continue
            if record.status != "active" or parse_datetime(record.expires_at) <= now:
                stale_ids.append(record.record_id)
                continue
            stale = any(
                current_source_versions.get(binding.source_ref) not in {None, binding.source_version}
                for binding in record.source_bindings
                if not binding.source_ref.startswith("DATA-080:")
            )
            if stale:
                stale_ids.append(record.record_id)
                if not query.include_stale:
                    continue
            returned.append(record)
        return MemoryReadResult(
            query_id=query.query_id,
            schema_version="1.0.0",
            returned_record_ids=tuple(record.record_id for record in returned),
            stale_record_ids=tuple(stale_ids),
            denied_record_ids=tuple(denied_ids),
            records=tuple(returned),
            generated_at=isoformat_z(now),
        )

    def delete(self, *, request: MemoryDeletionRequest, grant: MemoryConsentGrant) -> MemoryLifecycleResult:
        self._validate_grant(grant, request.scope, "delete")
        record = self.store.get_record(request.scope, request.record_id)
        if request.scope.user_id not in record.authorized_user_ids:
            raise PermissionError("memory_delete_user_not_authorized")
        now = utc_now()
        tombstone = {
            "schema_version": "1.0.0",
            "record_id": record.record_id,
            "scope": request.scope.__dict__,
            "previous_status": record.status,
            "new_status": "deleted",
            "reason": request.reason,
            "request_id": request.request_id,
            "completed_at": isoformat_z(now),
            "content_removed": True,
        }
        path = self.store.delete_record_content(request.scope, record.record_id, tombstone)
        return MemoryLifecycleResult(
            request_id=request.request_id,
            schema_version="1.0.0",
            record_id=record.record_id,
            previous_status=record.status,
            new_status="deleted",
            content_removed=True,
            tombstone_path=path,
            completed_at=isoformat_z(now),
        )

    def expire_due(self, *, scope: Scope, now=None) -> tuple[MemoryLifecycleResult, ...]:
        current = now or utc_now()
        results = []
        for record in self.store.list_records(scope):
            if record.status == "active" and parse_datetime(record.expires_at) <= current:
                request = MemoryDeletionRequest(
                    request_id=f"EXP-{record.record_id}",
                    schema_version="1.0.0",
                    scope=scope,
                    record_id=record.record_id,
                    reason="retention_expired",
                    requested_at=isoformat_z(current),
                )
                tombstone = {
                    "schema_version": "1.0.0",
                    "record_id": record.record_id,
                    "scope": scope.__dict__,
                    "previous_status": record.status,
                    "new_status": "expired",
                    "reason": "retention_expired",
                    "request_id": request.request_id,
                    "completed_at": isoformat_z(current),
                    "content_removed": True,
                }
                path = self.store.delete_record_content(scope, record.record_id, tombstone)
                results.append(
                    MemoryLifecycleResult(
                        request_id=request.request_id,
                        schema_version="1.0.0",
                        record_id=record.record_id,
                        previous_status=record.status,
                        new_status="expired",
                        content_removed=True,
                        tombstone_path=path,
                        completed_at=isoformat_z(current),
                    )
                )
        return tuple(results)

    def _validate_grant(self, grant: MemoryConsentGrant | None, scope: Scope, operation: str) -> None:
        if grant is None:
            raise PermissionError(f"memory_{operation}_requires_consent")
        if grant.scope != scope:
            if grant.scope.tenant_id != scope.tenant_id:
                raise PermissionError("cross_tenant_consent_denied")
            if grant.scope.case_id != scope.case_id:
                raise PermissionError("cross_case_consent_denied")
            raise PermissionError("consent_user_scope_mismatch")
        if not grant.permits(operation):
            raise PermissionError(f"memory_{operation}_consent_invalid")
        if grant.purpose != "case_session_continuity":
            raise PermissionError("memory_purpose_mismatch")

    @staticmethod
    def _reject_forbidden_fields(field_name: str, value: object) -> None:
        forbidden_fragments = {
            "callback_token",
            "approval_token",
            "signature",
            "final_legal_conclusion",
            "final_compliance_closure",
            "hidden_chain_of_thought",
        }
        lowered = field_name.lower()
        if any(fragment in lowered for fragment in forbidden_fragments):
            raise ValueError("forbidden_sensitive_or_authority_field_in_memory")
        if isinstance(value, str) and "BEGIN SYSTEM PROMPT" in value.upper():
            raise ValueError("instruction_like_memory_content_rejected")
