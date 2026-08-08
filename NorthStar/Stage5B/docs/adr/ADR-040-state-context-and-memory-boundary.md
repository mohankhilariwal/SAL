# ADR-040 — Separate Authoritative State, Regenerated Context and Memory

- **Status:** Accepted
- **Date:** 2026-08-01

## Context

`DATA-009` is the authoritative workflow state. `DATA-065` is a bounded context envelope. Stage 5A did not define whether a compacted context or persisted memory could become authoritative.

## Decision

NorthStar preserves three distinct planes:

1. `DATA-009` and external systems remain authoritative state/records.
2. `DATA-079`/`DATA-080` are derived regeneration and compaction artefacts.
3. `DATA-081` is optional, case-local continuity memory and can never override state, policy, tool, graph or human decisions.

## Alternatives

- Treat conversation history as state — rejected because it is untyped, incomplete and may contain model errors.
- Treat memory as an authoritative case database — rejected because it creates duplicate truth and conflict risk.
- Persist no continuity artefact — rejected because long waits and repeated sessions exceed the context budget.

## Rationale

The separation preserves deterministic recovery, provenance and accountability while adding the minimum continuity capability.

## Consequences

Context must be regenerated; memory may be stale or absent; consumers must resolve conflicts in favour of authoritative state.

## Risks and mitigations

- **Risk:** duplicate facts diverge. **Mitigation:** source version binding and stale-by-default reads.
- **Risk:** teams misuse memory as a record. **Mitigation:** schemas, names, tests and governance warnings.

## Review triggers

A production records store, event sourcing, cross-case learning, multiple agents or legal retention requirements.
