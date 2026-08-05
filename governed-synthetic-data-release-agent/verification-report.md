# Verification report

**Build date:** 2026-08-04  
**Execution environment:** CPython 3.13.5, Linux sandbox  
**Target local environment:** macOS with CPython 3.12 or 3.13

## What was executed

- Editable package build/install with the standard setuptools backend: **PASS**.
- Python bytecode compilation for `src`, `scripts`, and `tests`: **PASS**.
- FastAPI `GET /health`: **200 / PASS**.
- FastAPI `GET /ready`: **200 / PASS**.
- Pytest core, policy, security, workflow, API, database, evidence and acceptance suite: **25 passed**.
- Optional integration tests: **3 skipped** because SDV, SDMetrics and Presidio were not present in the restricted sandbox package mirror.
- Clean database rebuild, source-data generation, request-vector seeding and all-scenario execution: **PASS**.
- Four evidence manifests and the append-only audit hash chain: **PASS**.
- Four copied sample-evidence directories: **PASS**.

## Scenario outcomes

| Scenario | Final decision | Terminal stage | Observed result |
|---|---|---|---|
| `internal_allow` | `ALLOW` | `RELEASED` | Utility `0.941972`, privacy `LOW`; controlled internal export receipt created. |
| `external_approval` | `ALLOW` | `RELEASED` | Paused at `REQUIRE_APPROVAL` / `AWAITING_APPROVAL`; export blocked until DATA_OWNER, PRIVACY_OFFICER; then released after both approvals. |
| `privacy_leakage` | `DENY` | `QUARANTINED` | Exact-match rate `0.2578`, near-duplicate rate `0.134167`, rare-combination exposure `0.2002`; candidate quarantined. |
| `prompt_injection` | `DENY` | `SUSPENDED` | Triggered controls: POL-INJ-001, POL-TOOL-001, POL-DATA-001, POL-EXP-001; generation and export did not occur. |

## Tooling not executable in this sandbox

The sandbox package mirror did not expose Ruff, Mypy, Streamlit, SDV, SDMetrics or Presidio. Consequently:

- Ruff and Mypy configuration and commands are included, but their checks were **not executed here**.
- Streamlit source compiled, but the live Streamlit process was **not started here**.
- The full generator adapter and optional integration smoke tests are present, but the executed acceptance flow used the deterministic fallback generator.
- OPA and Ollama were not installed; the Python PDP and deterministic model stub were executed.

On a normal internet-connected Mac, `make setup` installs the full optional stack and `make test && make lint && make typecheck` performs those remaining checks.

## Evidence retained in the download

- `artifacts/scenario-results.json`
- `artifacts/sample-evidence/internal_allow/`
- `artifacts/sample-evidence/external_approval/`
- `artifacts/sample-evidence/privacy_leakage/`
- `artifacts/sample-evidence/prompt_injection/`
- `artifacts/test-results-detailed.txt`
- `artifacts/evidence-verification.log`
- `artifacts/api-smoke-results.txt`
- `artifacts/environment-report.json`

## Immediate human-review priorities

1. Privacy and utility thresholds in `src/governed_release/config/settings.py`.
2. Policy catalogue and precedence in `src/governed_release/adapters/policy_python/engine.py`.
3. Production identity, approval and recipient registries.
4. Cloud-region, data-residency and immutable-storage choices.
5. Full dependency vulnerability scan and license review in the target organization.
