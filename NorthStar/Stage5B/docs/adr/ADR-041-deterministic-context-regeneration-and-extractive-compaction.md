# ADR-041 — Deterministic Context Regeneration and Extractive Compaction

- **Status:** Accepted
- **Date:** 2026-08-01

## Context

Appending full history exceeds `DATA-077` limits and creates lost-in-the-middle, stale-data, privacy and cost risks. Free-form model summarization can omit qualifications or invent facts.

## Decision

Use `authoritative_regeneration_v1` to rebuild typed context from `DATA-009` and authorized source references. Use `deterministic_extractive_v1` to select complete typed items by fixed priority. Preserve source hashes and list every omitted reference. Do not use an LLM to create the persisted snapshot.

## Alternatives

- Full transcript replay — rejected.
- Rolling LLM summary — deferred until a separate quality/safety case exists.
- Retrieval-only regeneration — insufficient for case and approval state.
- Hierarchical memory paging — useful later, excessive for one bounded agent.

## Rationale

The design is locally runnable, reproducible and fails closed when critical items cannot fit.

## Consequences

Compression is less linguistically elegant and may omit lower-priority context. Exact omission evidence remains available for diagnostics.

## Risks and mitigations

- **Risk:** priority policy hides useful evidence. **Mitigation:** evaluation cases, omission list, target/hard budgets.
- **Risk:** character limits differ from model tokens. **Mitigation:** production token-aware adapter remains required.

## Review triggers

Representative long-document benchmarks, model/provider selection, measured token budgets or evidence that extractive compaction harms task success.
