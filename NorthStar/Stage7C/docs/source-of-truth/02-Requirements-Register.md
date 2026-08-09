# 02 — Requirements Register: Stage 7C Overlay

Full inherited requirements remain accepted. Collision-safe stage identifiers are used because the complete merged historical register is unavailable (`ISS-096`).

| ID | Requirement | Owner/components | Evidence |
|---|---|---|---|
| `S07C-REQ-001` | Register versioned managed, self-hosted and local-simulated inference profiles. | `CMP-010`, `CMP-011`, `DATA-122`, `INT-094` | `TEST-450`–`456` |
| `S07C-REQ-002` | Compare deployment paths without selecting unmeasured hardware/model claims. | `CMP-008`, `CMP-010` | `ADR-067`, stage decision matrix |
| `S07C-REQ-003` | Produce workload-specific optimization assessments for `WP-001`–`007`. | `CMP-008`, `DATA-123`, `INT-095` | `TEST-464`–`472` |
| `S07C-REQ-004` | Reject `WP-008 inactive_future`. | `CMP-008`, `CMP-011` | `TEST-458`, `473`, `500` |
| `S07C-REQ-005` | Reduce context only with required-state, evidence and citation parity. | `CMP-003`, `CMP-004`, `CMP-008` | policy gates, `EVAL-102`–`105` |
| `S07C-REQ-006` | Cap outputs with fail-closed schema completeness. | `CMP-003`, `CMP-008` | `DATA-123`, quality gate |
| `S07C-REQ-007` | Stream only as presentation; partial output has no final authority. | `CMP-001`, `CMP-003` | `ADR-068`, security tests |
| `S07C-REQ-008` | Bind any exact prompt/prefix cache to tenant, authorization, model, tokenizer, prompt/graph version and TTL. | `CMP-007`, `CMP-010`, `DATA-124`, `INT-096` | `TEST-452`–`454`, `497`–`499` |
| `S07C-REQ-009` | Prohibit semantic caching of regulatory conclusions. | `CMP-008`, `CMP-010` | `TEST-455`, `468`, `499` |
| `S07C-REQ-010` | Keep batching/KV scheduling in `CMP-010`; preserve `CMP-003` admission ownership. | `CMP-003`, `CMP-010`, `DATA-125`, `INT-097` | `ADR-069`, `TEST-469`, `501` |
| `S07C-REQ-011` | Benchmark cold, warm and representative cache states. | `CMP-008`, `CMP-009`, `DATA-127`, `DATA-128` | scenario validation, demo |
| `S07C-REQ-012` | Treat quantization and parallelism as concrete candidate benchmarks, not universal defaults. | `CMP-008`, `CMP-010` | planner assessments, `ADR-069` |
| `S07C-REQ-013` | Keep speculation disabled unless profile allowlist and parity/acceptance/latency/memory gates pass. | `CMP-008`, `DATA-126`, `INT-098`, `INT-100` | `TEST-459`–`463`, `474`–`485`, `EVAL-106`–`110` |
| `S07C-REQ-014` | Record baseline and candidate TTFT, ITL, E2E, throughput, cache hit, KV memory and speculative acceptance. | `CMP-009`, `DATA-128`, `INT-099` | `TEST-486`–`493`, `EVAL-111`–`114` |
| `S07C-REQ-015` | Couple performance evidence with structured validity, groundedness and task success. | `CMP-008`, `DATA-129`, `INT-100` | `TEST-502`–`504`, `EVAL-102`–`105` |
| `S07C-REQ-016` | Export reproducible, payload-free endpoint capability plans. | `CMP-008`, `CMP-009`, `INT-101` | `TEST-495`, `496` |
| `S07C-REQ-017` | Keep optimization recommendations advisory with no admission or authority mutation. | `CMP-003`, `CMP-007`, `DATA-130`, `INT-102` | `TEST-471`, `472`, `501` |
| `S07C-REQ-018` | Provide a standard-library local reference and toy lossless speculative-sampling lab. | `CMP-010` | `TEST-474`–`485`, `505`–`507` |

## Traceability summary

- Requirements are implemented by `src/northstar_compliance/inference/*`.
- Security controls are asserted in dataclass validation and security tests.
- Performance/quality gates are `EVAL-101`–`115`.
- Architecture decisions are `ADR-067`–`071`.
- No requirement declares a live production endpoint or production speedup complete.
