# 06 — Architecture Decision Register

**Version:** `1.2.0`  
**Accepted prior decisions:** `ADR-001`–`039` remain accepted and are not superseded.

## `ADR-040` — Separate authoritative state, context and memory

**Status:** Accepted.  
**Decision:** Keep `DATA-009` and authoritative repositories as truth, make `DATA-079/080` disposable invocation projections, and permit `DATA-081` only as subordinate continuity data. Memory never mutates or overrides state.

## `ADR-041` — Deterministic regeneration and extractive compaction

**Status:** Accepted.  
**Decision:** Regenerate context from typed authoritative fields and compact by deterministic complete-item selection with source bindings and omission records. Do not use model-generated summaries in the durable path.

## `ADR-042` — Enable only minimum case-local working memory

**Status:** Accepted.  
**Decision:** Enable one short-lived `case_working` record per tenant/case for an opted-in user. Keep cross-case, profile, semantic, episodic, organizational and shared-agent memory disabled; expose no memory tool to the model.

## `ADR-043` — Consent, provenance, expiry, deletion and isolation

**Status:** Accepted.  
**Decision:** Require operation-specific opt-in, exact scope, authoritative origins, source ID/version/digest, default 14-day and maximum 30-day provisional retention, stale-by-default exclusion, authorized deletion/automatic expiry and minimal tombstones.

## Decision relationships

- `ADR-040` preserves S05A's specification/authority separation and S04A's typed-state ownership.
- `ADR-041` preserves `DATA-077` budgets and access-before-load.
- `ADR-042` is the smallest approved exception to S05A's no-memory default.
- `ADR-043` implements privacy/security lifecycle controls but does not claim production legal compliance.

Detailed records are stored in `docs/adr/ADR-040...ADR-043*.md`.
