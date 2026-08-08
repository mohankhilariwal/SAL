from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

from northstar_compliance.agent.models import FailureEnvelope, PrincipalContext, WRITE_TOOLS


@dataclass(frozen=True)
class ToolResult:
    status: str
    payload: dict[str, Any] = field(default_factory=dict)
    failure: FailureEnvelope | None = None
    adapter: str = "primary"


class ToolGateway:
    """Application-owned gateway. Nodes cannot call adapters directly."""

    def __init__(self, failures: dict[str, str] | None = None) -> None:
        self.failures = dict(failures or {})
        self.calls: list[tuple[str, str]] = []
        self.store: dict[tuple[str, str], dict[str, Any]] = {}
        self._fired: set[str] = set()

    @staticmethod
    def idempotency_key(tool_id: str, arguments: dict[str, Any]) -> str:
        body = json.dumps({"tool_id": tool_id, "arguments": arguments}, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(body.encode()).hexdigest()

    def _authorize(self, tool_id: str, arguments: dict[str, Any], principal: PrincipalContext) -> str | None:
        if tool_id not in {f"TOOL-{i:03d}" for i in range(1, 7)}:
            return "tool_not_allowlisted"
        if arguments.get("publication_id") != principal.publication_scope:
            return "publication_scope_mismatch"
        forbidden = {"allow_writes", "groups", "approval_granted", "principal_id"}
        if forbidden.intersection(arguments):
            return "authority_like_argument_rejected"
        if tool_id in WRITE_TOOLS and not principal.allow_writes:
            return "write_scope_denied"
        return None

    def invoke(
        self,
        tool_id: str,
        arguments: dict[str, Any],
        principal: PrincipalContext,
        *,
        adapter: str = "primary",
    ) -> ToolResult:
        self.calls.append((tool_id, adapter))
        denied = self._authorize(tool_id, arguments, principal)
        if denied:
            return ToolResult(
                status="failure",
                failure=FailureEnvelope(
                    kind="authorization", code=denied, message=denied,
                    retryable=False, stage="before_dispatch", committed=False, tool_id=tool_id,
                ),
                adapter=adapter,
            )

        mode = self.failures.get(tool_id)
        first = tool_id not in self._fired
        if first:
            self._fired.add(tool_id)
        if first and mode == "transient_read" and adapter == "primary":
            return ToolResult(
                status="failure",
                failure=FailureEnvelope(
                    kind="transient", code="temporary_unavailable", message="temporary read failure",
                    retryable=True, stage="before_dispatch", committed=False, tool_id=tool_id,
                ),
                adapter=adapter,
            )

        key = self.idempotency_key(tool_id, arguments)
        if tool_id == "TOOL-001":
            return ToolResult("success", {"sources": ["SRC-OSFI-001"], "milestone": "regulatory_sources_found"}, adapter=adapter)
        if tool_id == "TOOL-002":
            return ToolResult("success", {"controls": ["CTL-LEND-017", "CTL-PRIV-004"], "milestone": "control_candidates_found"}, adapter=adapter)
        if tool_id == "TOOL-003":
            return ToolResult("success", {"citations": ["CIT-POL-001-L10-L14"], "milestone": "authorized_evidence_retrieved"}, adapter=adapter)

        existing = self.store.get((tool_id, key))
        if existing:
            return ToolResult("success", dict(existing, _replayed=True), adapter=adapter)

        case_id = arguments["case_id"]
        if tool_id == "TOOL-004":
            payload = {"case_id": case_id, "status": "draft_unapproved", "human_review_required": True, "milestone": "draft_case_created"}
            artifact = "case"
        elif tool_id == "TOOL-005":
            payload = {"case_id": case_id, "status": "candidate_unapproved", "milestone": "candidate_mapping_saved"}
            artifact = "mapping"
        elif tool_id == "TOOL-006":
            payload = {"case_id": case_id, "status": "queued_for_human_review", "human_review_required": True, "milestone": "human_review_queued"}
            artifact = "review"
        else:
            raise AssertionError(tool_id)

        payload["artifact_type"] = artifact
        payload["idempotency_key"] = key
        self.store[(tool_id, key)] = payload
        if first and mode == "ambiguous_after_commit":
            return ToolResult(
                status="failure",
                failure=FailureEnvelope(
                    kind="ambiguous_write", code="timeout_after_dispatch", message="timeout after commit",
                    retryable=False, stage="after_dispatch", committed=None, tool_id=tool_id,
                    idempotency_key=key,
                ),
                adapter=adapter,
            )
        return ToolResult("success", payload, adapter=adapter)

    def reconcile(self, tool_id: str, idempotency_key: str) -> dict[str, Any] | None:
        found = self.store.get((tool_id, idempotency_key))
        return dict(found, _reconciled=True) if found else None
