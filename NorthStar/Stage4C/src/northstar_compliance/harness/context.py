from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Callable

from northstar_compliance.common.jsonutil import canonical_json, isoformat_utc, new_id, sha256_text
from northstar_compliance.harness.models import ContextEnvelope, ContextItem


class ContextAssemblyError(RuntimeError):
    pass


@dataclass(frozen=True)
class ContextSource:
    source_id: str
    kind: str
    classification: str
    purpose: str
    authorized: bool
    priority: int
    loader: Callable[[], str]


class ContextAssembler:
    ALLOWED_KINDS = {"publication", "evidence", "run_state", "policy_context"}

    def __init__(self, *, max_items: int = 8, max_characters: int = 12_000):
        self.max_items = max_items
        self.max_characters = max_characters

    def assemble(self, *, agent_id: str, sources: list[ContextSource], now: datetime) -> ContextEnvelope:
        selected: list[ContextItem] = []
        omitted: list[str] = []
        total = 0
        for source in sorted(sources, key=lambda s: (s.priority, s.source_id)):
            if source.kind == "memory":
                raise ContextAssemblyError("memory_not_enabled")
            if source.kind not in self.ALLOWED_KINDS:
                raise ContextAssemblyError(f"unsupported_context_kind:{source.kind}")
            # Access is checked before loader invocation, so forbidden text is never assembled.
            if not source.authorized:
                omitted.append(source.source_id)
                continue
            if len(selected) >= self.max_items:
                omitted.append(source.source_id)
                continue
            content = source.loader()
            if not isinstance(content, str):
                raise ContextAssemblyError("context_loader_must_return_text")
            remaining = self.max_characters - total
            if remaining <= 0:
                omitted.append(source.source_id)
                continue
            truncated = len(content) > remaining
            bounded = content[:remaining]
            item = ContextItem(
                source_id=source.source_id,
                kind=source.kind,
                classification=source.classification,
                purpose=source.purpose,
                content=bounded,
                content_sha256=sha256_text(bounded),
                truncated=truncated,
            )
            selected.append(item)
            total += len(bounded)
            if truncated:
                omitted.append(f"{source.source_id}:truncated")
        envelope_basis = {
            "agent_id": agent_id,
            "items": [i.to_dict(include_content=True) for i in selected],
            "omitted": omitted,
            "created_at": isoformat_utc(now),
        }
        return ContextEnvelope(
            schema_version="1.0.0",
            envelope_id=new_id("CTX"),
            agent_id=agent_id,
            items=tuple(selected),
            omitted_source_ids=tuple(omitted),
            total_characters=total,
            created_at=envelope_basis["created_at"],
            content_sha256=sha256_text(canonical_json(envelope_basis)),
        )
