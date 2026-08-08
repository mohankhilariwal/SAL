# 07 — Repository Manifest

**Repository:** `northstar-agentic-compliance`  
**Version:** `0.5.0`

## Important tree

```text
northstar-agentic-compliance/
├── config/tools/
│   ├── tool-descriptor.schema.json
│   └── TOOL-001-*.json ... TOOL-006-*.json
├── datasets/stage3a/evaluation-cases.json
├── docs/
│   ├── adr/ADR-018-*.md ... ADR-021-*.md
│   ├── architecture/diagrams/
│   │   ├── cumulative-logical-architecture.mmd
│   │   ├── stage-3a-architecture-before.mmd
│   │   ├── stage-3a-architecture-after.mmd
│   │   ├── stage-3a-tool-gateway-sequence.mmd
│   │   └── stage-3a-trust-boundary.mmd
│   ├── baseline/Stage-2B-Handoff-Pack-supplied.md
│   ├── references/Stage-3A-Technical-Sources.md
│   ├── source-of-truth/00-...md through 09-...md
│   └── stages/Stage-3A-Tool-Contracts-and-Tool-Gateway.md
├── examples/stage3a-output/
├── reports/
├── scripts/
│   ├── run_stage3a_demo.py / .sh
│   ├── run_stage3a_evaluation.py
│   ├── benchmark_stage3a_gateway.py
│   ├── validate_stage3a.py
│   └── consistency_audit_stage3a.py
├── src/northstar_compliance/tools/
│   ├── models.py, registry.py, policy.py, gateway.py
│   ├── adapters.py, controls.py, idempotency.py
│   ├── storage.py, events.py, factory.py, utils.py, errors.py
│   └── __init__.py
├── tests/{unit,integration,security,evaluation,constitution}/
├── pyproject.toml
├── requirements.lock
├── README.md
└── CHANGELOG.md
```

## Entry points

- Local gateway factory: `src/northstar_compliance/tools/factory.py`.
- Enforcement pipeline: `src/northstar_compliance/tools/gateway.py`.
- Contracts: `src/northstar_compliance/tools/models.py` and `config/tools/`.
- Demo: `scripts/run_stage3a_demo.py`.
- Evaluation: `scripts/run_stage3a_evaluation.py`.
- Benchmark: `scripts/benchmark_stage3a_gateway.py`.
- Acceptance checks: `scripts/validate_stage3a.py`, `scripts/consistency_audit_stage3a.py`, `pytest`.
- Current chapter: `docs/stages/Stage-3A-Tool-Contracts-and-Tool-Gateway.md`.

## Files added

All Stage 3A tool modules, six descriptors, schemas, tests, scripts, diagrams, ADRs, stage chapter and updated source-of-truth files.

## Files modified

Package metadata, README, changelog and cumulative architecture advance to `0.5.0`.

## Files retired

None.

## Compatibility and migration

- The supplied S02B handoff is preserved under `docs/baseline/`.
- The byte-exact S02B repository was unavailable, so this is a compatible Stage 3A overlay rather than a claim of byte-for-byte repository continuation (`ISS-021`).
- Future network/OpenAPI/MCP adapters must preserve `DATA-035`–`DATA-040`, exact tool versions, error semantics and gateway ordering.
