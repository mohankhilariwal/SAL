# 03 — Architecture Baseline: Stage 7C Overlay

- **Architecture version:** `1.8.0`
- **Graph:** `GRAPH-001/1.4.0`
- **Prior graph:** `GRAPH-001/1.3.0`

## Architecture change

S07B described demand but did not decide how inference is served. S07C adds governed deployment profiles, optimization policies, cache/batching/speculation contracts, benchmark observations, quality-parity records and advisory recommendations inside existing boundaries.

## Selected architecture

1. `INF-001` — provider-neutral managed inference default class.
2. `INF-002` — version-pinned self-hosted candidate benchmark lane.
3. `INF-003` — local simulated reference for deterministic planning and tests.
4. `CMP-010` owns serving-runtime batching, KV cache and candidate execution.
5. `CMP-008` owns optimization planning, benchmark design and quality gates.
6. `CMP-009` normalizes payload-free inference observations.
7. `CMP-011` governs versions, evidence and changes.
8. `CMP-003` and `CMP-007` retain their existing ownership; no inference object grants authority or changes admission.

## Cumulative diagram

The authoritative Mermaid source is `docs/architecture/diagrams/GRAPH-001-v1.4.0.mmd`.

## Trust boundaries

- Managed provider boundary: data residency, retention, prompt-cache behaviour and telemetry must be contractually and technically verified.
- Self-hosted boundary: NorthStar owns model supply chain, runtime patching, accelerator isolation, scheduler, KV memory, availability and incident response.
- Cache boundary: exact prefix reuse only; all security and version bindings are mandatory.
- Benchmark boundary: no production side-effect tools, no raw content and no authority.

## Deferred architecture

A concrete model, tokenizer, provider, serving engine, GPU, autoscaling design, disaggregated prefill/decode topology and automatic model-routing policy remain deferred.
