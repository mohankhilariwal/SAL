# ADR-030 — Place human approval after the complete unapproved evidence package

**Status:** Accepted  
**Date:** 2026-07-31

## Context

Stage 4A can queue review but cannot wait for a decision across process lifetimes.

## Decision

`GRAPH-001` enters approval only after deterministic completion checks and before any human-accepted continuation.

## Alternatives

Process-blocking wait, polling, framework-only interrupts, managed cloud state machines and a durable workflow engine were considered.

## Rationale

The decision preserves application-owned authority, graph routes, typed state, gateway idempotency and local/offline execution while making the production migration boundary explicit.

## Consequences

NorthStar gains durable waiting, expiry and safe resumption. It also owns a local persistence adapter and must not describe it as event sourcing, distributed replay, disaster recovery or a managed workflow service.

## Risks and mitigations

Token theft, duplicate decisions, stale workers and timeout ambiguity are mitigated by signatures, expiry, role/SoD checks, uniqueness constraints, revisions and leases. Enterprise identity, key management and multi-region durability remain open.

## Review triggers

Production deployment, multiple workers, multi-region recovery, graph migration, enterprise IAM integration or a need for long-running workflow operational tooling.
