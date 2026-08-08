from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Iterable

from .canonical import sha256_hex
from .models import (
    CaseWorkingMemoryRecord,
    ContextItem,
    ContextRegenerationPlan,
    MemoryFact,
    Scope,
    SourceBinding,
    utc_now,
    isoformat_z,
)
from .policy import MemoryPolicy


@dataclass(frozen=True)
class RegeneratedContext:
    plan: ContextRegenerationPlan
    items: tuple[ContextItem, ...]
    facts: tuple[MemoryFact, ...]


class ContextRegenerator:
    """Rebuilds model context from authoritative state and optional, scoped memory.

    It intentionally performs no model call and creates no free-form summary.
    """

    def __init__(self, policy: MemoryPolicy):
        self.policy = policy
        self.policy.validate_boundary()

    def regenerate(
        self,
        *,
        scope: Scope,
        case_state: dict,
        state_version: str,
        include_memory: bool = False,
        memory_records: Iterable[CaseWorkingMemoryRecord] = (),
    ) -> RegeneratedContext:
        self._validate_state_scope(scope, case_state)
        state_payload = json.dumps(case_state, sort_keys=True, ensure_ascii=False)
        state_binding = SourceBinding(
            source_ref=f"DATA-009:{scope.case_id}",
            source_version=state_version,
            source_sha256=sha256_hex(state_payload),
            classification="confidential",
        )
        facts: list[MemoryFact] = []
        items: list[ContextItem] = []

        def add_fact(field_name: str, value: object, source: SourceBinding, origin: str) -> str:
            fact_id = f"FACT-{sha256_hex({'field': field_name, 'value': value, 'source': source.source_ref})[:16].upper()}"
            facts.append(
                MemoryFact(
                    fact_id=fact_id,
                    field_name=field_name,
                    value=value,
                    source=source,
                    origin=origin,  # type: ignore[arg-type]
                )
            )
            return fact_id

        critical_fields = {
            "case_id": case_state["case_id"],
            "status": case_state.get("status", "unknown"),
            "revision": case_state.get("revision", 0),
            "publication_id": case_state.get("publication_id"),
            "jurisdictions": case_state.get("jurisdictions", []),
            "risk_level": case_state.get("risk_level", "unassessed"),
            "preliminary_disposition": case_state.get("preliminary_disposition", "unapproved"),
        }
        critical_fact_ids = tuple(
            add_fact(field_name, value, state_binding, "authoritative_state")
            for field_name, value in critical_fields.items()
        )
        items.append(
            ContextItem(
                item_id="CTX-CASE-STATE",
                kind="case_state",
                priority=10,
                text=json.dumps(critical_fields, sort_keys=True, ensure_ascii=False),
                source=state_binding,
                scope=scope,
                authorized=True,
                fact_ids=critical_fact_ids,
            )
        )

        approval = case_state.get("human_review", {})
        approval_fact_ids = tuple(
            add_fact(f"human_review.{field}", value, state_binding, "human_decision_reference")
            for field, value in sorted(approval.items())
            if field not in {"callback_token", "approval_token", "signature"}
        )
        items.append(
            ContextItem(
                item_id="CTX-APPROVAL-STATE",
                kind="approval_state",
                priority=20,
                text=json.dumps(
                    {k: v for k, v in approval.items() if k not in {"callback_token", "approval_token", "signature"}},
                    sort_keys=True,
                    ensure_ascii=False,
                ),
                source=state_binding,
                scope=scope,
                authorized=True,
                fact_ids=approval_fact_ids,
            )
        )

        for index, question in enumerate(case_state.get("unresolved_questions", []), start=1):
            fact_id = add_fact(f"unresolved_question.{index}", question, state_binding, "authoritative_state")
            items.append(
                ContextItem(
                    item_id=f"CTX-QUESTION-{index:03d}",
                    kind="unresolved_question",
                    priority=30,
                    text=str(question),
                    source=state_binding,
                    scope=scope,
                    authorized=True,
                    fact_ids=(fact_id,),
                )
            )

        for index, evidence in enumerate(case_state.get("evidence_refs", []), start=1):
            evidence_binding = SourceBinding(
                source_ref=str(evidence["source_ref"]),
                source_version=str(evidence["source_version"]),
                source_sha256=str(evidence["source_sha256"]),
                classification=str(evidence.get("classification", "internal")),
            )
            fact_id = add_fact(f"evidence_ref.{index}", evidence["source_ref"], evidence_binding, "authoritative_state")
            items.append(
                ContextItem(
                    item_id=f"CTX-EVIDENCE-{index:03d}",
                    kind="evidence_reference",
                    priority=40 + index,
                    text=json.dumps(evidence, sort_keys=True, ensure_ascii=False),
                    source=evidence_binding,
                    scope=scope,
                    authorized=bool(evidence.get("authorized", False)),
                    fact_ids=(fact_id,),
                )
            )

        if include_memory:
            for record in memory_records:
                self._validate_memory_scope(scope, record)
                if record.status != "active":
                    continue
                memory_text = json.dumps(
                    {
                        "record_id": record.record_id,
                        "facts": [
                            {"field_name": fact.field_name, "value": fact.value, "source_ref": fact.source.source_ref}
                            for fact in record.facts
                        ],
                        "unresolved_questions": list(record.unresolved_questions),
                    },
                    sort_keys=True,
                    ensure_ascii=False,
                )
                memory_binding = SourceBinding(
                    source_ref=f"DATA-081:{record.record_id}",
                    source_version=record.schema_version,
                    source_sha256=record.content_sha256,
                    classification="confidential",
                )
                items.append(
                    ContextItem(
                        item_id=f"CTX-MEMORY-{record.record_id}",
                        kind="case_working_memory",
                        priority=70,
                        text=memory_text,
                        source=memory_binding,
                        scope=scope,
                        authorized=scope.user_id in record.authorized_user_ids,
                        fact_ids=tuple(fact.fact_id for fact in record.facts),
                    )
                )

        plan = ContextRegenerationPlan(
            plan_id=f"CRP-{sha256_hex({'scope': scope.__dict__, 'state_version': state_version, 'include_memory': include_memory})[:16].upper()}",
            schema_version="1.0.0",
            strategy="authoritative_regeneration_v1",
            scope=scope,
            state_object_id="DATA-009",
            state_version=state_version,
            include_memory=include_memory,
            max_items=self.policy.hard_max_items,
            max_chars=self.policy.hard_max_chars,
            generated_at=isoformat_z(utc_now()),
        )
        return RegeneratedContext(plan=plan, items=tuple(items), facts=tuple(facts))

    @staticmethod
    def _validate_state_scope(scope: Scope, case_state: dict) -> None:
        if case_state.get("tenant_id") != scope.tenant_id:
            raise PermissionError("tenant_scope_mismatch")
        if case_state.get("case_id") != scope.case_id:
            raise PermissionError("case_scope_mismatch")
        if case_state.get("principal_user_id") != scope.user_id:
            raise PermissionError("user_scope_mismatch")

    @staticmethod
    def _validate_memory_scope(scope: Scope, record: CaseWorkingMemoryRecord) -> None:
        if record.scope.tenant_id != scope.tenant_id:
            raise PermissionError("cross_tenant_memory_denied")
        if record.scope.case_id != scope.case_id:
            raise PermissionError("cross_case_memory_denied")
        if scope.user_id not in record.authorized_user_ids:
            raise PermissionError("memory_user_not_authorized")
