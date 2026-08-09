# 00 — Project Constitution (Reconstructed 1.6.0 Overlay)

## Status

- Project: NorthStar Agentic AI Architecture Playbook
- Architecture version: `1.6.0`
- Repository version: `1.6.0`
- Stage: `S07A`
- Reconstruction issue: `ISS-088`

## Retained constitution

NorthStar Financial Services, the eight accepted personas, `US-001`–`012`, `CMP-001`–`011`, stable identifiers, evidence-first narrative, vendor-neutral selection, deterministic enforcement outside models, human accountability, gateway-only tools, typed state, cumulative Mermaid architecture and one evolving repository remain authoritative.

## Stage 7A constitutional amendments

1. Concurrency is disabled by default unless branch independence is proven.
2. Exactly one active `AGT-001` remains; workflow branches are not agents.
3. `CMP-003` remains the sole task, route, state, cancellation, aggregation and system-termination owner.
4. `CMP-007` remains the sole authority issuer; queues, workers, adapters and capability advertisements grant no authority.
5. Concurrent work is limited to read-only or pure-compute operations over immutable inputs.
6. There are no concurrent protected-state writes, approvals, finalization, route changes, agent creation or shared-memory writes.
7. Every admitted work item requires a deadline, canonical input digest and idempotency key.
8. Backpressure is explicit and bounded; unbounded queues and task creation are prohibited.
9. Completion order never determines business ordering.
10. At-least-once-ready design does not imply exactly-once side effects.
11. Production distributed claims require evidence from an actual durable transport, identity system, database and operational test.
12. Hidden chain-of-thought is not stored; auditable records contain inputs, actions, policy outcomes, typed errors and concise evidence.

## Definition of done for S07A

The stage is complete only if the architecture, code, schemas, ADRs, tests, evaluations, source artefacts and handoff agree; exactly one active `AGT-001` is preserved; 47 tests and ten evaluations pass; the reference is runnable; and production limitations are explicit.
