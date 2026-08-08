# 08 — Risk, Assumption and Issue Register

Inherited active risks/issues from S03B remain. This stage adds:

## Risks

| ID | Risk | Treatment/status |
|---|---|---|
| `RSK-057` | Incorrect failure classification causes unsafe retry or avoidable escalation. | Typed matrix, tests; active residual risk. |
| `RSK-058` | Fallback adapter changes semantics or returns stale evidence. | Registered read-only fallback, evidence/citation checks; active. |
| `RSK-059` | Cost tariff or missing usage undercounts provider spend. | Explicit synthetic tariff; production must use provider normalization/reservations; active. |
| `RSK-060` | Retry amplification worsens dependency outage. | Global retry/failure/time budgets and bounded backoff; active. |
| `RSK-061` | Ambiguous write reconciliation returns stale/incorrect commit status. | Same idempotency key, authoritative adapter store required; active. |
| `RSK-062` | Cancellation arrives after a side effect but before checkpoint. | Reconciliation and partial outcome; active. |
| `RSK-063` | Local checkpoint is corrupted or modified. | SHA-256 detection, schema validation, restricted path; not signature; partially mitigated. |
| `RSK-064` | Resume duplicates work due stale checkpoint. | Milestones/idempotency keys and resume tests; active for external systems. |
| `RSK-065` | Recovery hides systemic defects and delays human escalation. | Attempt caps and visible recovery records; active. |
| `RSK-066` | Partial completion is mistaken for regulatory completion. | Fixed unapproved disposition and missing-milestone list; mitigated locally. |

## Assumptions

| ID | Assumption | Status |
|---|---|---|
| `ASM-022` | Registered fallback read adapters are semantically equivalent for the synthetic fixture. | Accepted for local stage only. |
| `ASM-023` | Tool stores can query authoritative local status by idempotency key. | Accepted locally; must be revalidated for each live connector. |
| `ASM-024` | Provider returns accurate token usage or production policy supplies a conservative approved estimate. | Open for managed-provider pilot. |

## Issues

| ID | Issue | Status |
|---|---|---|
| `ISS-029` | Byte-exact `0.6.0` repository/registers were not mounted; S03C is a compatible overlay reconstructed from S03B handoff/chapter. | Open/documented. |
| `ISS-030` | Local checkpoint is not multi-process/multi-host durable workflow storage and has no directory fsync/lease/version migration guarantee. | Open; graph/durable execution stage trigger. |
| `ISS-031` | Managed model usage, cancellation, live adapter error semantics, cost and reconciliation are not live-verified. | Open before production pilot. |

`ISS-014`, `ISS-015`, `ISS-021`–`ISS-028` and inherited production gaps remain active unless explicitly closed by a later stage.
