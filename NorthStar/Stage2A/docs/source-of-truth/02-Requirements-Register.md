# 02 — Requirements Register

**Version:** `0.3.0`

## 1. Preserved baseline

All accepted S00/S01 identifiers and meanings remain in force. The supplied S01 handoff explicitly requires preservation of `US-001`–`US-012`, `CMP-001`–`CMP-011`, the Stage 1 schemas/contracts/tests, application-owned disposition and deterministic authorization before future model context. Detailed text for the previous requirement register was not supplied separately; this file does not invent or renumber it.

Known S01 verified outcomes retained:

- bounded UTF-8 text/Markdown intake;
- SHA-256 and exact source-line provenance;
- provider-neutral one-turn summary contract;
- fixed preliminary/unapproved/human-review semantics;
- local atomic source/metadata/invocation/summary artifacts;
- no agent/tool/retrieval contract.

## 2. S02A functional requirements

| ID | Requirement | Priority | Status |
|---|---|---:|---|
| `FR-033` | Ingest a non-empty approved manifest of bounded local policy, control, business-process, taxonomy and prior-assessment sources. | Must | Verified locally |
| `FR-034` | Preserve source identity, type, owner, authority status, business version, effective dates, jurisdictions, domains, raw/normalized hashes and transformation lineage. | Must | Verified locally |
| `FR-035` | Produce deterministic structure-aware chunks with stable IDs, heading paths and exact line coordinates. | Must | Verified locally |
| `FR-036` | Require valid classification/group/purpose/residency metadata and copy it exactly to every chunk. | Must | Verified locally |
| `FR-037` | Publish immutable version packages, active/historical corpus manifest and ingestion run records atomically and idempotently. | Must | Verified locally |
| `FR-038` | Record limited risk flags for instruction-like/credential-seeking content without interpreting it as executable instruction. | Must | Verified locally |

## 3. S02A non-functional requirements

| ID | Requirement | Status |
|---|---|---|
| `NFR-026` | Identical content, metadata, parser and chunker versions produce stable source/chunk IDs. | Verified |
| `NFR-027` | Preparation runs locally without model, embedding, vector database or paid service. | Verified |
| `NFR-028` | A failed version preparation cannot become active or expose a partial version package. | Verified by design/integration tests |
| `NFR-029` | Independent validation detects hash, coordinate, duplicate-ID and access propagation corruption. | Verified |
| `NFR-030` | S02A exposes no search, model-context, agent, tool, graph or memory contract. | Verified |

## 4. Control objectives

| Control | S02A implementation |
|---|---|
| `CTL-001 Source Provenance` | raw/normalized SHA-256; source version; exact line coordinates; transformation versions. |
| `CTL-002 Structured Output Validation` | typed descriptors, scopes, versions, chunks, manifest and run record. |
| `CTL-006 Access Boundary Metadata` | fail-closed non-empty groups; public-only wildcard; exact chunk propagation. Enterprise PDP is still planned. |
| `CTL-014 Change and Dependency Verification` | parser/chunker/schema versions included in technical identity; tests and compilation recorded. |

## 5. Traceability

| Requirement | Component | Data | Interface | Tests/evaluations |
|---|---|---|---|---|
| `FR-033` | `CMP-004` | `DATA-019`, `DATA-024` | `INT-009` | `TEST-020`–`022`, `026` |
| `FR-034` | `CMP-004`, `CMP-009` | `DATA-019`, `DATA-021` | `INT-009` | `TEST-020`, `026`, `EVAL-005` |
| `FR-035` | `CMP-004` | `DATA-022` | `INT-010` | `TEST-023`–`025`, `EVAL-005`–`007` |
| `FR-036` | `CMP-004` | `DATA-020`, `DATA-022` | `INT-009`, `010` | `TEST-028`, `031`, `EVAL-008` |
| `FR-037` | `CMP-004`, `CMP-009` | `DATA-021`, `023`, `024` | `INT-010` | `TEST-026`, `027` |
| `FR-038` | `CMP-004`, `CMP-008` | `DATA-021`, `022`, `025` | `INT-011` | `TEST-029` |
| `NFR-030` | `CMP-011` | repository | none | `TEST-032` |

## 6. Deferred Stage 2 requirements

S02B must implement, test and trace:

- query contract and authenticated access context;
- filtering before candidate exposure;
- lexical and semantic candidate generation;
- hybrid fusion and reranking;
- effective-date/authority filters;
- citation assembly and exact validation;
- retrieval quality, leakage, latency and freshness evaluation.
