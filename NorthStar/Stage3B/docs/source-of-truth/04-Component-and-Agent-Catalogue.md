# 04 — Component and Agent Catalogue

**Version:** `0.6.0`

## Current component inventory

| ID | Name | S03B responsibility/status |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Partial local caller; submits one bounded goal and displays terminal outcome. |
| `CMP-002` | Regulatory Intake Boundary | Retained S01 bounded intake and provenance. |
| `CMP-003` | Case and Workflow Orchestration Boundary | **Extended:** application-owned single-agent loop, run state and termination; in-memory until final persistence. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Retains S02B authorized retrieval; exposed only through `TOOL-003`. |
| `CMP-005` | Enterprise Integration Boundary | Retains S03A gateway/registry/policy/runtime controls and six local adapters. |
| `CMP-006` | Human Review and Approval Boundary | Planned approval service; S03B only queues a local request. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Enterprise boundary remains planned; unauthenticated local PDP is partial. |
| `CMP-008` | Evaluation and Assurance Boundary | Extended with loop/termination/authority evaluation. |
| `CMP-009` | Observability and Audit Boundary | Final run and tool-event evidence only; not immutable audit. |
| `CMP-010` | Runtime and Deployment Boundary | Local Python process; no durable/resumable execution. |
| `CMP-011` | Source-of-Truth Governance Pack | Updated and validated at `0.6.0`. |

## Agent inventory

| ID | Name | Goal | Authority | Non-goals | Status |
|---|---|---|---|---|---|
| `AGT-001` | Regulatory Impact Assessment Agent | Prepare an evidence-backed unapproved impact package and queue human review for one accepted publication. | May propose only `TOOL-001`–`TOOL-006`; may create only idempotent reversible local unapproved artifacts when the gateway permits. | No legal conclusion, approval, final disposition, control change, remediation assignment, external notification, credential handling, delegation, code execution or sub-agent creation. | Implemented and locally verified. |

## Tool inventory

| ID | Name | Impact | Agent use | Authorization |
|---|---|---|---|---|
| `TOOL-001` | Search Regulatory Catalogue | Read-only | Find publication candidates. | Allowed group/purpose/residency through gateway. |
| `TOOL-002` | Query Control Catalogue | Read-only | Find candidate controls. | Same plus caller scope. |
| `TOOL-003` | Retrieve Authorized Evidence | Read-only | Obtain `CIT-*` evidence. | S02B authorization-before-scoring; cannot widen access. |
| `TOOL-004` | Create Draft Case | Reversible write | Create `draft_unapproved`. | Explicit write scope and idempotency key. |
| `TOOL-005` | Save Candidate Mapping | Reversible write | Create `candidate_unapproved`. | Explicit write scope and idempotency key. |
| `TOOL-006` | Queue Human Review | Reversible write | Create local queued review request. | Explicit write scope, reviewer allowlist and idempotency key. |

## Agent lifecycle

`AGT-001` exists only for one run. It does not retain cross-run memory. A new run starts from the accepted goal, principal context and current tool descriptors rather than prior model conversation.
