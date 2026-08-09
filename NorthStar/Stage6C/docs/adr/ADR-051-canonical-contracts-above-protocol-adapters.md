# ADR-051 — Keep NorthStar Canonical Handoff Contracts Authoritative Above Protocol Adapters

- **Status:** Accepted
- **Context:** S06B defined DATA-091–099 and INT-063–070. Every candidate protocol has different native objects and may omit NorthStar-specific authority, human-accountability and termination semantics.
- **Decision:** Protocol adapters translate to and from the canonical contracts. They may not redefine case ownership, authority issuance, approval, finalization or termination.
- **Alternatives:** Let each protocol become authoritative; use framework-native objects only; share a database.
- **Rationale:** Prevents semantic drift, vendor lock-in and protocol-specific security gaps.
- **Consequences:** Additional mapping and conformance code; explicit extension metadata may be necessary.
- **Risks:** Adapter bugs or loss hidden in metadata.
- **Mitigations:** DATA-104 semantic-loss records, fail-closed tests, version-pinned profiles.
- **Review trigger:** A production protocol proves complete native support and an ADR supersedes this decision.
