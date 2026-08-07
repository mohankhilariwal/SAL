# 09 - Stage Handoff Pack

## A. Stage completed

- **Stage identifier:** S01
- **Stage title:** Manual Process and Basic LLM Assistant
- **Architecture version:** 0.2.0
- **Repository version:** 0.2.0
- **Handoff version:** 0.2.0
- **Status:** Completed within the recorded local/offline verification boundary

## B. Capabilities now available

1. Controlled UTF-8 text/Markdown publication intake.
2. Immutable SHA-256 provenance and line coordinates.
3. Provider-neutral single-turn summarization contract.
4. Deterministic offline test double and optional managed-model adapter.
5. Structured preliminary summary with source facts, candidate affected areas, deadlines, missing information and uncertainty.
6. Exact source-line/excerpt validation outside model reasoning.
7. Application-owned unapproved disposition and mandatory human review.
8. Local atomic persistence of source, metadata, invocation and summary.
9. Local tests, adversarial fixture, evaluation cases and acceptance validation.
10. Updated cumulative architecture and all ten source-of-truth artefacts.

No RAG, agent, graph, model-selectable tool, persistent workflow state, memory, enterprise authorization, approval service, control plane or production audit runtime is implemented.

## C. Accepted architecture decisions

- `ADR-001` through `ADR-007` remain accepted.
- `ADR-008`: use a bounded, single-turn structured assistant rather than search, RAG, an agent or multiple agents for the immediate first-reading need.
- `ADR-009`: isolate provider-specific invocation behind a minimal model contract with an offline test double.
- `ADR-010`: enforce bounded text intake, hash/line provenance, deterministic evidence validation, fixed status and local atomic artifacts.

## D. Current component inventory

| ID | Name | Status |
|---|---|---|
| CMP-001 | Analyst Experience Portal | Partial local CLI |
| CMP-002 | Regulatory Intake Boundary | Implemented for bounded Stage 1 input |
| CMP-003 | Case and Workflow Orchestration Boundary | Partial one-shot flow; no case state |
| CMP-004 | Knowledge and Evidence Access Boundary | Planned; next-stage requirement |
| CMP-005 | Enterprise Integration Boundary | Planned |
| CMP-006 | Human Review and Approval Boundary | Planned; status semantics only |
| CMP-007 | Identity, Authorization and Policy Boundary | Planned |
| CMP-008 | Evaluation and Assurance Boundary | Partial local tests/evaluations |
| CMP-009 | Observability and Audit Boundary | Partial local evidence artifacts |
| CMP-010 | Runtime and Deployment Boundary | Partial local Python runtime |
| CMP-011 | Source-of-Truth Governance Pack | Implemented and updated |

## E. Current agent inventory

None. No agent identifier is allocated. The Stage 1 assistant makes one request and terminates; it does not select actions, observe tools, replan, loop, delegate or own authority.

## F. Current data and state objects

`DATA-001` through `DATA-014` remain accepted. S01 makes `DATA-001` and a line-based specialization of `DATA-004` executable and adds:

- `DATA-015 PreliminaryRegulatorySummary`.
- `DATA-016 SummaryClaim`.
- `DATA-017 ModelInvocationRecord`.
- `DATA-018 PublicationMetadata`.

No `DATA-002 RegulatoryCase`, `DATA-007 ReviewDecision`, `DATA-009 AgentRunState` or `DATA-010 AuthorizationGrant` is instantiated.

## G. Current interfaces and tools

`INT-001` intake, `INT-002` preliminary summary and `INT-007` local evaluation are implemented in constrained form; `INT-008` is partial through process and invocation evidence. Other conceptual interfaces remain planned. No model-selectable tool exists.

## H. Repository state

Repository `northstar-agentic-compliance` version 0.2.0. Important entry points:

- `src/northstar_compliance/cli.py`
- `src/northstar_compliance/model_gateway.py`
- `src/northstar_compliance/validation.py`
- `scripts/run_stage1_demo.sh`
- `scripts/validate_stage1.py`
- `docs/stages/Stage-1-Manual-Process-and-Basic-LLM-Assistant.md`
- `docs/source-of-truth/09-Stage-Handoff-Pack.md`

The complete tree is in `07-Repository-Manifest.md`.

## I. Tests completed

| Test/evaluation | Outcome |
|---|---|
| TEST-001 to TEST-007 | S00 structural checks retained; source-of-truth validator passed |
| TEST-008 | Source SHA-256 and line count preserved - passed |
| TEST-009 to TEST-011 | Unsupported, empty and oversized input rejected - passed |
| TEST-012 | Fixed preliminary disposition and human review - passed |
| TEST-013 | Exact evidence references validate - passed |
| TEST-014 | Fabricated line reference rejected - passed |
| TEST-015 | Four local artifacts persisted - passed |
| TEST-016 | Adversarial document cannot set approval - passed |
| TEST-017 | Model payload cannot override status - passed |
| TEST-018 | No agent/tool identifier allocated - passed |
| TEST-019 | Model protocol has no retrieval/action contract - passed |
| EVAL-001 | Explicit source obligations extracted in synthetic case - passed |
| EVAL-002 | Lending/payments/customer-data candidate labels present - passed with candidate-only caveat |
| EVAL-003 | Unapproved/human-review semantics invariant - passed |
| EVAL-004 | Prompt-injection fixture cannot widen authority - passed |

## J. Known limitations

1. Managed-model quality was not live-tested.
2. Only bounded text/Markdown input is supported.
3. No internal policies, controls, processes, taxonomy or prior cases are retrieved.
4. Candidate affected areas are hypotheses, not accepted mappings.
5. No case, workflow state, approval decision, retry, fallback or durable recovery exists.
6. No production identity, authorization, residency, observability, audit ledger or records integration exists.
7. Production latency, concurrency, cost and quality SLOs are unknown.
8. Mermaid was not rendered by CLI.
9. Python 3.13 is the accepted baseline; Python 3.13.5 passed (`ISS-006` closed).

## K. Open risks, assumptions and issues

Active immediate items include `RSK-003`, `RSK-005`, `RSK-010`, `RSK-015`, `RSK-018` through `RSK-023`; `ASM-001`, `ASM-002`, `ASM-005`, `ASM-009`; and `ISS-002`, `ISS-003`, `ISS-004`, `ISS-007`, `ISS-008`. `ISS-006` is closed.

## L. Compatibility constraints

1. Preserve NorthStar and all eight personas.
2. Preserve `US-001` through `US-012` meanings and existing identifiers.
3. Preserve `CMP-001` through `CMP-011` names/responsibilities.
4. Preserve `DATA-015` schema `1.0.0`, `stage1-summary-v1`, SHA-256 provenance and exact evidence semantics.
5. Preserve application ownership of disposition, human-review, approval and legal-conclusion fields.
6. Keep provider-specific types behind the model contract.
7. Do not treat local artifacts as cases, review decisions, audit ledger or enterprise records.
8. Do not introduce model-selected tools, agent loops, memory, graph or multi-agent design in Stage 2.
9. Retrieval authorization must be deterministic and precede model context assembly.

## M. Required input for the next stage

Stage 2 must reconstruct all ten files at version 0.2.0, use ADR-001 through ADR-010, preserve the Stage 1 schemas/contracts/tests, use the cumulative diagram and begin from the ungrounded candidate-impact limitation.

## N. Next architectural problem

Maya can obtain a disciplined first reading, but Daniel asks which NorthStar policies, controls and business processes justify the candidate lending, payments and customer-data impacts. The assistant has only the uploaded publication. Pasting the entire enterprise corpus into the prompt would create access, freshness, context, cost and citation problems. NorthStar now needs authorized, evidence-backed retrieval—not more autonomy.

## O. Exact continuation instruction

Execute only **Stage 2 - Retrieval and Grounded Knowledge**, reconstructing context from the ten S01 source-of-truth artefacts; add authorized ingestion, chunking, search, reranking, citations and retrieval evaluation while preserving the non-agentic boundary, update all affected artefacts, perform the consistency audit and stop after the Stage 2 handoff.
