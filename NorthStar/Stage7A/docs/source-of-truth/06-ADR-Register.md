# 06 — ADR Register (Reconstructed 1.6.0 Overlay)

`ADR-001`–`055` remain accepted.

| ID | Decision | Status |
|---|---|---|
| `ADR-056` | Use bounded asynchronous execution under existing CMP-003/CMP-010 owners; sequential remains default. | Accepted |
| `ADR-057` | Permit concurrency only for immutable read-only or pure-compute work; no concurrent protected-state writes. | Accepted |
| `ADR-058` | Enforce finite global, per-case and queue admission bounds. | Accepted |
| `ADR-059` | Require input digests, idempotency keys and bounded transient retry; do not claim exactly once. | Accepted |
| `ADR-060` | Aggregate deterministically by ordinal with explicit all-required, minimum-successes or first-satisfactory policy. | Accepted |
| `ADR-061` | Use cooperative cancellation, absolute deadlines and checkpoint resumption; termination ownership stays with CMP-003. | Accepted |

Standalone records are in `docs/adr/ADR-056.md` through `ADR-061.md`.
