from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum, IntEnum
from typing import Any


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class PrincipalKind(str, Enum):
    HUMAN = "human"
    WORKLOAD = "workload"
    AGENT = "agent"
    SERVICE = "service"
    TOOL = "tool"


class AuthorityTier(IntEnum):
    INFORMATIONAL = 0
    READ_ONLY = 1
    REVERSIBLE_INTERNAL = 2
    CONTROLLED_EXTERNAL = 3
    HIGH_IMPACT_REGULATED = 4
    PROHIBITED_AUTONOMOUS = 5


class ApprovalStatus(str, Enum):
    NOT_REQUIRED = "not_required"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


@dataclass(frozen=True)
class PrincipalIdentity:
    principal_id: str
    kind: PrincipalKind
    issuer: str
    tenant_id: str
    authn_method: str
    roles: tuple[str, ...] = ()
    attributes: dict[str, str] = field(default_factory=dict)
    key_thumbprint: str | None = None


@dataclass(frozen=True)
class AgentExecutionIdentity:
    execution_id: str
    agent_id: str
    agent_spec_version: str
    human_subject_id: str
    workload_principal_id: str
    tenant_id: str
    case_id: str
    run_id: str
    task_id: str
    started_at: datetime


@dataclass(frozen=True)
class ApprovalBinding:
    approval_id: str | None
    status: ApprovalStatus
    approver_subject_ids: tuple[str, ...] = ()
    decision_digest: str | None = None
    expires_at: datetime | None = None
    required_count: int = 0


@dataclass(frozen=True)
class AuthorizationGrant:
    grant_id: str
    issuer: str
    subject_execution_id: str
    human_actor_id: str
    workload_principal_id: str
    tenant_id: str
    case_id: str
    run_id: str
    task_id: str
    purpose: str
    audience: str
    intended_tool: str
    operations: tuple[str, ...]
    resource_prefixes: tuple[str, ...]
    data_scopes: tuple[str, ...]
    region_allowlist: tuple[str, ...]
    max_authority_tier: int
    max_uses: int
    max_tool_calls: int
    max_records: int
    max_bytes: int
    max_external_messages: int
    monetary_limit_cad: float
    reversible_only: bool
    delegation_depth: int
    max_delegation_depth: int
    approval: ApprovalBinding
    proof_key_thumbprint: str
    issued_at: datetime
    not_before: datetime
    expires_at: datetime
    nonce: str
    parent_grant_id: str | None = None
    revocation_ref: str | None = None


@dataclass(frozen=True)
class ProofOfPossession:
    proof_id: str
    grant_id: str
    key_thumbprint: str
    method: str
    audience: str
    operation: str
    resource: str
    request_nonce: str
    body_digest: str
    issued_at: datetime
    signature: str


@dataclass(frozen=True)
class ToolInvocationContext:
    tenant_id: str
    case_id: str
    run_id: str
    task_id: str
    execution_id: str
    human_actor_id: str
    workload_principal_id: str
    tool_id: str
    audience: str
    operation: str
    resource: str
    data_scope: str
    region: str
    authority_tier: AuthorityTier
    record_count: int = 0
    byte_count: int = 0
    external_messages: int = 0
    estimated_cost_cad: float = 0.0
    method: str = "POST"
    body_digest: str = ""


@dataclass(frozen=True)
class BlastRadiusBudget:
    budget_id: str
    tenant_id: str
    case_id: str
    run_id: str
    authority_tier_ceiling: AuthorityTier
    allowed_tools: tuple[str, ...]
    per_tool_call_limits: dict[str, int]
    max_total_calls: int
    max_records: int
    max_bytes: int
    max_external_messages: int
    max_cost_cad: float
    max_concurrent_writes: int
    region_allowlist: tuple[str, ...]
    data_scope_allowlist: tuple[str, ...]
    egress_domain_allowlist: tuple[str, ...] = ()
    reversible_only: bool = True
    emergency_stop: bool = False


@dataclass(frozen=True)
class PolicyDecision:
    decision_id: str
    allowed: bool
    reason_codes: tuple[str, ...]
    grant_id: str | None
    budget_id: str | None
    evaluated_at: datetime
    authority_effect: str = "none"


@dataclass
class BudgetConsumption:
    total_calls: int = 0
    per_tool_calls: dict[str, int] = field(default_factory=dict)
    records: int = 0
    bytes: int = 0
    external_messages: int = 0
    cost_cad: float = 0.0
    active_writes: int = 0


def to_dict(value: Any) -> dict[str, Any]:
    return asdict(value)
