# ADR-010 — Provenance, Deterministic Validation and Local Artifacts

- **Status:** Accepted
- **Context:** Fluent output cannot be treated as evidence. Stage 1 also lacks an enterprise case or records system.
- **Decision:** Accept only bounded UTF-8 text/Markdown, compute a content hash, require exact line citations, validate all references outside the model, and persist source/metadata/invocation/summary atomically to a local tutorial directory.
- **Alternatives:** free-form chat response; PDF ingestion; direct enterprise persistence.
- **Rationale:** The design provides reproducibility and a runnable lab without claiming enterprise records, authorization or audit guarantees.
- **Consequences:** Limited file support; local artifacts are single-user tutorial outputs.
- **Risks:** local data exposure, write failure, unsupported documents and false confidence in citation semantics.
- **Mitigations:** synthetic data, explicit trust boundary, atomic writes, validation failure stops success, human review.
- **Review trigger:** multi-user deployment, PDF/HTML ingestion, authoritative records retention or production audit.
