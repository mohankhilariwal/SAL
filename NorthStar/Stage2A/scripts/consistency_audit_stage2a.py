from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOT = ROOT / "docs" / "source-of-truth"
REQUIRED_SOT = [
    "00-Project-Constitution.md",
    "01-Business-and-User-Story-Baseline.md",
    "02-Requirements-Register.md",
    "03-Architecture-Baseline.md",
    "04-Component-and-Agent-Catalogue.md",
    "05-Data-and-Schema-Register.md",
    "06-ADR-Register.md",
    "07-Repository-Manifest.md",
    "08-Risk-Assumption-and-Issue-Register.md",
    "09-Stage-Handoff-Pack.md",
]


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> int:
    checks: list[str] = []

    for name in REQUIRED_SOT:
        if not (SOT / name).is_file():
            fail(f"missing source-of-truth file: {name}")
    checks.append("ten_source_of_truth_files")

    catalogue = (SOT / "04-Component-and-Agent-Catalogue.md").read_text(encoding="utf-8")
    component_ids = set(re.findall(r"CMP-\d{3}", catalogue))
    expected = {f"CMP-{i:03d}" for i in range(1, 12)}
    if component_ids != expected:
        fail(f"component inventory mismatch: {sorted(component_ids)}")
    checks.append("component_ids_preserved")

    source_files = list((ROOT / "src").rglob("*.py")) + [path for path in (ROOT / "scripts").glob("*.py") if path.name != Path(__file__).name]
    source_text = "\n".join(path.read_text(encoding="utf-8") for path in source_files)
    forbidden_symbols = ["class Agent", "def search(", "def retrieve(", "tool_registry", "vector_index", "embedding_model"]
    hits = [symbol for symbol in forbidden_symbols if symbol in source_text]
    if hits:
        fail(f"future-stage implementation symbol(s) found: {hits}")
    checks.append("no_agent_tool_search_contract")

    data_register = (SOT / "05-Data-and-Schema-Register.md").read_text(encoding="utf-8")
    for i in range(19, 26):
        if f"DATA-{i:03d}" not in data_register:
            fail(f"missing DATA-{i:03d}")
    for i in range(9, 12):
        if f"INT-{i:03d}" not in data_register:
            fail(f"missing INT-{i:03d}")
    checks.append("data_and_interface_ids")

    for diagram in (ROOT / "docs" / "architecture" / "diagrams").glob("*.mmd"):
        text = diagram.read_text(encoding="utf-8").strip()
        if not re.match(r"^(flowchart|sequenceDiagram|stateDiagram|graph)\b", text):
            fail(f"unknown Mermaid declaration: {diagram.name}")
        if text.count("[") != text.count("]"):
            fail(f"unbalanced square brackets: {diagram.name}")
    checks.append("mermaid_static_structure")

    manifest = json.loads((ROOT / "examples" / "stage2a-output" / "corpus-manifest.json").read_text(encoding="utf-8"))
    if manifest["source_count"] != 5 or manifest["active_chunk_count"] != 21:
        fail("unexpected prepared sample corpus counts")
    checks.append("prepared_corpus_counts")

    completed = subprocess.run(
        [sys.executable, "-m", "compileall", "-q", "src", "scripts", "tests"],
        cwd=ROOT,
        check=False,
    )
    if completed.returncode != 0:
        fail("Python compilation failed")
    checks.append("python_compilation")

    report = {
        "result": "PASSED_WITH_RECORDED_EXCEPTIONS",
        "checks": checks,
        "exceptions": ["ISS-009", "ISS-014", "ISS-015"],
    }
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
