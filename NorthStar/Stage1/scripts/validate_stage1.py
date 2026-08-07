from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> None:
    print("+", " ".join(args))
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(ROOT / "src") + (os.pathsep + existing if existing else "")
    subprocess.run(args, cwd=ROOT, env=env, check=True)


def main() -> int:
    run(sys.executable, "scripts/validate_source_of_truth.py")
    run(sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v")
    run(sys.executable, "-m", "compileall", "-q", "src", "scripts", "tests")
    with tempfile.TemporaryDirectory() as td:
        env = os.environ.copy()
        existing = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = str(ROOT / "src") + (os.pathsep + existing if existing else "")
        proc = subprocess.run(
            [sys.executable, "-m", "northstar_compliance.cli", "--provider", "mock",
             "--input", "datasets/stage1/sample-publication.txt", "--title", "Synthetic Notice",
             "--source-uri", "synthetic://notice", "--jurisdiction", "CA", "--output-dir", td],
            cwd=ROOT, env=env, check=True, text=True, capture_output=True,
        )
        result = json.loads(proc.stdout)
        assert result["disposition"] == "preliminary_unapproved"
        assert result["human_review_required"] is True
    print("Stage 1 validation: PASSED WITH RECORDED EXCEPTIONS (Python 3.12 and live provider not executed; Mermaid statically checked only)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
