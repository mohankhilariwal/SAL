# 07 — Repository Manifest

**Repository:** `northstar-agentic-compliance`  
**Version:** `1.0.0`

## 1. Current tree

```text
northstar-agentic-compliance/
├── config/
│   ├── graph/GRAPH-001-1.1.0.json
│   ├── harness/
│   │   ├── harness-manifest.json
│   │   └── instructions/AGT-001-system-1.0.0.txt
│   └── runtime/runtime.json
├── docs/
│   ├── adr/ADR-033...ADR-035*.md
│   ├── architecture/diagrams/stage-4c-*.mmd
│   ├── baseline/Stage-4B-Handoff-Pack-supplied.md
│   ├── references/Stage-4C-Technical-Sources.md
│   ├── source-of-truth/00...09*.md
│   └── stages/Stage-4C-Agent-Harness-Engineering.md
├── schemas/DATA-063...DATA-070*.schema.json
├── scripts/
│   ├── run_stage4c_demo.py
│   ├── run_stage4c_evaluation.py
│   ├── validate_stage4c.py
│   └── consistency_audit_stage4c.py
├── src/northstar_compliance/
│   ├── approval/{token,service}.py
│   ├── common/jsonutil.py
│   ├── durable/store.py
│   ├── evaluation/stage4c.py
│   ├── graph/{models,runtime,factory}.py
│   ├── harness/
│   │   ├── context.py
│   │   ├── factory.py
│   │   ├── hooks.py
│   │   ├── instructions.py
│   │   ├── models.py
│   │   ├── registries.py
│   │   ├── runtime.py
│   │   ├── tracing.py
│   │   ├── validation.py
│   │   └── workspace.py
│   └── tools/gateway.py
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── security/
│   └── evaluation/
├── README.md
└── pyproject.toml
```

## 2. Important entry points

- Build: `northstar_compliance.harness.factory.build_harness`.
- Runtime: `northstar_compliance.harness.runtime.AgentHarness`.
- Context: `northstar_compliance.harness.context.ContextAssembler`.
- Workspace: `northstar_compliance.harness.workspace.WorkspaceManager`.
- Existing graph: `northstar_compliance.graph.runtime.DurableGraphRuntime`.
- Demo/evaluation/validation/audit: scripts under `scripts/`.

## 3. Compatibility and commands

```bash
python -m pip install -e . --no-deps --no-build-isolation
python -m pytest -q
python -m compileall -q src scripts tests
python scripts/run_stage4c_demo.py
python scripts/run_stage4c_evaluation.py
python scripts/validate_stage4c.py
python scripts/consistency_audit_stage4c.py
```

- Python target: `>=3.11,<3.15`; executed `3.13.5`.
- Runtime dependencies: none beyond standard library.
- Test dependency: `pytest==9.0.2`.
- Local secrets are test/script inputs and are not committed.
- No files are retired. S04C adds `harness/`, new schemas/config/ADRs/diagrams/tests and updates all ten artefacts.

## 4. Migration notes

The reconstructed package implements the S04B contracts needed by S04C. It is not a byte-exact S04B repository patch (`ISS-043`). A production adapter may replace SQLite/workspace/tracing and framework internals only if it preserves `DATA-063`–`070`, `INT-041`–`046`, graph versioning, gateway-only tools, external decisions and preliminary disposition semantics.
