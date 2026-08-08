from __future__ import annotations

from .canonical import sha256_hex
from .models import ContextSnapshot, MemoryFact, SourceBinding, isoformat_z, utc_now
from .policy import MemoryPolicy
from .regeneration import RegeneratedContext


class ContextCompactor:
    """Deterministic, extractive compaction.

    It never generates new facts. It selects complete typed items, preserves source
    bindings, and records every omission.
    """

    REQUIRED_KINDS = {"case_state", "approval_state"}

    def __init__(self, policy: MemoryPolicy):
        self.policy = policy
        self.policy.validate_boundary()

    def compact(
        self,
        regenerated: RegeneratedContext,
        *,
        target_items: int | None = None,
        target_chars: int | None = None,
    ) -> ContextSnapshot:
        item_limit = target_items or self.policy.context_target_items
        char_limit = target_chars or self.policy.context_target_chars
        if item_limit > self.policy.hard_max_items or char_limit > self.policy.hard_max_chars:
            raise ValueError("compaction_budget_exceeds_stage5a_boundary")

        authorized = [item for item in regenerated.items if item.authorized]
        unauthorized = [item for item in regenerated.items if not item.authorized]
        ordered = sorted(authorized, key=lambda item: (item.priority, item.item_id))
        included = []
        omitted_refs = [f"unauthorized:{item.source.source_ref}" for item in unauthorized]
        total_chars = 0

        for item in ordered:
            rendered = self._render_item(item.kind, item.text, item.source)
            required = item.kind in self.REQUIRED_KINDS
            fits = len(included) < item_limit and total_chars + len(rendered) <= char_limit
            if fits:
                included.append((item, rendered))
                total_chars += len(rendered)
            elif required:
                raise ValueError(f"required_context_item_exceeds_budget:{item.item_id}")
            else:
                omitted_refs.append(f"budget:{item.source.source_ref}")

        rendered_context = "\n\n".join(rendered for _, rendered in included)
        fact_ids = {fact_id for item, _ in included for fact_id in item.fact_ids}
        included_facts: tuple[MemoryFact, ...] = tuple(
            fact for fact in regenerated.facts if fact.fact_id in fact_ids
        )
        source_bindings: tuple[SourceBinding, ...] = tuple(
            dict.fromkeys(item.source for item, _ in included)
        )
        payload = {
            "plan_id": regenerated.plan.plan_id,
            "strategy": "deterministic_extractive_v1",
            "rendered_context": rendered_context,
            "included_item_ids": [item.item_id for item, _ in included],
            "omitted_item_refs": omitted_refs,
            "fact_ids": [fact.fact_id for fact in included_facts],
            "source_bindings": [binding.__dict__ for binding in source_bindings],
        }
        digest = sha256_hex(payload)
        return ContextSnapshot(
            snapshot_id=f"CSN-{digest[:16].upper()}",
            schema_version="1.0.0",
            plan_id=regenerated.plan.plan_id,
            scope=regenerated.plan.scope,
            strategy="deterministic_extractive_v1",
            rendered_context=rendered_context,
            included_item_ids=tuple(item.item_id for item, _ in included),
            omitted_item_refs=tuple(omitted_refs),
            facts=included_facts,
            source_bindings=source_bindings,
            char_count=len(rendered_context),
            item_count=len(included),
            created_at=isoformat_z(utc_now()),
            content_sha256=digest,
        )

    @staticmethod
    def _render_item(kind: str, text: str, source: SourceBinding) -> str:
        return (
            f"[{kind}]\n"
            f"source_ref={source.source_ref}\n"
            f"source_version={source.source_version}\n"
            f"source_sha256={source.source_sha256}\n"
            f"content={text}"
        )
