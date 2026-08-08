# ADR-026 — Atomic local checkpoint and resume before graph engineering

- **Status:** Accepted
- **Date:** 2026-07-31

## Context
S03B persisted only terminal output. A process failure could lose in-flight progress even though idempotent write artifacts might already exist.

## Decision
After every accepted decision, observation, recovery action and terminal transition, write `DATA-050 RunCheckpoint` using a temporary file, `fsync`, atomic replacement and a SHA-256 checksum. Resume validates checkpoint and run-state schema, preserves completed milestones and idempotency keys, and continues the same `AGT-001` loop. The store is explicitly local checkpoint infrastructure, not event sourcing, audit, WORM, distributed durable execution or exactly-once delivery.

## Alternatives
1. Terminal-only persistence.
2. Database current-state row.
3. Event sourcing.
4. Durable workflow engine.
5. Local atomic checkpoint.

## Rationale
The local checkpoint is the smallest capability that demonstrates safe continuation while keeping graph/durable workflow design for the next stage.

## Consequences
Crash windows still exist around external side effects and checkpoint persistence; reconciliation remains mandatory. Concurrent writers and multi-host recovery are unsupported.

## Risks and mitigations
Checksum detects accidental/local tampering but is not a signature. Restrict filesystem access, validate schema, and do not call this an audit record.

## Review triggers
Multiple workers, concurrent runs on the same case, production deployment, workflow migration, event sourcing or multi-region recovery.
