# 01 - Business and User Story Baseline

| Field | Value |
|---|---|
| Version | 0.1.0 |
| Baseline date | 2026-07-31 |
| Status | Baseline candidate |
| Business owner persona | Daniel Brooks, Chief Compliance Officer |
| Primary user persona | Maya Chen, Regulatory Compliance Analyst |

## 1. Organization

**NorthStar Financial Services** is a fictional regulated enterprise operating in Canada, the United States and selected European markets. It provides banking, payments, lending and insurance-related services.

NorthStar receives thousands of regulatory notices, policy updates, supervisory publications and legal changes each year. Its present process depends on manual monitoring, interpretation, mapping, review and evidence assembly across fragmented applications and teams.

## 2. Core business problem

Regulatory analysts currently spend days or weeks determining whether a publication affects NorthStar, which obligations it introduces, which jurisdictions and business units are implicated, which internal policies and controls require attention, and what evidence must be routed for review. The process is vulnerable to missed obligations, inconsistent interpretation, incomplete traceability and delayed remediation.

The project objective is not autonomous legal or compliance decision-making. It is a human-accountable, evidence-backed system that reduces cycle time and increases consistency while preserving review authority.

## 3. Personas and responsibilities

| Persona | Role | Responsibilities in the narrative |
|---|---|---|
| Maya Chen | Regulatory Compliance Analyst | Intake, triage, obligation analysis, evidence review, case preparation and analyst decisions. |
| Daniel Brooks | Chief Compliance Officer | Accountable executive, risk acceptance, high-risk approval and regulatory governance. |
| Priya Raman | Enterprise Agentic AI Architect | Architecture, progressive capability selection, contracts, boundaries and technical decisions. |
| Elena Petrov | AI Platform Engineer | Model, inference, runtime, platform integration and performance engineering. |
| Marcus Green | Cybersecurity Architect | Threat modelling, identity, authorization, secrets, trust boundaries and incident controls. |
| Sofia Alvarez | AI Governance and Model Risk Lead | AI risk classification, evaluation, model change controls, assurance and governance evidence. |
| Liam O'Connor | Site Reliability and AgentOps Engineer | Reliability, observability, deployment, capacity, incident response and operational SLOs. |
| Aisha Rahman | Business Process and Controls Owner | Policy and control ownership, remediation approval, process impact and closure evidence. |

## 4. Main user story

### US-001 - Evidence-backed regulatory impact assessment

As a regulatory compliance analyst, Maya Chen wants an AI-assisted system to analyse a new regulatory publication, identify its obligations, determine which business units, policies and controls may be affected, generate an evidence-backed impact assessment and route high-risk findings for human approval, so that NorthStar can respond faster without transferring accountability to an autonomous AI system.

Acceptance intent:

- Every material conclusion is traceable to source evidence.
- The system clearly distinguishes fact, inference and uncertainty.
- High-risk findings require human approval.
- The system does not make final legal determinations or autonomously change production policies and controls.

## 5. Supporting user stories

| ID | User story |
|---|---|
| US-002 | As Maya, I want to register a regulatory publication with source metadata and immutable provenance so that later analysis can be reproduced. |
| US-003 | As Maya, I want candidate obligations separated from explanatory text so that I can review each obligation independently. |
| US-004 | As Aisha, I want candidate mappings to policies, processes and controls with evidence and confidence so that I can validate operational impact. |
| US-005 | As Daniel, I want high-risk or uncertain findings routed to accountable reviewers so that no regulated decision is silently automated. |
| US-006 | As Sofia, I want evaluation evidence, model and prompt versions, and known limitations so that the system can pass governance review. |
| US-007 | As Marcus, I want every tool and data access scoped to the initiating user, agent purpose and case so that authority cannot expand during execution. |
| US-008 | As Liam, I want end-to-end traces, durable state and recovery information so that failed or disputed runs can be reconstructed. |
| US-009 | As Priya, I want stable contracts, identifiers and ADRs so that the architecture can evolve without losing continuity. |
| US-010 | As Maya, I want a concise executive summary generated only from approved findings so that leaders receive consistent, attributable information. |
| US-011 | As Aisha, I want remediation actions assigned, tracked and closed with evidence so that identified gaps become governed work. |
| US-012 | As an auditor, I want a tamper-evident evidence package showing sources, actions, approvals and final disposition so that the case can be independently reviewed. |

## 6. Current manual business process

```mermaid
flowchart LR
    SRC[External regulatory sources] --> M1[Maya monitors publications]
    M1 --> M2[Register and triage publication]
    M2 --> M3[Read and extract obligations]
    M3 --> M4[Identify jurisdictions and business units]
    M4 --> M5[Search policies and controls]
    M5 --> M6[Map impact and identify gaps]
    M6 --> M7[Assess risk and urgency]
    M7 --> M8[Prepare evidence package]
    M8 --> H1{Human review required}
    H1 -->|Analyst| M9[Maya reviews]
    H1 -->|High risk| D1[Daniel and Aisha approve]
    M9 --> M10[Assign remediation]
    D1 --> M10
    M10 --> M11[Track implementation and closure]
    M11 --> AUD[Audit evidence retained]
```

The process is human-accountable but fragmented, slow and difficult to reproduce. Stage 0 does not change this runtime process; it creates the stable architecture and delivery constitution for evolving it safely.

## 7. User journey baseline

| Journey step | Primary actor | Current input | Current output | Primary pain point |
|---|---|---|---|---|
| Detect publication | Maya | Websites, mailing lists, feeds | Candidate publication | Coverage is inconsistent and manual. |
| Triage relevance | Maya | Publication and metadata | Relevance decision | Criteria vary by analyst. |
| Extract obligations | Maya | Full text | Obligation notes | Time-consuming and vulnerable to omission. |
| Determine scope | Maya | Obligations and business metadata | Jurisdiction and business-unit scope | Information is scattered. |
| Map policies and controls | Maya and Aisha | Internal repositories | Candidate mappings | Search and terminology mismatch. |
| Assess risk | Maya, Aisha and Daniel | Impact evidence | Risk and urgency | Evidence quality and confidence vary. |
| Approve | Maya, Daniel and Aisha | Draft assessment | Approved findings or rework | Review queues and decision rationale are fragmented. |
| Remediate | Aisha | Approved gaps | Action plan and status | Ownership and closure evidence are disconnected. |
| Report and audit | Daniel, Sofia, auditor | Case artefacts | Executive summary and evidence package | Reconstruction requires manual effort. |

## 8. Business-process scope

### In scope

1. Publication intake, registration and provenance.
2. Relevance triage and classification.
3. Candidate obligation extraction.
4. Jurisdiction, business-unit, policy, process and control mapping.
5. Evidence retrieval and attribution.
6. Risk and urgency recommendation.
7. Human review, approval, override and escalation.
8. Draft remediation planning, assignment and tracking.
9. Executive summary generation from approved findings.
10. Audit evidence packaging, status history and closure.
11. Evaluation, monitoring, incident and change-management evidence.

### Out of scope

1. Final legal advice or authoritative legal interpretation.
2. Autonomous filing or communication with regulators.
3. Autonomous modification of production policies, controls, code or financial systems.
4. Autonomous financial transactions, customer eligibility or personnel decisions.
5. Unrestricted internet browsing or unbounded tool execution.
6. Replacement of accountable compliance, legal, risk or business owners.
7. Collection of data unrelated to regulatory-change purpose.
8. Production use of real confidential data in early local labs.
9. Claims that the system ensures legal compliance.

## 9. Business success criteria

| ID | Criterion | Initial measure | Status |
|---|---|---|---|
| BSC-001 | Faster initial impact assessment | Baseline and target established in S01; measured end-to-end from intake to review-ready draft. | Pending baseline |
| BSC-002 | Improved obligation recall | Compare reviewed obligations with a human-curated reference set. | Pending evaluation design |
| BSC-003 | Evidence completeness | Percentage of material findings with valid, accessible source evidence. | Target: 100% for approved findings |
| BSC-004 | Reduced analyst effort | Human minutes per completed assessment, including review. | Pending baseline |
| BSC-005 | Reduced missed mappings | Reviewed policy/control mappings missed by the system. | Pending evaluation design |
| BSC-006 | Controlled escalation | High-risk and low-confidence cases correctly routed to people. | Target defined in S04/S08 |
| BSC-007 | Reproducible audit | An independent reviewer can reconstruct sources, actions, versions and approvals. | Required for production readiness |
| BSC-008 | No accountability transfer | Final regulated decisions remain attributable to named human roles. | Mandatory invariant |

## 10. Narrative opening for Stage 1

Maya Chen receives an urgent regulatory publication that may affect NorthStar's lending, payments and customer-data processes. She must determine relevance quickly, but the publication is long, the internal policy landscape is fragmented and the review deadline is close. Priya Raman must first decide whether the right response is better manual workflow, deterministic automation, search, an LLM assistant, RAG, an agent or a multi-agent system. Stage 1 will derive that choice progressively rather than assume it.
