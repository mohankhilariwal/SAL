# 04 — Component and Agent Catalogue

| ID | Name | S03C responsibility/status |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Starts/cancels/resumes a local run and displays partial/recovery evidence. Partial local implementation. |
| `CMP-002` | Regulatory Intake Boundary | Retained unchanged. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Owns `AGT-001`, budgets, recovery, cancellation observation, termination and checkpoint lifecycle. Implemented locally. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Retained through `TOOL-003`; synthetic authorized evidence only. |
| `CMP-005` | Enterprise Integration Boundary | Gateway, registry, policy, local adapters, read fallback and write reconciliation. Implemented locally. |
| `CMP-006` | Human Review and Approval Boundary | Local queued request only; no reviewer workflow or decision. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Partial local principal/write-scope checks; no enterprise IAM/PDP. |
| `CMP-008` | Evaluation and Assurance Boundary | Adds budget, recovery, cancellation and resume tests/evaluations. |
| `CMP-009` | Observability and Audit Boundary | Stores local outcomes/checkpoints; not audit or production telemetry. |
| `CMP-010` | Runtime and Deployment Boundary | Python 3.13.5 local single-process runtime. |
| `CMP-011` | Source-of-Truth Governance Pack | Updated to `0.7.0`. |

## Agent inventory

| ID | Name | Authority | Status |
|---|---|---|---|
| `AGT-001` | Regulatory Impact Assessment Agent | Proposes only `TOOL-001`–`TOOL-006`, complete or escalate. Cannot create authority/budgets/fallbacks, approve, finalize, compensate, delegate, create agents or execute code. | Implemented and locally verified. |

## Tool inventory

`TOOL-001`–`TOOL-003` remain read-only. `TOOL-004`–`TOOL-006` remain reversible unapproved local writes. No tool ID is added. Tool fallback exists only for `TOOL-001`–`TOOL-003`; reconciliation exists only for `TOOL-004`–`TOOL-006` by idempotency key.
