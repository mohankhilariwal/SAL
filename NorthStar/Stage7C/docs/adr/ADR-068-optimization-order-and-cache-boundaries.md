# ADR-068 — Optimize Context and Output Before Infrastructure Complexity

- **Status:** Accepted
- **Date:** 2026-08-01

## Context
NorthStar profiles include repeated long prefixes, growing sessions, long outputs and tool-dominated trajectories. Not every bottleneck requires additional inference infrastructure.

## Decision
Apply optimization in this order: remove duplicated non-authoritative context; cap outputs with fail-closed completeness checks; stream interactive output; enable exact prefix/prompt caching only with tenant, authorization, model, tokenizer and prompt-version bindings; then benchmark runtime techniques. Prohibit semantic caching of regulatory conclusions and approval-sensitive responses.

## Alternatives
Infrastructure-first scaling; unrestricted response caching; prompt-only optimization; or staged optimization.

## Rationale
The staged approach reduces avoidable work while preserving evidence and authority boundaries. It also makes later benchmarks easier to interpret.

## Consequences
Context reduction requires citation-coverage and required-state tests. Output caps cannot silently truncate. Cache invalidation becomes a governed interface.

## Risks and mitigations
Evidence loss is mitigated with required-state and citation parity gates. Cross-tenant reuse is prevented by complete cache-key binding and fail-closed misses.

## Review triggers
Material prompt assembly changes, profile drift, cache capability changes or quality regressions.
