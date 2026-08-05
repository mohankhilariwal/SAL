# Stage 1 Validation Report

**Validation date:** 28 July 2026  
**Environment:** Python 3.13.5 on the supplied isolated runtime

## Executed checks

| Check | Result |
|---|---|
| Python source compilation (`compileall`) | Passed |
| Required Stage 1 headings | 11/11 present |
| Mermaid blocks | 13 extracted and structurally validated |
| Audit JSONL | 10 records parsed and required fields present |
| Offline behavioural tests | 8 passed |
| Optional framework tests | 2 skipped because packages were not installed |
| Plain Python approved run | Completed in 4 turns and 3 tool calls |
| Idempotent ticket behaviour | Covered by tests |
| Safe default without write approval | Covered by tests |
| Budget/repetition controls | Covered by tests |

## Compatibility result

- Python 3.13.5: supported.
- Pydantic 2.13.4: exact match.
- python-dotenv 1.2.2: exact match.
- pytest 9.0.2: exact match.
- pytest-cov: installed 7.0.0, target 7.1.0; optional development mismatch correctly detected.
- typing-extensions: installed 4.15.0, target 4.16.0; mismatch correctly detected.
- LangGraph 1.2.10: optional dependency not installed.
- OpenAI Agents SDK 0.19.0: optional dependency not installed.

The compatibility command therefore returned non-zero as designed. The offline core was validated directly from `src` using `PYTHONPATH=src`.

## Installation limitation

An editable-install attempt invoked PEP 517 build isolation, but the isolated package index could not supply the requested setuptools build backend. This is an environment/package-index limitation. It is not represented as a successful packaging test.

## Claim boundaries

- **Executed:** offline core, compile checks, JSONL validation, diagram structural checks and pytest tests.
- **Statically aligned with official documentation:** LangGraph and OpenAI Agents SDK examples.
- **Not executed here:** optional framework runtimes, provider-backed model call, rendering Mermaid through the Mermaid CLI.

For production use, install all pinned dependencies from an approved mirror, render the `.mmd` diagrams with the organization’s Mermaid toolchain, and run live integration/security tests in the target environment.
