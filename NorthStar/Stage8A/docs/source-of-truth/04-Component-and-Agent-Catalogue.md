# 04 — Component and Agent Catalogue (1.9.0 Overlay)

| ID | Name | S08A responsibility |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | No new authority; future evaluation feedback display only. |
| `CMP-002` | Regulatory Intake Boundary | Future approved sample provenance; local data is synthetic. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Production owner unchanged; evaluation cannot mutate admission/state/route/termination. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Supplies authorized evidence references for future cases. |
| `CMP-005` | Enterprise Integration Boundary | Remains sole gateway for `TOOL-001`–`006`; tool traces are graded. |
| `CMP-006` | Human Review and Approval Boundary | Owns review assignments and human decisions. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Authorizes dataset/split/case access; sole grant issuer. |
| `CMP-008` | Evaluation and Assurance Boundary | Owns suite/dataset/grader/run/result architecture. |
| `CMP-009` | Observability and Audit Boundary | Records payload-minimized run and finding evidence. |
| `CMP-010` | Runtime and Deployment Boundary | Future candidate endpoint adapter; no live model in S08A. |
| `CMP-011` | Source-of-Truth Governance Pack | Governs versions, ADRs, quarantine and handoff. |

## Agent inventory

| ID | Name | Authority | Status |
|---|---|---|---|
| `AGT-001` | Regulatory Impact Assessment Agent | Existing bounded proposal/complete/escalate authority; cannot approve/finalize, route, grant authority, bypass owners, create agents or write unrestricted/shared memory. | **Only active agent**; spec `1.1.0` unchanged. |

No concurrent agents exist. `WP-008` is an inactive future workload placeholder.
