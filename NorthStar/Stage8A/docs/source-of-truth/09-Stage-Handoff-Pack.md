# Stage Handoff Pack

## A. Stage completed

- **Stage identifier:** `S08A`
- **Stage title:** Evaluation Architecture and Datasets
- **Architecture version:** `1.9.0`
- **Repository version:** `1.9.0`
- **Handoff version:** `1.9.0`
- **Graph version:** `GRAPH-001/1.5.0`
- **Completion date:** 2026-08-01
- **Status:** Completed as a compatible reconstruction overlay with a local synthetic evaluation architecture only.
- **Consistency audit:** Passed with inherited `ISS-096`, sequence issue `ISS-114` and production-evidence gaps `ISS-115`–`122`.

## B. Capabilities now available

1. All S07C authority, state, memory, cache, concurrency, inference and human-control constraints remain.
2. `DATA-131`–`142` define suites, datasets, cases, ground truth, rubrics, graders, runs, trials, results, lineage, contamination and human review assignments.
3. `INT-103`–`111` define registry, materialization, isolated execution, grading, sampling, aggregation, quarantine and evidence export.
4. `EVAL-SUITE-001/1.0.0` is a deterministic offline contract/regression suite for `AGT-001` and existing graph contracts.
5. `EDS-001`–`008` cover normal, negative, permission, tool-failure, adversarial, temporal, multilingual and conflicting-evidence scenarios.
6. The local dataset has 24 synthetic cases: 10 dev, 8 validation, 6 logically sealed test.
7. Twelve deterministic graders enforce schema, expected outcome, citations, permission, human authority, tool gateway, termination, recovery, injection resistance, temporal validity, non-authority and payload minimization.
8. The harness runs independent isolated trials with bounded concurrency two and two local trials per case.
9. Case/file digests and exact/near cross-split contamination checks are implemented.
10. Sealed test execution is blocked by default.
11. Human-review sampling prioritizes failed/high-risk cases but cannot decide.
12. Evidence exports contain digests and findings, not raw payload or hidden chain-of-thought.
13. `EVAL-116`–`130` pass; 53 pytest cases pass.
14. Evaluation remains advisory and cannot mutate `DATA-106`, authority, route, approval or finalization.
15. Stage 7D model selection/routing remains unresolved; no model or route is selected.

**Not implemented:** production dataset; live LLM/agent run; production trace replay; human annotation/calibration; LLM-as-a-Judge; online/shadow/canary/A-B evaluation; statistical power/uncertainty; CI/CD deployment gates; enterprise registry/WORM; access-controlled test store; production model selection or routing.

## C. Accepted architecture decisions

`ADR-001`–`071` remain accepted.

- `ADR-072`: build evaluation evidence before final model selection/routing.
- `ADR-073`: use layered outcome-first evaluation with trace evidence.
- `ADR-074`: govern immutable versioned datasets, split lineage and contamination checks.
- `ADR-075`: use deterministic and human evaluation first; defer LLM-as-a-Judge.
- `ADR-076`: use a local isolated standard-library harness with advisory outputs.

## D. Current component inventory

| ID | Name | Current S08A responsibility/status |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | No new authority; future evaluation feedback only. |
| `CMP-002` | Regulatory Intake Boundary | Future approved sample provenance; S08A local data synthetic. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Sole task/route/state/admission/cancellation/aggregation/system-termination owner; evaluation cannot mutate it. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Future authorized evidence references and temporal metadata. |
| `CMP-005` | Enterprise Integration Boundary | Sole gateway for `TOOL-001`–`006`; tool traces graded. |
| `CMP-006` | Human Review and Approval Boundary | Owns reviewer assignments and human decisions. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Sole grant issuer; authorizes dataset/split/case access. |
| `CMP-008` | Evaluation and Assurance Boundary | Owns suites, datasets, graders, isolated runs and results. |
| `CMP-009` | Observability and Audit Boundary | Records payload-minimized evaluation evidence. |
| `CMP-010` | Runtime and Deployment Boundary | Future candidate adapter; no live model in S08A. |
| `CMP-011` | Source-of-Truth Governance Pack | Governs `1.9.0`, ADRs, dataset versions and quarantine. |

## E. Current agent inventory

| ID | Name | Authority | Status |
|---|---|---|---|
| `AGT-001` | Regulatory Impact Assessment Agent | Existing bounded proposal/complete/escalate boundary; cannot approve/finalize, route, grant authority, create agents, bypass owners or write unrestricted/shared memory. | **Only active agent**; spec `1.1.0` unchanged. |

No concurrent agents exist. `WP-008` remains `inactive_future`.

## F. Current data and state objects

- `DATA-001`–`130` retained; `DATA-009` remains `1.1.0`.
- `DATA-131 EvaluationSuite`.
- `DATA-132 EvaluationDataset`.
- `DATA-133 EvaluationCase`.
- `DATA-134 GroundTruthReference`.
- `DATA-135 EvaluationRubric`.
- `DATA-136 GraderSpecification`.
- `DATA-137 EvaluationRun`.
- `DATA-138 TrialRecord`.
- `DATA-139 EvaluationResult`.
- `DATA-140 DatasetLineageRecord`.
- `DATA-141 ContaminationAssessment`.
- `DATA-142 HumanReviewAssignment`.
- No new protected-state, approval, route or shared-memory writer exists.

## G. Current interfaces and tools

- `INT-001`–`102` retained.
- `INT-103` Evaluation Suite Registry.
- `INT-104` Dataset Registry and Version Resolution.
- `INT-105` Authorized Case Materialization.
- `INT-106` Isolated Evaluation Execution.
- `INT-107` Deterministic Grader Execution.
- `INT-108` Human Review Sampling.
- `INT-109` Result Aggregation.
- `INT-110` Dataset Promotion or Quarantine.
- `INT-111` Evaluation Evidence Export.
- `TOOL-001`–`006` remain unchanged and gateway-only.

## H. Repository state

```text
northstar-agentic-compliance-stage8a/
├── config/evaluation/{graders,suites}/
├── datasets/evaluation/v1.0.0/
├── docs/{adr,architecture/diagrams,references,source-of-truth,stages}/
├── reports/
├── schemas/DATA-131...DATA-142.schema.json
├── scripts/{run_stage8a_demo,run_stage8a_evaluation,generate_dataset_manifest,validate_stage8a,consistency_audit_stage8a}.py
├── src/northstar_compliance/evaluation/{models,datasets,graders,registry,harness,sampling,gates,io}.py
├── tests/{unit,integration,security,evaluation,performance}/
├── README.md
└── pyproject.toml
```

Python `>=3.11,<3.15`; executed `3.13.5`; runtime standard library; pytest `9.0.2`. Offline execution uses `PYTHONPATH=src`.

## I. Tests completed

- `TEST-508`–`515`: suite/result model guards — passed.
- `TEST-516`–`523`: split, sealing, category and contamination controls — passed.
- `TEST-524`–`544`: grader positive/negative behaviour — passed.
- `TEST-545`–`552`: harness isolation, determinism, test block and candidate failures — passed.
- `TEST-553`–`558`: authority, state, policy and payload security mutations — passed.
- `TEST-559`–`560`: gate and evidence export checks — passed.
- `TEST-561`–`562`: bounded local performance properties — passed.

Executed result: **53 pytest cases passed**. `EVAL-116`–`130`: **15/15 passed**.

## J. Known limitations

1. Compatible overlay; full history merge remains `ISS-096`.
2. Stage 7D model selection/routing skipped and remains open (`ISS-114`).
3. Synthetic small dataset; no production distribution.
4. Fixture candidate outputs; no live model or agent execution.
5. No human calibration or independent assessment.
6. No LLM judge or bias testing.
7. No online/shadow/canary/A-B evaluation.
8. Logical rather than cryptographic test sealing.
9. Internal duplicate checks cannot prove absence from model training.
10. No statistical confidence/power or production thresholds.
11. No enterprise registry/WORM/retention backend.
12. Mermaid not CLI-rendered.

## K. Open risks, assumptions and issues

- New risks: `RSK-248`–`274`.
- New assumptions: `ASM-081`–`087`.
- New issues: `ISS-114`–`122`.
- Inherited `ISS-096` and all inherited production gaps remain.

## L. Compatibility constraints

1. Preserve NorthStar, eight personas, `US-001`–`012`, `CMP-001`–`011` and exactly one active `AGT-001`.
2. Preserve `AGT-001-spec 1.1.0`, `DATA-009 1.1.0` and `GRAPH-001/1.5.0`.
3. Preserve `DATA-091`–`142`, `INT-063`–`111`, `TOOL-001`–`006` and canonical contracts above transports/platforms.
4. `CMP-003` remains sole task/route/protected-state/admission/cancellation/aggregation/system-termination owner.
5. `CMP-007` remains the only authority issuer.
6. Human decisions remain external; evaluation results never approve/finalize.
7. Preserve memory, cache, bounded-concurrency and sequential-fallback constraints.
8. No concurrent protected-state writes, approvals, route mutation, agent creation or shared-memory writes.
9. `WP-008` remains `inactive_future` and is not part of executable evaluation.
10. `DATA-120`, `DATA-130`, `DATA-139` and their interfaces remain advisory and cannot mutate `DATA-106` automatically.
11. Semantic regulatory-answer caching remains prohibited.
12. Speculative decoding remains disabled unless exact profile/model/runtime and gates are approved.
13. Do not present local synthetic scores as production accuracy, reliability, cost or model ranking.
14. Do not implement an LLM judge until the dedicated bias/calibration stage.
15. Dataset corrections create new immutable versions; do not rewrite accepted cases silently.
16. Model selection/routing remains unresolved until an explicit stage/ADR.
17. Resolve/merge `ISS-096` before claiming a complete historical register.

## M. Required input for the next stage

Use all ten `1.9.0` overlays after merge; `ADR-001`–`076`; `AGT-001-spec 1.1.0`; `GRAPH-001/1.5.0`; `DATA-007`, `009`, `041`–`142`; `INT-009`–`111`; `TOOL-001`–`006`; S07A concurrency; S07B workloads; S07C inference evidence; S08A suite/datasets/graders/results, risks/issues and primary-source notes.

## N. Next architectural problem

NorthStar can run a governed local evaluation suite, but it lacks a complete metric catalogue, denominators, thresholds, uncertainty treatment, repeated-trial reliability policy, regression baselines, champion–challenger comparison and CI/CD deployment-gate semantics. It also lacks production/human evidence. These must be defined before a model or route can be approved. LLM-as-a-Judge remains deferred.

## O. Exact continuation instruction

> Continue the NorthStar Agentic AI Architecture Playbook by executing only **Stage 8B — Metrics, Regression Testing and Deployment Gates**. Reconstruct the `1.9.0` S08A baseline; preserve exactly one active `AGT-001`, `GRAPH-001/1.5.0`, `DATA-131`–`142`, `INT-103`–`111`, immutable dataset versions, sealed-test controls, deterministic hard gates, advisory-only results, inactive `WP-008`, authority/state/human/memory/cache/concurrency owners and unresolved Stage 7D model routing; define metric formulas, denominators, thresholds, category slices, repeated-trial reliability, uncertainty, regression baselines, champion–challenger comparison and CI/CD promotion policy; update all artefacts, run the consistency audit and stop after the stage. Do not implement LLM-as-a-Judge.

Audit assertions: exactly one active `AGT-001`; no concurrent protected-state writes; no automatic `DATA-106` mutation; test exposure is controlled; mandatory security/authority failures cannot be averaged away; semantic regulatory-answer caching remains prohibited; no model route is activated.
