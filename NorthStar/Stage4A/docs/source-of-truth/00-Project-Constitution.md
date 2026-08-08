# 00 — Project Constitution

**Version:** `0.8.0`  
**Stage:** `S04A`  
**Repository:** `northstar-agentic-compliance`

## Preserved constitution

NorthStar Financial Services, the eight accepted personas, `US-001`–`US-012`, stable identifiers, human accountability, evidence-first outputs, critical controls outside model reasoning, vendor-neutral contracts, local-first labs and one cumulative repository remain unchanged.

## S04A constitutional invariants

1. `AGT-001` remains the only agent and proposes actions; it does not own graph routing, budgets, recovery, authorization, completion or final disposition.
2. `TOOL-001`–`TOOL-006` execute only through `INT-017` and `CMP-005`.
3. `DATA-009 AgentRunState` remains schema `1.1.0`; `DATA-054` wraps it without redefining it.
4. `DATA-045`–`DATA-052` and `INT-026`–`INT-030` retain S03C semantics.
5. Every graph state mutation is a node-owned, runtime-validated patch; protected authority and disposition paths are immutable.
6. Ambiguous writes are reconciled by the same idempotency key or escalated; no blind retry is permitted.
7. Completed, partial, guard, cancel and escalation outcomes remain `preliminary_grounded_unapproved` and require human review.
8. Stage 4A is a local typed graph, not event sourcing, distributed durable execution, a harness, memory or multi-agent orchestration.

## S04A definition of done

The stage is complete only when the graph definition, typed state, node/edge runtime, checkpoint binding, failure routes, tests, cumulative Mermaid, three ADRs, all ten artefacts, handoff and consistency audit agree and execute locally.
