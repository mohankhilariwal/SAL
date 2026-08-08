# 09 — Stage Handoff Pack

## A. Stage completed

- **Stage identifier:** S02A
- **Stage title:** Ingestion, Chunking and Knowledge Preparation
- **Architecture version:** `0.3.0`
- **Repository version:** `0.3.0`
- **Handoff version:** `0.3.0`
- **Completion date:** 2026-07-31
- **Status:** Completed within the recorded local/offline verification boundary
- **Consistency audit:** Passed with recorded exceptions `ISS-009`, `ISS-014` and `ISS-015`

## B. Capabilities now available

1. Approved local manifest intake for synthetic/public-safe internal knowledge exports.
2. Strict UTF-8 `.txt`/`.md` parsing with bounded path, size, NUL and type validation.
3. Raw and normalized SHA-256 provenance with exact line preservation.
4. Deterministic Markdown-aware, line-window chunking with configurable overlap.
5. Stable `KSV-*` source-version and `CHK-*` chunk identities.
6. Source authority, owner, business version, effective dates, jurisdiction, domain, purpose, residency, retention and classification metadata.
7. Fail-closed non-empty access groups and exact access propagation to chunks.
8. Immutable source-version packages, active/historical corpus manifest, idempotent replay and supersession.
9. Atomic local publication through staging and same-filesystem replacement.
10. Diagnostic risk flags for instruction-like or credential-seeking content; content remains untrusted data.
11. Independent corpus validation for hashes, coordinates, line coverage, duplicate IDs and access propagation.
12. Synthetic five-source corpus, adversarial fixture, runnable demo and 12 automated tests.
13. Updated cumulative architecture and all ten source-of-truth artefacts.

Not implemented: search, embeddings, lexical/vector indexes, reranking, query-time authorization, context assembly, grounded model generation, model-selectable tools, agents, graphs, memory, workflow/case state, approvals or production audit.

## C. Accepted architecture decisions

- `ADR-001` through `ADR-010` remain accepted and unchanged.
- `ADR-011`: split Stage 2 at the preparation/retrieval contract boundary; S02A stops before search and context assembly.
- `ADR-012`: use deterministic structure-aware, line-preserving chunks with versioned policy and overlap.
- `ADR-013`: use immutable content-addressed packages with required fail-closed access metadata and active pointers.

## D. Current component inventory

| ID | Name | Current status/responsibility |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Partial local CLI from S01; unchanged. |
| `CMP-002` | Regulatory Intake Boundary | Implemented for bounded S01 publication input; unchanged. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Partial one-shot flow; no case/workflow state and no corpus query. |
| `CMP-004` | Knowledge and Evidence Access Boundary | **Partial S02A:** manifest validation, parsing, provenance, chunking, metadata, immutable corpus and validation. No retrieval. |
| `CMP-005` | Enterprise Integration Boundary | Planned; no live connector or change feed. |
| `CMP-006` | Human Review and Approval Boundary | Planned; S01 status semantics only. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Planned; local access strings are metadata, not authenticated authorization. |
| `CMP-008` | Evaluation and Assurance Boundary | Partial local preparation integrity/evaluation tests. |
| `CMP-009` | Observability and Audit Boundary | Partial local ingestion/provenance artifacts; not audit ledger. |
| `CMP-010` | Runtime and Deployment Boundary | Partial local Python runtime. |
| `CMP-011` | Source-of-Truth Governance Pack | Implemented and updated to `0.3.0`. |

## E. Current agent inventory

None. No `AGT-*` identifier is allocated. The preparation service executes a fixed deterministic procedure; it cannot select actions, use tools, replan, delegate, maintain semantic memory or own authority.

## F. Current data and state objects

`DATA-001` through `DATA-018` remain accepted with S01 meanings and schemas. S02A adds:

| ID | Name | Schema/owner |
|---|---|---|
| `DATA-019` | KnowledgeSourceDescriptor | `1.0.0`; source owner/governance metadata |
| `DATA-020` | AccessScope | `1.0.0`; identity/data owner input, locally asserted |
| `DATA-021` | KnowledgeDocumentVersion | `1.0.0`; `CMP-004` prepared-source record |
| `DATA-022` | KnowledgeChunk | `1.0.0`; exact line/citation-ready chunk |
| `DATA-023` | KnowledgeCorpusManifest | `1.0.0`; active/historical corpus and transformation versions |
| `DATA-024` | IngestionRunRecord | `1.0.0`; local operational evidence |
| `DATA-025` | KnowledgePreparationReport | logical local validation result |

No `DATA-002 RegulatoryCase`, `DATA-007 ReviewDecision`, `DATA-009 AgentRunState` or `DATA-010 AuthorizationGrant` is instantiated. S01 `DATA-015 PreliminaryRegulatorySummary` remains schema `1.0.0`, contract `stage1-summary-v1`.

## G. Current interfaces and tools

| ID | Contract | Control/authorization | Status |
|---|---|---|---|
| `INT-001` | S01 publication intake | bounded local validation | Retained |
| `INT-002` | S01 preliminary summary | application-owned preliminary/human-review status | Retained |
| `INT-007` | S01 local evaluation | local test boundary | Retained |
| `INT-008` | S01 partial process/invocation evidence | provider-specific types behind contract | Retained |
| `INT-009` | Authorized Knowledge Ingestion Contract | approved manifest, bounded root, valid access metadata; enterprise auth pending | Implemented locally |
| `INT-010` | Prepared Corpus Export Contract | immutable version packages and corpus manifest; access metadata must not be bypassed | Implemented locally |
| `INT-011` | Knowledge Preparation Evaluation Contract | independent hash/coordinate/access/coverage validation | Implemented locally |

No executable model-selectable tool exists and no `TOOL-*` identifier is allocated.

## H. Repository state

Repository `northstar-agentic-compliance` version `0.3.0`. Important entry points:

- `src/northstar_compliance/knowledge/service.py`
- `src/northstar_compliance/knowledge/parser.py`
- `src/northstar_compliance/knowledge/chunker.py`
- `src/northstar_compliance/knowledge/store.py`
- `src/northstar_compliance/knowledge/validation.py`
- `scripts/run_stage2a_demo.py`
- `scripts/validate_stage2a.py`
- `scripts/consistency_audit_stage2a.py`
- `datasets/stage2a/input/manifest.json`
- `docs/stages/Stage-2A-Ingestion-Chunking-and-Knowledge-Preparation.md`
- `docs/source-of-truth/09-Stage-Handoff-Pack.md`

The complete current tree is in `07-Repository-Manifest.md`. The supplied S01 handoff is preserved at `docs/baseline/Stage-1-Handoff-Pack-supplied.md`. Prior S01 implementation paths remain compatibility constraints and are not silently recreated in this overlay package.

## I. Tests completed

| Test/evaluation | Outcome |
|---|---|
| `TEST-001`–`TEST-019`, `EVAL-001`–`EVAL-004` | Retained as accepted S01 evidence from the supplied handoff; not re-executed because the S01 repository was not attached. |
| `TEST-020` | Raw/normalized hashes and lines preserved — passed. |
| `TEST-021` | NUL, malformed UTF-8, unsupported and oversized input rejected — passed. |
| `TEST-022` | Path traversal outside approved root rejected — passed. |
| `TEST-023` | Chunk IDs deterministic and text matches exact lines — passed. |
| `TEST-024` | Chunks do not cross Markdown section boundaries — passed. |
| `TEST-025` | Every nonempty source line covered — passed. |
| `TEST-026` | Identical replay reuses the same source-version ID — passed. |
| `TEST-027` | Changed content creates a new version and retains history — passed. |
| `TEST-028` | Missing access groups fail closed — passed. |
| `TEST-029` | Instruction-like fixture flagged but never executed — passed. |
| `TEST-030` | Validator reconstructs exact chunk text from coordinates — passed. |
| `TEST-031` | Descriptor and chunk access scopes match — passed. |
| `TEST-032` | Compilation/repository audit finds no agent/tool/search implementation — passed. |
| `EVAL-005` | Line-coordinate correctness — `100%` on sample corpus. |
| `EVAL-006` | Nonempty line coverage — `100%` on sample corpus. |
| `EVAL-007` | Deterministic identity on replay — `100%` stable. |
| `EVAL-008` | Missing/mismatched access scope — `0` chunks. |

Executed environment: Python `3.13.5`, pytest `9.0.2`; 12 pytest tests passed, demo completed with expected diagnostic warnings, validator passed and package compilation passed.

## J. Known limitations

1. Text/Markdown only; no PDF, Office, HTML, image or OCR parser.
2. Local metadata claims are not enterprise IAM/PDP decisions.
3. No authoritative repository connector, feed, reconciliation or freshness SLO.
4. No malware scanner, DLP service, KMS signing, WORM or enterprise retention.
5. Risk flags are incomplete diagnostics and do not establish content safety.
6. Chunking is character/line based rather than token-aware or empirically tuned for retrieval.
7. No search/index/reranking/query-time authorization or grounded generation.
8. Small synthetic English corpus only.
9. No large-corpus concurrency, throughput or cost benchmark.
10. Local artifacts are not cases, records or audit ledger entries.
11. Mermaid was structurally checked but not rendered by Mermaid CLI.
12. Python 3.12 direct execution remains open.
13. The nine detailed S01 registers and S01 repository were not attached; S02A was reconstructed from the supplied handoff.

## K. Open risks, assumptions and issues

Preserve the S01 active identifiers listed in the supplied handoff. New active items are:

- Risks: `RSK-024`–`RSK-032`.
- Assumptions: `ASM-010`–`ASM-012`.
- Issues: `ISS-009`–`ISS-015`.

Immediate S02B priorities: `RSK-024`, `RSK-025`, `RSK-026`, `RSK-027`, `RSK-032`, `ISS-011`, `ISS-012` and `ASM-012`.

## L. Compatibility constraints

1. Preserve NorthStar and all eight personas.
2. Preserve `US-001`–`US-012` and all existing identifiers/meanings.
3. Preserve `CMP-001`–`CMP-011` names and boundaries.
4. Preserve S01 schema `1.0.0`, `stage1-summary-v1`, SHA-256 and exact evidence semantics.
5. Preserve application ownership of disposition, human review, approval and legal-conclusion fields.
6. Keep provider/index-specific types behind contracts.
7. Consume `DATA-022` only through `INT-010`; do not independently re-chunk raw sources in S02B.
8. Enforce deterministic authorization before candidate text is exposed or model context is assembled.
9. Rebuild/re-evaluate indexes when parser, chunker, schema or retrieval-relevant metadata changes.
10. Do not treat local artifacts as cases, review decisions, enterprise records or audit ledger.
11. Do not allocate agent/tool IDs or introduce graph/memory/multi-agent behavior in S02B unless separately requested and justified.
12. Preserve source authority, active/historical versions and exact citation coordinates.

## M. Required input for the next stage

S02B must reconstruct:

- all ten version `0.3.0` source-of-truth artefacts;
- `ADR-001` through `ADR-013`;
- `DATA-019` through `DATA-025` and `INT-009` through `INT-011`;
- the prepared sample corpus and validation output;
- the S01 summary/disposition compatibility constraints;
- the cumulative architecture diagram and active risks/issues.

## N. Next architectural problem

Maya can inspect exact, current, access-labelled chunks, but cannot ask which passages support the candidate lending, payments and customer-data impacts. Manually reading the prepared corpus recreates the original bottleneck. Search must combine exact terminology and semantic similarity, filter authorization before exposure, manage overlapping chunks, rerank evidence and return citation-correct context without adding autonomy.

## O. Exact continuation instruction

> Continue the NorthStar Agentic AI Architecture Playbook by executing only **Stage 2B — Authorized Retrieval, Ranking and Grounded Evidence**. Reconstruct the current architecture from all ten version `0.3.0` source-of-truth artefacts, preserve all accepted identifiers, S01 summary/disposition contracts and the S02A prepared-corpus contract, begin with Maya’s inability to locate the best authorized evidence, add lexical and semantic candidate generation, deterministic pre-retrieval access filtering, hybrid fusion, reranking, exact citations and retrieval evaluation, update the cumulative Mermaid architecture and same repository, add security/performance/cost/failure tests, update all affected artefacts, finish with the complete handoff pack, perform the consistency audit and stop before tools or agents.
