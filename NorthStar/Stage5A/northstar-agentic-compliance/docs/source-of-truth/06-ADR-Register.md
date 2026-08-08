# 06 — ADR Register

**Version:** `1.1.0`

`ADR-001`–`035` remain accepted.

| ID | Title | Status | Decision summary |
|---|---|---|---|
| `ADR-036` | Formal Machine-Readable Specification for `AGT-001` | Accepted | Use one application-owned `DATA-071` as the complete design-time definition; it grants no authority. |
| `ADR-037` | JSON, JSON Schema 2020-12, Semantic Validation and Canonical Digest | Accepted | Use canonical JSON plus schema artefact, cross-contract semantic validation and SHA-256 content binding. |
| `ADR-038` | Specification-Derived Assertions and Gates | Accepted | Bind the spec to the harness and derive deterministic assertions, evaluation obligations and deny-by-default release gates without replacing control owners. |
| `ADR-039` | Context Policy Profile Without Memory | Accepted | Formalize existing bounded authorized context in `DATA-077`; keep memory, cross-case reuse and compaction disabled. |

Full ADRs are in `docs/adr/`.
