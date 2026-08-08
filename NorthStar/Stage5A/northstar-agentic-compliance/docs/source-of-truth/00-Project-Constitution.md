# 00 — Project Constitution

**Architecture/repository/handoff version:** `1.1.0`  
**Current completed stage:** `S05A`  
**Baseline:** S04C `1.0.0`, reconstructed from the supplied handoff and chapter.

## Purpose and unchanged principles

NorthStar Financial Services continues to build one evidence-backed regulatory impact assessment solution for Maya Chen while preserving accountable human decision-making. The accepted organization, eight personas, `US-001`–`012`, `CMP-001`–`011`, `AGT-001`, `GRAPH-001`, tools, interfaces, data contracts and security boundaries remain unchanged unless an ADR explicitly supersedes them.

Constitutional principles retained:

1. Introduce the simplest viable capability only when the narrative requires it.
2. AI output is advisory; no model, prompt, instruction, specification or evaluator grants authority.
3. Critical authorization, tool execution, graph routing, approval and final disposition controls remain deterministic and externally owned.
4. Preserve stable identifiers, schemas, repository paths, provenance and change history.
5. Authorization precedes retrieval/context loading.
6. Every tool call passes through `INT-017`/`CMP-005`.
7. Human decisions remain typed, signed, role-checked, separation-of-duties checked, expiring and single-use through `CMP-006`.
8. Timeout never approves; late decisions fail closed.
9. Approved/rejected outputs remain preliminary human-reviewed dispositions, never final legal/compliance closure.
10. Traces, workspaces and checkpoints are not memory, audit/WORM, event sourcing or exactly-once proof.

## S05A constitutional additions

1. `DATA-071 AgentSpecification` is the single machine-readable design-time definition of `AGT-001`.
2. The specification is declarative and non-authoritative; runtime control owners remain unchanged.
3. JSON plus JSON Schema Draft 2020-12 is the canonical local representation; application semantic validation is mandatory.
4. A canonical SHA-256 digest binds the specification to `DATA-063` through `DATA-072 SpecificationBinding`.
5. New starts require an active, valid, compatible specification and passing pre-start assertions.
6. Results require passing post-result assertions before being accepted by the harness caller.
7. Required tests/evaluations and security evidence feed a deny-by-default local deployment gate.
8. `DATA-077` formalizes current context selection, authorization, provenance, ordering and budgets without enabling memory, cross-case reuse or compaction.
9. `DATA-078` defines retirement criteria; retired specifications deny new starts.
10. Specification changes to purpose, goals/non-goals, authority, tools, data/context, approval, termination, SLOs, evaluation or retirement require version advancement, impact analysis, ADR and regression evidence.

## Stage boundary

S05A does not implement memory, context compaction/regeneration, cross-case recall, concurrent branches, a second agent, delegation, MCP/A2A, a control plane, production signing/attestation, audit/WORM, live models/connectors, deployment or disaster recovery.

## Definition of done for S05A

- Machine-readable `AGT-001` specification and schemas exist.
- Structural and semantic validation passes.
- Manifest/specification digest compatibility is enforced.
- Runtime assertions and fail-closed evaluation/deployment gates are executable.
- Current context policy is explicit and no-memory boundaries are negative-tested.
- Retirement denies new starts.
- Code, tests, diagrams, ADRs, traceability and all ten source-of-truth artefacts agree.
- Stage consistency audit is executed with exceptions recorded.
