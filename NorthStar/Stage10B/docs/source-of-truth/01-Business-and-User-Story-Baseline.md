# 01 — Business and User Story Baseline: Stage 10B Overlay

Version: `1.16.0`

NorthStar, the eight accepted personas and `US-001`–`012` remain unchanged.

## Narrative extension

After Stage 10A, Liam O’Connor can trace a regulatory assessment and verify its audit chain, but a test incident reveals that observability does not itself contain failure. A model timeout causes retries, the retrieval index becomes unavailable, a tool call times out after submission, and a reviewer does not respond before the deadline. Without deterministic recovery rules, the same evidence trail can faithfully record an unsafe cascade.

## Stage 10B business objective

Allow Maya Chen and operators to obtain bounded partial service, safe resumption, explicit escalation and incident evidence when dependencies fail, while preserving human accountability and preventing recovery logic from bypassing authority, audit or business-state controls.

## Success conditions

- A transient read failure may recover within a bounded retry and time budget.
- Ambiguous protected outcomes are reconciled, not blindly repeated.
- Authorization, policy, audit and integrity failures fail closed.
- Workflow checkpoints can resume execution without replaying into `DATA-106`.
- Permanent or poison messages are quarantined with controlled redrive.
- Release artefacts are version-bound and non-production promotion is gated.
- Production promotion is explicitly denied on the current baseline.
