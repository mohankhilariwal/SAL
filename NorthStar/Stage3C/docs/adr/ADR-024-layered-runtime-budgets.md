# ADR-024 — Application-owned layered runtime budgets

- **Status:** Accepted
- **Date:** 2026-07-31

## Context
S03B bounded iterations but could still consume excessive wall time, model tokens, monetary cost, tool calls or failures. One count cannot represent these independent resources.

## Decision
`CMP-003` owns `DATA-045 RuntimeBudget` and `DATA-046 BudgetLedger`. It enforces iteration, wall-time, input-token, output-token, total-token, synthetic cost, tool-call, model-call, failure, retry and replan limits independently. Actual provider usage is settled after each model response. Time uses a monotonic clock. Exhaustion never maps to success.

## Alternatives
1. Prompt the model to spend less.
2. One combined “step” budget.
3. Provider-specific quota only.
4. Application-owned independent ledgers.

## Rationale
Independent deterministic limits make the failure reason observable, prevent a low-iteration high-token run from escaping control, and keep authority outside model reasoning.

## Consequences
More state and tests are required. A production implementation needs provider usage normalization, reservations for in-flight calls and enterprise cost attribution.

## Risks and mitigations
Incorrect tariffs could misstate cost; the local tariff is explicitly synthetic and denominated in micro-CAD. Missing provider usage must fail closed or use an approved conservative estimate in production.

## Review triggers
Managed-provider pilot, new billing model, streaming, concurrency, batch execution or enterprise FinOps integration.
