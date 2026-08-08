# 00 — Project Constitution

**Architecture/repository version:** `1.0.0`  
**Stage:** `S04C — Agent Harness Engineering`  
**Status:** Accepted within the local/offline verification boundary.

## 1. Purpose and continuity

NorthStar Financial Services continues the single narrative and repository established in S00. The purpose remains an AI-assisted regulatory impact assessment that accelerates Maya Chen's work while retaining named human accountability. S04C does not restart the story or broaden business scope. It consolidates the already accepted model/agent, graph, gateway, durable state, approval, budget, recovery, evaluation and tracing responsibilities into a repeatable harness.

## 2. Preserved constitutional facts

- Organization: NorthStar Financial Services.
- Personas: Maya Chen, Daniel Brooks, Priya Raman, Elena Petrov, Marcus Green, Sofia Alvarez, Liam O'Connor and Aisha Rahman.
- User stories: `US-001`–`US-012` unchanged.
- Components: `CMP-001`–`CMP-011` unchanged.
- Only agent: `AGT-001 Regulatory Impact Assessment Agent`.
- Tools: `TOOL-001`–`006`, all through `CMP-005`/`INT-017`.
- State: `DATA-009` remains schema `1.1.0`.
- Graph: `GRAPH-001` remains version `1.1.0`.
- Decisions: `ADR-001`–`032` remain accepted; `ADR-033`–`035` extend rather than supersede them.
- Approved/rejected outcomes remain preliminary human-reviewed dispositions, not legal conclusions or case closure.

## 3. Stage 4C invariants

1. The harness is surrounding software, not a second agent and not a new authority boundary.
2. Prompts/instructions may guide behavior but may not authorize tools, validate arguments, choose graph routes, set budgets, approve, persist state or override deterministic policy.
3. Context authorization occurs before a loader exposes text.
4. The harness may compose existing contracts but may not bypass `CMP-005`, `CMP-006`, state checksums, revision/lease controls or graph route ownership.
5. A run is bound to a versioned/hashed manifest, instruction bundle and context envelope.
6. Registries are immutable after startup; no model output may register a tool, hook, validator or agent.
7. Workspace and trace output exclude raw approval tokens, credentials, authorization headers and hidden chain-of-thought.
8. Evaluation hooks are observers and cannot mutate execution or grant authority.
9. Memory, concurrent graph branches and multiple agents remain disabled and unimplemented.
10. Local traces, checkpoints and workspaces are not memory, event sourcing, audit/WORM, records management or exactly-once proof.

## 4. Technology and verification boundary

- Python target `>=3.11,<3.15`; executed on Python `3.13.5`.
- Runtime dependencies: Python standard library only.
- Development test dependency: `pytest==9.0.2`.
- Local SQLite, local JSON/JSONL workspace, synthetic identities and deterministic fixtures.
- No managed SDK/framework dependency is required to execute this stage.

## 5. Definition of done for S04C

S04C is done only when the harness manifest and instruction are integrity-checked; authorized context is assembled deterministically; a session/workspace is created safely; unchanged `GRAPH-001` starts, suspends and resumes; approved/rejected/expired routes remain correct; `TOOL-006` is not duplicated; lifecycle validators/hooks/traces run; future-stage flags fail closed; all source-of-truth artefacts are synchronized; tests/evaluations/demo/validation/audit pass; and the handoff stops before specification, memory, concurrency or multi-agent design.

## 6. Recorded reconstruction exception

`ISS-043` records that the supplied S04B handoff was the authoritative reconstruction input. This package is compatible with that accepted baseline but is not represented as a byte-exact modification of the prior archive.
