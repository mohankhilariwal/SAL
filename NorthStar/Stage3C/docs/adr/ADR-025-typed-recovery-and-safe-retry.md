# ADR-025 — Typed recovery, bounded retry and safe fallback

- **Status:** Accepted
- **Date:** 2026-07-31

## Context
S03B escalated every tool failure. Retrying all failures would be unsafe, particularly when a reversible write times out after dispatch and its commit status is unknown.

## Decision
Classify failures into transient, rate-limited, timeout, authorization, validation, permanent, dependency, ambiguous-write and cancelled categories. Permit bounded retry/fallback only when both the failure class and tool impact allow it. Read-only calls may use one registered fallback adapter. Reversible writes may retry only after a definite pre-dispatch non-commit. An ambiguous write must be reconciled by the same idempotency key; if status remains unknown, escalate without retry. Model fallback is provider-neutral and budgeted. Dead ends permit bounded replanning with blocked action signatures.

## Alternatives
1. No recovery.
2. Retry every error.
3. Framework default retry policies.
4. Typed application policy.

## Rationale
Recovery must be based on failure semantics and side effects, not an LLM instruction or generic exception count.

## Consequences
Adapters must return precise error metadata. False classification can create duplicate writes or unnecessary escalation. Tool fallback is restricted to semantically equivalent registered read adapters.

## Risks and mitigations
Fallback can hide systemic failure or change semantics. Record every fallback, cap attempts, and test result equivalence. Compensation is plan-only unless an authoritative inverse operation and approval policy exist.

## Review triggers
Live connectors, irreversible tools, financial actions, distributed transactions, circuit breakers or compensation execution.
