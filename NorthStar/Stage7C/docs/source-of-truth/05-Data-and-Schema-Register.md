# 05 — Data and Schema Register: Stage 7C Overlay

`DATA-001`–`121` remain accepted. `DATA-009` remains `1.1.0`; `DATA-081 case_working` is not transferred.

| ID | Object | Owner | Purpose |
|---|---|---|---|
| `DATA-122` | `InferenceDeploymentProfile` | `CMP-010`/`CMP-011` | Versioned managed/self-hosted/local capability and provenance. |
| `DATA-123` | `InferenceOptimizationPolicy` | `CMP-008`/`CMP-011` | Profile-specific context, output, streaming, cache, batching, quantization, parallelism and speculation policy. |
| `DATA-124` | `CachePolicy` | `CMP-007`/`CMP-010` | Exact cache eligibility, scope bindings, TTL and prohibition flags. |
| `DATA-125` | `BatchingPolicy` | `CMP-010` | Runtime batching mode, token/concurrency/wait bounds, chunked-prefill and priority policy. |
| `DATA-126` | `SpeculativeDecodingPlan` | `CMP-008`/`CMP-010` | Method, allowlist, lookahead and promotion gates. |
| `DATA-127` | `InferenceBenchmarkScenario` | `CMP-008` | Workload/deployment/policy/evidence/cache/quality binding. |
| `DATA-128` | `InferenceBenchmarkObservation` | `CMP-009` | Baseline/candidate latency, throughput, acceptance, cache and memory evidence. |
| `DATA-129` | `QualityParityRecord` | `CMP-008` | Structured validity, groundedness, task success and distribution claim evidence. |
| `DATA-130` | `OptimizationRecommendation` | `CMP-008` | Advisory technique assessment and selected policy reference. |

Schemas are under `schemas/DATA-122.schema.json` through `DATA-130.schema.json`.

## Interfaces

| ID | Contract | Authorization/ownership |
|---|---|---|
| `INT-094` | Inference Deployment Profile Registry | Governance write; runtime/evaluation read. |
| `INT-095` | Workload-to-Optimization Planning | `CMP-008`; analytical only. |
| `INT-096` | Cache Eligibility and Key Binding | `CMP-007` policy plus `CMP-010` enforcement. |
| `INT-097` | Batching and Scheduling Policy | `CMP-010`; cannot change workflow admission. |
| `INT-098` | Speculative/Inference Benchmark Execution | Sanitized non-side-effect endpoint or local simulator. |
| `INT-099` | Inference Observation Normalization | `CMP-009`; metrics and identifiers only. |
| `INT-100` | Quality-Parity Gate | `CMP-008`; joins existing task evaluation. |
| `INT-101` | Optimization Evidence Export | Governance evidence package. |
| `INT-102` | Advisory Optimization Recommendation | No authority or automatic `DATA-106` mutation. |

`INT-001`–`093` and `TOOL-001`–`006` remain unchanged.
