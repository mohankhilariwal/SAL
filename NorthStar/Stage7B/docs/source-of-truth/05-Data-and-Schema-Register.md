# 05 — Data and Schema Register — Version 1.7.0 overlay

`DATA-001`–`113` remain preserved.

| ID | Name | Owner | Purpose |
|---|---|---|---|
| `DATA-114` | `WorkloadProfile` | `CMP-008` / governed by `CMP-011` | Versioned workload identity, tokenizer, status, distributions, arrival pattern and SLO hypothesis. |
| `DATA-115` | `SequenceLengthDistribution` | `CMP-008` | Weighted joint ISL/OSL bucket plus call and turn counts. |
| `DATA-116` | `ArrivalPattern` | `CMP-008` | Open-loop, closed-loop, burst or batch scheduling assumptions. |
| `DATA-117` | `ServiceDemandModel` | `CMP-008` | Calibratable prefill, decode, tool, retrieval, network and contention assumptions. |
| `DATA-118` | `BenchmarkScenario` | `CMP-008` | Profile digest, service model, seed, request count and evidence kind. |
| `DATA-119` | `BenchmarkObservation` | `CMP-009` | Per-request queue, TTFT, ITL, E2E, tokens, call counts and success metadata. |
| `DATA-120` | `CapacityEnvelope` | `CMP-008` | Profile-specific tested rate/concurrency and percentile envelope with evidence label. |
| `DATA-121` | `SLOHypothesis` | `CMP-008` / business review | Non-contractual profile-specific latency, queue and success hypotheses. |

## Privacy rule

`DATA-114.capture_payloads` is fixed to false in the local reference. Raw prompt, response, document and tool argument contents are outside Stage 7B measurement records.
