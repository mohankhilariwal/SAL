# ADR-027 — Explicit typed execution graph replaces imperative control flow

- **Status:** Accepted
- **Date:** 2026-07-31

## Context
The S03C loop has deterministic prerequisites, model choices, gateway calls, recovery and termination branches mixed in one imperative function.

## Decision
Represent orchestration as `GRAPH-001` with typed deterministic, model, policy, tool, recovery and termination nodes and named conditional/error/terminal edges. Preserve exactly one agent and all existing authority boundaries.

## Alternatives
Keep the imperative loop; use only a finite-state enum; adopt a framework graph immediately; use a managed workflow service immediately.

## Rationale
The graph exposes ownership and paths without granting new authority or prematurely claiming distributed durability.

## Consequences
Graph definitions, transition records and path tests become first-class. The runtime adds local complexity and versioning obligations.

## Risks and mitigations
Graph sprawl and hidden cycles are mitigated by validation, bounded transitions, reachable-node checks and explicit route tables.

## Review triggers
Parallel branches, real waiting states, distributed workers, graph migration or a need for managed operations.
