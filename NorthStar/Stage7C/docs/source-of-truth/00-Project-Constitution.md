# 00 — Project Constitution: Stage 7C Overlay

- **Architecture/repository version:** `1.8.0`
- **Graph version:** `GRAPH-001/1.4.0`
- **Baseline:** compatible continuation of S07B `1.7.0`
- **Reconstruction status:** `ISS-096` remains open because the complete merged historical registers were not supplied in this turn.

## Preserved constitutional invariants

1. NorthStar Financial Services, the eight accepted personas and `US-001`–`012` remain unchanged.
2. `CMP-001`–`011` remain the accepted top-level component inventory.
3. `AGT-001 Regulatory Impact Assessment Agent` is the only active agent; specification `1.1.0` is unchanged.
4. `CMP-003` remains sole owner of task, route, protected state, admission, cancellation, aggregation and system termination.
5. `CMP-007` remains the sole authorization-grant issuer.
6. `CMP-005` remains the only gateway for `TOOL-001`–`006`.
7. Human approval remains external, typed and non-transferable to inference components.
8. Bounded concurrency, immutable independent branch work, deterministic fan-in, deadlines, cancellation and sequential fallback remain.
9. `WP-008` remains `inactive_future` and cannot be executed or used to claim multi-agent capacity.
10. `DATA-120`, `INT-093` and new `DATA-130`, `INT-102` are advisory and cannot mutate `DATA-106` automatically.

## Stage 7C inference invariants

1. A deployment capability declaration is not evidence of benefit.
2. Managed inference is the default deployment class; self-hosted serving remains a governed candidate lane until evidence supports promotion.
3. Context reduction cannot remove required state, approved instructions, access-control context or cited evidence needed for correctness.
4. Output limits fail closed when a required schema or finding is incomplete.
5. Cache reuse is exact and fully bound to tenant, authorization scope, model, tokenizer, prompt/graph version and invalidation epoch.
6. Semantic caching of regulatory conclusions or approval-sensitive outputs is prohibited.
7. Batching and KV-cache scheduling belong to `CMP-010`; workflow admission remains with `CMP-003`.
8. Quantization and parallelism require concrete model/runtime/hardware benchmarks and quality evidence.
9. Speculative decoding is disabled by default, profile allowlisted and gated by parity, acceptance, decode, end-to-end and memory evidence.
10. A lossless claim refers to the output distribution of the declared target algorithm; it does not imply identical sampled text across independent random seeds.
11. Inference benchmarks capture metadata and metrics, not raw prompts, responses, retrieved evidence or tool arguments.
12. Stage 7C simulated results are not production capacity, production cost or production speedup evidence.
