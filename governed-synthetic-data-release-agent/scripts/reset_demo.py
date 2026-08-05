from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def clean_directory(path: Path) -> None:
    if not path.exists():
        return
    for child in path.iterdir():
        if child.name == ".gitkeep":
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def main() -> None:
    database = ROOT / "data" / "governed_release.db"
    if database.exists():
        database.unlink()
    for relative in [
        "candidate",
        "quarantine",
        "evidence",
        "logs",
        "released/internal_sandbox",
        "released/named_external_partner",
    ]:
        clean_directory(ROOT / "data" / relative)
    subprocess.run([sys.executable, str(ROOT / "scripts" / "bootstrap.py")], check=True, cwd=ROOT)
    subprocess.run([sys.executable, str(ROOT / "scripts" / "seed_demo.py")], check=True, cwd=ROOT)
    print("Demo reset complete.")


if __name__ == "__main__":
    main()
