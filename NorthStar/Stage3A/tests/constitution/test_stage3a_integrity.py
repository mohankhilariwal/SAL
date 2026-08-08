from __future__ import annotations

import json
import re
from pathlib import Path


def test_source_of_truth_pack_and_versions(repo_root: Path):
    truth = repo_root / "docs" / "source-of-truth"
    expected = [
        "00-Project-Constitution.md", "01-Business-and-User-Story-Baseline.md",
        "02-Requirements-Register.md", "03-Architecture-Baseline.md",
        "04-Component-and-Agent-Catalogue.md", "05-Data-and-Schema-Register.md",
        "06-ADR-Register.md", "07-Repository-Manifest.md",
        "08-Risk-Assumption-and-Issue-Register.md", "09-Stage-Handoff-Pack.md",
    ]
    for name in expected:
        text = (truth / name).read_text(encoding="utf-8")
        assert "0.5.0" in text


def test_catalogue_descriptor_ids_and_names_match(repo_root: Path):
    catalogue = (repo_root / "docs/source-of-truth/04-Component-and-Agent-Catalogue.md").read_text()
    descriptors = []
    for path in sorted((repo_root / "config/tools").glob("TOOL-*.json")):
        raw = json.loads(path.read_text())
        descriptors.append(raw)
        assert raw["tool_id"] in catalogue
        assert raw["name"] in catalogue
    assert len(descriptors) == 6


def test_no_numbered_agent_or_later_stage_code(repo_root: Path):
    current = "\n".join(
        p.read_text(encoding="utf-8", errors="ignore")
        for base in [repo_root / "src", repo_root / "config", repo_root / "docs/source-of-truth", repo_root / "docs/stages"]
        for p in base.rglob("*") if p.is_file()
    )
    assert re.search(r"\bAGT-\d{3}\b", current) is None
    assert "langgraph" not in current.casefold()
    assert "crewai" not in current.casefold()


def test_handoff_authorizes_only_stage3b(repo_root: Path):
    handoff = (repo_root / "docs/source-of-truth/09-Stage-Handoff-Pack.md").read_text()
    assert "Stage 3B — Bounded Single-Agent Loop" in handoff
    assert "Stage 4" not in handoff
