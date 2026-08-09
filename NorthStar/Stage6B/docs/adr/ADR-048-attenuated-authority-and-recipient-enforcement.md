# ADR-048 — Attenuated Authority and Recipient-Side Enforcement

- **Status:** Accepted
- **Context:** A future recipient must not inherit AGT-001's full identity, user credential or tool catalogue.
- **Decision:** `CMP-007` issues a short-lived, audience/case/run/task/resource/data-scope-bound `DATA-093` grant. Child scope must be a strict subset, use/delegation are bounded, and the recipient or tool boundary verifies signature, expiry, audience, nonce and scope before loading data or acting.
- **Alternatives:** Pass user token; shared service credential; prompt instruction; unsigned claims; central check only at sender.
- **Rationale:** Delegation is an authorization event, not a conversational instruction. Enforcement at the recipient/tool boundary limits confused-deputy and replay risk.
- **Consequences:** Token service, revocation/use ledger, clock and key management are production dependencies.
- **Risks:** Local HMAC reference can be mistaken for production OAuth/DPoP. Documentation and tests explicitly prohibit that claim.
- **Review trigger:** Production IAM selection, cross-domain delegation, stronger proof-of-possession, or legal/security review.
