from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Any

from northstar_compliance.agent.cancellation import CancellationToken
from northstar_compliance.agent.models import FailureEnvelope
from .gateway import ToolInvocationRequest, ToolResult

@dataclass
class LocalStores:
    drafts: dict[str, dict[str, Any]] = field(default_factory=dict)
    mappings: dict[str, dict[str, Any]] = field(default_factory=dict)
    reviews: dict[str, dict[str, Any]] = field(default_factory=dict)

class FailureInjector:
    def __init__(self, plans: dict[str, list[str]] | None = None):
        self.plans = {k: deque(v) for k, v in (plans or {}).items()}

    def next(self, tool_id: str) -> str | None:
        q = self.plans.get(tool_id)
        return q.popleft() if q else None

class NorthStarLocalTools:
    def __init__(self, *, stores: LocalStores | None = None, failures: FailureInjector | None = None, fallback: bool = False):
        self.stores = stores or LocalStores()
        self.failures = failures or FailureInjector()
        self.fallback = fallback
        self.call_counts = defaultdict(int)

    def adapter(self, request: ToolInvocationRequest, token: CancellationToken) -> ToolResult:
        token.raise_if_cancelled()
        self.call_counts[request.tool_id] += 1
        planned = self.failures.next(request.tool_id)
        if planned:
            result = self._planned_failure(request, planned)
            if result is not None:
                return result
        return self._execute(request)

    def _planned_failure(self, request: ToolInvocationRequest, planned: str) -> ToolResult | None:
        if planned == "empty_success":
            return ToolResult(status="success", payload={"records": []}, adapter=self._adapter_name)
        if planned == "transient":
            return self._failure(request, "transient", "temporary_unavailable", True, "before_dispatch", False)
        if planned == "rate_limited":
            return self._failure(request, "rate_limited", "rate_limited", True, "before_dispatch", False)
        if planned == "timeout_before_dispatch":
            return self._failure(request, "timeout", "timeout_before_dispatch", True, "before_dispatch", False)
        if planned == "authorization":
            return self._failure(request, "authorization", "authorization_denied", False, "before_dispatch", False)
        if planned == "permanent":
            return self._failure(request, "permanent", "invalid_request", False, "before_dispatch", False)
        if planned == "timeout_after_commit":
            success = self._execute(request)
            if success.status != "success":
                return success
            return self._failure(request, "ambiguous_write", "timeout_after_dispatch", False, "after_dispatch", None)
        return None

    @property
    def _adapter_name(self) -> str:
        return "fallback" if self.fallback else "primary"

    def _failure(self, request: ToolInvocationRequest, kind: str, code: str, retryable: bool, stage: str, committed: bool | None) -> ToolResult:
        return ToolResult(
            status="error",
            failure=FailureEnvelope(
                kind=kind,
                code=code,
                message=code.replace("_", " "),
                retryable=retryable,
                stage=stage,
                committed=committed,
                tool_id=request.tool_id,
                idempotency_key=request.idempotency_key,
            ),
            adapter=self._adapter_name,
        )

    def _execute(self, request: ToolInvocationRequest) -> ToolResult:
        tid = request.tool_id
        args = request.arguments
        if tid == "TOOL-001":
            return ToolResult(status="success", payload={"records": [{"publication_id": args.get("publication_id", "PUB-001"), "title": "Synthetic lending notice"}]}, adapter=self._adapter_name)
        if tid == "TOOL-002":
            return ToolResult(status="success", payload={"controls": [{"control_id": "CTL-LEND-017", "name": "Adverse action evidence retention"}]}, adapter=self._adapter_name)
        if tid == "TOOL-003":
            # Borealis evidence is intentionally absent for Maya's internal clearance.
            return ToolResult(status="success", payload={"citations": [{"citation_id": "CIT-NS-001", "source": "POL-LEND-004", "excerpt": "Retain evidence for automated credit decisions."}]}, adapter=self._adapter_name)
        if tid == "TOOL-004":
            key = request.idempotency_key or ""
            artifact = self.stores.drafts.get(key)
            if artifact is None:
                artifact = {"case_id": f"CASE-{len(self.stores.drafts)+1:03d}", "status": "draft_unapproved", "human_review_required": True}
                self.stores.drafts[key] = artifact
            return ToolResult(status="success", payload=artifact, adapter=self._adapter_name)
        if tid == "TOOL-005":
            key = request.idempotency_key or ""
            case_id = args.get("case_id")
            artifact = self.stores.mappings.get(key)
            if artifact is None:
                artifact = {"mapping_id": f"MAP-{len(self.stores.mappings)+1:03d}", "case_id": case_id, "status": "candidate_unapproved"}
                self.stores.mappings[key] = artifact
            return ToolResult(status="success", payload=artifact, adapter=self._adapter_name)
        if tid == "TOOL-006":
            key = request.idempotency_key or ""
            case_id = args.get("case_id")
            artifact = self.stores.reviews.get(key)
            if artifact is None:
                artifact = {"review_id": f"REV-{len(self.stores.reviews)+1:03d}", "case_id": case_id, "status": "queued_for_human_review", "human_review_required": True}
                self.stores.reviews[key] = artifact
            return ToolResult(status="success", payload=artifact, adapter=self._adapter_name)
        return self._failure(request, "validation", "unknown_tool", False, "before_dispatch", False)

    def reconcile(self, tool_id: str, idempotency_key: str) -> dict[str, Any] | None:
        if tool_id == "TOOL-004":
            return self.stores.drafts.get(idempotency_key)
        if tool_id == "TOOL-005":
            return self.stores.mappings.get(idempotency_key)
        if tool_id == "TOOL-006":
            return self.stores.reviews.get(idempotency_key)
        return None
