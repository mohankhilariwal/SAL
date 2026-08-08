# 00 — Project Constitution

**Architecture/repository version:** `0.5.0`  
**Current completed stage:** `S03A — Tool Contracts and Tool Gateway`

## Stable project identity

- Organization: **NorthStar Financial Services**.
- Repository: `northstar-agentic-compliance`.
- Personas: Maya Chen, Daniel Brooks, Priya Raman, Elena Petrov, Marcus Green, Sofia Alvarez, Liam O’Connor and Aisha Rahman.
- Main user story and supporting stories `US-001`–`US-012` retain their accepted meanings.
- Components `CMP-001`–`CMP-011` retain their accepted names and boundaries.

## Source precedence

1. This versioned source-of-truth pack.
2. The supplied `S02B` handoff for inherited definitions not repeated byte-for-byte here.
3. Accepted ADRs.
4. Stage chapter and implementation.
5. Narrative conversation.

## S03A constitutional invariants

1. Critical authorization and side-effect controls are deterministic and external to model reasoning.
2. `DATA-032 RetrievalContext` access may never be widened by a tool wrapper.
3. All tool calls resolve an exact `TOOL-*` and version through `INT-016` before adapter execution.
4. Input and output schemas fail closed; undeclared arguments are rejected.
5. S03A permits only read-only and reversible local-write impact classes.
6. Reversible writes require idempotency keys, preserve unapproved/human-review semantics and receive no automatic retry.
7. No tool can approve a case, accept a mapping, send an external notification or make a legal conclusion.
8. Local draft artefacts and JSONL events are not enterprise records or a tamper-evident audit ledger.
9. No `AGT-*` identifier, goal-directed loop, graph, durable workflow, memory, delegation, MCP server or multi-agent behavior is implemented.
10. Production identity, PDP, connectors, records, secrets and observability remain future boundaries.

## Version and implementation baseline

- Python compatibility target: `>=3.12,<3.14`.
- Executed runtime: Python `3.13.5`.
- `jsonschema 4.26.0`, `pytest 9.0.2`; NumPy `2.3.5` retained for S02B compatibility.
- Canonical tool schemas: JSON Schema Draft 2020-12.
- Repository and architecture version: `0.5.0`.

## Definition of done for S03A

The stage is complete only when six tool descriptors, the gateway controls, local adapters, tests, evaluation, diagrams, four ADRs, all ten registers, a handoff and a consistency audit agree. No later-stage agent behavior may be claimed.
