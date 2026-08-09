# Stage Handoff Pack

## A. Stage completed

- **Stage identifier:** `S07C`
- **Stage title:** Inference Optimization and Speculative Decoding
- **Architecture version:** `1.8.0`
- **Repository version:** `1.8.0`
- **Handoff version:** `1.8.0`
- **Graph version:** `GRAPH-001/1.4.0`
- **Completion date:** 2026-08-01
- **Status:** Completed as a compatible reconstruction overlay with local simulated planning and algorithmic evidence only.
- **Consistency audit:** Passed with inherited reconstruction exception `ISS-096` and recorded production-evidence gaps `ISS-105`–`113`.

## B. Capabilities now available

1. All S07B workload, capacity, bounded-concurrency, authority, state, human and memory constraints remain.
2. `INF-001` describes a provider-neutral managed inference default class.
3. `INF-002` describes a version-pinned self-hosted candidate benchmark lane; it is not production-selected.
4. `INF-003` implements a local standard-library planning/simulation path.
5. `DATA-122`–`130` define deployment profiles, optimization/cache/batching/speculation policy, scenarios, observations, parity records and advisory recommendations.
6. `INT-094`–`102` define profile registry, planning, cache binding, batching policy, benchmark, normalization, parity, evidence export and advisory recommendation.
7. The planner evaluates context reduction, output controls, streaming, caching, batching, chunked prefill, quantization, parallelism, speculation and deferred routing against `WP-001`–`007`.
8. Exact cache reuse requires tenant, authorization scope, model, tokenizer, prompt/graph version and TTL/invalidation bindings.
9. Semantic caching of regulatory conclusions is prohibited.
10. Speculative decoding is disabled by default and can only be a profile-specific benchmark candidate.
11. A tiny Markov-model lab implements distribution-preserving rejection correction and empirical parity checks.
12. A transparent analytical proxy emits baseline/candidate TTFT, ITL, E2E, throughput, cache, KV memory and acceptance sensitivity.
13. Quality and performance are joined through `EVAL-101`–`115`.
14. `DATA-130` recommendations cannot grant authority or mutate `DATA-106`.
15. `WP-008` remains `inactive_future` and cannot run.

**Not implemented:** production traces; live managed/self-hosted endpoint; selected model/tokenizer/provider/runtime/hardware; production prompt/KV cache; cache invalidation service; live batching; quantization; parallelism; prefill/decode disaggregation; production speculative decoding; autoscaling; automatic routing; production cost rates; production quality-performance join; human clock policy; production telemetry/WORM.

## C. Accepted architecture decisions

`ADR-001`–`066` remain accepted.

- `ADR-067`: managed inference default class with a governed self-hosted benchmark lane.
- `ADR-068`: optimize context/output/streaming and exact prefix reuse before infrastructure complexity; prohibit semantic regulatory-answer caching.
- `ADR-069`: keep batching and KV scheduling in `CMP-010`; benchmark quantization/parallelism only with concrete model/runtime/hardware.
- `ADR-070`: keep speculative decoding disabled by default and promote only per profile after parity, acceptance, decode, E2E and memory gates.
- `ADR-071`: use a standard-library planner, proxy and toy lossless speculation lab until endpoint evidence exists.

## D. Current component inventory

| ID | Name | Current S07C responsibility/status |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Supports labelled streaming; partial output has no final authority. |
| `CMP-002` | Regulatory Intake Boundary | Supplies document metadata/provenance; no raw benchmark payload export. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Sole task/route/state/admission/cancellation/aggregation/system-termination owner; receives only governed advisory configuration. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Supports evidence-preserving context reduction and invalidation metadata. |
| `CMP-005` | Enterprise Integration Boundary | Sole gateway for `TOOL-001`–`006`; benchmarks cannot bypass it. |
| `CMP-006` | Human Review and Approval Boundary | Human authority remains external; inference success never approves. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Sole grant issuer; supplies cache authorization-scope binding. |
| `CMP-008` | Evaluation and Assurance Boundary | Owns optimization planning, scenario design, parity gates and recommendations. |
| `CMP-009` | Observability and Audit Boundary | Normalizes `DATA-128` and performance/cache/speculation provenance. |
| `CMP-010` | Runtime and Deployment Boundary | Hosts inference profiles, local simulator and future runtime cache/batching/speculation enforcement. |
| `CMP-011` | Source-of-Truth Governance Pack | Governs `1.8.0`, ADRs, profiles and exceptions. |

## E. Current agent inventory

| ID | Name | Authority | Status |
|---|---|---|---|
| `AGT-001` | Regulatory Impact Assessment Agent | Existing proposal/complete/escalate boundary. Cannot route/mutate protected state, approve/finalize, grant consent, write unrestricted/shared memory, create agents or bypass owners. | **Only active agent**; spec `1.1.0` unchanged. |

No concurrent agents exist. `WP-008` is a disabled workload-profile placeholder, not an agent.

## F. Current data and state objects

- `DATA-001`–`121` retained; `DATA-009` remains `1.1.0`.
- `DATA-122 InferenceDeploymentProfile`.
- `DATA-123 InferenceOptimizationPolicy`.
- `DATA-124 CachePolicy`.
- `DATA-125 BatchingPolicy`.
- `DATA-126 SpeculativeDecodingPlan`.
- `DATA-127 InferenceBenchmarkScenario`.
- `DATA-128 InferenceBenchmarkObservation`.
- `DATA-129 QualityParityRecord`.
- `DATA-130 OptimizationRecommendation`.
- `DATA-081 case_working` is not transferred.
- No new protected-state, approval, route or shared-memory writer exists.

## G. Current interfaces and tools

- `INT-001`–`093` retained.
- `INT-094` Inference Deployment Profile Registry.
- `INT-095` Workload-to-Optimization Planning.
- `INT-096` Cache Eligibility and Key Binding.
- `INT-097` Batching and Scheduling Policy.
- `INT-098` Speculative/Inference Benchmark Execution.
- `INT-099` Inference Observation Normalization.
- `INT-100` Quality-Parity Gate.
- `INT-101` Optimization Evidence Export.
- `INT-102` Advisory Optimization Recommendation.
- `TOOL-001`–`006` remain unchanged and gateway-only.

## H. Repository state

```text
northstar-agentic-compliance-stage7c/
├── config/{inference,workloads}/
├── docs/{adr,architecture/diagrams,references,source-of-truth,stages}/
├── reports/
├── schemas/DATA-122...DATA-130.schema.json
├── scripts/{run_stage7c_demo,run_stage7c_inference_plan,run_stage7c_speculative_benchmark,run_stage7c_evaluation,validate_stage7c,consistency_audit_stage7c}.py
├── src/northstar_compliance/inference/{adapters,evaluation,io,models,planner,simulation,speculative}.py
├── tests/{unit,integration,security,evaluation,performance}/
├── README.md
└── pyproject.toml
```

Python `>=3.11,<3.15`; executed on Python `3.13.5`; runtime standard library; pytest `9.0.2`.

## I. Tests completed

- `TEST-450`–`463`: models, policies, cache bindings and speculative-plan guards — passed.
- `TEST-464`–`473`: profile-specific planner and `WP-008` block — passed.
- `TEST-474`–`485`: lossless speculative-sampling mechanics and empirical parity — passed.
- `TEST-486`–`493`: inference proxy sensitivity and metric integrity — passed.
- `TEST-494`–`496`: end-to-end planning/evidence integration — passed.
- `TEST-497`–`501`: security/authority/admission boundaries — passed.
- `TEST-502`–`504`: evaluation positive and negative gates — passed.
- `TEST-505`–`507`: determinism and bounded performance properties — passed.

Executed result: **58 pytest cases passed**.

`EVAL-101`–`115` all passed for the declared local synthetic `WP-002` candidate at assumed acceptance `0.85`. The negative tests prove low acceptance and quality regression fail the gate.

Toy speculative lab at 20,000 trials: parity passed; total-variation distance `0.00625`. This is algorithmic simulated evidence, not transformer/GPU performance.

## J. Known limitations

1. Compatible reconstruction overlay; `ISS-096` remains.
2. Bootstrap workload signals, not measured traces.
3. No selected model/provider/runtime/hardware.
4. No live endpoint or production cache/batching/speculation.
5. Local rates and speedups are assumptions.
6. Toy Markov model only.
7. No kernel/GPU/scheduler/collective/OOM fidelity.
8. No production parity backend or cost rates.
9. No automatic routing/autoscaling/admission change.
10. Mermaid not CLI-rendered.

## K. Open risks, assumptions and issues

- New risks: `RSK-224`–`247`.
- New assumptions: `ASM-073`–`080`.
- New issues: `ISS-105`–`113`.
- Inherited `ISS-096` and all inherited production gaps remain.

## L. Compatibility constraints

1. Preserve NorthStar, eight personas, `US-001`–`012`, `CMP-001`–`011` and exactly one active `AGT-001`.
2. Preserve `AGT-001-spec 1.1.0`, `DATA-009 1.1.0` and `GRAPH-001/1.4.0`.
3. Preserve `DATA-091`–`130`, `INT-063`–`102`, `TOOL-001`–`006` and canonical contracts above execution transports.
4. `CMP-003` remains sole task/route/state/admission/cancellation/aggregation/system-termination owner.
5. `CMP-007` remains the only authority issuer.
6. Human decisions remain external; inference/cache/speculation/benchmark outcomes never approve.
7. Preserve memory boundaries and no automatic transfer/shared-agent memory.
8. Preserve bounded concurrency, immutable independent branch work, idempotency, deadlines, deterministic fan-in and sequential fallback.
9. No concurrent protected-state writes, approvals, finalization, route mutation, agent creation or shared-memory writes.
10. `WP-008` remains `inactive_future`.
11. `DATA-120`, `INT-093`, `DATA-130` and `INT-102` remain advisory and cannot mutate `DATA-106` automatically.
12. Semantic response caching for regulatory conclusions remains prohibited.
13. Any enabled prefix/prompt cache must preserve all tenant/authorization/model/tokenizer/prompt-version/evidence-version bindings.
14. Speculative decoding remains disabled unless the exact profile, model/runtime and gates are approved.
15. Do not present local simulated metrics as production speedup/capacity/cost.
16. Model routing remains deferred until an explicit next-stage ADR.
17. Resolve/merge `ISS-096` before claiming a complete historical register.

## M. Required input for the next stage

Use all ten `1.8.0` overlays after merge; `ADR-001`–`071`; `AGT-001-spec 1.1.0`; `GRAPH-001/1.4.0`; `DATA-007`, `009`, `041`–`130`; `INT-009`–`102`; `TOOL-001`–`006`; S07A concurrency policies; S07B workload profiles/evidence; S07C inference profiles, optimization policies, quality gates, risks/issues and primary-source notes. Replace placeholder model/provider/tokenizer/hardware identities and bootstrap traces with measured evidence when available.

## N. Next architectural problem

NorthStar has a governed inference architecture but no selected model portfolio or routing policy. It must compare managed and open-weight LLMs, SLMs, reasoning models, embeddings, rerankers and classifiers; evaluate quality, tool/structured-output reliability, context, latency, throughput, cost, privacy, residency, license and hardware; decide whether SLM-first escalation or a single target is justified; define fallback and judge separation; and preserve authority and risk controls across routes.

## O. Exact continuation instruction

> Continue the NorthStar Agentic AI Architecture Playbook by executing only **Stage 7D — Model Selection and Routing**. Reconstruct the `1.8.0` S07C baseline; preserve exactly one active `AGT-001`, `GRAPH-001/1.4.0`, `DATA-091`–`130`, `INT-063`–`102`, managed-default/self-hosted-benchmark inference architecture, exact cache boundaries, disabled-by-default speculative decoding, bounded concurrency, authority/state/human/memory owners, sequential fallback and advisory-only capacity/optimization evidence; compare model categories and routing options against `WP-001`–`007`; implement only the selected local-compatible routing design, update all artefacts, run the consistency audit and stop after the stage.

Audit assertions: exactly one active `AGT-001`; no concurrent protected-state writes; `WP-008` remains `inactive_future`; no automatic `DATA-106` mutation; semantic regulatory-answer caching remains prohibited; model routes cannot grant authority or bypass residency/risk policy.
