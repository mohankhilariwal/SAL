# Evidence model

Every workflow creates machine-readable JSON, a Markdown summary, CSV metrics, an audit timeline, a ZIP bundle and a SHA-256 manifest. Allowed exports add an export receipt.

Evidence includes request, identities, delegated authority, dataset profile, classification, source schema, plan, generator/run configuration, utility, privacy, recipient assessment, policy decision, approvals, workflow lineage, export receipt, trace, limitations and file hashes.

The evidence builder is called before export so the gateway can verify the manifest. It is called again after export so the final bundle includes the receipt. `scripts/verify_evidence.py` verifies every manifest and the global audit chain.

This model is deliberately described as tamper-evident local demonstration evidence. Production should use immutable/versioned object storage, independent time sources, key-managed signing or attestations, segregated administrative roles and retention controls.
