# Repository Manifest — 0.9.0

Python target `>=3.11,<3.15`; executed on Python `3.13.5`. Runtime dependencies: standard library only. Test dependency: pytest `9.0.2`.

Important entry points:

```text
config/graph/stage4b-regulatory-impact-graph.json
src/northstar_compliance/approval/{token,service}.py
src/northstar_compliance/durable/store.py
src/northstar_compliance/graph/{models,definition,runtime,factory}.py
src/northstar_compliance/tools/gateway.py
scripts/{run_stage4b_demo,run_stage4b_evaluation,validate_stage4b,consistency_audit_stage4b}.py
tests/{unit,integration,security,evaluation}/
docs/stages/Stage-4B-Checkpointing-Durable-Execution-and-Human-Approval.md
```

No files are added under `memory/`, `harness/`, `agents/`, `multi_agent/` or concurrency branch execution.
