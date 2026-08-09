# NorthStar Stage 7A — Concurrency and Distributed Execution

This package is the runnable `1.6.0` reconstruction overlay for Stage 7A. It preserves exactly one active `AGT-001` and adds bounded concurrent workflow branches, deterministic fan-in, backpressure, idempotency, retry, cancellation and checkpoint resumption.

## Important limitation

The nine complete predecessor source registers were not attached. The package preserves all S06C items named in the supplied handoff and records `ISS-088`; it must be merged with the full `1.5.0` registers before claiming complete historical coverage.

## Run

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
pytest -q
PYTHONPATH=src python scripts/run_stage7a_demo.py
PYTHONPATH=src python scripts/run_stage7a_evaluation.py
PYTHONPATH=src python scripts/benchmark_stage7a.py
PYTHONPATH=src python scripts/validate_stage7a.py
PYTHONPATH=src python scripts/consistency_audit_stage7a.py
```

## Tested

- Python 3.13.5
- pytest 9.0.2
- 47 tests passed
- 10 evaluations passed
- no external or paid service required
