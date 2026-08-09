# 00 — Project Constitution

**Architecture/repository version:** `1.4.0`  
**Current stage:** `S06B`  
**Source precedence:** this governance pack, accepted ADRs, executable schemas/code/tests, then narrative explanation.

## Stable project facts

- Organization: **NorthStar Financial Services**.
- Personas: Maya Chen, Daniel Brooks, Priya Raman, Elena Petrov, Marcus Green, Sofia Alvarez, Liam O'Connor and Aisha Rahman.
- Main outcome: evidence-backed regulatory impact assessment with human accountability preserved.
- Stable user stories: `US-001`–`012`.
- Stable components: `CMP-001`–`011`.
- Only active agent: `AGT-001 Regulatory Impact Assessment Agent` at specification `1.1.0`.
- Accepted graph/state: `GRAPH-001 1.1.0`, `DATA-009 1.1.0`.
- Accepted tools: `TOOL-001`–`006`, all gateway-only through `CMP-005`.
- Human decisions: external, typed, role/SoD controlled, expiring and single-use; timeout never approves; approved/rejected are preliminary, not final closure.
- Memory: optional `DATA-081 case_working` only, case-local, consented, expiring/deletable and harness-owned.

## S06B constitutional invariants

1. A handoff or role label cannot allocate an agent.
2. Exactly one active `AGT-*` identity remains: `AGT-001`.
3. `CAND-EVIDENCE-VERIFIER-001` is a candidate sandbox endpoint, not an accepted agent.
4. `CMP-003` alone creates/routes/cancels tasks and determines system termination.
5. `CMP-007` alone issues delegated authority.
6. Delegated authority can only narrow tools, operations, resources, data scopes, use count, expiry and delegation depth.
7. The recipient/resource boundary verifies authority before loading data or acting.
8. `DATA-009` remains authoritative and cannot be directly mutated by a recipient.
9. Inter-participant exchange uses immutable hashed artefacts and signed receipts.
10. Shared mutable state, shared-agent memory, peer delegation and concurrent execution remain disabled.
11. MCP, A2A, REST, gRPC, queue and event-bus choices remain unselected.
12. HMAC/SHA-256 fixtures are local teaching controls and are not production OAuth, DPoP, macaroon, KMS, audit or non-repudiation claims.
13. A completed verification artefact cannot approve or finalize a case.
14. A late, expired, cancelled, tampered, duplicate or replayed handoff fails closed.
15. Any future agent activation requires `INT-062`, a new ADR-controlled inventory change, threat/privacy review, production authorization design and representative evaluation.

## Definition of done for S06B

- `DATA-091`–`099` and `INT-063`–`070` defined and implemented where locally testable.
- `ADR-047`–`050` accepted.
- Exactly one active agent preserved in config, code, diagrams and handoff.
- 36 tests and eight evaluations pass.
- Demo, benchmark, validation and consistency audit run.
- All ten source-of-truth artefacts updated.
- No later-stage protocol or concurrency capability falsely claimed.
