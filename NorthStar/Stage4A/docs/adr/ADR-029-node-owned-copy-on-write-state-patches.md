# ADR-029 — Node-owned copy-on-write state patches and graph-version-bound checkpoints

- **Status:** Accepted
- **Date:** 2026-07-31

## Context
Allowing nodes or models to mutate shared state directly would hide ownership, permit authority changes and make replay/debugging unsafe.

## Decision
Each node receives a state snapshot and returns a typed `DATA-055` result containing a `DATA-056` patch. `INT-033` validates exact owned paths and rejects protected fields. Checkpoints bind to graph ID/version.

## Alternatives
Shared mutable state; immutable event sourcing now; whole-state replacement; framework reducer semantics.

## Rationale
Copy-on-write patches make mutation reviewable while preserving the existing current-state checkpoint boundary and avoiding an event-sourcing claim.

## Consequences
Patch schemas and ownership lists must evolve with the graph. Running checkpoint migration is not implemented in Stage 4A.

## Risks and mitigations
Large copy costs and schema drift are mitigated by small local state, explicit versioning and tests; production stores may need structural sharing or database transactions.

## Review triggers
Large state, concurrent writers, event sourcing, cross-version in-flight migration or distributed durability.
