# 03 — Architecture Baseline

**Version:** 1.14.0  
**Graph:** `GRAPH-001/1.10.0`  
**Threat model:** `TM-001/1.2.0`  
**AUTH:** `AUTH-001/1.0.0` unchanged  
**Blast radius:** `BR-001/1.0.0` unchanged  
**Guardrails:** `GR-001/1.0.0`  
**Governance:** `GOV-001/1.0.0`  
**Control plane:** `CP-001/0.1.0` bounded local reference

## Architecture statement

NorthStar remains a single-agent, graph/orchestrator-owned regulatory assessment architecture. Stage 9C distributes guardrail PEPs to the accepted component owners and governs them using immutable local bundles. It adds no new top-level runtime authority component.

## PEP allocation

- CMP-002: input.
- CMP-003: context, planning, state, memory, runtime.
- CMP-004: retrieval after AUTH-001.
- CMP-005: tool/result after AUTH-001 and BR-001.
- CMP-006: human review validation.
- CMP-008: asynchronous advisory/model-assisted and policy test evidence.
- CMP-009: minimized evidence.
- CMP-010: local verified cache.
- CMP-011: lifecycle/releases/exceptions.

## Invariants

Exactly one active AGT-001; no tool beyond TOOL-001–006; CMP-003/CMP-005/CMP-006/CMP-007 ownership unchanged; no Data-106 mutation by policy/evaluation; no active MCP/A2A; unresolved Stage 8D; no full production control plane.

## Diagrams

- `docs/architecture/diagrams/cumulative-logical-architecture.mmd`
- `stage-9c-guardrail-pipeline.mmd`
- `stage-9c-policy-lifecycle.mmd`
- `stage-9c-control-plane-data-plane.mmd`
- `stage-9c-human-accountability-sequence.mmd`
