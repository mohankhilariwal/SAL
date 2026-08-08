# ADR-016 — Deterministic Metadata-Aware Reranking and Overlap Suppression

- **Status:** Accepted
- **Context:** Fusion ranks relevance signals but does not account for authority, explicit domain/jurisdiction filters or duplicated evidence created by chunk overlap.
- **Decision:** Apply a deterministic reranker using query-term coverage, source authority and explicit metadata matches; then suppress substantially overlapping spans from the same source version.
- **Alternatives:** no reranking; cross-encoder; LLM reranker; maximal marginal relevance; learned-to-rank.
- **Rationale:** Deterministic reasoning is auditable, cheap and runnable offline. A production cross-encoder remains an adapter choice after evaluation.
- **Consequences:** Ranking reasons are explainable; heuristic weights may not represent actual relevance.
- **Risks:** authority boost may over-rank broad policy text; deduplication may hide distinct clauses in overlapping chunks.
- **Mitigations:** small bounded boosts, exact-span tests, versioned thresholds and human-labeled review before pilot.
- **Review trigger:** labeled corpus, cross-encoder benchmark, poor precision, diverse-content requirement or multilingual rollout.
