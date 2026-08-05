from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from governed_release.adapters.observability.audit import AuditLedger
from governed_release.adapters.persistence.repository import Database, SQLAlchemyAuditStore
from governed_release.application.evidence import verify_evidence_directory


def main() -> None:
    evidence_root = ROOT / "data" / "evidence"
    failures: list[str] = []
    checked = 0
    for directory in sorted(evidence_root.iterdir()) if evidence_root.exists() else []:
        if not directory.is_dir():
            continue
        ok, errors = verify_evidence_directory(directory)
        checked += 1
        print(f"{directory.name}: {'OK' if ok else 'FAILED'}")
        failures.extend(f"{directory.name}: {error}" for error in errors)
    database = Database(f"sqlite:///{ROOT / 'data' / 'governed_release.db'}")
    database.create()
    audit = AuditLedger(SQLAlchemyAuditStore(database), ROOT / "data" / "logs" / "audit.jsonl")
    audit_ok, audit_errors = audit.verify()
    print(f"audit hash chain: {'OK' if audit_ok else 'FAILED'}")
    failures.extend(audit_errors)
    print(f"Checked {checked} evidence bundles")
    if failures:
        print("\n".join(failures))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
