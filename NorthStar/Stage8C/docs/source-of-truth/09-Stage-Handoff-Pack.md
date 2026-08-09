# Stage Handoff Pack

## A. Stage completed

- Stage identifier: `S08C`
- Stage title: Judge-Bias Laboratory
- Architecture version: `1.11.0`
- Repository version: `1.11.0`
- Handoff version: `1.11.0`
- Graph version: `GRAPH-001/1.7.0`
- Completion date: 2026-08-01
- Status: completed as a compatible, provider-neutral, synthetic replay bias-science laboratory; no live judge, production threshold, deployment gate or route.
- Consistency audit: passed with recorded exceptions.

## B. Capabilities now available

1. All S08A/S08B dataset, deterministic-gate, human-authority, judge-contract, calibration, state, memory, cache and concurrency constraints remain.
2. `DATA-155`-`164` define bias taxonomy, matched probes, variants, manifests, trial plans/observations, paired estimates, slice reports, lab reports and quarantine recommendations.
3. `INT-121`-`129` define taxonomy/probe resolution, manifest/planning, replay execution, validation, paired estimation, slicing/quarantine and minimized export.
4. `JBD-001/1.0.0` contains 23 synthetic probe families and 3,312 replay observations; no Stage 8A sealed or production data.
5. The local lab uses one-factor matched pairs, blocking, counterbalancing, three repetitions, stable seeds/digests, paired effects, bootstrap intervals, exact McNemar tests and Holm correction.
6. Critical injection, instruction-contamination or mandatory-gate override evidence recommends quarantine and cannot be averaged away.
7. Bias dimensions remain separate; no universal bias score or production threshold is approved.
8. 66 pytest tests and `EVAL-151`-`168` (18/18) pass.
9. `JUDGE-CONTROL` and `JUDGE-BIASED` are deterministic replay fixtures, not provider/model claims.
10. Metrics/regression baselines, champion-challenger promotion, CI/CD gates, live human evidence and Stage 7D routing remain unresolved.

## C. Accepted architecture decisions

`ADR-001`-`082` remain accepted. New:
- `ADR-083`: execute explicit S08C judge-bias laboratory and defer handed-off deployment-gate stage.
- `ADR-084`: use matched single-factor probes with blocking, randomization and counterbalancing.
- `ADR-085`: use repeated paired estimands with uncertainty and exact tests.
- `ADR-086`: report bias dimensions separately; no production threshold.
- `ADR-087`: critical instruction-boundary/hard-gate failures recommend quarantine.
- `ADR-088`: keep provider-neutral replay-only execution; no live judge route.

## D. Current component inventory

`CMP-001`-`011` remain. `CMP-008` owns the internal bias lab; `CMP-006` owns expert equivalence/adjudication; `CMP-007` authorizes access; `CMP-009` records minimized evidence; `CMP-011` governs versions. `CMP-003`, `CMP-005` and `CMP-010` authority boundaries are unchanged.

## E. Current agent inventory

- `AGT-001 Regulatory Impact Assessment Agent`, spec `1.1.0`, remains the **only active agent**.
- No judge, replay adapter, estimator or panel is an agent.
- `WP-008` remains `inactive_future`.

## F. Current data and state objects

- Preserve `DATA-001`-`154`; `DATA-009` remains `1.1.0`.
- Add `DATA-155`-`164` as listed above.
- No protected-state, approval, route, shared-memory or authority writer is added.
- All S08C artefacts have `authority_effect: none`.

## G. Current interfaces and tools

- Preserve `INT-001`-`120` and `TOOL-001`-`006`.
- Add `INT-121`-`129`.
- The replay adapter is not a tool gateway and has no enterprise side effects.

## H. Repository state

```text
northstar-agentic-compliance-stage8c-judge-bias-lab/
├── config/evaluation/judge_bias/
├── datasets/evaluation/judge-bias/v1.0.0/
├── docs/{adr,architecture/diagrams,references,source-of-truth,stages}/
├── reports/
├── schemas/DATA-155..164.schema.json
├── scripts/
├── src/northstar_compliance/evaluation/judge_bias/
├── tests/{unit,integration,evaluation,security,performance}/
├── README.md
└── pyproject.toml
```

Entry points: `validate_stage8c.py`, `run_stage8c_bias_lab.py`, `run_stage8c_evaluation_gates.py`, `consistency_audit_stage8c.py`.

## I. Tests completed

- `TEST-619`-`625`: design/counterbalancing/digests - passed.
- `TEST-626`-`641`: estimators/statistics - passed.
- `TEST-642`-`651`: validation - passed.
- `TEST-652`-`661`: integration/report - passed.
- `TEST-662`-`670`: security/authority/sealed boundaries - passed.
- `TEST-671`-`682`: signal separation - passed.
- `TEST-683`-`684`: bounded local performance - passed.
- `EVAL-151`-`168`: 18/18 passed.
- Executed: 66 pytest cases passed.

## J. Known limitations

No byte-exact S08B merge, live judge, independent real human calibration, production-derived samples, approved thresholds/power study, adaptive red team, enterprise evidence registry, online/shadow/canary evaluation, regression baseline, deployment gates or model route.

## K. Open risks, assumptions and issues

- Inherited: `ISS-096`, `ISS-114`-`130` and prior risks/issues.
- New risks: `RSK-293`-`309`.
- New assumptions: `ASM-097`-`104`.
- New issues: `ISS-131`-`139`.

## L. Compatibility constraints

1. Preserve NorthStar, eight personas, `US-001`-`012`, `CMP-001`-`011` and exactly one active `AGT-001`.
2. Preserve `AGT-001-spec 1.1.0`, `DATA-009 1.1.0`, `GRAPH-001/1.7.0` and canonical contracts.
3. Preserve `DATA-091`-`164`, `INT-063`-`129`, `TOOL-001`-`006` after merge.
4. `CMP-003` remains sole task/route/protected-state/admission/cancellation/aggregation/system-termination owner.
5. `CMP-005` remains the only tool gateway; `CMP-007` remains the only authority issuer.
6. Humans remain approval/finalization owners.
7. Deterministic mandatory failures and critical injection/contamination failures cannot be averaged, voted or thresholded away.
8. Evaluation results cannot mutate `DATA-106`, approve/finalize, create agents or activate routes.
9. `WP-008` remains inactive; no judge is an agent.
10. Stage 8A immutable/sealed controls remain; no sealed case for calibration or probe development.
11. Semantic regulatory-answer caching remains prohibited.
12. Synthetic replay evidence is not production/fairness/reliability evidence.
13. Any material judge/prompt/rubric/dataset/schema change requires a new manifest and recalibration.
14. No model/provider/route until Stage 7D or a superseding ADR.
15. Resolve/merge `ISS-096`/`ISS-131` before claiming a complete historical register.

## M. Required input for the next stage

Use the merged `1.11.0` overlays; `ADR-001`-`088`; `AGT-001-spec 1.1.0`; `GRAPH-001/1.7.0`; `DATA-131`-`164`; `INT-103`-`129`; Stage 8A suites/datasets/graders; S08B judge contracts/calibration; S08C probe catalogue, experiment manifests, paired estimators and all active risks/issues.

## N. Next architectural problem

NorthStar can measure evaluator sensitivity under controlled perturbations, but still lacks the complete system metric catalogue, category thresholds, minimum sample and repeated-trial reliability policy, immutable regression baselines, champion-challenger comparison, CI/CD promotion states and real human/production evidence needed to approve any model or route.

## O. Exact continuation instruction

> Continue the NorthStar Agentic AI Architecture Playbook by executing only **Stage 8D - Metrics, Regression Testing and Deployment Gates**. Reconstruct the `1.11.0` S08C baseline; preserve exactly one active `AGT-001`, `GRAPH-001/1.7.0`, `DATA-131`-`164`, `INT-103`-`129`, immutable/sealed datasets, deterministic and critical bias failures as non-overridable, judge outputs as advisory only, human authority, inactive `WP-008` and unresolved Stage 7D routing; define metric formulas/denominators, category thresholds, minimum samples, repeated-trial reliability, uncertainty, regression baselines, champion-challenger semantics and CI/CD promotion policy; update all artefacts, run the consistency audit and stop without activating a production model route.

Audit assertions: exactly one active `AGT-001`; no concurrent protected-state writes; no automatic `DATA-106` mutation; sealed-test exposure controlled; mandatory/critical failures cannot be averaged away; all evaluation has `authority_effect: none`; semantic regulatory-answer caching prohibited; no model route activated.
