# ADR-015 — Hybrid Lexical and Latent-Semantic Retrieval with RRF

- **Status:** Accepted
- **Context:** NorthStar queries mix exact policy terminology and paraphrased business language. Either lexical-only or semantic-only retrieval creates avoidable blind spots.
- **Decision:** Use BM25 and deterministic TF-IDF/truncated-SVD latent semantic ranking over the authorized subset, then combine rankings using weighted reciprocal-rank fusion with versioned configuration.
- **Alternatives:** long-context prompting; BM25 only; vector only; calibrated score interpolation; learned fusion; graph/SQL retrieval.
- **Rationale:** The selected design is local, reproducible, inspectable and score-scale independent. It demonstrates the architecture without claiming production embedding quality.
- **Consequences:** Better candidate diversity than a single channel, extra compute and more tuning dimensions.
- **Risks:** local LSA is weak on domain semantics; RRF parameters can be suboptimal; two channels can reinforce noise.
- **Mitigations:** evaluation cases, index/config hashes, optional transformer adapter and production review trigger.
- **Review trigger:** production corpus, multilingual content, managed/open embedding selection, labeled relevance data or latency constraints.
