# 04 — Component and Agent Catalogue: Stage 7C Overlay

| ID | Name | S07C responsibility |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Streams clearly labelled partial output; final structured validation remains required. |
| `CMP-002` | Regulatory Intake Boundary | Supplies provenance and document metadata; no raw benchmark payload export. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Keeps route/state/admission/cancellation/aggregation/termination ownership; consumes advisory optimization configuration only through governance. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Supports evidence-preserving context reduction and version-aware cache invalidation signals. |
| `CMP-005` | Enterprise Integration Boundary | Remains sole gateway for `TOOL-001`–`006`; inference benchmark cannot bypass it. |
| `CMP-006` | Human Review and Approval Boundary | Human authority and review clocks remain external to inference optimizations. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Sole grant issuer; supplies cache authorization-scope binding and endpoint policy. |
| `CMP-008` | Evaluation and Assurance Boundary | Owns optimization planner, inference benchmark design, parity gates and recommendation. |
| `CMP-009` | Observability and Audit Boundary | Normalizes `DATA-128`, cache/acceptance/memory metrics and evidence provenance. |
| `CMP-010` | Runtime and Deployment Boundary | Hosts managed adapter, self-hosted candidate lane, local simulator and runtime batching/cache/speculation policies. |
| `CMP-011` | Source-of-Truth Governance Pack | Governs `1.8.0`, ADRs, profile versions and reconstruction exceptions. |

## Agent inventory

| ID | Name | Authority | Status |
|---|---|---|---|
| `AGT-001` | Regulatory Impact Assessment Agent | Existing proposal/complete/escalate boundary; cannot route, mutate protected state, approve/finalize, issue grants, write unrestricted/shared memory, create agents or bypass owners. | **Only active agent**; spec `1.1.0` unchanged. |

`WP-008` is not an agent and remains `inactive_future`.
