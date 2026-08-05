# Production migration

The domain and application layers remain unchanged. Replace adapters behind existing ports.

| Local adapter | Production replacement |
|---|---|
| SQLite | PostgreSQL/Aurora/Cloud SQL/Azure Database for PostgreSQL |
| local files | versioned encrypted object storage with retention/immutability |
| local process | containers, managed agent runtime or approved orchestration platform |
| stub/Ollama | managed model endpoint through the model gateway |
| Python PDP/OPA CLI | separately administered hosted PDP or OPA service |
| seeded identities | enterprise IdP, workload identity and approver directory |
| in-process approval | durable workflow callback with signed, expiring single-use action |
| SQLite/JSONL audit | OpenTelemetry plus centralized immutable evidence storage |
| local export folders | governed object-store delivery, data clean room or controlled transfer service |

## Required production work

- Mutual TLS/private connectivity and service-to-service workload identity.
- Separate control-plane administration from workload administration.
- Database transactions/locking for concurrent resume and approval calls.
- Object versioning, immutability, KMS/HSM-managed keys and formal retention.
- Enterprise identity, recipient due diligence, contract and entitlement integration.
- A formal privacy attack suite and approved thresholds per data domain.
- High availability, disaster recovery, SLOs and chaos/failure testing.
- Supply-chain controls, SBOM, signed images, vulnerability scanning and patch policy.
- Centralized secrets, configuration, feature flags and emergency access.
- Legal/privacy/security review; this reference implementation is not a substitute.
