# 05 — Data and Schema Register

## Preserved objects

`DATA-001` through `DATA-025` retain their accepted meanings. S01 `DATA-015 PreliminaryRegulatorySummary` remains schema `1.0.0` and `stage1-summary-v1`; S02B does not alter disposition, review or legal-conclusion semantics. S02A `DATA-019`–`DATA-025` remain the prepared-corpus contract.

## New S02B objects

| ID | Name | Purpose/owner | Schema |
|---|---|---|---|
| `DATA-026` | RetrievalPrincipalContext | Locally asserted subject groups, clearance, purpose, residency, as-of date and jurisdictions; future owner `CMP-007`. | `1.0.0` |
| `DATA-027` | RetrievalQuery | Query text, top-k/candidate limits and explicit source/domain/jurisdiction filters; owner `CMP-004`. | `1.0.0` |
| `DATA-028` | RetrievalIndexManifest | Binds index ID to corpus/config hashes, algorithms, dimensions and source versions; owner `CMP-004`. | `1.0.0` |
| `DATA-029` | RetrievalCandidate | Authorized chunk plus lexical/semantic ranks and fused score; transient inside `CMP-004`. | `1.0.0` logical |
| `DATA-030` | RankedEvidence | Reranked evidence, metadata, score and ranking reasons; owner `CMP-004`. | `1.0.0` |
| `DATA-031` | EvidenceCitation | Exact source/version/chunk IDs, lines, source hash and excerpt; owner `CMP-004`. | `1.0.0` |
| `DATA-032` | RetrievalContext | Bounded cited evidence and untrusted-content notice; owner `CMP-004`. | `1.0.0` |
| `DATA-033` | RetrievalEvaluationCaseResult | Query/principal labels plus precision, recall, reciprocal rank, citation correctness, forbidden hits, duplicate spans, latency and retrieved IDs; owner `CMP-008`. | `1.0.0` |

## Key validation rules

- `DATA-026` is rejected when principal, groups, purpose or residency is empty.
- Clearance is an ordered ceiling; access is also constrained by group intersection, purpose, residency and effective date.
- Query filters narrow access; they never broaden `DATA-020` scope.
- `DATA-028.index_id` is content-derived from corpus and retrieval configuration.
- `DATA-031` is valid only when normalized source reconstruction exactly equals the excerpt.
- `DATA-032.authorization_applied_before_scoring` is application-owned and always true in this contract.
- Retrieved evidence remains candidate context; it is not `DATA-003 CandidateObligation`, an accepted mapping, a case or a review decision.

## Interfaces

| ID | Name | Contract/control | Status |
|---|---|---|---|
| `INT-009` | Authorized Knowledge Ingestion Contract | Preserved from S02A. | Retained |
| `INT-010` | Prepared Corpus Export Contract | Immutable corpus consumed by S02B; no independent rechunking. | Retained/consumed |
| `INT-011` | Knowledge Preparation Evaluation Contract | Preserved validator. | Retained |
| `INT-012` | Authorized Retrieval Request Contract | `DATA-026` + `DATA-027` + index ID → authorized retrieval operation; fail closed. | Implemented locally |
| `INT-013` | Retrieval Index and Ranking Contract | Prepared corpus/config → compatible index manifest and ranked authorized candidates. | Implemented locally |
| `INT-014` | Cited Retrieval Context Contract | Ranked candidates → validated `DATA-030`–`DATA-032`; no approval/disposition fields. | Implemented locally |
| `INT-015` | Retrieval/RAG Evaluation Contract | Versioned cases + retrieval service → `DATA-033` results and gate evidence. | Implemented locally |

No model generation interface is added in S02B.
