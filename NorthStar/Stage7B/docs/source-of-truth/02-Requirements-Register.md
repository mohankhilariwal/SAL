# 02 — Requirements Register — Stage 7B overlay

The full 1.6.0 requirement register was not supplied in this turn. To avoid identifier collision, Stage 7B uses stage-scoped requirement identifiers pending merge under `ISS-096`.

| ID | Requirement | Trace |
|---|---|---|
| `S07B-REQ-001` | Represent versioned joint ISL/OSL distributions rather than only fixed lengths. | `DATA-114`, `DATA-115`, `ADR-062`, `TEST-408`–`427` |
| `S07B-REQ-002` | Represent constant, Poisson, burst, batch and closed-loop arrival patterns. | `DATA-116`, `INT-088`, `TEST-411`, `412`, `424` |
| `S07B-REQ-003` | Model model-call, tool-call, retrieval-call and turn counts. | `DATA-115`, `WP-001`–`007`, `EVAL-097` |
| `S07B-REQ-004` | Capture queue, TTFT, ITL/TPOT, end-to-end latency, request throughput and token throughput. | `DATA-119`, `INT-090`, `EVAL-091`–`096` |
| `S07B-REQ-005` | Define profile-specific SLO hypotheses and label them non-contractual. | `DATA-121`, `ADR-064` |
| `S07B-REQ-006` | Support simulated, synthetic endpoint, trace replay and production evidence classes. | `ADR-063`, `DATA-118`, `DATA-120` |
| `S07B-REQ-007` | Record tokenizer identity, profile version and digest. | `DATA-114`, `TEST-414`, `439` |
| `S07B-REQ-008` | Keep workload measurements free of raw prompt/response payloads by default. | `DATA-114`, `EVAL-098`, `TEST-438` |
| `S07B-REQ-009` | Generate reproducible samples using recorded seeds. | `DATA-118`, `TEST-420`, `447` |
| `S07B-REQ-010` | Produce an advisory capacity envelope with explicit evidence type. | `DATA-120`, `INT-091`, `ADR-065` |
| `S07B-REQ-011` | Prevent capacity analysis from changing `DATA-106` automatically. | `INT-093`, `ADR-065`, `TEST-442` |
| `S07B-REQ-012` | Preserve sequential fallback and all S07A concurrency invariants. | `GRAPH-001/1.3.0`, audit |
| `S07B-REQ-013` | Include tool, retrieval and network delay in workflow modelling. | `DATA-117`, `TEST-432`–`434` |
| `S07B-REQ-014` | Provide local execution without GPU or paid endpoint. | `ADR-066`, scripts, `TEST-447`–`449` |
| `S07B-REQ-015` | Prevent inactive multi-agent workloads from executing. | `WP-008`, `TEST-417`, `440` |
