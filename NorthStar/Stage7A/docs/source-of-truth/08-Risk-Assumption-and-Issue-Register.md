# 08 — Risk, Assumption and Issue Register (Reconstructed 1.6.0 Overlay)

All inherited active S06C production gaps remain.

## Risks added

| ID | Risk | Mitigation/status |
|---|---|---|
| `RSK-180` | Unbounded concurrency exhausts runtime or dependencies. | Finite queue and worker limits; mitigated in reference. |
| `RSK-181` | One case monopolizes workers. | Per-case semaphore; residual scheduling risk. |
| `RSK-182` | Duplicate work causes repeated side effects. | Idempotency; writes prohibited concurrently. |
| `RSK-183` | Same idempotency key is reused for different input. | Digest conflict fails closed. |
| `RSK-184` | Retry storm amplifies an outage. | Typed retry, cap, deadline, jitter; caller retry still pending. |
| `RSK-185` | Completion order changes business output. | Ordinal-based deterministic fan-in. |
| `RSK-186` | Cancellation arrives after external work completes. | Cooperative cancellation; no automatic commit. |
| `RSK-187` | Worker crash leaves ambiguous in-flight work. | Checkpoint and idempotency; production lease pending. |
| `RSK-188` | Local checkpoint is tampered with. | File boundary only; production integrity store pending. |
| `RSK-189` | Queue payload leaks regulated data. | Minimum payload and redaction; encryption pending. |
| `RSK-190` | Worker or message impersonation. | Production workload identity/signing pending. |
| `RSK-191` | Stale authorization persists during long work. | Short deadline; production revalidation/revocation pending. |
| `RSK-192` | Partial result is mistaken for complete assessment. | Explicit `partial` and failed/cancelled sets. |
| `RSK-193` | First-satisfactory predicate is model-biased. | Require deterministic approved predicate. |
| `RSK-194` | Queue metrics expose sensitive values. | Metadata-only design; production redaction tests pending. |
| `RSK-195` | Local idempotency is lost on process restart. | Known limitation; durable store required for production. |
| `RSK-196` | Cross-host clock skew breaks deadlines. | Absolute deadline design; production trusted clock/lease policy pending. |
| `RSK-197` | Priority scheduling starves normal cases. | No priority scheduler in reference; future fairness design. |
| `RSK-198` | Concurrent result conflict creates hidden lost update. | No concurrent protected writes. |
| `RSK-199` | Broker semantics are assumed without verification. | Broker-neutral contract and explicit no-production claim. |
| `RSK-200` | Overlap increases token/tool cost. | Limits, cancellation, retry cap; workload benchmark pending. |
| `RSK-201` | Async cancellation is treated as hard termination. | Documentation and typed terminal records. |
| `RSK-202` | Candidate endpoint is accidentally activated as a worker agent. | One-agent invariant tests. |
| `RSK-203` | Reconstructed requirement IDs collide with unattached register. | `ISS-088`; merge validation required. |

## Assumptions added

| ID | Assumption | Status |
|---|---|---|
| `ASM-058` | Selected concurrent branches are I/O-bound. | Valid for reference fixtures only. |
| `ASM-059` | Branch inputs are immutable after fan-out. | Enforced by design. |
| `ASM-060` | Branch handlers cooperate with cancellation. | True for reference handlers; external calls may not. |
| `ASM-061` | Local atomic file replace is available. | Tested in current environment. |
| `ASM-062` | Python event-loop scheduling is sufficient for local POC. | Accepted for S07A. |
| `ASM-063` | Production transport can preserve DATA-107/108 semantics. | To be validated. |
| `ASM-064` | Capacity limits will be derived in the next workload stage. | Open. |

## Issues added

| ID | Issue | Status |
|---|---|---|
| `ISS-088` | Nine full S06C source registers were not attached. | Open merge task; reconstructed overlays produced. |
| `ISS-089` | Handoff called scope S06D while user explicitly requested S07A. | Resolved in favor of explicit S07A instruction. |
| `ISS-090` | No production broker or durable workflow engine selected. | Intentionally deferred pending workload/SLO evidence. |
| `ISS-091` | No durable distributed idempotency store. | Open production gap. |
| `ISS-092` | No worker lease/heartbeat/dead-letter semantics. | Open production gap. |
| `ISS-093` | No live identity, encryption or signed work-item implementation. | Open production gap. |
| `ISS-094` | No production load, fairness or cost benchmark. | Next-stage input. |
| `ISS-095` | Mermaid diagrams not CLI-rendered. | Syntax reviewed as text; visual renderer not part of reference. |
