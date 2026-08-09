# 08 — Risk, Assumption and Issue Register: Stage 7C Overlay

Inherited active items remain. New entries continue after the S07B ranges.

## Risks

| ID | Risk | Control/status |
|---|---|---|
| `RSK-224` | Managed provider retention/residency or cache behaviour differs from declaration. | Contract, configuration and runtime verification; open. |
| `RSK-225` | Self-hosted model/runtime supply-chain compromise. | Signed artefacts, SBOM, scanning and pinning; production control deferred. |
| `RSK-226` | Context reduction removes decisive evidence. | Required-state and citation parity gate. |
| `RSK-227` | Output cap silently truncates obligations. | Schema completeness and explicit incomplete outcome. |
| `RSK-228` | Cross-tenant/cache-scope leakage. | Full exact binding and fail-closed miss. |
| `RSK-229` | Stale prefix cache after policy/evidence change. | Version/invalidation epoch and TTL. |
| `RSK-230` | Continuous batching worsens interactive TTFT/fairness. | Mixed-profile p95 and starvation tests. |
| `RSK-231` | Long prefill causes head-of-line blocking. | Chunked-prefill candidate benchmark; no default claim. |
| `RSK-232` | KV-cache OOM causes rejection or crash. | Token/concurrency bounds and OOM tests. |
| `RSK-233` | Quantization changes structured output or groundedness. | `DATA-129` parity gate. |
| `RSK-234` | Parallelism communication overhead exceeds benefit. | Hardware-topology benchmark. |
| `RSK-235` | Speculative acceptance is low or unstable. | Acceptance distribution and profile rollback gate. |
| `RSK-236` | Target verification dominates speculative execution. | Decode and E2E gate. |
| `RSK-237` | Draft model consumes capacity needed by target. | Memory/utilization measurement and high-concurrency negative test. |
| `RSK-238` | Speculative KV pages increase memory pressure. | Maximum overhead gate. |
| `RSK-239` | Approximate method is mislabeled lossless. | Algorithm/version claim plus empirical and deterministic parity tests. |
| `RSK-240` | Faster microbenchmark has no workflow benefit due to tool/retrieval latency. | E2E and successful-task cost gate. |
| `RSK-241` | Streaming partial text is mistaken for accepted result. | Partial label and final validation/authority boundary. |
| `RSK-242` | Benchmark cache hit rate is unrepresentative. | Cold/warm/representative scenarios. |
| `RSK-243` | Provider/runtime upgrade invalidates evidence. | Digests and review triggers. |
| `RSK-244` | Optimization recommendation changes admission indirectly. | Typed advisory object and tests. |
| `RSK-245` | Raw content leaks through benchmark telemetry. | Payload prohibition and schema validation. |
| `RSK-246` | Simulated speedup is presented as production. | Evidence-kind label and audit check. |
| `RSK-247` | Model routing is introduced prematurely. | Automatic routing flag prohibited; deferred. |

## Assumptions

| ID | Assumption | Status |
|---|---|---|
| `ASM-073` | Managed inference remains operationally simpler for the current NorthStar maturity. | Planning assumption; review on evidence. |
| `ASM-074` | Repeated exact prefixes exist in long-document and multi-turn profiles. | Bootstrap from S07B; requires traces. |
| `ASM-075` | Semantic response reuse is unsafe for regulated conclusions. | Accepted design assumption. |
| `ASM-076` | Prompt-lookup is the lowest-complexity speculative candidate for input-grounded text. | Experimental assumption. |
| `ASM-077` | Stage 7C local service rates are sensitivity parameters, not measurements. | Explicit. |
| `ASM-078` | Existing quality evaluators can be joined by run/trace IDs in a future endpoint test. | Not integrated with production backend. |
| `ASM-079` | No live model/provider/hardware is selected. | True in S07C. |
| `ASM-080` | Human-review latency remains outside the automated inference clock. | Inherited pending policy. |

## Issues

| ID | Issue | Status |
|---|---|---|
| `ISS-096` | Full historical registers/repository were not supplied for byte-exact merge. | Open; inherited. |
| `ISS-105` | No tokenizer-accurate NorthStar trace set. | Open. |
| `ISS-106` | No selected managed provider/model or contractual cache evidence. | Open. |
| `ISS-107` | No selected self-hosted model/runtime/accelerator. | Open. |
| `ISS-108` | No live mixed-profile endpoint benchmark. | Open. |
| `ISS-109` | No production cache invalidation service. | Open. |
| `ISS-110` | No production quality-performance join backend. | Open. |
| `ISS-111` | No current production cost rates. | Open. |
| `ISS-112` | Mermaid diagrams were syntax reviewed but not CLI-rendered. | Open. |
| `ISS-113` | Model-selection/routing decision is intentionally deferred. | Open; next stage problem. |
