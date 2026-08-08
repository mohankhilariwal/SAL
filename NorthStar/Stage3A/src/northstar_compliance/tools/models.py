from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Mapping


class ImpactClass(str, Enum):
    READ_ONLY = "read_only"
    REVERSIBLE_WRITE = "reversible_write"
    IRREVERSIBLE_WRITE = "irreversible_write"
    PRIVILEGED_REGULATED = "privileged_regulated"


class ToolStatus(str, Enum):
    SUCCESS = "success"
    DRY_RUN = "dry_run"
    REPLAYED = "replayed"
    DENIED = "denied"
    APPROVAL_REQUIRED = "approval_required"
    VALIDATION_ERROR = "validation_error"
    NOT_FOUND = "not_found"
    VERSION_MISMATCH = "version_mismatch"
    IDEMPOTENCY_CONFLICT = "idempotency_conflict"
    RATE_LIMITED = "rate_limited"
    CIRCUIT_OPEN = "circuit_open"
    TIMEOUT = "timeout"
    EXECUTION_ERROR = "execution_error"
    OUTPUT_VALIDATION_ERROR = "output_validation_error"
    RESULT_TOO_LARGE = "result_too_large"


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 1
    retryable_errors: tuple[str, ...] = ()


@dataclass(frozen=True)
class ToolDescriptor:
    schema_version: str
    tool_id: str
    name: str
    version: str
    description: str
    impact_class: ImpactClass
    input_schema: Mapping[str, Any]
    output_schema: Mapping[str, Any]
    allowed_groups: tuple[str, ...]
    allowed_purposes: tuple[str, ...]
    allowed_residencies: tuple[str, ...]
    timeout_ms: int
    max_result_bytes: int
    idempotency_required: bool
    approval_required: bool
    retry_policy: RetryPolicy
    sensitive_input_fields: tuple[str, ...] = ()
    descriptor_hash: str = ""


@dataclass(frozen=True)
class ToolPrincipalContext:
    principal_id: str
    groups: tuple[str, ...]
    clearance: str
    purpose: str
    residency: str
    correlation_id: str
    authenticated: bool = False


@dataclass(frozen=True)
class ToolInvocationRequest:
    invocation_id: str
    tool_id: str
    tool_version: str
    principal: ToolPrincipalContext
    arguments: Mapping[str, Any]
    idempotency_key: str | None = None
    dry_run: bool = False
    approval_reference: str | None = None


@dataclass(frozen=True)
class ToolAuthorizationDecision:
    decision_id: str
    allowed: bool
    reason_codes: tuple[str, ...]
    obligations: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ToolError:
    code: str
    message: str
    retryable: bool = False
    details: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ToolResultEnvelope:
    schema_version: str
    invocation_id: str
    tool_id: str
    tool_version: str
    status: ToolStatus
    started_at: str
    finished_at: str
    duration_ms: float
    authorization_decision_id: str | None
    attempts: int
    data: Mapping[str, Any] | None = None
    error: ToolError | None = None
    replayed: bool = False
    descriptor_hash: str | None = None

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["status"] = self.status.value
        if self.error is not None:
            value["error"] = asdict(self.error)
        return value


@dataclass(frozen=True)
class ToolExecutionEvent:
    schema_version: str
    event_id: str
    invocation_id: str
    tool_id: str
    tool_version: str
    principal_id: str
    correlation_id: str
    status: str
    arguments_sha256: str
    redacted_arguments: Mapping[str, Any]
    authorization_decision_id: str | None
    attempts: int
    duration_ms: float
    timestamp: str
    descriptor_hash: str
