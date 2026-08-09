# 04 — Component and Agent Catalogue (Reconstructed 1.6.0 Overlay)

## Components

| ID | Name | S07A responsibility/status |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Starts/resumes cases and shows preliminary branch/queue evidence. |
| `CMP-002` | Regulatory Intake Boundary | Unchanged provenance boundary. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Sole task/route/state/cancellation/aggregation/system-termination owner; eligibility, admission, fan-out/fan-in, idempotency coordination and resumption. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Authorized immutable evidence reads for eligible branches. |
| `CMP-005` | Enterprise Integration Boundary | Sole gateway for `TOOL-001`–`006`; no worker bypass. |
| `CMP-006` | Human Review and Approval Boundary | External typed approval; timeout never approves. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Sole grant issuer; validates worker/task policy in production target. |
| `CMP-008` | Evaluation and Assurance Boundary | `EVAL-079`–`088`, concurrency regression and invariant checks. |
| `CMP-009` | Observability and Audit Boundary | Branch attempts, queue health, duplicates, cancellations and aggregate evidence; still not production WORM. |
| `CMP-010` | Runtime and Deployment Boundary | Bounded async queue/worker reference and broker-neutral transport seam. |
| `CMP-011` | Source-of-Truth Governance Pack | Version `1.6.0`, concurrency policy, ADRs and reconstruction issue. |

## Active agent

| ID | Name | Authority | Status |
|---|---|---|---|
| `AGT-001` | Regulatory Impact Assessment Agent | Existing proposal/complete/escalate boundary; no route, protected-state mutation, approval, finalization, grant, unrestricted memory, agent creation or worker ownership. | **Only active agent**; spec `1.1.0` unchanged. |

## Candidate endpoint

`CAND-EVIDENCE-VERIFIER-001` remains `candidate_sandbox_only`; it is not scheduled, activated, converted to `AGT-002` or allowed concurrency.

## Runtime sub-capabilities (not new agents or authority owners)

- eligibility gate;
- admission controller;
- bounded work queue;
- async worker pool;
- idempotency coordinator;
- fan-in aggregator;
- cancellation/deadline coordinator;
- checkpoint/resumption coordinator.
