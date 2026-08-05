# Contributing

1. Create a Python 3.12 or 3.13 virtual environment.
2. Run `make setup`.
3. Add tests for every policy or workflow change.
4. Run `make lint`, `make typecheck`, and `make test`.
5. Never commit generated datasets, evidence bundles, databases, secrets, or logs.
6. Preserve deterministic policy outcomes and stable policy IDs.
