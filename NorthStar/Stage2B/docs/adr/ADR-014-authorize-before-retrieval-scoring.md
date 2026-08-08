# ADR-014 — Authorize Before Retrieval Scoring and Text Exposure

- **Status:** Accepted
- **Context:** `DATA-022` chunks carry access metadata, but S02A had no authenticated query path. Filtering after global retrieval could expose restricted content through results, caches, logs, timing or model context.
- **Decision:** Construct lexical and semantic scorers only from the deterministic authorized subset derived from `DATA-026`, `DATA-027` and each chunk's `DATA-020` scope. Fail closed on incomplete principal context.
- **Alternatives:** post-filter global candidates; rely on prompt instructions; separate indexes only by classification; enterprise PDP/PEP integration.
- **Rationale:** The local implementation can prove the ordering invariant without pretending that group strings authenticate a user.
- **Consequences:** Per-query local index construction is slower and does not scale, but unauthorized chunk text is not scored or exposed.
- **Risks:** locally asserted attributes can be forged; side channels and production caches require further analysis.
- **Mitigations:** label this as a tutorial assertion boundary, record scored IDs in tests, and require `CMP-007` integration before production.
- **Review trigger:** enterprise identity/PDP integration, shared index deployment, caching, multi-tenancy or latency SLOs.
