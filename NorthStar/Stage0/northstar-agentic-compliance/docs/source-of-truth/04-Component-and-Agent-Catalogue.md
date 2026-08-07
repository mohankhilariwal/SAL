# 04 - Component and Agent Catalogue

| Field | Value |
|---|---|
| Version | 0.1.0 |
| Baseline date | 2026-07-31 |
| Status | Baseline candidate |

## 1. Component catalogue

All components are conceptual boundaries at Stage 0 unless status says otherwise.

| ID | Name | Responsibility | Authority | Stage 0 status | Requirements |
|---|---|---|---|---|---|
| CMP-001 | Analyst Experience Portal | Presents intake, evidence, uncertainty, case status, review and approval actions to authorized people. | No independent business authority. | Planned | FR-007, FR-009, FR-014, FR-019 |
| CMP-002 | Regulatory Intake Boundary | Accepts publications, validates metadata, preserves source content and creates provenance records. | May register data; no compliance decision authority. | Planned | FR-001, FR-002 |
| CMP-003 | Case and Workflow Orchestration Boundary | Owns case lifecycle, structured analysis workflow, state transitions and completion semantics. | Bounded by policy and human approval. | Planned | FR-002, FR-003, FR-005-FR-009, FR-011, FR-019 |
| CMP-004 | Knowledge and Evidence Access Boundary | Ingests, retrieves, ranks and attributes authorized internal and external evidence. | Read-only by default. | Planned | FR-003-FR-006 |
| CMP-005 | Enterprise Integration Boundary | Provides typed adapters to policy, control, business, case, messaging and external source systems. | Per-adapter, least privilege. | Planned | FR-004, FR-005, FR-010, FR-018 |
| CMP-006 | Human Review and Approval Boundary | Manages review queues, approvals, rejection, override, escalation, dual control and reviewer workload. | Human decisions only. | Planned | FR-009-FR-011 |
| CMP-007 | Identity, Authorization and Policy Boundary | Resolves identity, evaluates policy, attenuates delegation and enforces tool/data/action scopes. | Security enforcement authority; cannot invent business evidence. | Planned | FR-009, FR-013, FR-015, FR-017 |
| CMP-008 | Evaluation and Assurance Boundary | Manages datasets, rubrics, evaluators, test results, quality gates and model-risk evidence. | Can block promotion; cannot approve regulatory findings. | Planned | FR-006, FR-015, FR-016, FR-020 |
| CMP-009 | Observability and Audit Boundary | Captures correlated telemetry, audit events, evidence lineage and tamper-evident case packages. | Append and verify evidence; no business decision authority. | Planned | FR-012, FR-016, FR-019, FR-020 |
| CMP-010 | Runtime and Deployment Boundary | Hosts services, state stores, model/inference adapters, queues, resilience and environment promotion. | Operational authority bounded by deployment policy. | Planned | FR-008, FR-015, FR-017, FR-018, FR-020 |
| CMP-011 | Source-of-Truth Governance Pack | Ten authoritative Markdown artefacts, stage chapter, validation script and change-control rules. | Governs accepted architecture facts and identifiers. | Implemented in S00 | FR-015, FR-020 |

## 2. Agent inventory

No agent is accepted or implemented in Stage 0.

| ID | Name | Authority | Status | Note |
|---|---|---|---|---|
| - | - | - | Empty | Agent identifiers will be allocated only when the architecture demonstrates that agent behaviour is needed. |

This empty inventory is intentional. Stage 1 begins with a basic assistant and must not mislabel it as an agent.

## 3. Tool inventory

No runtime tools are accepted or implemented in Stage 0.

| ID | Name | Impact class | Authorization | Status |
|---|---|---|---|---|
| - | - | - | - | Empty |

Tool identifiers will be assigned when a concrete contract and authority requirement are introduced.

## 4. Interface inventory

Interfaces are conceptual contracts at Stage 0.

| ID | Name | Producer | Consumer | Contract intent | Authorization |
|---|---|---|---|---|---|
| INT-001 | Regulatory Publication Intake Contract | CMP-001/CMP-002 | CMP-003 | Versioned metadata plus source content or reference. | Authenticated analyst; create-case scope. |
| INT-002 | Evidence Query Contract | CMP-003 | CMP-004 | Query, case, purpose, filters and required provenance. | Read scope constrained by case, identity and classification. |
| INT-003 | Enterprise Adapter Contract | CMP-004/CMP-003 | CMP-005 | Typed request/response, idempotency and error semantics. | Adapter-specific least privilege. |
| INT-004 | Review and Approval Contract | CMP-003 | CMP-006 | Finding set, evidence, risk, required role and decision schema. | Named reviewer and separation-of-duties policy. |
| INT-005 | Policy Decision Contract | Any enforcement point | CMP-007 | Subject, action, resource, purpose, context and decision. | Mutual service identity; deny by default. |
| INT-006 | Evaluation Event Contract | Runtime components | CMP-008 | Versioned input, output, trace reference, labels and metrics. | Approved evaluation role; protected data handling. |
| INT-007 | Audit Event Contract | All material components | CMP-009 | Attributable event, evidence references, versions and outcome. | Append-only service identity. |
| INT-008 | Runtime Health Contract | CMP-010 | CMP-001/CMP-009 | Health, status, queue, capacity and incident signals. | Operational roles only. |

## 5. Component ownership by persona

| Component | Architecture owner | Operational owner | Business/governance owner |
|---|---|---|---|
| CMP-001 | Priya | Liam | Maya |
| CMP-002 | Priya | Liam | Maya |
| CMP-003 | Priya | Liam | Daniel |
| CMP-004 | Priya | Elena/Liam | Maya/Aisha |
| CMP-005 | Priya | Liam | Aisha |
| CMP-006 | Priya | Liam | Daniel/Aisha |
| CMP-007 | Marcus | Liam | Daniel/Sofia |
| CMP-008 | Sofia/Priya | Liam | Sofia |
| CMP-009 | Liam/Marcus | Liam | Sofia/Daniel |
| CMP-010 | Elena/Liam | Liam | Priya |
| CMP-011 | Priya | Priya | Project reviewers |

## 6. Catalogue rules

1. A new component must map to at least one accepted requirement.
2. A new agent requires a role, goal, non-goals, authority, tools, context, memory, inputs, outputs, handoff, failure behaviour, termination and evaluation criteria.
3. A new tool requires impact classification, typed schema, authorization, timeout, retry, idempotency and audit semantics.
4. Planned components are not described as deployed or implemented.
5. Split, merge, rename or retirement requires impact analysis and an ADR.
