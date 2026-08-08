# Component and Agent Catalogue — 0.9.0

| ID | Name | Stage 4B responsibility/status |
|---|---|---|
| CMP-001 | Analyst Experience Portal | Starts, displays wait/deadline and requests resume. |
| CMP-002 | Regulatory Intake Boundary | Retained. |
| CMP-003 | Case and Workflow Orchestration Boundary | `GRAPH-001` 1.1.0, suspend/resume and decision routes. |
| CMP-004 | Knowledge and Evidence Access Boundary | Retained. |
| CMP-005 | Enterprise Integration Boundary | Authoritative gateway and idempotent `TOOL-006`. |
| CMP-006 | Human Review and Approval Boundary | Local durable wait, signed callback validation, decision persistence and expiry. |
| CMP-007 | Identity, Authorization and Policy Boundary | Synthetic reviewer claims only; enterprise IAM/PDP pending. |
| CMP-008 | Evaluation and Assurance Boundary | Wait, decision, timeout, restart and security tests. |
| CMP-009 | Observability and Audit Boundary | Local transitions/decision hashes; not audit. |
| CMP-010 | Runtime and Deployment Boundary | Python 3.13.5, SQLite, sequential single process; resume lease only. |
| CMP-011 | Source-of-Truth Governance Pack | Updated to 0.9.0. |

## Agent

`AGT-001 Regulatory Impact Assessment Agent` remains the only agent. It proposes `TOOL-006`; it cannot create waits, validate reviewers, approve, reject, set expiry, select a branch or set a final compliance conclusion.
