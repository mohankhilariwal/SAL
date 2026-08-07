# 05 - Data and Schema Register

| Field | Value |
|---|---|
| Version | 0.1.0 |
| Baseline date | 2026-07-31 |
| Status | Baseline candidate; schemas are conceptual until introduced in code |

## 1. Data principles

1. The regulatory case is the principal unit of workflow state, authorization context and audit reconstruction.
2. Original source content and provenance are immutable or content-addressed after registration.
3. Facts, AI inferences, human decisions and unresolved uncertainty are distinct fields.
4. Schemas are versioned and validated at boundaries.
5. Personal, confidential and regulated data are minimized, classified and redacted in telemetry.
6. Structured business state is not replaced by model-generated memory.

## 2. Data object register

| ID | Name | Owner | Classification | Lifecycle | Stage first implemented |
|---|---|---|---|---|---|
| DATA-001 | RegulatoryPublication | CMP-002 | Internal; may contain public or licensed source content | Immutable source plus metadata; retained per policy | S01 |
| DATA-002 | RegulatoryCase | CMP-003 | Confidential business record | Mutable versioned state; durable through closure and retention | S01/S03 |
| DATA-003 | CandidateObligation | CMP-003 | Confidential analysis with source evidence | Draft, reviewed, approved, rejected or superseded | S01/S02 |
| DATA-004 | EvidenceReference | CMP-004 | Inherits source classification | Immutable reference with provenance and access metadata | S02 |
| DATA-005 | PolicyControlMapping | CMP-003/CMP-005 | Confidential | Draft through approved or rejected | S02/S03 |
| DATA-006 | RiskAssessment | CMP-003 | Confidential/high impact | Versioned; human decision recorded separately | S03/S04 |
| DATA-007 | ReviewDecision | CMP-006 | Confidential/high impact | Append-only decision event; may supersede, never overwrite history | S04 |
| DATA-008 | RemediationAction | CMP-005/CMP-006 | Confidential | Open, assigned, in progress, blocked, completed, verified, closed | S04/S10 |
| DATA-009 | AgentRunState | CMP-003/CMP-010 | Confidential operational data | Checkpointed and expired per run policy | S03/S04 |
| DATA-010 | AuthorizationGrant | CMP-007 | Restricted security data | Short lived; revocable; audit reference retained | S09 |
| DATA-011 | EvaluationRecord | CMP-008 | Internal/confidential | Versioned dataset/result record | S01/S08 |
| DATA-012 | AuditEvent | CMP-009 | Restricted evidence | Append-only; protected retention | S01/S10 |
| DATA-013 | ExecutiveSummary | CMP-003 | Confidential | Derived only from approved findings; versioned | S03/S04 |
| DATA-014 | ArchitectureArtefact | CMP-011 | Internal project record | Version-controlled and cumulative | S00 |

## 3. Conceptual schema summaries

### DATA-001 - RegulatoryPublication v0.1

```yaml
publication_id: string
schema_version: "0.1"
source_uri: string
source_name: string
publication_title: string
publication_date: date | null
retrieved_at: datetime
content_hash: string
content_location: string
jurisdictions: [string]
languages: [string]
license_or_usage_note: string | null
registered_by: human_identity
classification: data_classification
```

### DATA-002 - RegulatoryCase v0.1

```yaml
case_id: string
schema_version: "0.1"
publication_id: string
status: intake | analysing | review_pending | approved | rework | remediating | closed | cancelled
owner_user_id: string
business_owner_ids: [string]
created_at: datetime
updated_at: datetime
risk_tier: unknown | low | medium | high | critical
current_version: integer
required_approvals: [approval_requirement]
artefact_refs: [string]
trace_id: string
```

### DATA-003 - CandidateObligation v0.1

```yaml
obligation_id: string
case_id: string
schema_version: "0.1"
source_text: string
source_location: source_locator
normalized_statement: string
jurisdictions: [string]
effective_date: date | null
fact_or_inference: source_fact | system_inference
confidence: number | null
uncertainty_notes: string | null
evidence_refs: [string]
review_status: draft | accepted | rejected | needs_evidence
```

### DATA-004 - EvidenceReference v0.1

```yaml
evidence_id: string
schema_version: "0.1"
source_object_id: string
source_type: publication | policy | control | process | prior_assessment | business_metadata
source_location: source_locator
content_hash: string
retrieved_at: datetime
retrieval_method: string
access_scope: [string]
classification: data_classification
snippet: string | null
```

### DATA-005 - PolicyControlMapping v0.1

```yaml
mapping_id: string
case_id: string
obligation_id: string
policy_ids: [string]
process_ids: [string]
control_ids: [string]
business_unit_ids: [string]
evidence_refs: [string]
confidence: number | null
rationale_summary: string
status: draft | accepted | rejected | needs_review
```

### DATA-006 - RiskAssessment v0.1

```yaml
risk_assessment_id: string
case_id: string
finding_id: string
impact: low | medium | high | critical | unknown
urgency: routine | time_bound | urgent | immediate | unknown
likelihood: low | medium | high | unknown
recommended_tier: low | medium | high | critical | unknown
reason_summary: string
evidence_refs: [string]
model_or_rule_version: string
human_decision_id: string | null
```

### DATA-007 - ReviewDecision v0.1

```yaml
decision_id: string
case_id: string
reviewer_identity: string
reviewer_role: string
decision: approve | reject | request_rework | override | abstain
decision_at: datetime
reason_summary: string
evidence_refs: [string]
approval_policy_version: string
supersedes_decision_id: string | null
```

### DATA-012 - AuditEvent v0.1

```yaml
event_id: string
schema_version: "0.1"
timestamp: datetime
trace_id: string
run_id: string | null
case_id: string | null
actor_type: human | service | agent | tool | policy
actor_id: string
action: string
object_refs: [string]
version_refs: [string]
outcome: success | denied | failed | partial | cancelled
policy_decision_ref: string | null
protected_payload_ref: string | null
previous_event_hash: string | null
event_hash: string | null
```

## 4. State ownership and mutation rules

| Object | Authoritative owner | Mutation rule |
|---|---|---|
| RegulatoryPublication | CMP-002 | Metadata correction creates a new version; original content hash remains preserved. |
| RegulatoryCase | CMP-003 | Optimistic versioning; transitions must satisfy workflow policy. |
| CandidateObligation | CMP-003 | AI drafts; human review state is separate and attributable. |
| EvidenceReference | CMP-004 | Immutable after capture except access-status updates. |
| PolicyControlMapping | CMP-003 | Drafted by system; accepted only through review policy. |
| RiskAssessment | CMP-003 | Recommendation may change; human decision remains separate. |
| ReviewDecision | CMP-006 | Append-only; corrections supersede rather than overwrite. |
| AuthorizationGrant | CMP-007 | Short-lived and revocable; secrets are never stored in the case. |
| EvaluationRecord | CMP-008 | Versioned and immutable after publication. |
| AuditEvent | CMP-009 | Append-only and tamper-evident in production. |

## 5. Schema evolution rules

1. Every externally persisted or exchanged object has `schema_version`.
2. Additive backward-compatible changes increment the minor version.
3. Breaking changes require a major version, migration plan, compatibility tests and ADR.
4. Running workflows are not migrated silently.
5. Sensitive-field changes trigger privacy and telemetry impact review.
6. Data retention and deletion behaviour are part of the contract, not deployment-only settings.

## 6. Stage 0 limitations

These schemas are conceptual and intentionally incomplete. Field types, enums, constraints and storage technology are finalized only when the corresponding object is implemented. No production data has been ingested.
