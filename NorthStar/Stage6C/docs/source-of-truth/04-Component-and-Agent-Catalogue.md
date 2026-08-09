# 04 — Component and Agent Catalogue

**Version:** 1.5.0

`CMP-001`–`011` names remain unchanged. S06C responsibility extensions:

- `CMP-003`: invokes canonical adapters, owns profile selection, tasks, cancellation and termination.
- `CMP-005`: remains the only tool gateway; MCP tools/resources map here.
- `CMP-007`: remains the only authority issuer and production trust-policy owner.
- `CMP-008`: owns adapter-conformance and semantic-loss evaluation.
- `CMP-009`: receives local delivery receipts; no audit/WORM claim.
- `CMP-010`: owns direct and loopback HTTP reference runtime.
- `CMP-011`: governs protocol profiles and compatibility decisions.


## Component inventory

| ID | Name | S06C status |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Preserved |
| `CMP-002` | Regulatory Intake Boundary | Preserved |
| `CMP-003` | Case and Workflow Orchestration Boundary | Extended with adapter invocation; sole lifecycle/termination owner |
| `CMP-004` | Knowledge and Evidence Access Boundary | Preserved |
| `CMP-005` | Enterprise Integration Boundary | MCP tool/resource mapping terminates here |
| `CMP-006` | Human Review and Approval Boundary | Preserved |
| `CMP-007` | Identity, Authorization and Policy Boundary | Sole grant issuer and production protocol-policy owner |
| `CMP-008` | Evaluation and Assurance Boundary | Adapter conformance and semantic-loss evaluation |
| `CMP-009` | Observability and Audit Boundary | Local receipts only |
| `CMP-010` | Runtime and Deployment Boundary | Direct and loopback HTTP reference runtime |
| `CMP-011` | Source-of-Truth Governance Pack | Version/profile governance |

## Agent inventory

| ID | Name | Status |
|---|---|---|
| `AGT-001` | Regulatory Impact Assessment Agent | **Only active agent**, spec 1.1.0. |

## Candidate endpoint

`CAND-EVIDENCE-VERIFIER-001` remains `candidate_sandbox_only`, not an `AGT-*` allocation. It has no tools, memory write, routing, delegation, approval, finalization or concurrency.
