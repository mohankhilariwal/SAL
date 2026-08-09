# 04 — Component and Agent Catalogue — Version 1.7.0 overlay

| ID | Name | Stage 7B responsibility |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Emits interactive-session timings and profile labels without raw content capture. |
| `CMP-002` | Regulatory Intake Boundary | Supplies document-size and arrival metadata; provenance boundary unchanged. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Classifies workflow profile, preserves `DATA-106`, receives advisory `INT-093`, remains sole admission/state/route owner. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Exposes retrieval timing and result-count metadata. |
| `CMP-005` | Enterprise Integration Boundary | Exposes gateway tool-call timing/status; workers still cannot bypass it. |
| `CMP-006` | Human Review and Approval Boundary | Human elapsed time is separately measured and excluded/included only by declared clock policy. |
| `CMP-007` | Identity, Authorization and Policy Boundary | No change; benchmark runners receive no new authority. |
| `CMP-008` | Evaluation and Assurance Boundary | Owns workload profiles, benchmark design, SLO-hypothesis evaluation and capacity envelopes. |
| `CMP-009` | Observability and Audit Boundary | Normalizes `DATA-119` metrics and evidence metadata; not production WORM. |
| `CMP-010` | Runtime and Deployment Boundary | Runs the local simulator and future endpoint benchmark adapters under bounded resources. |
| `CMP-011` | Source-of-Truth Governance Pack | Versions profiles, ADRs, schemas and evidence; records reconstruction exception `ISS-096`. |

## Agent inventory

| ID | Name | Authority | Status |
|---|---|---|---|
| `AGT-001` | Regulatory Impact Assessment Agent | Existing proposal/complete/escalate boundary only; cannot route, approve, finalize, grant authority or write shared/protected state concurrently. | **Only active agent; unchanged** |

`WP-008` is `inactive_future`. It is not an agent and cannot be executed.
