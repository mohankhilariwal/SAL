# 09 — Stage Handoff Pack

## A. Stage completed

- **Stage identifier:** S02B
- **Stage title:** Retrieval, Reranking, Citations and RAG Evaluation
- **Architecture version:** `0.4.0`
- **Repository version:** `0.4.0`
- **Handoff version:** `0.4.0`
- **Completion date:** 2026-07-31
- **Status:** Completed within the recorded local/offline verification boundary
- **Consistency audit:** Passed with recorded exceptions `ISS-014`, `ISS-015`, `ISS-016`, `ISS-018`, `ISS-019` and `ISS-020`

## B. Capabilities now available

1. Deterministic query-time filtering by group, clearance, purpose, residency, effective date, jurisdiction and explicit query metadata.
2. Authorization before lexical/semantic scoring or candidate-text exposure.
3. Local BM25 lexical candidate generation.
4. Local deterministic TF-IDF/truncated-SVD latent semantic candidate generation.
5. Weighted reciprocal-rank fusion with versioned configuration.
6. Deterministic metadata-aware reranking with ranking reasons.
7. Suppression of substantially overlapping passages from the same source version.
8. Application-built `CIT-*` exact citations containing `KSV-*`, `CHK-*`, line range, source hash and excerpt.
9. Independent citation reconstruction and tamper rejection.
10. Bounded `DATA-032 RetrievalContext` with an untrusted-content notice.
11. Index manifest bound to corpus hash, source versions and ranking configuration.
12. Retrieval evaluation with precision@k, recall@k, reciprocal rank, citation correctness, forbidden hits, duplicate spans and local latency.
13. Five synthetic normal/negative/permission-boundary evaluation cases.
14. Updated cumulative architecture, four new ADRs, repository and all ten source-of-truth artefacts.

Not implemented: authenticated enterprise identity/PDP, live repository/index service, production embeddings/cross-encoder, query rewriting, graph/SQL RAG, grounded model generation, answer faithfulness evaluation, model-selectable tools, agents, graphs, memory, case/workflow state, approvals, production telemetry/audit or enterprise records.

## C. Accepted architecture decisions

- `ADR-001` through `ADR-013` remain accepted.
- `ADR-014`: authorize before retrieval scoring and text exposure.
- `ADR-015`: use local hybrid lexical/latent-semantic retrieval and weighted RRF behind provider-neutral contracts.
- `ADR-016`: use deterministic metadata-aware reranking and overlap suppression.
- `ADR-017`: use exact application-owned citations and retrieval-first RAG evaluation; defer generated-answer claims.

## D. Current component inventory

| ID | Name | Current status/responsibility |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Partial local evidence consumer. |
| `CMP-002` | Regulatory Intake Boundary | Retained S01 bounded input. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Partial one-shot pipeline; no durable state. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Partial implemented through preparation, authorized retrieval, ranking, citations and context assembly. |
| `CMP-005` | Enterprise Integration Boundary | Planned. |
| `CMP-006` | Human Review and Approval Boundary | Planned; preliminary review semantics only. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Planned; local principal claims are not authentication. |
| `CMP-008` | Evaluation and Assurance Boundary | Partial preparation and retrieval evaluation. |
| `CMP-009` | Observability and Audit Boundary | Partial local reports/manifests; not audit ledger. |
| `CMP-010` | Runtime and Deployment Boundary | Partial local Python runtime. |
| `CMP-011` | Source-of-Truth Governance Pack | Implemented and updated to `0.4.0`. |

## E. Current agent inventory

None. No `AGT-*` identifier is allocated. The fixed retrieval pipeline has no goal-directed action selection, tools, replanning, delegation, loop or authority.

## F. Current data and state objects

`DATA-001` through `DATA-025` remain accepted. S02B adds `DATA-026 RetrievalPrincipalContext`, `DATA-027 RetrievalQuery`, `DATA-028 RetrievalIndexManifest`, `DATA-029 RetrievalCandidate`, `DATA-030 RankedEvidence`, `DATA-031 EvidenceCitation`, `DATA-032 RetrievalContext` and `DATA-033 RetrievalEvaluationCaseResult`, all schema `1.0.0` or a documented transient logical form.

No `DATA-002 RegulatoryCase`, `DATA-007 ReviewDecision`, `DATA-009 AgentRunState` or `DATA-010 AuthorizationGrant` is instantiated. `DATA-015` remains `stage1-summary-v1`, preliminary and human-reviewed.

## G. Current interfaces and tools

- `INT-001`, `INT-002`, `INT-007`, `INT-008` retained from S01.
- `INT-009`, `INT-010`, `INT-011` retained from S02A.
- `INT-012 Authorized Retrieval Request Contract` implemented locally.
- `INT-013 Retrieval Index and Ranking Contract` implemented locally.
- `INT-014 Cited Retrieval Context Contract` implemented locally.
- `INT-015 Retrieval/RAG Evaluation Contract` implemented locally.

No executable model-selectable tool exists and no `TOOL-*` identifier is allocated.

## H. Repository state

Repository `northstar-agentic-compliance` version `0.4.0`. Primary entry points are the modules under `src/northstar_compliance/knowledge/`, the three S02B scripts, the S02B datasets/tests, the current chapter and the ten registers. The complete tree is recorded in `07-Repository-Manifest.md` and included in the packaged ZIP.

## I. Tests completed

- Accepted S02A evidence `TEST-020`–`TEST-032` and `EVAL-005`–`EVAL-008` is retained from the supplied handoff; a compatible subset of preparation behavior is re-executed in this overlay.
- `TEST-033` index manifest/corpus compatibility — passed.
- `TEST-034` authorization precedes scoring; restricted chunks are absent — passed.
- `TEST-035` BM25 exact-term retrieval — passed.
- `TEST-036` latent-semantic paraphrase retrieval — passed.
- `TEST-037` RRF determinism — passed.
- `TEST-038` metadata-aware reranking — passed.
- `TEST-039` overlap deduplication — passed.
- `TEST-040` exact citations validate — passed.
- `TEST-041` tampered citation rejected — passed.
- `TEST-042` pre-effective content filtered — passed.
- `TEST-043` purpose/residency mismatch fails closed — passed.
- `TEST-044` incompatible index configuration rejected — passed.
- `TEST-045` retrieval metrics and permission boundaries — passed.
- `TEST-046` no agent/tool/generation contract — passed.

**Executed result:** 20 pytest tests passed on Python 3.13.5 with NumPy 2.3.5 and pytest 9.0.2. Demo and validator passed.

Synthetic evaluation results:

| Evaluation | Precision@4 | Recall@4 | MRR | Citation correctness | Forbidden hits | Duplicate spans |
|---|---:|---:|---:|---:|---:|---:|
| `EVAL-009` lending | 0.50 | 0.25 | 1.00 | 1.00 | 0 | 0 |
| `EVAL-010` payments | 1.00 | 0.444 | 1.00 | 1.00 | 0 | 0 |
| `EVAL-011` customer data | 1.00 | 0.444 | 1.00 | 1.00 | 0 | 0 |
| `EVAL-012` Maya restricted-negative | 0.00* | 1.00* | 0.00 | 1.00 | 0 | 0 |
| `EVAL-013` Sofia restricted-positive | 1.00 | 1.00 | 1.00 | 1.00 | 0 | 0 |

`*` The negative case has no relevant authorized labels; recall is conventionally 1.0 for an empty relevant set. The meaningful security result is zero forbidden hits, not the precision/recall pair.

## J. Known limitations

1. Five synthetic English documents and nineteen chunks only.
2. Local LSA is not a production embedding model.
3. Scorers are rebuilt per authorized subset and do not represent enterprise scale.
4. Principal attributes are not authenticated by `CMP-007`.
5. No live source connector, freshness SLO or automatic reconciliation.
6. No query rewriting, multi-hop, graph RAG or structured enterprise query.
7. No production cross-encoder or learned reranker benchmark.
8. Correct citations do not prove correct interpretation.
9. No generated answer, faithfulness or answer-relevance evaluation.
10. No production concurrency, throughput, tail latency or cost benchmark.
11. Local reports are not audit/records systems.
12. Mermaid CLI and direct Python 3.12 execution remain open.
13. Nine byte-exact S02A registers/repository were not attached.

## K. Open risks, assumptions and issues

Active immediate items include `RSK-024`–`RSK-027`, `RSK-032`–`RSK-039`; `ASM-012`–`ASM-015`; and `ISS-011`, `ISS-012`, `ISS-014`–`ISS-020`.

## L. Compatibility constraints

1. Preserve NorthStar, eight personas, `US-001`–`US-012` and all stable identifiers/meanings.
2. Preserve `CMP-001`–`CMP-011` names and boundaries.
3. Preserve S01 `DATA-015`, `stage1-summary-v1`, SHA-256, exact evidence and application-owned disposition semantics.
4. Preserve S02A `DATA-019`–`DATA-025`, `INT-009`–`INT-011`, `KSV-*`, `CHK-*`, exact lines and active/historical version meaning.
5. Preserve authorization before scoring/text exposure; later tools/agents may not widen `DATA-032` access.
6. Rebuild and re-evaluate after corpus, parser, chunker, schema, semantic model, fusion, reranker or retrieval metadata changes.
7. Keep provider-specific embedding/reranker types behind contracts.
8. Do not treat retrieval evidence as accepted obligation, policy mapping, gap, case or review decision.
9. Do not treat local artifacts as enterprise records or audit ledger.
10. Do not introduce graph, memory or multi-agent behavior in the next stage unless explicitly requested and justified.

## M. Required input for the next stage

The next stage must reconstruct all ten `0.4.0` artefacts; `ADR-001`–`ADR-017`; `DATA-019`–`DATA-033`; `INT-009`–`INT-015`; the cumulative diagram; the prepared corpus, index manifest, evaluation cases/results; Stage 1 disposition invariants; and active risks/issues.

## N. Next architectural problem

Maya can now locate and cite authorized evidence, but retrieval cannot perform the remaining business operations. It cannot search a live external source, query authoritative control/case services, create a draft case, persist a candidate mapping or send a review request. Those actions require typed capability contracts, deterministic authorization, observed results, explicit run state, bounded iteration and safe termination. Greater retrieval complexity will not solve that problem.

## O. Exact continuation instruction

> Continue the NorthStar Agentic AI Architecture Playbook by executing only **Stage 3 — Tool-Using Single Agent**. Reconstruct the `0.4.0` baseline, preserve authorized retrieval and preliminary human-accountability invariants, introduce only justified typed tools and one bounded agent loop, update all affected artefacts, run the consistency audit and stop after the Stage 3 handoff.
