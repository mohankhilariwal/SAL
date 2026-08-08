from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from northstar_compliance.agent.cancellation import CancellationToken
from northstar_compliance.agent.models import FailureEnvelope

@dataclass(frozen=True)
class Principal:
    subject: str
    groups: tuple[str, ...] = ("regulatory-analysts",)
    clearance: str = "internal"
    write_scope: tuple[str, ...] = (
        "draft_case",
        "candidate_mapping",
        "review_request",
    )

@dataclass(frozen=True)
class ToolInvocationRequest:
    tool_id: str
    tool_version: str
    arguments: dict[str, Any]
    principal: Principal
    idempotency_key: str | None = None

@dataclass(frozen=True)
class ToolResult:
    status: str
    payload: dict[str, Any] = field(default_factory=dict)
    failure: FailureEnvelope | None = None
    adapter: str = "primary"

@dataclass(frozen=True)
class ToolDescriptor:
    tool_id: str
    version: str
    impact: str
    required_write_scope: str | None = None

class ToolGateway:
    def __init__(self, adapters: dict[str, Callable[[ToolInvocationRequest, CancellationToken], ToolResult]], fallback_adapters: dict[str, Callable[[ToolInvocationRequest, CancellationToken], ToolResult]] | None = None):
        self.adapters = adapters
        self.fallback_adapters = fallback_adapters or {}
        self.descriptors = {
            "TOOL-001": ToolDescriptor("TOOL-001", "1.0.0", "read_only"),
            "TOOL-002": ToolDescriptor("TOOL-002", "1.0.0", "read_only"),
            "TOOL-003": ToolDescriptor("TOOL-003", "1.0.0", "read_only"),
            "TOOL-004": ToolDescriptor("TOOL-004", "1.0.0", "reversible_write", "draft_case"),
            "TOOL-005": ToolDescriptor("TOOL-005", "1.0.0", "reversible_write", "candidate_mapping"),
            "TOOL-006": ToolDescriptor("TOOL-006", "1.0.0", "reversible_write", "review_request"),
        }

    def model_view(self) -> list[dict[str, Any]]:
        return [
            {"tool_id": d.tool_id, "version": d.version, "impact": d.impact}
            for d in self.descriptors.values()
        ]

    def validate_request(self, request: ToolInvocationRequest) -> ToolDescriptor:
        descriptor = self.descriptors.get(request.tool_id)
        if descriptor is None or descriptor.version != request.tool_version:
            raise ValueError("unregistered tool/version")
        forbidden = {"principal", "write_scope", "authorization", "admin"} & set(request.arguments)
        if forbidden:
            raise ValueError(f"authority-like argument rejected: {sorted(forbidden)}")
        if descriptor.required_write_scope and descriptor.required_write_scope not in request.principal.write_scope:
            raise PermissionError("write scope denied")
        if descriptor.impact == "reversible_write" and not request.idempotency_key:
            raise ValueError("write requires idempotency key")
        return descriptor

    def invoke(self, request: ToolInvocationRequest, token: CancellationToken, *, use_fallback: bool = False) -> ToolResult:
        self.validate_request(request)
        token.raise_if_cancelled()
        adapter = self.fallback_adapters.get(request.tool_id) if use_fallback else self.adapters.get(request.tool_id)
        if adapter is None:
            return ToolResult(
                status="error",
                failure=FailureEnvelope(
                    kind="dependency",
                    code="adapter_unavailable",
                    message="No adapter is available",
                    retryable=False,
                    stage="before_dispatch",
                    tool_id=request.tool_id,
                    idempotency_key=request.idempotency_key,
                ),
                adapter="fallback" if use_fallback else "primary",
            )
        return adapter(request, token)

    def impact(self, tool_id: str) -> str:
        return self.descriptors[tool_id].impact
