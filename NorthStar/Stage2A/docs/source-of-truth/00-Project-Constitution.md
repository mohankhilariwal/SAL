# 00 — Project Constitution

**Project:** NorthStar Agentic AI Architecture Playbook  
**Repository:** `northstar-agentic-compliance`  
**Architecture / repository / handoff version:** `0.3.0`  
**Current completed stage:** `S02A — Ingestion, Chunking and Knowledge Preparation`  
**Updated:** 2026-07-31

## 1. Purpose

Maintain one narrative-driven, implementation-oriented architecture playbook for NorthStar Financial Services. Each capability is introduced only when the evolving regulatory-change use case requires it. The project progresses from the simplest viable design to a production-grade architecture without relabelling assistants as agents or transferring regulated accountability to probabilistic software.

## 2. Authoritative source order

1. Execution Controller.
2. Approved narrative-driven master prompt.
3. Current continuation instruction.
4. The ten files under `docs/source-of-truth/`.
5. Stage chapters, code, tests and examples.

For S02A, the uploaded `Stage-1-Handoff-Pack(3)(1).md` is the immediate authoritative S01 reconstruction input. The other nine detailed S01 files were not supplied separately; this repository preserves known S01 facts and does not invent missing definitions.

## 3. Stable narrative

- Organization: **NorthStar Financial Services**.
- Primary user: **Maya Chen — Regulatory Compliance Analyst**.
- Supporting personas: Daniel Brooks, Priya Raman, Elena Petrov, Marcus Green, Sofia Alvarez, Liam O’Connor and Aisha Rahman.
- Main user story: AI-assisted analysis of a new regulatory publication, evidence-backed candidate impact mapping and risk-based human review, without transferring accountability to an autonomous system.

## 4. Architecture principles

1. Human accountability is non-transferable.
2. Critical authorization, legal, privacy, financial and irreversible-action controls are deterministic and outside model reasoning.
3. Add the simplest sufficient capability; no autonomy before an action requirement.
4. Preserve source provenance, authority, version, uncertainty and human decisions as separate concepts.
5. Treat external and internal document content as untrusted data.
6. Enforce authorization before retrieval and before model-context assembly.
7. Keep provider and index implementation types behind stable application contracts.
8. Use one cumulative architecture and one evolving repository.
9. Accepted identifiers are stable; changes require impact analysis and ADR updates.
10. Do not store or require hidden chain-of-thought; store concise evidence and observable decisions.
11. Local tutorial artifacts are not enterprise cases, review decisions, records or audit ledger entries.
12. A capability is “implemented” only when code and stated tests execute within a recorded boundary.

## 5. S02A constitutional boundary

S02A implements only deterministic knowledge preparation within `CMP-004`:

- approved manifest ingestion;
- strict UTF-8 text/Markdown parsing;
- raw and normalized SHA-256 provenance;
- deterministic structure-aware, line-preserving chunking;
- source authority, effective-date, jurisdiction, domain and access metadata;
- immutable source-version packages;
- idempotent replay and supersession;
- risk flags for instruction-like content;
- local preparation validation.

S02A explicitly does **not** implement search, embeddings, reranking, query-time authorization, context assembly, grounded generation, model-selected tools, agent loops, graph state, memory, case state or approval decisions.

## 6. Technology and compatibility policy

- Declared Python: `>=3.11,<3.15`.
- Executed: Python `3.13.5`.
- Test dependency: pytest `9.0.2`.
- Runtime dependencies for S02A: Python standard library only.
- Content hashing: SHA-256.
- Files: strict UTF-8 `.txt` and `.md` only.
- Structured artifacts: JSON and JSONL schema `1.0.0`.
- Atomic publication: staging plus same-filesystem `os.replace()`.
- S01 `DATA-015` schema `1.0.0`, `stage1-summary-v1` and exact evidence semantics remain unchanged.

## 7. Definition of done for S02A

S02A is complete only when:

- all ten source-of-truth files are updated;
- `CMP-004` remains correctly labelled partial/preparation-only;
- new data and interface IDs are consistent across docs and code;
- demo corpus preparation executes;
- tests cover parsing, path safety, deterministic chunks, coverage, access propagation, idempotency, version changes and untrusted instruction flags;
- no search or agent capability is claimed;
- the handoff identifies authorized retrieval as the next problem.

## 8. Change history

| Version | Stage | Change |
|---|---|---|
| `0.1.0` | S00 | Architecture constitution and governance baseline. |
| `0.2.0` | S01 | Manual process and bounded basic LLM assistant. |
| `0.3.0` | S02A | Controlled ingestion, chunking and prepared knowledge corpus. |
