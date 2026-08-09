# ADR-074 — Govern immutable versioned evaluation datasets and split lineage

- **Status:** Accepted
- **Context:** Dataset edits, duplicate cases, temporal drift and test exposure can invalidate regression evidence.
- **Decision:** Register datasets by immutable version; store dev, validation and logically sealed test splits separately; create case and file digests; document provenance, labels, intended use and limitations; detect exact and near cross-split duplicates; quarantine invalid versions rather than rewriting history.
- **Alternatives:** Mutable spreadsheet; one shared JSON file; public-only benchmarks.
- **Rationale:** Reproducibility and contamination control require lineage at case level.
- **Consequences:** Dataset maintenance becomes a governed engineering activity.
- **Risks:** Logical sealing is weaker than cryptographic/organizational separation.
- **Mitigations:** Explicit execution flag, exposure audit, future access-controlled registry and held-back production test set.
- **Review trigger:** Production data onboarding, label change, new jurisdiction, model training on evaluation data or suspected leakage.
