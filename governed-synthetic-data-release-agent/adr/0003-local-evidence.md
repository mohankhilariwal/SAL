# ADR 0003: Local tamper-evident evidence

**Status:** Accepted for the reference implementation

Use SQLite audit metadata, append-only JSONL events, chained SHA-256 hashes, per-bundle manifests and ZIP artifacts. Describe this honestly as tamper-evident demonstration evidence. Production migration requires immutable storage and stronger signing/attestation.
