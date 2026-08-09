# 04 — Component and Agent Catalogue: Stage 10B Overlay

Version: `1.16.0`

| ID | Name | Stage 10B responsibility |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Presents degraded/partial status, recovery reference and incident limitations; never implies completion after timeout. |
| `CMP-002` | Regulatory Intake Boundary | Applies intake timeout/quarantine; preserves digest and source reference. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Owns failure classification, retry eligibility, checkpoint resume, dead-letter routing, cancellation and deterministic recovery state. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Exposes freshness-aware read fallback and retrieval health; stale evidence is visibly labelled and cannot support protected completion. |
| `CMP-005` | Enterprise Integration Boundary | Owns idempotency lookup, effect reconciliation and approved compensation; never retries ambiguous protected writes blindly. |
| `CMP-006` | Human Review and Approval Boundary | Keeps timed-out approvals pending, escalates and supports controlled redrive/release approval. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Reissues fresh grants after authentication expiry; policy/authority outages fail closed. |
| `CMP-008` | Evaluation and Assurance Boundary | Runs recovery, chaos, compatibility and promotion-gate evaluations; remains advisory. |
| `CMP-009` | Observability and Audit Boundary | Records failures, attempts, circuit changes, checkpoints, incidents, recovery, release and rollback evidence; mandatory audit stays unsampled. |
| `CMP-010` | Runtime and Deployment Boundary | Owns timers, retry scheduler, circuit breakers, bulkheads, load shedding, health probes and non-production deployment reference. |
| `CMP-011` | Source-of-Truth Governance Pack | Owns reliability policy, release manifest, deployment profiles, DR assumptions, ADRs, risks and promotion denial. |

## Agent inventory

`AGT-001 Regulatory Impact Assessment Agent` remains the only active agent, specification `1.1.0`. It may observe a recovery decision but cannot choose a less restrictive policy, issue a grant, redrive a dead letter, perform compensation outside `CMP-005`, activate a deployment route or approve a release.

No retry executor, circuit breaker, checkpoint store, dead-letter queue, release manager, deployment planner, incident manager or chaos harness is an agent. `WP-008`, MCP/A2A peers and all additional agents remain `inactive_future`.
