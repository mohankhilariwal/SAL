# 02 — Requirements Register

## Preserved requirements

All accepted `FR-*`, `NFR-*`, `POL-*` and `CTL-*` identifiers through S02A retain their meanings. In particular, `FR-033`–`FR-038` and `NFR-026`–`NFR-030` continue to govern preparation, provenance, deterministic chunks, access metadata, immutable publication and the non-agentic boundary.

## S02B functional requirements

| ID | Requirement | Status/evidence |
|---|---|---|
| `FR-039` | Accept a typed retrieval query and complete principal context containing principal, groups, clearance, purpose, residency, as-of date and jurisdictions. | Implemented locally; `TEST-034`, `TEST-042`, `TEST-043`. |
| `FR-040` | Apply deterministic authorization and metadata/effective-date filtering before candidate text is scored or exposed. | Implemented locally; `TEST-034`, `TEST-042`, `TEST-043`, `EVAL-012`. |
| `FR-041` | Generate lexical candidates that preserve exact identifiers and regulatory terminology. | Implemented with BM25; `TEST-035`, `EVAL-009`–`EVAL-011`. |
| `FR-042` | Generate semantic-similarity candidates through a provider-neutral vector contract with a deterministic local implementation. | Implemented with local TF-IDF/SVD LSA; `TEST-036`; transformer adapter optional/unverified. |
| `FR-043` | Fuse lexical and semantic rankings without comparing incompatible raw score scales. | Implemented with weighted RRF; `TEST-037`. |
| `FR-044` | Rerank using deterministic relevance/metadata signals and suppress substantially overlapping source spans. | Implemented; `TEST-038`, `TEST-039`, `EVAL-009`–`EVAL-013`. |
| `FR-045` | Return ranked evidence with immutable source/chunk identity, exact line range, normalized source hash, excerpt and ranking reasons. | Implemented; `TEST-040`, `TEST-041`. |
| `FR-046` | Assemble bounded retrieval context that labels content as untrusted evidence and cannot set disposition, approval or legal conclusion. | Implemented; `TEST-040`, `TEST-046`. |
| `FR-047` | Evaluate retrieval precision, recall, reciprocal rank, citation correctness, forbidden hits, duplicate spans and local latency on normal and permission-boundary cases. | Implemented; `TEST-045`, `EVAL-009`–`EVAL-013`. |
| `FR-048` | Reject a stale or incompatible retrieval index when corpus hash, source versions or retrieval configuration change. | Implemented; `TEST-033`, `TEST-044`. |

## S02B non-functional requirements

| ID | Requirement | Status/evidence |
|---|---|---|
| `NFR-031` | Retrieval results must be deterministic for fixed corpus, principal, query and versioned configuration. | Implemented locally; `TEST-037`. |
| `NFR-032` | Unauthorized chunks must not enter lexical/semantic scoring, result context or evaluation traces. | Implemented locally; `TEST-034`, `EVAL-012`. |
| `NFR-033` | Citation correctness must be independently reconstructable from immutable normalized source text. | Implemented; `TEST-040`, `TEST-041`; measured `1.0` on five cases. |
| `NFR-034` | Retrieval index identity must bind corpus hash, source versions and ranking configuration. | Implemented; `TEST-033`, `TEST-044`. |
| `NFR-035` | Local execution must not require a managed model, embedding endpoint, vector database or LLM judge. | Implemented; NumPy-only runtime dependency. |
| `NFR-036` | Stage reports must distinguish synthetic local latency/quality from production SLOs. | Enforced in docs and handoff. |
| `NFR-037` | S02B must not allocate an agent/tool identifier or implement model-selected actions, workflow state, memory or grounded generation. | Implemented; `TEST-046`, consistency audit. |

## Controls advanced or introduced

| ID | Control | S02B realization |
|---|---|---|
| `CTL-001` | Source provenance | Source version, chunk ID, source hash and exact lines in every citation. |
| `CTL-002` | Structured validation | Typed query/context/evidence/evaluation objects. |
| `CTL-006` | Access boundary | Classification, groups, purpose, residency, effective date and jurisdiction filters. |
| `CTL-014` | Change/dependency verification | Corpus/config/source-version hashes bind the index manifest. |
| `CTL-016` | Authorized retrieval enforcement | Fail-closed filter executes before scorer construction. |
| `CTL-017` | Citation integrity | Independent excerpt reconstruction and tamper rejection. |
| `CTL-018` | Retrieval regression gate | Versioned positive, negative and permission-boundary cases. |

## Traceability summary

| Requirement range | Component | Data | Interface | Tests/evaluations |
|---|---|---|---|---|
| `FR-039`–`FR-040` | `CMP-004`, future `CMP-007` | `DATA-020`, `DATA-026`, `DATA-027` | `INT-012` | `TEST-034`, `TEST-042`, `TEST-043`, `EVAL-012` |
| `FR-041`–`FR-044` | `CMP-004` | `DATA-028`, `DATA-029`, `DATA-030` | `INT-013` | `TEST-035`–`TEST-039` |
| `FR-045`–`FR-046` | `CMP-004` | `DATA-031`, `DATA-032` | `INT-014` | `TEST-040`, `TEST-041`, `TEST-046` |
| `FR-047` | `CMP-008` | `DATA-033` | `INT-015` | `TEST-045`, `EVAL-009`–`EVAL-013` |
| `FR-048` | `CMP-004`, `CMP-008` | `DATA-023`, `DATA-028` | `INT-013`, `INT-015` | `TEST-033`, `TEST-044` |
