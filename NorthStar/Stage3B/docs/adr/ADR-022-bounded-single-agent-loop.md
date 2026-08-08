# ADR-022 — One Application-Owned Bounded Single-Agent Loop

**Status:** Accepted  
**Date:** 2026-07-31

## Context

S03A exposes six controlled capabilities but invokes them through a hard-coded caller. The next capability must select one allowed next action from current progress without moving authorization or policy into model reasoning.

## Decision

Create `AGT-001 Regulatory Impact Assessment Agent` within `CMP-003`. Implement a plain-Python observation-action loop with a provider-neutral `INT-022` decision contract. The provider returns one structured `call_tool`, `complete` or `escalate` proposal. All actions still traverse `CMP-005`.

## Alternatives

1. Retain a fixed deterministic sequence.
2. Use an open-ended ReAct-style prompt loop.
3. Use planner/executor model roles.
4. Introduce LangGraph or a durable workflow engine now.
5. Decompose into multiple agents.

## Rationale

The fixed sequence cannot branch from observations. Open-ended loops expose runaway and authority risks. Planner/executor and multi-agent designs add roles and calls without a demonstrated need. A graph is valuable once branching, waiting and recovery justify it; S03B needs only one bounded decision cycle.

## Consequences

- NorthStar now has one genuine but low-authority agent.
- Decision-provider quality is independently testable.
- Loop control is explicit and framework-neutral.
- Durable execution and complex branching remain absent.

## Risks

Prompt/tool hijacking, wrong tool choice, repetition, early completion and provider drift.

## Mitigations

Strict decision schema, tool allowlist, trusted context injection, gateway-only actions, explicit state, deterministic termination and negative tests.

## Review triggers

Complex branching, asynchronous human waiting, process restart, parallelism, multiple independently accountable roles or production model adoption.
