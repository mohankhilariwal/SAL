# ADR-036 — Formal Machine-Readable Specification for AGT-001

- **Status:** Accepted
- **Date:** 2026-08-01

## Context

`AGT-001` is executable, but its purpose, authority, completion rules, context limits, human-control rules, tests and lifecycle are distributed across instructions, graph code, gateway contracts, requirements and tests. The harness makes composition repeatable but does not establish one authoritative definition of the agent.

## Decision

Create `DATA-071 AgentSpecification` as the single machine-readable design-time definition of `AGT-001`. It records purpose, users, goals, non-goals, inputs, outputs, preconditions, postconditions, invariants, allowed/prohibited actions, tools, context/data policy, authority, autonomy, human control, termination, errors, provisional SLOs, evaluation obligations and retirement criteria.

The specification is declarative evidence and a source for assertions and gates. It does **not** grant runtime authority. Existing owners remain authoritative: `CMP-005` for tools, `CMP-006` for human decisions, `CMP-003/GRAPH-001` for routes and termination, and `CMP-007` for authorization policy.

## Alternatives

1. Continue scattered documentation.
2. Treat the system prompt as the specification.
3. Use only a human-readable agent card.
4. Use a framework-native agent configuration as canonical.
5. Use a custom policy language for every concern.

## Rationale

A formal application-owned specification improves traceability, reviewability, drift detection and portability without moving authority into prompts or framework metadata.

## Consequences

- Every start is bound to an accepted specification version and digest.
- Specification changes become controlled architecture changes.
- Duplicate expression of constraints can drift and therefore requires semantic validation.
- The local specification remains a reconstruction overlay until the complete prior repository is available.

## Risks and mitigations

- **Risk:** specification mistaken for authorization. **Mitigation:** explicit non-authority invariant and independent runtime PEPs.
- **Risk:** incomplete specification. **Mitigation:** strict required fields, semantic checks, negative tests and deny-by-default deployment gate.
- **Risk:** governance bottleneck. **Mitigation:** ownership, semantic versioning and bounded change categories.

## Review triggers

A new agent, changed authority, tool, graph, state, context/memory policy, approval semantics, risk tier, production SLO, model-routing policy or retirement process.
