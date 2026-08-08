# ADR-028 — Framework-neutral application-owned graph kernel before framework selection

- **Status:** Accepted
- **Date:** 2026-07-31

## Context
Current graph frameworks and durable workflow products offer useful capabilities, but NorthStar must first preserve application-owned budget, recovery, gateway and disposition semantics in a local/offline teaching boundary.

## Decision
Use Python dataclasses, protocols and JSON configuration for Stage 4A. Treat LangGraph, AWS Step Functions and Temporal as future adapters/options rather than the current authority model.

## Alternatives
LangGraph now; AWS Step Functions now; Temporal now; a generic third-party FSM library.

## Rationale
The selected kernel is inspectable, dependency-light, portable and directly testable. It avoids confusing a framework feature with a NorthStar control.

## Consequences
NorthStar owns more code and does not yet gain distributed timers, workers, leases or replay guarantees.

## Risks and mitigations
Custom-engine defects are mitigated by a deliberately small feature set, strict validation and a future review trigger rather than indefinite custom growth.

## Review triggers
Production durability, operational scaling, multi-process execution, human waits or framework conformance requirements.
