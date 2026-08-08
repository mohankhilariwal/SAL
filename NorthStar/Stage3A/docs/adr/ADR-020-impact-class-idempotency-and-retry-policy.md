# ADR-020 — Impact Classification, Idempotency and Retry Policy

- **Status:** Accepted
- **Date:** 2026-07-31

## Context
Read operations and writes have different failure and replay consequences. A generic retry policy can duplicate business actions.

## Decision
Classify tools as read-only, reversible write, irreversible write or privileged/regulated. Stage 3A registers only the first two. Reversible writes require an idempotency key, support dry-run and are never automatically retried. Read-only tools may use bounded retry for explicitly named transient errors.

## Alternatives
One retry policy for all tools; no retries; compensation-based retries; unrestricted high-impact tools.

## Rationale
The design demonstrates blast-radius control before an agent loop exists and prevents a transient error from silently multiplying writes.

## Consequences
Some ambiguous write failures require manual reconciliation. In-memory idempotency is only a local proof.

## Risks and mitigations
Duplicate writes are mitigated by principal/tool/version/key binding and argument-hash conflict detection. Production requires durable, transactional idempotency records.

## Review triggers
Durable workflow execution, distributed writes, compensation, financial/irreversible actions or multi-region operation.
