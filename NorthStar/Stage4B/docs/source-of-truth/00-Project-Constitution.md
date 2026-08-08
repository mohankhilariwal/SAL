# Project Constitution — 0.9.0

All accepted names, personas, `US-001`–`US-012`, `CMP-001`–`CMP-011`, `AGT-001`, `TOOL-001`–`006`, gateway-only authority, access-before-context, S03C recovery/budget semantics and S04A typed graph ownership remain.

Stage 4B constitutional additions:

- a human decision is an external authenticated/authorized event, never model output;
- waiting must release execution resources and persist correlation, expiry and graph version;
- approve/reject/expiry routes are application-owned;
- one decision is accepted per wait; timeout never means approval;
- reviewer and initiator separation of duties is enforced locally;
- `preliminary_grounded_human_approved` means approved for controlled continuation, not a final legal or compliance conclusion;
- no raw callback token, hidden chain-of-thought, memory, harness, concurrent graph branch or second agent is added.
