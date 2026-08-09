# 01 — Business and User Story Baseline: Stage 7C Overlay

## Context carried forward

Maya can run a bounded, evidence-backed regulatory impact workflow with exactly one active `AGT-001`. Stage 7B established seven workload profiles and local capacity-planning evidence. Elena can now see which profiles are long-context, decode-heavy, tool-heavy, batch or interactive, but NorthStar still has no inference architecture or controlled optimization policy.

## Stage 7C narrative outcome

Elena initially proposes “turn on speculative decoding and continuous batching.” Priya refuses a global switch because `WP-001` short queries, `WP-002` long-document analysis, `WP-005` tool-heavy trajectories and `WP-006` batch processing have different bottlenecks. Marcus requires cache isolation. Sofia requires quality and evidence gates. Liam requires failure, memory and mixed-traffic measurements.

NorthStar therefore chooses a managed-default inference architecture with a self-hosted benchmark lane and a workload-specific optimization planner. The system can now recommend context reduction, output control, streaming, prefix caching and candidate serving techniques. It cannot activate those recommendations automatically.

## User-story effect

- `US-001`–`012` are preserved.
- Maya gains no new authority and sees no unapproved partial output as final.
- Elena gains versioned inference plans and benchmark scenarios.
- Marcus gains explicit cache and inference trust boundaries.
- Sofia gains quality-parity and evidence-kind gates.
- Liam gains normalized TTFT, ITL, end-to-end, acceptance, KV-memory and failure evidence requirements.
- Daniel and Aisha retain external accountability and approval ownership.

## Business acceptance criteria for S07C

1. Every active workload receives an auditable, advisory optimization plan.
2. Inactive `WP-008` is blocked.
3. Regulatory conclusions cannot be semantically cached.
4. Speculative decoding cannot be recommended without workload eligibility and all declared gates.
5. No benchmark or optimization can approve, finalize, route, grant authority or change admission.
6. Local code and tests run without a GPU or paid service.
