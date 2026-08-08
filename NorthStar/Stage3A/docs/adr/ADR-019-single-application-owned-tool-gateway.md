# ADR-019 — Single Application-Owned Tool Gateway

- **Status:** Accepted
- **Date:** 2026-07-31

## Context
Allowing callers or future models to execute adapters directly would scatter validation, authorization, idempotency, timeout and evidence controls.

## Decision
Route every Stage 3A invocation through one application-owned `ToolGateway` inside `CMP-005`. The gateway resolves exact versions, validates arguments, obtains a deterministic policy decision, enforces impact controls, invokes an adapter, validates output, bounds result size and emits a redacted result envelope/event.

## Alternatives
Direct Python calls; model-to-tool calls; per-adapter control logic; API-management-only enforcement; workflow-engine activities.

## Rationale
A single policy-enforcement seam makes control ordering testable while remaining small enough for the local tutorial.

## Consequences
The gateway is a local bottleneck and not highly available. Production may distribute adapters while preserving the logical enforcement contract.

## Risks and mitigations
Confused-deputy and bypass risk are mitigated by making adapters non-discoverable to model code and testing that denial precedes adapter execution.

## Review triggers
Multiple runtimes, high throughput, remote adapters, tenant isolation or control-plane federation.
