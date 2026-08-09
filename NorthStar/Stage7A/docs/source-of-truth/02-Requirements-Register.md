# 02 — Requirements Register (Reconstructed 1.6.0 Overlay)

> `ISS-088`: predecessor register not attached. Existing requirements remain retained by reference; S07A uses the high range below pending collision verification.

## Functional requirements added

| ID | Requirement | Status | Trace |
|---|---|---|---|
| `FR-201` | Classify branch independence before concurrent admission | Implemented | ADR-057; TEST-393–400 |
| `FR-202` | Bound global and per-case concurrent execution | Implemented | DATA-106; TEST-378,403–405 |
| `FR-203` | Aggregate by declared ordinal | Implemented | DATA-110; TEST-379 |
| `FR-204` | Bound queue capacity and admission wait | Implemented | ADR-058; INT-079 |
| `FR-205` | Attach canonical digest and idempotency key | Implemented | DATA-107; TEST-361–374 |
| `FR-206` | Retry only typed transient eligible work | Implemented | ADR-059; TEST-380–382 |
| `FR-207` | Propagate cooperative cancellation | Implemented | DATA-111; TEST-387–388 |
| `FR-208` | Propagate branch deadlines | Implemented | DATA-107; TEST-383 |
| `FR-209` | Checkpoint and resume incomplete branches | Implemented | DATA-112; TEST-375–377,390 |
| `FR-210` | Support explicit aggregation policies | Implemented | DATA-110; TEST-385–387 |
| `FR-211` | Retain sequential feature-switch fallback | Implemented | TEST-389 |
| `FR-212` | Emit branch and queue telemetry | Implemented | DATA-108,113; INT-086 |
| `FR-213` | Preserve broker-neutral transport seam | Designed/reference implemented | ADR-056,061 |
| `FR-214` | Deny concurrent authority and protected-state claims | Implemented | TEST-393–400; EVAL-085,088 |

## Non-functional requirements added

| ID | Requirement | Status |
|---|---|---|
| `NFR-201` | Exactly one active AGT-001 | Satisfied |
| `NFR-202` | Preserve CMP-003/CMP-006/CMP-007 ownership | Satisfied |
| `NFR-203` | No unbounded tasks or queues | Satisfied |
| `NFR-204` | Deterministic aggregation for identical records | Satisfied |
| `NFR-205` | No exactly-once claim | Satisfied |
| `NFR-206` | Python >=3.11,<3.15; standard-library runtime | Satisfied |
| `NFR-207` | Measurable and disable-able concurrency | Satisfied |
| `NFR-208` | Metadata-minimized telemetry | Designed; production redaction pending |
| `NFR-209` | Per-case fairness cap | Satisfied |
| `NFR-210` | Bounded backoff and jitter | Satisfied |
| `NFR-211` | Atomic local checkpoint writes | Satisfied |
| `NFR-212` | Transport substitution preserves canonical semantics | Designed |
