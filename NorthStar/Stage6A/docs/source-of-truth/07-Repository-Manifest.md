# 07 — Repository Manifest
**Repository version:** `1.3.0`  
**Python:** `>=3.11,<3.15`; executed `3.13.5`  
**Runtime:** standard library only; tests: pytest `9.0.2`

```text
config/{agents,architecture,evaluation,prompts}/
docs/{adr,architecture/diagrams,baseline,references,source-of-truth,stages}/
schemas/DATA-087...DATA-090*.schema.json
scripts/{run_stage6a_demo,run_stage6a_evaluation,benchmark_stage6a,validate_stage6a,consistency_audit_stage6a}.py
src/northstar_compliance/architecture_decision/{canonical,models,policy,assessment,profiles,binding,report}.py
tests/{unit,evaluation}/
```

```bash
PYTHONPATH=src python3 -m pytest -q
PYTHONPATH=src python3 scripts/run_stage6a_demo.py
PYTHONPATH=src python3 scripts/run_stage6a_evaluation.py
PYTHONPATH=src python3 scripts/benchmark_stage6a.py
PYTHONPATH=src python3 scripts/validate_stage6a.py
PYTHONPATH=src python3 scripts/consistency_audit_stage6a.py
```

The byte-exact `1.2.0` repository was not mounted; `ISS-065` records a compatible reconstruction overlay based on the supplied S05B handoff/chapter.
