# ADR-078 - Deterministic-first human-model hybrid judging

**Status:** Accepted

**Decision:** Run deterministic authority, permission, schema and tool checks before any model judge. A model judge may assess semantic criteria but cannot override hard failures. Human labels remain the calibration reference and humans retain deployment and regulatory accountability.
