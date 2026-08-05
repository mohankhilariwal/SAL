# Known limitations

- Fictional data and a small single-table fraud scenario.
- The source and partner delivery are local folders.
- Seeded identities are not authentication.
- SQLite is not intended for concurrent production orchestration.
- The workflow checkpoints major durable stages; production should add transactional outbox, distributed locking and retry semantics.
- The local hash chain is detectable evidence, not non-repudiation.
- No formal differential privacy guarantee or comprehensive inference attack library.
- The simple fraud classifier and thresholds are demonstration-only.
- Presidio is optional; deterministic structured recognizers are the core path.
- OPA and Ollama are optional and unavailable dependencies fall back safely.
- Local filesystem permissions cannot stop a machine administrator from copying data; downstream release validation should require a valid receipt.
- Cloud IaC files are placeholders and require organizational networking, identity, security and data-residency decisions.
