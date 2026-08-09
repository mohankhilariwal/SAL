# 04 — Component and Agent Catalogue
**Version:** `1.3.0`

| ID | Name | S06A status |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Starts/resumes cases; surfaces decision/profile evidence. |
| `CMP-002` | Regulatory Intake Boundary | Unchanged provenance boundary. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Owns graph/state/routes/termination and profile validation/binding. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Unchanged authorized evidence. |
| `CMP-005` | Enterprise Integration Boundary | Unchanged gateway-only tools. |
| `CMP-006` | Human Review and Approval Boundary | Unchanged external human authority. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Unchanged runtime authority owner. |
| `CMP-008` | Evaluation and Assurance Boundary | Boundary/profile/counterfactual evaluations. |
| `CMP-009` | Observability and Audit Boundary | Local evidence; not audit/WORM. |
| `CMP-010` | Runtime and Deployment Boundary | Local sequential Python. |
| `CMP-011` | Source-of-Truth Governance Pack | Governance at `1.3.0`. |

| Agent | Authority | Status |
|---|---|---|
| `AGT-001 Regulatory Impact Assessment Agent` | May propose exact `TOOL-001`–`006` through `CMP-005`, complete or escalate. Cannot route, mutate protected state, approve/finalize, grant consent, write memory, delegate, hand off, create agents, run concurrent branches or recall across cases. | **Only agent**; spec `1.1.0`; six task profiles. |

No `AGT-002` is allocated.
