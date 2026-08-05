from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from governed_release.adapters.local_files.source_data import generate_maplebridge_source
from governed_release.adapters.persistence.repository import Database
from governed_release.config.settings import Settings


def main() -> None:
    settings = Settings(
        data_dir=ROOT / "data", database_url=f"sqlite:///{ROOT / 'data' / 'governed_release.db'}"
    )
    settings.ensure_directories()
    migrated = subprocess.run(
        [sys.executable, "-m", "alembic", "-c", str(ROOT / "alembic.ini"), "upgrade", "head"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if migrated.returncode != 0:
        # A prior direct SQLAlchemy bootstrap may have created the same schema without
        # Alembic's version marker. Stamp that existing schema, then continue normally.
        if "already exists" in migrated.stderr.lower():
            stamped = subprocess.run(
                [sys.executable, "-m", "alembic", "-c", str(ROOT / "alembic.ini"), "stamp", "head"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            if stamped.returncode != 0:
                raise RuntimeError(f"Could not stamp existing database: {stamped.stderr.strip()}")
            print("Existing compatible schema recorded in Alembic version history.")
        else:
            Database(settings.database_url).create()
            print("Alembic unavailable; SQLAlchemy schema bootstrap used.")
    if not settings.source_path.exists():
        data = generate_maplebridge_source(settings.source_path)
        print(f"Generated fictional source data: {settings.source_path} ({len(data)} rows)")
    else:
        print(f"Source data already exists: {settings.source_path}")
    print("Bootstrap complete.")


if __name__ == "__main__":
    main()
