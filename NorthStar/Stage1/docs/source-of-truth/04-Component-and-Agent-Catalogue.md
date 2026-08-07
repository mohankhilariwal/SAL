# 04 - Component and Agent Catalogue

**Version:** 0.2.0

| ID | Name | Responsibility | S01 status |
|---|---|---|---|
| CMP-001 | Analyst Experience Portal | Intake, evidence display, status, review and approval UX. | Partial: local CLI only |
| CMP-002 | Regulatory Intake Boundary | Source registration, validation and provenance. | Implemented for bounded text/Markdown |
| CMP-003 | Case and Workflow Orchestration Boundary | Case state, workflow control and structured results. | Partial: single-turn orchestration; no case state |
| CMP-004 | Knowledge and Evidence Access Boundary | Authorized retrieval and evidence attribution. | Planned; Stage 2 trigger |
| CMP-005 | Enterprise Integration Boundary | Typed adapters to enterprise and external systems. | Planned |
| CMP-006 | Human Review and Approval Boundary | Risk-based review, approval, override and escalation. | Planned; only status semantics exist |
| CMP-007 | Identity, Authorization and Policy Boundary | Identity, scoped authority and deterministic enforcement. | Planned |
| CMP-008 | Evaluation and Assurance Boundary | Datasets, metrics, tests and quality gates. | Partial: local unit/integration/evaluation tests |
| CMP-009 | Observability and Audit Boundary | Traces, audit events and evidence packages. | Partial: local invocation and evidence artifacts |
| CMP-010 | Runtime and Deployment Boundary | Runtime, persistence, resilience and promotion. | Partial: local Python package and scripts |
| CMP-011 | Source-of-Truth Governance Pack | Authoritative artefacts and validation. | Implemented and updated |

## Agent inventory

No agent identifier is allocated. The S01 system performs one model call inside deterministic application code, does not choose tools, does not loop, does not update durable business state and does not pursue a goal autonomously.

## Tool inventory

No executable tool identifier is allocated. The CLI, intake function, model adapter and local store are application modules, not model-selectable tools.

## Interface status

The conceptual S00 interfaces `INT-001` through `INT-008` remain accepted. S01 specializes them only within the following boundaries:

- `INT-001` controlled publication intake: implemented locally.
- `INT-002` single-turn preliminary summary request/response: implemented through the model protocol and validated summary schema.
- `INT-003` case/workflow interface: not implemented beyond in-process one-shot flow.
- `INT-004` knowledge/evidence query: not implemented.
- `INT-005` enterprise integration: not implemented.
- `INT-006` human review/approval: not implemented beyond mandatory status fields.
- `INT-007` evaluation/assurance: implemented locally.
- `INT-008` observability/runtime health: partially implemented through invocation records and process failures.
