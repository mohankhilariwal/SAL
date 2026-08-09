# 04 — Component and Agent Catalogue

**Version:** `1.18.0`

| ID | Name | Final responsibility |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Controlled user entry and evidence presentation. |
| `CMP-002` | Regulatory Intake Boundary | Validated intake; external content remains untrusted. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Sole task, route, protected-state, admission, cancellation, aggregation, termination and recovery owner. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Access-aware retrieval, provenance, citations and freshness. |
| `CMP-005` | Enterprise Integration Boundary | Only gateway to `TOOL-001`–`006`; typed validation, authorization, reconciliation and compensation. |
| `CMP-006` | Human Review and Approval Boundary | Human review, separation of duties, approval and finalization. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Sole authority issuer; receiver-side authorization, blast radius and guardrails. |
| `CMP-008` | Evaluation and Assurance Boundary | Evaluation, judge-bias, threat, topology and readiness evidence. |
| `CMP-009` | Observability and Audit Boundary | Correlated telemetry, protected-effect audit and evidence packages. |
| `CMP-010` | Runtime and Deployment Boundary | Runtime, reliability, release, capacity, SLO and DR profiles; no production route. |
| `CMP-011` | Source-of-Truth Governance Pack | Stable artefacts, ADRs, risks, traceability and `CAPSTONE-001`. |

## Agent inventory

- `AGT-001 Regulatory Impact Assessment Agent/1.1.0` — only active agent; bounded propose/complete/escalate behaviour; no approval, route, authority, protected-state, agent-creation or deployment capability.
- `WP-008`, MCP/A2A peers and all additional agents — `inactive_future`.
