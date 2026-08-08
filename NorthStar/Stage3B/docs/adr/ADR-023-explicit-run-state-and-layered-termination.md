# ADR-023 — Explicit Run State and Layered Safe Termination

**Status:** Accepted  
**Date:** 2026-07-31

## Context

A language model can emit “complete” even when required evidence, mapping or review artifacts are absent. Maximum turns can stop a runaway loop, but reaching a limit is not task success.

## Decision

Make `DATA-009 AgentRunState` executable. Derive progress only from validated gateway results. Separate:

- semantic proposal: `complete` or `escalate` from `INT-022`;
- business completion: required milestone and artifact invariants in `INT-024`;
- safety/resource termination: iteration, repetition and no-progress guards;
- execution failure: tool denial/error leading to escalation.

## Alternatives

Stop on a magic word, trust final model output, stop only after a fixed tool sequence, or use framework-native termination without application invariants.

## Rationale

Production meaning belongs to the application. Layered termination makes success, escalation and guard exhaustion distinguishable and preserves partial evidence.

## Consequences

Completion logic is domain-specific and versioned. Every new required artifact or status change must update state projection, tests, diagrams and this ADR's review analysis.

## Risks

Milestone projection defects, corrupted state, stale completion rules and false escalation.

## Mitigations

Typed objects, monotonic milestones, status/linkage checks, unit/integration tests and fixed unapproved disposition.

## Review triggers

New tools, changed completion semantics, durable checkpoints, approval resume, schema migration or compensation requirements.
