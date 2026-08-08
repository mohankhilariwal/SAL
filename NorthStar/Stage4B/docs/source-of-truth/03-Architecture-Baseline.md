# Architecture Baseline — 0.9.0

`GRAPH-001` advances from `1.0.0` to `1.1.0`. Existing nodes remain conceptually preserved; Stage 4B adds `N75_CREATE_REVIEW_WAIT`, `N80_REVIEW_DECISION_GATE`, `N82_APPROVED_BRANCH`, `N84_REJECTED_BRANCH` and `N86_EXPIRED_ESCALATION`.

`CMP-006` is now partially executable with a local durable approval adapter. `CMP-010` adds SQLite transactional persistence and a per-run resume lease. `CMP-009` records local transition and decision evidence but remains explicitly not an audit ledger.

See `docs/architecture/diagrams/cumulative-logical-architecture.mmd`.
