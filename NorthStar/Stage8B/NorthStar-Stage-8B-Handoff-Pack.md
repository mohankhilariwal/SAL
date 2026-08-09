# Stage Handoff Pack
### A. Stage completed

- **Stage identifier:** `S08B`
- **Stage title:** LLM-as-a-Judge
- **Architecture version:** `1.10.0`
- **Repository version:** `1.10.0`
- **Handoff version:** `1.10.0`
- **Graph version:** `GRAPH-001/1.6.0`
- **Completion date:** 2026-08-01
- **Status:** Completed as a provider-neutral advisory judge architecture and replay-based calibration/bias laboratory; no live judge model or production route.
- **Consistency audit:** Passed with inherited and recorded exceptions.

### B. Capabilities now available

1. All S08A evaluation, dataset, authority, state, memory, cache, concurrency and human-control constraints remain.
2. `DATA-143`–`154` define judge policies, prompts, envelopes, criterion findings, verdicts, calibration data, bias probes, reports, panels and audit evidence.
3. `INT-112`–`120` define policy resolution, envelope creation, adapter invocation, validation, bias execution, human calibration, panel aggregation, evidence export and eligibility/quarantine.
4. `JUDGE-POLICY-001` requires deterministic-first, evidence-first, score-last, abstention-capable judging with `authority_effect: none`.
5. `JDS-001/1.0.0` contains 24 immutable synthetic calibration cases and human-label/replay fixtures; it excludes Stage 8A sealed tests.
6. The local lab measures agreement, coverage, score error, tail recall, position, framing, acquiescence, premature commitment, surface, self-preference, injection and language gaps.
7. Strict validation rejects hidden reasoning, extra authority fields, wrong digests, missing criteria, score-first output, unacknowledged checks and mandatory-failure overrides.
8. Qualified panel aggregation supports abstention/disagreement and human review; it cannot override hard gates.
9. 56 pytest cases and `EVAL-131`–`150` (20/20) pass; validation, demo, bias, calibration and stage-gate reports are generated.
10. Model routing, production model selection, deployment gates and real human/live-model evidence remain unresolved.

### C. Accepted architecture decisions

`ADR-001`–`076` remain accepted. New decisions:

- `ADR-077`: execute the explicitly requested judge stage before metrics/deployment gates with conservative scope.
- `ADR-078`: use deterministic-first human-model hybrid judging.
- `ADR-079`: use evidence-first criterion-isolated score-last pointwise judging by default.
- `ADR-080`: use immutable calibration data and paired bias probes.
- `ADR-081`: use only qualified panels, with abstention and human escalation.
- `ADR-082`: keep provider-neutral adapters and select no live judge route.

### D. Current component inventory

| ID | Name | Current S08B responsibility/status |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | May display advisory evaluation evidence; no authority change. |
| `CMP-002` | Regulatory Intake Boundary | Future authorized sample provenance; local judge data is synthetic. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Sole workflow/state/route owner; judge cannot mutate it. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Supplies authorized evidence references/versions when invoked by evaluation. |
| `CMP-005` | Enterprise Integration Boundary | Sole gateway for `TOOL-001`–`006`; judge has no tool access. |
| `CMP-006` | Human Review and Approval Boundary | Owns expert labels, adjudication and uncertain/disputed review. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Authorizes calibration case, rubric and reference access. |
| `CMP-008` | Evaluation and Assurance Boundary | Owns judge contracts, bias lab, calibration and advisory panels. |
| `CMP-009` | Observability and Audit Boundary | Records minimized judge evidence and digests. |
| `CMP-010` | Runtime and Deployment Boundary | Future adapter endpoint only; no live judge route. |
| `CMP-011` | Source-of-Truth Governance Pack | Governs versions, ADRs, risks and quarantine. |

### E. Current agent inventory

| ID | Name | Authority | Status |
|---|---|---|---|
| `AGT-001` | Regulatory Impact Assessment Agent | Existing bounded proposal/complete/escalate authority; no approval, finalization, route, grant, agent-creation or unrestricted/shared-memory authority. | **Only active agent**, spec `1.1.0`. |

No judge is an agent. `WP-008` remains `inactive_future`.

### F. Current data and state objects

- `DATA-001`–`142` retained; `DATA-009` remains `1.1.0`.
- New `DATA-143`–`154` as listed in Section 14.
- No protected-state, approval, route or shared-memory writer is added.
- All judge artefacts are advisory with `authority_effect: none`.

### G. Current interfaces and tools

- `INT-001`–`111` retained.
- New `INT-112`–`120` as listed in Section 14.
- `TOOL-001`–`006` remain unchanged and gateway-only.
- The judge adapter is not a tool gateway and has no enterprise side effects.

### H. Repository state

```text
northstar-agentic-compliance-stage8b-llm-judge/
├── config/evaluation/judges/
├── datasets/evaluation/judge-calibration/v1.0.0/
├── docs/adr/
├── docs/architecture/diagrams/
├── docs/references/
├── docs/source-of-truth/
├── docs/stages/
├── reports/
├── schemas/DATA-143..154.schema.json
├── scripts/
├── src/northstar_compliance/evaluation/judge/
├── tests/{unit,integration,evaluation,security,performance}/
├── README.md
└── pyproject.toml
```

Important entry points: `run_stage8b_demo.py`, `run_stage8b_bias_lab.py`, `run_stage8b_calibration.py`, `validate_stage8b.py`, `consistency_audit_stage8b.py`.

### I. Tests completed

- `TEST-563`–`570`: model/policy/envelope guards — passed.
- `TEST-571`–`578`: prompt, schema, score-last, mandatory and injection guards — passed.
- `TEST-579`–`594`: agreement and bias metric primitives — passed.
- `TEST-595`–`604`: calibration and eligibility — passed.
- `TEST-605`–`608`: panel aggregation — passed.
- `TEST-609`–`616`: security and data-boundary tests — passed.
- `TEST-617`–`618`: bounded local performance — passed.
- `EVAL-131`–`150`: Stage 8B contract, security, calibration, bias, boundary and audit gates — 20/20 passed.
- **Executed:** 56 pytest cases passed.

### J. Known limitations

The limitations in Section 24 remain. Most importantly: no live judge, no real human calibration, small synthetic dataset, no production thresholds/statistics, no online evaluation, no enterprise registry/WORM and no deployment gates.

### K. Open risks, assumptions and issues

- Inherited risks/issues remain, including `ISS-096` and `ISS-114`–`122`.
- New risks: `RSK-275`–`292`.
- New assumptions: `ASM-088`–`096`.
- New issues: `ISS-123`–`130`.

### L. Compatibility constraints

1. Preserve NorthStar, eight personas, `US-001`–`012`, `CMP-001`–`011` and exactly one active `AGT-001`.
2. Preserve `AGT-001-spec 1.1.0`, `DATA-009 1.1.0` and `GRAPH-001/1.6.0`.
3. Preserve `DATA-091`–`154`, `INT-063`–`120`, `TOOL-001`–`006` and canonical contracts above providers.
4. `CMP-003` remains sole task/route/protected-state/admission/cancellation/aggregation/system-termination owner.
5. `CMP-007` remains the only authority issuer; `CMP-005` remains the only tool gateway.
6. Humans remain approval/finalization owners.
7. Deterministic mandatory failures cannot be overridden, averaged away or outvoted.
8. Evaluation and judge results cannot mutate `DATA-106` or activate routes automatically.
9. `WP-008` remains `inactive_future`; no judge is an agent.
10. Stage 8A immutable datasets, split lineage, contamination and sealed-test controls remain.
11. Do not use Stage 8A sealed test cases for prompt/judge development or calibration.
12. Semantic regulatory-answer caching remains prohibited.
13. Speculative decoding remains disabled unless separately approved.
14. Do not present replay scores as live-model, production, fairness or reliability evidence.
15. A judge configuration requires real human calibration and security testing before production eligibility.
16. No model/provider/route is activated until Stage 7D or an explicit superseding ADR.
17. Resolve/merge `ISS-096` before claiming a complete historical register.

### M. Required input for the next stage

Use all ten `1.10.0` overlays after merge; `ADR-001`–`082`; `AGT-001-spec 1.1.0`; `GRAPH-001/1.6.0`; `DATA-007`, `009`, `041`–`154`; `INT-009`–`120`; `TOOL-001`–`006`; S07A concurrency; S07B workloads; S07C inference evidence; S08A suites/datasets/deterministic graders; S08B judge policies, calibration contracts, bias probes/reports and all active risks/issues.

### N. Next architectural problem

NorthStar has deterministic and model-based evaluation primitives, but it still lacks a complete metric catalogue with explicit denominators, category slices and thresholds; repeated-trial reliability and statistical uncertainty; regression baselines; champion–challenger semantics; and CI/CD promotion states. It also lacks real production and human evidence. Those controls must be defined before model selection, routing or deployment can be approved.

### O. Exact continuation instruction

> Continue the NorthStar Agentic AI Architecture Playbook by executing only **Stage 8C — Metrics, Regression Testing and Deployment Gates**. Reconstruct the `1.10.0` S08B baseline; preserve exactly one active `AGT-001`, `GRAPH-001/1.6.0`, `DATA-131`–`154`, `INT-103`–`120`, immutable/sealed datasets, deterministic non-overridable hard gates, calibrated-judge advisory-only semantics, human authority, inactive `WP-008` and unresolved Stage 7D routing; define metric formulas and denominators, category thresholds, repeated-trial reliability, uncertainty, regression baselines, champion–challenger comparison and CI/CD promotion policy; update all artefacts, run the consistency audit and stop after the stage. Do not activate a production model route.

Audit assertions: exactly one active `AGT-001`; no concurrent protected-state writes; no automatic `DATA-106` mutation; sealed-test exposure remains controlled; mandatory failures cannot be averaged or voted away; judge outputs have `authority_effect: none`; semantic regulatory-answer caching remains prohibited; no model route is activated.
