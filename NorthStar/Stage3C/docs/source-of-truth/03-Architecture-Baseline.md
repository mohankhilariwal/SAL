# 03 — Architecture Baseline

**Version:** `0.7.0`

## Architecture before S03C

The `0.6.0` runtime had one application-owned agent loop, deterministic completion and simple iteration/repetition/no-progress guards. Any gateway error immediately escalated. In-flight state existed only in memory until terminal persistence.

Source: `docs/architecture/diagrams/stage-3c-architecture-before.mmd`.

## Architecture after S03C

The same `CMP-003` runtime now contains four deterministic runtime services:

1. `INT-026` Budget Enforcement using `DATA-045/046`.
2. `INT-027` Failure Classification and Recovery using `DATA-047/048`.
3. `INT-028` Cancellation using `DATA-049`.
4. `INT-029` Checkpoint/Resume using `DATA-050`.

`CMP-005` adds `INT-030` ambiguous-write reconciliation using `DATA-051`. `CMP-009` records `DATA-052 RecoveryOutcome`. No new agent or tool is created.

Source: `docs/architecture/diagrams/stage-3c-cumulative-logical-architecture.mmd`.

## Security boundaries

- Decision provider and evidence content remain untrusted/probabilistic.
- Principal, write scope, budget policy, retry policy, idempotency key, reconciliation, completion and final disposition are application-owned.
- The checkpoint contains application state and protected references; it is a local file, not an audit ledger.
- Fallback adapters are selected by configuration, never invented by `AGT-001`.

## Recovery matrix

| Failure | Read-only | Reversible write |
|---|---|---|
| Transient/rate-limit/pre-dispatch timeout | Bounded retry or registered fallback | Retry only if definitely not dispatched/committed, same idempotency key |
| Authorization/validation/permanent | Escalate; no retry | Escalate; no retry |
| Post-dispatch timeout/unknown commit | Usually retry only when read semantics are safe | Reconcile by idempotency key; unresolved => escalate |
| Cancellation | Stop cooperatively | Stop; reconcile any in-flight ambiguous result before manual continuation |

## Durability statement

The implementation writes atomic checksummed local snapshots. It does not provide distributed locking, exactly-once execution, event sourcing, multi-host lease ownership, workflow version migration, WORM retention or disaster recovery.
