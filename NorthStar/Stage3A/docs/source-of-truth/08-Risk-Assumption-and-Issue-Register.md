# 08 — Risk, Assumption and Issue Register

**Version:** `0.5.0`

The active S02B risks, assumptions and issues remain inherited, including `RSK-024`–`RSK-027`, `RSK-032`–`RSK-039`, `ASM-012`–`ASM-015`, and `ISS-011`, `ISS-012`, `ISS-014`–`ISS-020` unless explicitly closed later.

## New risks

| ID | Risk | Current control/residual risk |
|---|---|---|
| `RSK-040` | Tool misuse or excessive functionality | Allowlist, impact classes, no high-impact tools; residual model-selection risk deferred. |
| `RSK-041` | Forged local principal attributes | Local warning/fail-closed fields; high residual until enterprise IAM/PDP. |
| `RSK-042` | Tool schema/description poisoning | Change-controlled files, meta-schema validation, hashing; no signed registry. |
| `RSK-043` | Duplicate or conflicting writes | Mandatory idempotency and argument-hash conflict; store is not durable/distributed. |
| `RSK-044` | Confused deputy or retrieval access widening | Gateway PEP and `TOOL-003` boundary tests; enterprise OBO tokens absent. |
| `RSK-045` | Sensitive data in arguments/results/events | Schema minimization, result limits, hashing/redaction; classification/DLP incomplete. |
| `RSK-046` | Timeout/retry after partial side effect | No automatic write retry; local writes atomic; ambiguous remote outcomes unresolved. |
| `RSK-047` | Local drafts/events mistaken for records or approval | Fixed labels and documentation; organizational misuse remains possible. |
| `RSK-048` | Protocol/provider schema drift | Canonical internal schemas and conformance tests; exports not live-tested. |

## New assumptions

| ID | Assumption |
|---|---|
| `ASM-016` | Local fixtures contain only synthetic/public-safe data. |
| `ASM-017` | In-process adapters are adequate to teach the capability boundary before networking. |
| `ASM-018` | Versioned descriptor schemas are the authoritative runtime-validation source for S03A. |
| `ASM-019` | S03B can consume the gateway without widening authority or changing tool semantics. |

## New issues

| ID | Issue | Status |
|---|---|---|
| `ISS-021` | Byte-exact S02B repository/register set was not available in the sandbox; compatible overlay reconstructed from handoff. | Open/recorded exception. |
| `ISS-022` | Enterprise authentication, workload identity, token exchange and PDP are not connected. | Open; blocks production. |
| `ISS-023` | Regulatory/control/review adapters are synthetic and no live endpoint was exercised. | Open; blocks production claims. |
| `ISS-024` | OpenAPI, vendor function-calling and MCP exports/conformance were not executed. | Open; review when interoperability is introduced. |

## Issues retained as execution exceptions

- `ISS-014`: Mermaid CLI rendering not executed unless separately closed by the validation report.
- `ISS-015`: direct Python 3.12 execution not available; Python 3.13.5 is the verified runtime.
- `ISS-016`, `ISS-018`, `ISS-020`: production model/provider, identity/PDP and generated-answer gaps remain outside S03A.
