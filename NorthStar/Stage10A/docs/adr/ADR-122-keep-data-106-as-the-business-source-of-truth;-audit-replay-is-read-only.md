# ADR-122: Keep DATA-106 as the business source of truth; audit replay is read-only

- **Status:** Accepted
- **Stage:** S10A
- **Architecture version:** 1.15.0

## Context

Event histories can reconstruct evidence, but automatic replay into protected state could bypass CMP-003 ownership and current policy.

## Decision

Audit records describe state changes and digests. Replay produces a forensic timeline or candidate reconstruction, never an automatic DATA-106 mutation.

## Alternatives

Treat audit ledger as the operational database; omit state-change evidence; allow auditors to restore production state directly.

## Rationale

Preserves accepted state ownership and prevents evidence systems from gaining business authority.

## Consequences

Forensic reconstruction may require external snapshots.

## Risks

Forensic reconstruction may require external snapshots.

## Mitigations

Snapshot references, version IDs, read-only verification and separate recovery procedures.

## Review trigger

A future event-sourced architecture is approved by ADR.
