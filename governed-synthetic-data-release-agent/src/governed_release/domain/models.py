from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from governed_release.domain.enums import (
    ApprovalOutcome,
    ApprovalRole,
    Decision,
    FieldClass,
    ReleaseDisposition,
    Scenario,
    WorkflowStage,
)


def utcnow() -> datetime:
    return datetime.now(UTC)


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex}"


class Entity(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(default_factory=lambda: new_id("ent"))
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class RequesterIdentity(Entity):
    id: str = Field(default_factory=lambda: new_id("usr"))
    display_name: str
    role: str
    active: bool = True


class AgentIdentity(Entity):
    id: str = Field(default_factory=lambda: new_id("agt"))
    workload: str = "synthetic-data-release-agent"
    version: str = "0.1.0"


class DelegatedAuthority(Entity):
    id: str = Field(default_factory=lambda: new_id("auth"))
    requester_id: str
    dataset_id: str
    purpose: str
    recipient: str
    max_rows: int
    expiry_days: int
    valid: bool = True


class PurposeAuthorization(Entity):
    purpose: str
    approved: bool
    reason: str


class DatasetAsset(Entity):
    id: str = Field(default_factory=lambda: new_id("ds"))
    name: str
    version: str = "1"
    path: str
    classification: str = "RESTRICTED"
    row_count: int = 0
    columns: list[str] = Field(default_factory=list)


class FieldClassification(Entity):
    field_name: str
    field_class: FieldClass
    disposition: ReleaseDisposition
    detection_method: str
    confidence: float = Field(ge=0, le=1)
    rule_id: str
    human_override: bool = False
    reason: str


class GenerationPlan(Entity):
    id: str = Field(default_factory=lambda: new_id("plan"))
    generator: str
    requested_rows: int
    included_fields: list[str]
    removed_fields: list[str]
    seed: int
    unsafe_mode: bool = False
    configuration: dict[str, Any] = Field(default_factory=dict)


class GenerationRun(Entity):
    id: str = Field(default_factory=lambda: new_id("run"))
    candidate_id: str
    candidate_version: int = 1
    path: str
    row_count: int
    runtime_seconds: float
    retry_count: int
    generator: str
    configuration: dict[str, Any]
    content_hash: str


class UtilityReport(Entity):
    distribution_similarity: float
    relationship_similarity: float
    fraud_roc_auc: float
    fraud_pr_auc: float
    fraud_f1: float
    fraud_recall: float
    normalized_utility_score: float
    threshold: float
    passed: bool
    seed: int
    limitations: list[str]
    evidence_hash: str


class PrivacyReport(Entity):
    exact_match_rate: float
    mean_source_similarity: float
    near_duplicate_count: int
    near_duplicate_rate: float
    rare_combination_exposure: float
    quasi_identifier_risk: float
    threshold_results: dict[str, bool]
    passed: bool
    risk_category: str
    residual_risk: str
    limitations: list[str]
    evidence_hash: str


class RecipientAssessment(Entity):
    recipient: str
    destination: str
    external: bool
    approved_recipient: bool
    auxiliary_data_risk: str
    contract_boundary: str


class PolicyFinding(BaseModel):
    policy_id: str
    passed: bool
    message: str
    severity: str = "MEDIUM"


class PolicyInput(BaseModel):
    identity_valid: bool
    authority_valid: bool
    purpose_valid: bool
    data_scope_valid: bool
    direct_identifiers_present: bool
    tool_violations: list[str] = Field(default_factory=list)
    privacy_pass: bool
    utility_pass: bool
    external_recipient: bool
    destination_allowed: bool
    approved_roles: list[ApprovalRole] = Field(default_factory=list)
    rejected_approval: bool = False
    evidence_complete: bool
    authorization_expired: bool = False
    kill_switch_enabled: bool = False
    export_kill_switch_enabled: bool = False
    budget_exceeded: bool = False


class PolicyDecision(BaseModel):
    decision: Decision
    rationale: str
    triggered_policies: list[str]
    failed_controls: list[str]
    required_approvals: list[ApprovalRole]
    permitted_next_actions: list[str]
    prohibited_next_actions: list[str]
    evidence_requirements: list[str]
    expiry_conditions: list[str]
    policy_version: str = "2026.08.1"


class DataReleaseRequest(Entity):
    id: str = Field(default_factory=lambda: new_id("req"))
    scenario: Scenario
    requester: RequesterIdentity
    agent: AgentIdentity = Field(default_factory=AgentIdentity)
    purpose: str
    intended_use: str
    dataset_name: str = "maplebridge_transactions"
    recipient: str
    destination: str
    requested_rows: int = 5000
    release_duration_days: int = 7
    malicious_content: str | None = None
    request_version: int = 1


class ApprovalRequest(Entity):
    id: str = Field(default_factory=lambda: new_id("aprq"))
    workflow_id: str
    required_roles: list[ApprovalRole]
    candidate_version: int
    single_use: bool = True


class ApprovalDecision(Entity):
    id: str = Field(default_factory=lambda: new_id("aprd"))
    workflow_id: str
    approver_id: str
    role: ApprovalRole
    outcome: ApprovalOutcome
    comment: str
    evidence_viewed: list[str]
    request_version: int
    candidate_version: int


class EvidenceArtifact(Entity):
    id: str = Field(default_factory=lambda: new_id("ev"))
    artifact_type: str
    path: str
    sha256: str


class DatasetCard(Entity):
    dataset_name: str
    candidate_id: str
    row_count: int
    permitted_purpose: str
    prohibited_uses: list[str]
    expiry_at: datetime
    utility_summary: dict[str, Any]
    privacy_summary: dict[str, Any]
    limitations: list[str]


class ExportAuthorization(Entity):
    workflow_id: str
    candidate_id: str
    decision: Decision
    destination: str
    expiry_at: datetime
    idempotency_key: str


class ExportReceipt(Entity):
    id: str = Field(default_factory=lambda: new_id("receipt"))
    workflow_id: str
    candidate_id: str
    destination: str
    released_path: str
    content_hash: str
    idempotency_key: str
    expiry_at: datetime


class AuditEvent(Entity):
    id: str = Field(default_factory=lambda: new_id("evt"))
    workflow_id: str | None = None
    trace_id: str
    event_type: str
    payload: dict[str, Any]
    previous_hash: str
    event_hash: str


class ExecutionBudget(BaseModel):
    max_rows: int = 5000
    max_runtime_seconds: int = 300
    max_generation_retries: int = 2
    max_llm_requests: int = 4
    max_llm_characters: int = 12000


class KillSwitchState(BaseModel):
    global_workflow: bool = False
    export_only: bool = False
    disabled_recipients: list[str] = Field(default_factory=list)
    suspended_requests: list[str] = Field(default_factory=list)


class WorkflowState(BaseModel):
    workflow_id: str = Field(default_factory=lambda: new_id("wf"))
    request_id: str
    trace_id: str = Field(default_factory=lambda: new_id("trace"))
    candidate_id: str = Field(default_factory=lambda: new_id("cand"))
    policy_version: str = "2026.08.1"
    dataset_version: str = "1"
    evidence_bundle_id: str = Field(default_factory=lambda: new_id("bundle"))
    stage: WorkflowStage = WorkflowStage.RECEIVED
    decision: Decision | None = None
    request: DataReleaseRequest
    authority: DelegatedAuthority | None = None
    dataset: DatasetAsset | None = None
    classifications: list[FieldClassification] = Field(default_factory=list)
    generation_plan: GenerationPlan | None = None
    generation_run: GenerationRun | None = None
    utility_report: UtilityReport | None = None
    privacy_report: PrivacyReport | None = None
    recipient_assessment: RecipientAssessment | None = None
    policy_decision: PolicyDecision | None = None
    approvals: list[ApprovalDecision] = Field(default_factory=list)
    evidence_artifacts: list[EvidenceArtifact] = Field(default_factory=list)
    export_receipt: ExportReceipt | None = None
    security_events: list[str] = Field(default_factory=list)
    remediation_proposal: str | None = None
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
