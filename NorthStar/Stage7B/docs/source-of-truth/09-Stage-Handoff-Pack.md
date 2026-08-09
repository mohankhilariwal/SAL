# Stage Handoff Pack

## A. Stage completed

- **Stage identifier:** `S07B`
- **Stage title:** ISL, OSL and Workload Modelling
- **Architecture version:** `1.7.0`
- **Repository version:** `1.7.0`
- **Handoff version:** `1.7.0`
- **Graph version:** `GRAPH-001/1.3.0`
- **Completion date:** 2026-08-01
- **Status:** Completed as a compatible reconstruction overlay with local planning evidence only.
- **Consistency audit:** Passed with recorded reconstruction exception `ISS-096`.

## B. Capabilities now available

1. All accepted S07A bounded-concurrency, idempotency, cancellation, checkpoint, authority, state, human and memory constraints remain.
2. Seven executable workload profiles (`WP-001`–`007`) cover short queries, long documents, policy comparison, multi-document assessment, tool-heavy `AGT-001` work, batch processing and interactive sessions.
3. `WP-008` is `inactive_future` and cannot execute; there is exactly one active `AGT-001`.
4. `DATA-114`–`121` define versioned profiles, joint ISL/OSL buckets, arrival patterns, service-demand assumptions, benchmark scenarios, observations, capacity envelopes and SLO hypotheses.
5. Deterministic weighted sampling supports constant, Poisson, burst, closed-loop and batch load shapes.
6. A local discrete-event proxy measures queue, TTFT, ITL/TPOT, end-to-end latency and token/request throughput without GPU or paid infrastructure.
7. Benchmark adapters generate payload-free traces and command plans for external endpoint tools.
8. Capacity sweeps produce an advisory `DATA-120` envelope; they do not alter `DATA-106`.
9. Profile digests, tokenizer identity, evidence kind and seed provide benchmark provenance.
10. Raw prompt/response capture is disabled in the local reference.

**Not implemented:** production trace collection; live endpoint benchmarking; tokenizer-accurate NorthStar measurements; model/server/hardware selection; dynamic/continuous batching; live KV or prefix caching; quantization; parallelism; speculative decoding; autoscaling; broker selection; automatic admission changes; production cost rates; human clock policy; production telemetry backend.

## C. Accepted architecture decisions

`ADR-001`–`061` remain accepted.

- `ADR-062`: model workloads with versioned joint ISL/OSL mixtures and call/turn distributions.
- `ADR-063`: use an evidence ladder of simulated, synthetic endpoint, trace replay and production results.
- `ADR-064`: define workload-specific SLO hypotheses, not one universal limit.
- `ADR-065`: capacity envelopes are advisory; `CMP-003` and `DATA-106` retain admission ownership.
- `ADR-066`: use a standard-library planning simulator plus external adapters until a production inference stack exists.

## D. Current component inventory

| ID | Name | Current S07B responsibility/status |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Emits profile labels and interaction timings without raw content capture. |
| `CMP-002` | Regulatory Intake Boundary | Supplies document-size/arrival metadata; provenance boundary unchanged. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Sole task/route/state/cancellation/aggregation/system-termination and admission owner; receives only advisory capacity recommendations. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Exposes authorized retrieval timing/count metadata. |
| `CMP-005` | Enterprise Integration Boundary | Sole gateway for `TOOL-001`–`006`; exposes tool timing/status; no benchmark bypass. |
| `CMP-006` | Human Review and Approval Boundary | Human elapsed time remains separately governed; authority unchanged. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Sole grant issuer; benchmark artefacts grant no authority. |
| `CMP-008` | Evaluation and Assurance Boundary | Owns profiles, benchmark design, SLO-hypothesis evaluation and capacity analysis. |
| `CMP-009` | Observability and Audit Boundary | Normalizes `DATA-119` and benchmark provenance; not production WORM. |
| `CMP-010` | Runtime and Deployment Boundary | Runs bounded local simulator and optional endpoint adapters. |
| `CMP-011` | Source-of-Truth Governance Pack | Governs `1.7.0` overlays, profile versions and reconstruction issue. |

## E. Current agent inventory

| ID | Name | Authority | Status |
|---|---|---|---|
| `AGT-001` | Regulatory Impact Assessment Agent | Existing exact proposal/complete/escalate boundary. Cannot route/mutate protected state, approve/finalize, grant consent, write unrestricted/shared memory, create agents or bypass owners. | **Only active agent**; spec `1.1.0` unchanged. |

No concurrent agents exist. `WP-008` is a disabled workload-profile placeholder, not an agent.

## F. Current data and state objects

- `DATA-001`–`113` retained; `DATA-009` remains `1.1.0`.
- `DATA-114 WorkloadProfile`.
- `DATA-115 SequenceLengthDistribution`.
- `DATA-116 ArrivalPattern`.
- `DATA-117 ServiceDemandModel`.
- `DATA-118 BenchmarkScenario`.
- `DATA-119 BenchmarkObservation`.
- `DATA-120 CapacityEnvelope`.
- `DATA-121 SLOHypothesis`.
- `DATA-081 case_working` is not transferred.
- No new shared mutable state or worker-owned state writer exists.

## G. Current interfaces and tools

- `INT-001`–`086` retained.
- `INT-087` Workload Profile Registry.
- `INT-088` Workload Sample and Trace Generation.
- `INT-089` Benchmark Execution.
- `INT-090` Measurement Ingestion and Normalization.
- `INT-091` Capacity Analysis.
- `INT-092` Benchmark Evidence Export.
- `INT-093` Advisory Admission Recommendation.
- `TOOL-001`–`006` remain unchanged and gateway-only.

## H. Repository state

```text
northstar-agentic-compliance-stage7b/
├── config/workloads/{WP-001...WP-008,service-model-local}.json
├── docs/{adr,architecture/diagrams,references,source-of-truth,stages}/
├── reports/
├── schemas/DATA-114...DATA-121.schema.json
├── scripts/{run_stage7b_demo,run_stage7b_benchmark,run_stage7b_capacity_plan,run_stage7b_evaluation,validate_stage7b,consistency_audit_stage7b}.py
├── src/northstar_compliance/workload/{adapters,evaluation,io,metrics,models,sampling,simulation}.py
├── tests/{unit,integration,security,evaluation,performance}/
├── README.md
└── pyproject.toml
```

Primary entry points are the six scripts above. Python target `>=3.11,<3.15`; executed `3.13.5`; runtime standard library; pytest `9.0.2`.

## I. Tests completed

- `TEST-408`–`419`: models, validation, digest, SLO and inactive-profile guards — passed.
- `TEST-420`–`427`: deterministic sampling, arrivals, bounds and context growth — passed.
- `TEST-428`–`437`: simulation, queueing, percentiles, sensitivity, capacity and Little’s Law — passed.
- `TEST-438`–`442`: payload minimization, tokenizer provenance, authority separation and no admission mutation — passed.
- `TEST-443`–`446`: evaluation registry and integrity — passed.
- `TEST-447`–`449`: determinism, throughput and contention properties — passed.

Executed result: **42 pytest cases passed**.

Evaluations `EVAL-089`–`100`:

- At the derived local simulated envelope of `0.2 requests/s`, all 12 passed.
- At the bootstrap overload probe of `0.8 requests/s`, `EVAL-093` queue, `EVAL-094` end-to-end and `EVAL-095` TTFT failed as expected; the result is retained as saturation evidence, not hidden.
- Local simulated `DATA-120` envelope: `0.2 requests/s`, eight tested workflow slots, evidence kind `simulated`. It is not a production limit.

Structural validation and 42-test suite passed. Consistency audit passed with `ISS-096`.

## J. Known limitations

Compatible reconstruction overlay; bootstrap synthetic profiles; placeholder tokenizer; simple p50 external latency assumptions; conservative per-call token multiplication; no endpoint/hardware/kernel/batching/KV-cache fidelity; no confidence intervals; no production trace; no production model/server/accelerator; no live cache; no pricing; no human clock policy; no autoscaling; no broker selection; no automatic `DATA-106` change; no production telemetry/WORM; Mermaid not CLI-rendered.

## K. Open risks, assumptions and issues

- New risks: `RSK-204`–`223`.
- New assumptions: `ASM-065`–`072`.
- New issues: `ISS-096`–`104`.
- All inherited active production gaps remain.

## L. Compatibility constraints

1. Preserve NorthStar, eight personas, `US-001`–`012`, `CMP-001`–`011` and exactly one active `AGT-001`.
2. Preserve `AGT-001-spec 1.1.0`; use `GRAPH-001/1.3.0`; preserve `DATA-009 1.1.0`.
3. Preserve application-owned routes/state/termination and gateway-only `TOOL-001`–`006`.
4. Preserve external human authority; timeout, benchmark result and capacity recommendation never approve.
5. Preserve memory boundaries and no automatic transfer/shared-agent memory.
6. Preserve canonical `DATA-091`–`113` and `INT-063`–`086` above execution transports.
7. `CMP-007` remains the only authority issuer; workload profiles, traces and benchmark runners cannot grant authority.
8. `CMP-003` remains sole task, route, admission, cancellation, aggregation and system-termination owner.
9. Concurrent branches remain workflow work items, not agents.
10. Concurrency still requires immutable independent read-only or pure-compute work.
11. Preserve no concurrent protected-state writes, approvals, finalization, route mutation, agent creation or shared-memory writes.
12. Preserve finite admission, deadlines, idempotency and deterministic fan-in.
13. Treat all S07B ranges and SLOs as profile-specific bootstrap assumptions until replaced by measured evidence.
14. Record tokenizer, profile version/digest, evidence kind, model/server/hardware and load shape for every benchmark claim.
15. Do not present fixed-length smoke tests or simulated results as production capacity.
16. `DATA-120` and `INT-093` remain advisory and cannot mutate `DATA-106` automatically.
17. `WP-008` remains `inactive_future` until a later explicit architecture decision activates additional agents.
18. Merge `1.7.0` overlays with the complete historical registers and resolve `ISS-096` before claiming a complete historical register.

## M. Required input for the next stage

Use all ten `1.7.0` artefacts after merge; `ADR-001`–`066`; `AGT-001-spec 1.1.0`; `GRAPH-001/1.3.0`; `DATA-007`, `009`, `041`–`121`; `INT-009`–`093`; `TOOL-001`–`006`; S07A concurrency policies and S07B workload profiles, benchmark traces, overload evidence, capacity envelope, active risks/issues and primary-source reference notes. Replace bootstrap profiles with tokenizer-accurate measured traces when available.

## N. Next architectural problem

NorthStar now understands the shape of its demand but has not designed the inference architecture that must serve it. It must compare managed and self-hosted paths; model prefill/decode and KV-cache pressure; evaluate batching, caching, context reduction, quantization, parallelism, streaming and routing; and benchmark speculative decoding only against the relevant NorthStar workload profiles without assuming it always helps.

## O. Exact continuation instruction

> Continue the NorthStar Agentic AI Architecture Playbook by executing only **Stage 7C — Inference architecture, batching, caching and speculative decoding**. Reconstruct the `1.7.0` S07B baseline; preserve exactly one active `AGT-001`, `GRAPH-001/1.3.0`, `DATA-091`–`121`, `INT-063`–`093`, bounded concurrency, authority/state/human/memory owners, sequential fallback and advisory-only capacity evidence; compare inference deployment and optimization options against `WP-001`–`007`; implement only the selected local-compatible design, update all artefacts, run the consistency audit and stop after the stage.

Audit assertions: exactly one active `AGT-001`; no concurrent protected-state writes; `WP-008` remains `inactive_future`; capacity recommendations remain advisory and concurrency bounds remain configured rather than universal SLOs.
