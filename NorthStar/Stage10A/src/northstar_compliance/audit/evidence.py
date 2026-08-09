from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any

from northstar_compliance.common import canonical_dumps

from .ledger import AuditIntegrityError, HashChainedAuditLedger

FORBIDDEN_EVIDENCE_KEYS = {
    "chain_of_thought",
    "reasoning_content",
    "raw_prompt",
    "raw_response",
    "password",
    "secret",
    "access_token",
    "refresh_token",
    "private_key",
}


@dataclass(slots=True)
class EvidencePackageBuilder:
    ledger: HashChainedAuditLedger

    def build(
        self,
        *,
        run_id: str,
        artefact_digests: dict[str, str] | None = None,
        release_refs: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        verification = self.ledger.verify()
        if not verification.valid:
            raise AuditIntegrityError("audit chain verification failed")
        records = [record for record in self.ledger.records() if record["run_id"] == run_id]
        if not records:
            raise ValueError(f"no audit records for run {run_id}")
        manifest = {
            "schema_id": "DATA-232",
            "run_id": run_id,
            "event_count": len(records),
            "first_sequence": records[0]["sequence"],
            "last_sequence": records[-1]["sequence"],
            "first_hash": records[0]["record_hash"],
            "last_hash": records[-1]["record_hash"],
            "artefact_digests": artefact_digests or {},
            "release_refs": release_refs or {},
            "contains_hidden_chain_of_thought": False,
            "authority_effect": "none",
        }
        package = {
            "schema_id": "DATA-233",
            "manifest": manifest,
            "audit_records": records,
            "verification": verification.to_dict(),
            "authority_effect": "none",
        }
        package["package_digest"] = hashlib.sha256(canonical_dumps(package).encode("utf-8")).hexdigest()
        def find_unredacted_forbidden(
            node: Any, path: str = "", *, metadata_container: bool = False
        ) -> list[str]:
            violations: list[str] = []
            if isinstance(node, dict):
                for key, value in node.items():
                    child_path = f"{path}.{key}" if path else str(key)
                    is_metadata = metadata_container or str(key) in {"redacted_digests", "redacted_paths"}
                    if str(key).lower() in FORBIDDEN_EVIDENCE_KEYS and not is_metadata:
                        if value != "[REDACTED]":
                            violations.append(child_path)
                    else:
                        violations.extend(
                            find_unredacted_forbidden(value, child_path, metadata_container=is_metadata)
                        )
            elif isinstance(node, list):
                for index, value in enumerate(node):
                    violations.extend(
                        find_unredacted_forbidden(
                            value, f"{path}[{index}]", metadata_container=metadata_container
                        )
                    )
            return violations

        forbidden = find_unredacted_forbidden(package)
        if forbidden:
            raise ValueError(f"unredacted forbidden evidence fields present: {sorted(forbidden)}")
        return package

    @staticmethod
    def verify_package(package: dict[str, Any]) -> bool:
        supplied = package.get("package_digest")
        if not isinstance(supplied, str):
            return False
        copy = dict(package)
        copy.pop("package_digest", None)
        expected = hashlib.sha256(canonical_dumps(copy).encode("utf-8")).hexdigest()
        return supplied == expected
