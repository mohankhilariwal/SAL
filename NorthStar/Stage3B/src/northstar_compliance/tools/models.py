from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal

ToolStatus = Literal[
    "success",
    "replayed",
    "dry_run",
    "denied",
    "validation_error",
    "not_found",
    "version_mismatch",
    "idempotency_conflict",
    "rate_limited",
    "circuit_open",
    "timeout",
    "execution_error",
    "output_error",
]


@dataclass(frozen=True)
class ToolPrincipalContext:
    principal_id: str
    groups: tuple[str, ...]
    purpose: str
    residency: str
    clearance: str
    write_scopes: tuple[str, ...]
    correlation_id: str

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["groups"] = list(self.groups)
        data["write_scopes"] = list(self.write_scopes)
        return data


@dataclass(frozen=True)
class ToolInvocationRequest:
    tool_id: str
    tool_version: str
    arguments: dict[str, Any]
    principal: ToolPrincipalContext
    idempotency_key: str | None = None
    dry_run: bool = False


@dataclass(frozen=True)
class ToolAuthorizationDecision:
    decision_id: str
    allowed: bool
    reason: str
    obligations: tuple[str, ...]
    authenticated_claims: bool = False


@dataclass(frozen=True)
class ToolResultEnvelope:
    status: ToolStatus
    invocation_id: str
    tool_id: str
    tool_version: str
    data: dict[str, Any] | None = None
    error_code: str | None = None
    error_message: str | None = None
    authorization_decision_id: str | None = None
    replayed: bool = False
    attempts: int = 1

    @property
    def succeeded(self) -> bool:
        return self.status in {"success", "replayed", "dry_run"}

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
