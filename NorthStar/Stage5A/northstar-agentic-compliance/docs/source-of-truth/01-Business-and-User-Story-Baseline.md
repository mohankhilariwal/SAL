# 01 — Business and User Story Baseline

**Version:** `1.1.0`

## Context carried from S04C

Maya can start a bounded regulatory assessment through the compositional harness, wait for external human review, submit an authorized decision and resume the same `GRAPH-001` lifecycle. Instructions, authorized context, frozen tools, workspaces, validation, traces and hooks are versioned and repeatable. The output remains preliminary and no final legal/compliance authority has moved to AI.

## S05A narrative development

Priya Raman finds that the accepted definition of `AGT-001` is split among the system instruction, graph invariants, tool catalogue, harness manifest, approval contract, requirements, ADRs and tests. Sofia Alvarez cannot answer one governance question from one artefact: “What exactly is this agent permitted, required and prohibited to do, and what evidence blocks deployment when that definition changes?” Marcus Green warns that simply putting the answer into a prompt would make a probabilistic instruction look like a security boundary.

NorthStar therefore creates one formal machine-readable agent specification. It records the complete design contract while preserving all external enforcement owners. Elena binds its digest into the harness manifest. Liam adds pre-start and post-result assertions. Sofia turns the traceability section into required tests/evaluations and a deny-by-default local release gate.

## User-story effect

- `US-001`–`US-012` meanings remain unchanged.
- Maya gains no new autonomy or data access.
- Daniel remains accountable for business use and human review.
- Priya owns technical specification integrity and compatibility.
- Sofia owns evaluation/risk review and gate evidence.
- Marcus reviews authority, context and tampering boundaries.
- Liam owns operational validation and lifecycle evidence.
- Aisha remains the accountable process/control owner for later accepted remediation decisions.

## Business acceptance criteria added

1. One accepted artefact states `AGT-001` purpose, scope, goals, non-goals, authority, context, human control, termination, SLOs, evaluation and retirement.
2. A modified or incompatible specification blocks a new run before any context loader, model or tool executes.
3. A retired specification cannot start new work.
4. Missing required evaluation/security evidence blocks release.
5. The specification cannot authorize a tool, approve a result, choose a graph route or create final closure.
6. Context remains case-bounded, authorized-before-load, provenance-preserving, capped at eight items/12,000 characters and memory-free.

## Remaining business limitation

The current context envelope is bounded but short-lived. Long investigations may exceed its limit, yet NorthStar has not defined safe compaction, regeneration, working history, memory write policy, deletion, temporal validity or cross-case isolation. That is the next business/architecture problem; it is not solved in S05A.
