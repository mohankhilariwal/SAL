# 05 — Data and Schema Register

**Version:** 1.5.0

`DATA-001`–`099` and `INT-001`–`070` remain accepted.

## New data objects

| ID | Name | Owner |
|---|---|---|
| `DATA-100` | InteroperabilityProtocolProfile | CMP-003/CMP-011 |
| `DATA-101` | ProtocolBindingManifest | CMP-003 |
| `DATA-102` | CapabilityAdvertisement | Registry governance |
| `DATA-103` | VersionNegotiationRecord | Adapter boundary |
| `DATA-104` | AdapterConformanceRecord | CMP-008 |
| `DATA-105` | TransportDeliveryReceipt | Adapter/CMP-003 |

## New interfaces

| ID | Name |
|---|---|
| `INT-071` | Protocol Profile Registry |
| `INT-072` | Capability Advertisement and Discovery |
| `INT-073` | Version and Binding Negotiation |
| `INT-074` | HTTP/JSON Reference Handoff Delivery |
| `INT-075` | MCP Tool/Resource Conformance Mapping |
| `INT-076` | A2A Task-Lifecycle Conformance Mapping |
| `INT-077` | Adapter Conformance and Semantic-Loss Evaluation |
| `INT-078` | Protocol Security and Fail-Closed Enforcement |

Schemas are in `schemas/DATA-100.schema.json` through `DATA-105.schema.json`.
