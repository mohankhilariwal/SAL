# 05 — Data and Schema Register (Reconstructed 1.6.0 Overlay)

`DATA-001`–`105` remain retained; `DATA-009` remains `1.1.0`; `DATA-081 case_working` is not transferred.

| ID | Name | Version | Owner | Schema |
|---|---|---|---|---|
| `DATA-106` | ConcurrencyExecutionPolicy | `1.0.0` | CMP-003/CMP-011 | `schemas/DATA-106.schema.json` |
| `DATA-107` | WorkItemEnvelope | `1.0.0` | CMP-003 | `schemas/DATA-107.schema.json` |
| `DATA-108` | BranchExecutionRecord | `1.0.0` | CMP-010 -> CMP-003 | `schemas/DATA-108.schema.json` |
| `DATA-109` | IdempotencyRecord | `1.0.0` | CMP-003 | `schemas/DATA-109.schema.json` |
| `DATA-110` | FanInAggregationRecord | `1.0.0` | CMP-003 | `schemas/DATA-110.schema.json` |
| `DATA-111` | CancellationRecord | `1.0.0` | CMP-003 | `schemas/DATA-111.schema.json` |
| `DATA-112` | ResumptionCheckpoint | `1.0.0` | CMP-003/CMP-010 | `schemas/DATA-112.schema.json` |
| `DATA-113` | QueueHealthSnapshot | `1.0.0` | CMP-009 | `schemas/DATA-113.schema.json` |

## State rules

- branch inputs are immutable snapshots;
- workers return provisional output only;
- no shared mutable state or shared-agent memory;
- one authoritative state transition occurs in CMP-003 after fan-in;
- same idempotency key with different input digest fails closed;
- checkpoint evidence is local reference durability, not a production event log.
