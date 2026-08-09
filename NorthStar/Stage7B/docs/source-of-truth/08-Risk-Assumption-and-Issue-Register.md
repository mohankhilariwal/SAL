# 08 — Risk, Assumption and Issue Register — Version 1.7.0 overlay

## New risks

| ID | Risk | Mitigation / status |
|---|---|---|
| `RSK-204` | Synthetic distributions misrepresent production tails. | Trace replay and drift comparison required. Open. |
| `RSK-205` | Tokenizer drift changes ISL/OSL without business change. | Record tokenizer identity; reprofile on change. Open. |
| `RSK-206` | Independent ISL/OSL assumptions hide correlation. | Joint buckets selected by `ADR-062`. Mitigated. |
| `RSK-207` | Cache-warm benchmarks overstate cold or diverse-prefix performance. | Separate cold/warm runs and cache metadata. Open. |
| `RSK-208` | Tool/retrieval latency dominates while inference-only benchmark appears healthy. | Workflow-level observations required. Mitigated locally. |
| `RSK-209` | Burst arrivals trigger queue collapse and timeouts. | Burst profiles, queue percentiles, load shedding review. Open. |
| `RSK-210` | Capacity recommendation is mistaken for approved production limit. | Evidence labels and `ADR-065`. Mitigated. |
| `RSK-211` | Raw workload payload telemetry exposes regulated data. | Payload capture prohibited in reference. Mitigated. |
| `RSK-212` | Dropped or failed requests improve latency percentiles deceptively. | Report success, rejection and SLO attainment together. Open. |
| `RSK-213` | Long-running human review is mixed into machine-service latency. | Explicit clock policy and separate human elapsed time. Open. |
| `RSK-214` | Simulator false precision drives infrastructure purchase. | Planning-only label; endpoint calibration gate. Open. |
| `RSK-215` | Model-call and turn distributions drift after prompt/graph changes. | Profile digest and change triggers. Open. |
| `RSK-216` | Prefix reuse leaks tenant-sensitive cache state in a future implementation. | Later security design; no live cache in Stage 7B. Open. |
| `RSK-217` | Batch work starves interactive traffic. | Separate profile classes and later fair scheduling policy. Open. |
| `RSK-218` | Multi-agent workload is accidentally treated as active. | `WP-008 inactive_future`; executable validation. Mitigated. |
| `RSK-219` | Percentiles from small samples are unstable. | Minimum sample sizes and confidence analysis in endpoint phase. Open. |
| `RSK-220` | Vendor benchmark thresholds are copied as NorthStar SLOs. | `ADR-064`; thresholds are workload hypotheses only. Mitigated. |
| `RSK-221` | Benchmark endpoint differs from production network and policy path. | End-to-end path replay before approval. Open. |
| `RSK-222` | Cost model omits retries, evaluation or human review. | Report cost components separately. Open. |
| `RSK-223` | Telemetry cardinality or storage cost grows excessively. | Bounded labels, aggregation and sampling policy later. Open. |

## New assumptions

- `ASM-065`: Token counts are tokenizer-specific and the placeholder tokenizer must be replaced before endpoint benchmarking.
- `ASM-066`: Local service-demand rates are illustrative calibration values, not hardware measurements.
- `ASM-067`: Stage 7B benchmark work uses non-production or sanitized data.
- `ASM-068`: Tool and retrieval latency can initially be represented by distributions independent of content quality.
- `ASM-069`: Human review time is measured separately from automated service time unless a scenario explicitly includes it.
- `ASM-070`: Seven active profiles are sufficient for the first segmentation pass.
- `ASM-071`: `CMP-008` can own workload definitions without becoming a runtime bottleneck.
- `ASM-072`: A production model/server/hardware selection will occur in a later stage.

## New issues

- `ISS-096`: Only the Stage 7A handoff, not all nine other 1.6.0 source artefacts, was supplied in this turn. Stage 7B therefore produces a compatible overlay requiring merge before claiming a complete historical register.
- `ISS-097`: No measured NorthStar tokenizer trace is available.
- `ISS-098`: No production endpoint, server, model or accelerator has been selected.
- `ISS-099`: No representative arrival trace or concurrency trace is available.
- `ISS-100`: Human clock-pause policy is not yet approved.
- `ISS-101`: Cost rates for model, infrastructure, tools and human review are not supplied.
- `ISS-102`: Prefix-cache and prompt-cache behaviour is not measured.
- `ISS-103`: Production telemetry semantic-convention version is not selected.
- `ISS-104`: `DATA-106` production limits remain uncalibrated; no automatic change is authorized.
