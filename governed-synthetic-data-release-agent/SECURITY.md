# Security policy

This repository is a local reference implementation, not a deployed security product. Bind services to `127.0.0.1`, use only fictional data, and never point the source adapter at production data. Report vulnerabilities privately to the repository owner. Do not include secrets, personal information, or live customer data in a report.

The release gateway accepts only two logical destinations, rejects path fragments, validates workflow state, approvals, evidence, expiry, kill switches and idempotency, and writes a receipt beside every released file. Local operating-system users can still alter files; the hash chain is tamper-evident demonstration evidence, not non-repudiation.
