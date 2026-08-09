# 07 — Repository Manifest

**Repository version:** `1.4.0`  
**Python target:** `>=3.11,<3.15`  
**Executed:** Python `3.13.5`; pytest `9.0.2`  
**Runtime dependencies:** standard library only.

## Repository

```text
northstar-agentic-compliance-stage6b/
├── config/
│   ├── agents/candidate-endpoints-v1.json
│   ├── architecture/handoff-policy-v1.json
│   └── evaluation/stage6b-cases.json
├── docs/
│   ├── adr/ADR-047...ADR-050*.md
│   ├── architecture/diagrams/{cumulative-logical-architecture,stage-6b-*}.mmd
│   ├── baseline/Stage-6A-Handoff-Pack-supplied.md
│   ├── references/Stage-6B-Technical-Sources.md
│   ├── source-of-truth/00...09*.md
│   └── stages/Stage-6B-Bounded-Agent-Handoff-Communication-and-Authority-Contracts.md
├── schemas/DATA-091...DATA-099*.schema.json
├── scripts/{run_stage6b_demo,run_stage6b_evaluation,benchmark_stage6b,validate_stage6b,consistency_audit_stage6b}.py
├── src/northstar_compliance/
│   ├── handoff/{canonical,models,policy,authority,envelopes,artifacts,lifecycle,simulator,fixtures}.py
│   └── evaluation/
├── tests/{unit,integration,security,evaluation}/
├── reports/
├── README.md
└── pyproject.toml
```

## Commands

```bash
python -m compileall -q src scripts
pytest
PYTHONPATH=src python scripts/run_stage6b_demo.py
PYTHONPATH=src python scripts/run_stage6b_evaluation.py
PYTHONPATH=src python scripts/benchmark_stage6b.py
PYTHONPATH=src python scripts/validate_stage6b.py
PYTHONPATH=src python scripts/consistency_audit_stage6b.py
```

## Compatibility and limitations

- No migration of `GRAPH-001`, `DATA-009`, agent specification, tools or memory.
- No environment variables or external service required.
- Local secrets in fixtures are non-production.
- No protocol adapter, network, queue or concurrency.
- Reconstructed overlay because the complete S06A repository was not supplied.
