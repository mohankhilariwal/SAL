# 06 — Architecture Decision Record Register

**Version:** `0.3.0`

## 1. Preserved decisions

- `ADR-001` through `ADR-007` remain accepted.
- `ADR-008`: bounded, single-turn structured assistant for the immediate S01 first-reading need.
- `ADR-009`: provider-neutral model contract with deterministic offline test double.
- `ADR-010`: bounded text intake, SHA-256/line provenance, deterministic evidence validation, fixed status and local atomic artifacts.

## 2. New decisions

| ID | Title | Status | Decision |
|---|---|---|---|
| `ADR-011` | Split Stage 2 at Preparation and Retrieval Boundary | Accepted | S02A ends after prepared-corpus validation; S02B adds search/ranking/citations. |
| `ADR-012` | Deterministic Structure-Aware Line-Preserving Chunking | Accepted | Markdown headings are hard boundaries; use bounded line windows and configurable overlap. |
| `ADR-013` | Immutable Content-Addressed Knowledge Packages and Fail-Closed Access Metadata | Accepted | Stable hashes/versions, historical retention, atomic publication and required access scope precede retrieval. |

## 3. Detailed ADRs

See:

- `docs/adr/ADR-011-stage2a-preparation-retrieval-boundary.md`
- `docs/adr/ADR-012-structure-aware-line-preserving-chunking.md`
- `docs/adr/ADR-013-immutable-knowledge-packages-and-access-metadata.md`

## 4. Review triggers

- need for PDF/Office/HTML or OCR parsing;
- actual corpus/query evaluation shows heading/line chunks underperform;
- enterprise source systems provide authoritative native records better queried directly;
- access policy cannot be represented safely as chunk metadata;
- required deletion/retention semantics conflict with immutable local history;
- corpus scale requires parallel/event-driven ingestion;
- S02B index technology requires a schema change.
