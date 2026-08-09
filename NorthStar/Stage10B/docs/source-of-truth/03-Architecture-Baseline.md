# 03 — Architecture Baseline: Stage 10B Overlay

Version: `1.16.0`
Graph: `GRAPH-001/1.12.0`
Threat model: `TM-001/1.4.0`

## Preserved boundaries

- `CMP-003` remains sole owner of route, protected state, admission, cancellation, aggregation, termination and workflow recovery decisions.
- `CMP-005` remains the only tool and protected-effect gateway.
- `CMP-007` remains the sole authority issuer and policy authority.
- `CMP-006` and authenticated humans remain approval/finalization owners.
- `CMP-009` remains non-authorizing observability/audit owner.
- `DATA-106` remains the business source of truth; checkpoints and audit replay cannot mutate it.
- Exactly one active agent remains `AGT-001`.

## Stage 10B additions

- `CMP-003`: deterministic failure classification, recovery routing, checkpoint resume, dead-letter quarantine and manual redrive workflow.
- `CMP-005`: idempotency reconciliation and compensation entry point with fresh grant/approval checks.
- `CMP-008`: recovery evaluations and isolated chaos invariants.
- `CMP-009`: incident/recovery/release evidence, unsampled mandatory audit events.
- `CMP-010`: timeout enforcement, retry budgets, circuit breakers, bulkheads, overload shedding, health signals and reference deployment manifests.
- `CMP-011`: reliability policies, release manifests, compatibility checks, promotion gates, rollback plans and unresolved DR ownership.

## Deployment posture

Local and pre-production reference deployment only. No production route, production credentials, managed backend, multi-region topology, enterprise RTO/RPO, WORM/KMS upgrade or production certification is introduced.
