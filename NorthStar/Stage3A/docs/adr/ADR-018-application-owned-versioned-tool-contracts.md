# ADR-018 — Application-Owned Versioned Tool Contracts

- **Status:** Accepted
- **Date:** 2026-07-31

## Context
S02B exposes authorized evidence but no callable business capability. NorthStar needs one canonical representation of tool identity, version, impact, schemas, authorization metadata and runtime limits without binding the architecture to a model vendor.

## Decision
Use application-owned `DATA-035 ToolDescriptor` files. Input and output contracts use JSON Schema Draft 2020-12, prohibit undeclared properties and carry a descriptor SHA-256. Vendor function-calling, OpenAPI or MCP representations may be generated as adapters later.

## Alternatives
Model-vendor schemas as source of truth; OpenAPI as the immediate source of truth; MCP server definitions as the immediate source of truth; untyped Python callables.

## Rationale
The canonical contract is locally validatable, protocol-neutral, deterministic and change-detectable. It preserves critical controls outside probabilistic model behavior.

## Consequences
Schema evolution and adapter conformance must be governed. JSON Schema validity does not establish business correctness.

## Risks and mitigations
Contract-description poisoning is mitigated by repository change control, exact tool/version resolution, descriptor hashing, strict schemas and evaluation.

## Review triggers
Remote deployment, provider export, schema incompatibility, signed registries or a production tool marketplace.
