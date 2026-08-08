# 06 — ADR Register

## Accepted decisions

`ADR-001` through `ADR-013` remain accepted and unchanged from the S02A baseline.

| ADR | Decision | Status |
|---|---|---|
| `ADR-014` | Authorize and filter chunks before retrieval scoring or candidate-text exposure. | Accepted |
| `ADR-015` | Use local BM25 plus TF-IDF/SVD latent semantic ranking and weighted RRF; keep production embedding/reranker choices behind contracts. | Accepted |
| `ADR-016` | Apply deterministic metadata-aware reranking and same-source overlap suppression before context assembly. | Accepted |
| `ADR-017` | Build exact application-owned citations and evaluate retrieval independently; defer answer faithfulness/relevance until generation exists. | Accepted |

## Decision impacts

- `CMP-004` becomes retrieval-capable but remains partial.
- `CMP-007` remains planned and cannot be implied by local group strings.
- `CMP-008` gains retrieval evaluation but no LLM judge.
- New schemas are additive at `1.0.0`.
- Repository advances to `0.4.0`.
- S02B explicitly stops before grounded generation and tool use.

Complete ADR text is in `docs/adr/ADR-014-...` through `ADR-017-...`.
