# 06 - ADR Register

**Version:** 0.2.0

## Preserved accepted decisions

- `ADR-001` Instruction precedence and stage sequence.
- `ADR-002` Progressive simplest-sufficient architecture.
- `ADR-003` Human-accountable bounded autonomy.
- `ADR-004` One cumulative repository and source-of-truth location.
- `ADR-005` Evidence-first audit without hidden chain-of-thought.
- `ADR-006` Vendor-neutral contracts and deferred framework selection.
- `ADR-007` Conceptual component boundaries before runtime decomposition.

## S01 accepted decisions

- `ADR-008` Stage 1 bounded basic LLM assistant: one source-bounded, structured, human-reviewed summarization request; no RAG, tools, stateful agent or multi-agent design.
- `ADR-009` Provider-neutral model contract: minimal Python protocol, deterministic offline test double and optional managed-provider adapter.
- `ADR-010` Provenance, deterministic validation and local artifacts: bounded UTF-8 input, SHA-256, exact line evidence, application-owned status and atomic local persistence.

Detailed S01 records are stored in `docs/adr/`.

## Superseded decisions

None.
