# ADR-021 — Defer MCP and Model-Selected Agent Execution

- **Status:** Accepted
- **Date:** 2026-07-31

## Context
MCP standardizes remote context/tool integration, while a true agent would choose actions from a goal and observed state. Neither is needed to prove the controlled capability boundary itself.

## Decision
Use an in-process registry and deterministic demonstration caller in S03A. Do not allocate an `AGT-*` identifier, expose the gateway directly to a model, or operate an MCP server. Preserve descriptor and adapter seams so S03B or a later interoperability stage can add those capabilities through a new ADR.

## Alternatives
Implement MCP immediately; add a model-selected loop in the same substage; use OpenAPI network services now.

## Rationale
Separating capability control from action selection makes failures attributable and prevents protocol, networking and autonomy risks from obscuring the gateway design.

## Consequences
S03A cannot decide the next action, replan or terminate a goal-directed run. Its external services are synthetic/local.

## Risks and mitigations
Future adapter drift is mitigated by protocol-neutral schemas and conformance tests.

## Review triggers
S03B bounded-agent loop, remote tool servers, cross-language clients, dynamic discovery or enterprise API deployment.
