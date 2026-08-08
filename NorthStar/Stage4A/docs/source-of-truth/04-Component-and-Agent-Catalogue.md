# 04 — Component and Agent Catalogue

**Version:** `0.8.0`

| ID | Name | S04A responsibility/status |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Local graph run/cancel/resume caller and outcome/path viewer. |
| `CMP-002` | Regulatory Intake Boundary | Retained unchanged. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Implements `GRAPH-001`, typed state/patches/routes, transition checkpointing, S03C budgets/recovery and deterministic termination. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Retained synthetic authorized evidence behind gateway tools. |
| `CMP-005` | Enterprise Integration Boundary | Remains authoritative tool gateway, read fallback and write reconciliation boundary. |
| `CMP-006` | Human Review and Approval Boundary | Local queued request only; no waiting/decision service. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Partial local principal/write-scope rules; graph policy node is preflight only. |
| `CMP-008` | Evaluation and Assurance Boundary | Adds graph definition, path, state ownership, resume and recovery evaluations. |
| `CMP-009` | Observability and Audit Boundary | Local transition/checkpoint evidence only; not audit. |
| `CMP-010` | Runtime and Deployment Boundary | Python 3.13.5, single process, sequential graph. |
| `CMP-011` | Source-of-Truth Governance Pack | Updated to `0.8.0`. |

## Agent inventory

| ID | Name | Authority | Status |
|---|---|---|---|
| `AGT-001` | Regulatory Impact Assessment Agent | May propose `TOOL-001`–`006`, complete or escalate. Cannot choose node IDs/routes, mutate state, set budgets/recovery, approve/finalize, compensate, delegate, create agents or bypass `CMP-005`. | Implemented; only agent |

No second agent, specialist agent, memory agent or supervisor is introduced.
