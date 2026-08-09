# 04 — Component and Agent Catalogue

**Version:** 1.14.0

## Components

| ID | Name | Stage 9C responsibility |
|---|---|---|
| CMP-001 | Analyst Experience Portal | Authenticated case UX; presents guardrail/review evidence; no policy or approval authority. |
| CMP-002 | Regulatory Intake Boundary | Input size/type/secret/malware/injection checks and quarantine. |
| CMP-003 | Case and Workflow Orchestration Boundary | Sole task/route/protected-state/admission/cancellation/aggregation/termination owner; context, plan, state, memory and runtime PEPs. |
| CMP-004 | Knowledge and Evidence Access Boundary | AUTH-001 receiver PEP plus retrieval scope/limits/citation/freshness guardrails. |
| CMP-005 | Enterprise Integration Boundary | Only TOOL-001–006 gateway; AUTH-001 + BR-001 + schema/approval/write/result guardrails. |
| CMP-006 | Human Review and Approval Boundary | Authenticated role/SoD/digest/expiry validation; humans own approval/finalization. |
| CMP-007 | Identity, Authorization and Policy Boundary | Sole AUTH-001 issuer; owns policy semantics/invariants; guardrails cannot issue grants. |
| CMP-008 | Evaluation and Assurance Boundary | Policy tests, advisory classifiers, TM-001 delta and post-runtime assurance; no authority. |
| CMP-009 | Observability and Audit Boundary | Minimized guardrail/exception/release evidence; no WORM claim. |
| CMP-010 | Runtime and Deployment Boundary | Local verified bundle cache, pinning, stale-bundle behavior; no production route. |
| CMP-011 | Source-of-Truth Governance Pack | Policy lifecycle, owners, releases, exceptions, incidents and version governance. |

## Agent inventory

| ID | Name | Spec | Authority | Status |
|---|---|---|---|---|
| AGT-001 | Regulatory Impact Assessment Agent | 1.1.0 | May propose bounded actions and drafts; cannot alter guardrails, AUTH/BR, policy bundles, routes, agents, approvals, finalization or protected state. | **only active agent** |

`WP-008`, MCP/A2A peers and all additional agents remain `inactive_future`. No guardrail engine, classifier, evaluator, policy engine or control-plane module is an agent.
