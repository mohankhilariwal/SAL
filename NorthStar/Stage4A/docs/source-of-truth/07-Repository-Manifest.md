# 07 — Repository Manifest

**Repository version:** `0.8.0`  
**Python:** `>=3.11,<3.15`; executed on `3.13.5`  
**Runtime dependencies:** standard library only  
**Test dependency:** pytest `9.0.2`

## Important entry points

```text
config/graph/stage4a-regulatory-impact-graph.json
src/northstar_compliance/graph/{models,definition,state,nodes,runtime,factory}.py
src/northstar_compliance/agent/{models,budgets,decision,termination}.py
src/northstar_compliance/tools/gateway.py
src/northstar_compliance/state/checkpoint.py
schemas/DATA-053...DATA-057*.schema.json
scripts/{run_stage4a_demo,run_stage4a_evaluation,validate_stage4a,consistency_audit_stage4a}.py
tests/{unit,integration,security,evaluation}/
docs/stages/Stage-4A-Graph-Foundations-and-Typed-State.md
```

## Added

Graph package/configuration, five schemas, three ADRs, six diagrams, Stage 4A scripts/tests/chapter/references and all updated registers.

## Modified/reconstructed

Stage 3C agent budget/recovery/checkpoint/tool concepts are implemented as a compatible `0.8.0` overlay because the byte-exact `0.7.0` repository and nine individual registers were not mounted (`ISS-032`).

## Retired

No accepted ID or capability is retired. The imperative `agent/runtime.py` implementation is superseded by `graph/runtime.py`; its authority, budget, recovery and completion semantics remain.


## Complete current tree

```text
northstar-agentic-compliance/
├── config/
│   ├── graph/
│   │   └── stage4a-regulatory-impact-graph.json
│   └── runtime/
│       └── stage3c-budget.json
├── docs/
│   ├── adr/
│   │   ├── ADR-027-explicit-typed-execution-graph.md
│   │   ├── ADR-028-framework-neutral-local-graph-kernel.md
│   │   └── ADR-029-node-owned-copy-on-write-state-patches.md
│   ├── architecture/
│   │   └── diagrams/
│   │       ├── cumulative-logical-architecture.mmd
│   │       ├── stage-4a-architecture-before.mmd
│   │       ├── stage-4a-execution-graph.mmd
│   │       ├── stage-4a-recovery-sequence.mmd
│   │       ├── stage-4a-trust-boundary.mmd
│   │       └── stage-4a-typed-state.mmd
│   ├── baseline/
│   │   └── Stage-3C-Handoff-Pack.md
│   ├── references/
│   │   └── Stage-4A-Technical-Sources.md
│   ├── source-of-truth/
│   │   ├── 00-Project-Constitution.md
│   │   ├── 01-Business-and-User-Story-Baseline.md
│   │   ├── 02-Requirements-Register.md
│   │   ├── 03-Architecture-Baseline.md
│   │   ├── 04-Component-and-Agent-Catalogue.md
│   │   ├── 05-Data-and-Schema-Register.md
│   │   ├── 06-ADR-Register.md
│   │   ├── 07-Repository-Manifest.md
│   │   ├── 08-Risk-Assumption-and-Issue-Register.md
│   │   └── 09-Stage-Handoff-Pack.md
│   └── stages/
│       └── Stage-4A-Graph-Foundations-and-Typed-State.md
├── schemas/
│   ├── DATA-053-ExecutionGraphDefinition.schema.json
│   ├── DATA-054-TypedGraphExecutionState.schema.json
│   ├── DATA-055-GraphNodeResult.schema.json
│   ├── DATA-056-GraphStatePatch.schema.json
│   └── DATA-057-GraphTransitionRecord.schema.json
├── scripts/
│   ├── consistency_audit_stage4a.py
│   ├── run_stage4a_demo.py
│   ├── run_stage4a_evaluation.py
│   └── validate_stage4a.py
├── src/
│   └── northstar_compliance/
│       ├── agent/
│       │   ├── __init__.py
│       │   ├── budgets.py
│       │   ├── decision.py
│       │   ├── models.py
│       │   └── termination.py
│       ├── graph/
│       │   ├── __init__.py
│       │   ├── definition.py
│       │   ├── factory.py
│       │   ├── models.py
│       │   ├── nodes.py
│       │   ├── runtime.py
│       │   └── state.py
│       ├── state/
│       │   ├── __init__.py
│       │   └── checkpoint.py
│       ├── tools/
│       │   ├── __init__.py
│       │   └── gateway.py
│       └── __init__.py
├── tests/
│   ├── evaluation/
│   │   └── test_graph_evaluation.py
│   ├── integration/
│   │   ├── test_checkpoint_resume.py
│   │   └── test_graph_runtime.py
│   ├── security/
│   │   └── test_boundaries.py
│   └── unit/
│       ├── test_graph_definition.py
│       └── test_typed_state.py
├── .env.example
├── CHANGELOG.md
├── pyproject.toml
├── README.md
├── Stage-4A-Evaluation-Report.json
├── Stage-4A-Graph-Foundations-and-Typed-State.md
├── Stage-4A-Handoff-Pack.md
└── Stage-4A-Validation-Report.txt
```
