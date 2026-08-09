# 02 — Requirements Register

**Version:** `1.3.0`

All accepted items through `FR-154`, `NFR-121`, and `CTL-099` remain.

## Functional requirements
- `FR-155` — Assess single-agent, profiled-agent, specialized-graph and multi-agent alternatives using explicit reproducible criteria.
- `FR-156` — Distinguish an agent boundary from a prompt, model call, graph node, role label or tool subset.
- `FR-157` — Preserve exactly one AGT-001 unless a separate promotion gate is satisfied and an ADR-controlled change is approved.
- `FR-158` — Define six bounded task profiles for research, extraction, mapping, risk, verification and reporting.
- `FR-159` — Bind every profile to AGT-001-spec 1.1.0 and GRAPH-001 1.1.0 with deterministic digests.
- `FR-160` — Restrict profiles to subsets of TOOL-001–006 and preserve gateway-only execution.
- `FR-161` — Prevent profiles from granting identity, authority, routes, approval, final closure, memory writes, delegation, handoff or concurrency.
- `FR-162` — Record candidate scores, eligibility, reasons, limitations and policy version in DATA-088.
- `FR-163` — Require an independent boundary or representative measured gain before multi-agent review eligibility.
- `FR-164` — Treat promotion eligibility as non-authoritative; it cannot allocate or start an agent.
- `FR-165` — Preserve human-review and preliminary-disposition semantics.
- `FR-166` — Preserve case-local memory isolation and permit profile visibility only through harness-assembled context.
- `FR-167` — Test legitimate future promotion triggers and invalid pseudo-triggers.
- `FR-168` — Produce local evaluation and microbenchmark evidence without production/model-quality claims.
- `FR-169` — Stop before delegation, handoff, interoperability, shared-agent state or concurrent execution.

## Non-functional requirements
- `NFR-122` — Decision output must be deterministic for identical inputs and policy.
- `NFR-123` — Profile/binding identities must be canonical and SHA-256 bound locally.
- `NFR-124` — Unknown agent, graph, tool or profile IDs fail closed.
- `NFR-125` — Remain provider/framework neutral and standard-library runnable.
- `NFR-126` — No additional agent identity or authority surface in runtime configuration.
- `NFR-127` — Validate profiles before binding.
- `NFR-128` — Measure decision/profile overhead separately from model/tool latency.
- `NFR-129` — Multi-agent claims require representative repeated-trial evaluation and a single-agent control.
- `NFR-130` — Coordination overhead, duplicate work, handoff error and error propagation are explicit metrics.
- `NFR-131` — Artefacts preserve stable identifiers.
- `NFR-132` — No production SLO/cost/security/legal sufficiency claim.
- `NFR-133` — No-concurrency, no-MCP/A2A and no-shared-agent-memory flags remain false.

## Controls
- `CTL-100` — Agent Boundary Classification.
- `CTL-101` — Minimum Agent Count.
- `CTL-102` — Task Profile Allowlists.
- `CTL-103` — Profile Capability Denylist.
- `CTL-104` — Profile Digest Binding.
- `CTL-105` — Promotion Gate.
- `CTL-106` — Non-Authority Gate.
- `CTL-107` — State/Route Ownership.
- `CTL-108` — Gateway Preservation.
- `CTL-109` — Human Authority Preservation.
- `CTL-110` — Memory Boundary Preservation.
- `CTL-111` — Counterfactual Evaluation.
- `CTL-112` — Stage Boundary Validator.

## Critical traceability

| Requirement | Components | Data/interfaces | Controls | Evidence |
|---|---|---|---|---|
| `FR-155/156/162` | `CMP-003/008/011` | `DATA-087/088`, `INT-059` | `CTL-100/101` | `TEST-243`–`255`, `EVAL-055/059` |
| `FR-158`–`161` | `CMP-003` | `DATA-089/090`, `INT-060/061` | `CTL-102`–`104` | `TEST-256`–`269`, `EVAL-056/057/060` |
| `FR-163/164/167` | `CMP-008/011` | `INT-062` | `CTL-105/106/111` | `TEST-248`–`253`, `EVAL-058/061` |
| `FR-165/166/169` | `CMP-003/005/006/007` | retained state/memory/gateway contracts | `CTL-107`–`112` | `TEST-260/270`, audit |

No item is production-complete.
