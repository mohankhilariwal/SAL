# 07 — Repository Manifest

**Repository:** `northstar-agentic-compliance`  
**Version:** `1.1.0`  
**Python target:** `>=3.11,<3.15`  
**Executed environment:** Python 3.13.5; pytest 9.0.2; runtime standard library only.

## New/modified structure

```text
northstar-agentic-compliance/
├── config/
│   ├── agents/AGT-001.spec.json
│   ├── evaluation/stage5a-gates.json
│   └── harness/harness-manifest.json
├── docs/
│   ├── adr/ADR-036...ADR-039*.md
│   ├── architecture/diagrams/stage-5a-*.mmd
│   ├── baseline/Stage-4C-Handoff-Pack-supplied.md
│   ├── references/Stage-5A-Technical-Sources.md
│   ├── source-of-truth/00...09*.md
│   └── stages/Stage-5A-Agent-Specification-and-Context-Engineering.md
├── schemas/DATA-071...DATA-078*.schema.json
├── scripts/
│   ├── benchmark_stage5a.py
│   ├── consistency_audit_stage5a.py
│   ├── run_stage5a_demo.py
│   ├── run_stage5a_evaluation.py
│   └── validate_stage5a.py
├── src/northstar_compliance/
│   ├── harness/specification_guard.py
│   └── specification/
│       ├── assertions.py
│       ├── canonical.py
│       ├── context_policy.py
│       ├── gates.py
│       ├── integration.py
│       ├── loader.py
│       ├── models.py
│       └── validator.py
├── tests/
│   ├── unit/test_stage5a_specification.py
│   ├── integration/test_stage5a_runtime_binding.py
│   ├── security/test_stage5a_security_boundaries.py
│   └── evaluation/test_stage5a_evaluation_gates.py
├── README.md
└── pyproject.toml
```

## Important entry points

- Canonical spec: `config/agents/AGT-001.spec.json`
- Runtime composition: `src/northstar_compliance/specification/integration.py`
- Harness wrapper: `src/northstar_compliance/harness/specification_guard.py`
- Validation: `scripts/validate_stage5a.py`
- Audit: `scripts/consistency_audit_stage5a.py`
- Demo/evaluation/benchmark scripts.

## Commands

```bash
python -m pip install -e . --no-deps --no-build-isolation
python -m pytest -q
python -m compileall -q src scripts tests
python scripts/run_stage5a_demo.py
python scripts/run_stage5a_evaluation.py
python scripts/benchmark_stage5a.py
python scripts/validate_stage5a.py
python scripts/consistency_audit_stage5a.py
```

## Compatibility notes

- `GRAPH-001` and `DATA-009` stay `1.1.0`.
- Tool contracts stay `1.0.0` and gateway-only.
- The manifest advances to `1.1.0` only to add the specification binding.
- The supplied S04C handoff/chapter, not a byte-exact complete repository, is the reconstruction source (`ISS-050`).
