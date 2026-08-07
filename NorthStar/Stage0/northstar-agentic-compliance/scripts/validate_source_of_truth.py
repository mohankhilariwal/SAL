#!/usr/bin/env python3
"""Validate the Stage 0 source-of-truth pack using only the standard library."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from northstar_agentic_compliance.constitution import (  # noqa: E402
    IDENTIFIER_PATTERN,
    REQUIRED_HANDOFF_HEADINGS,
    REQUIRED_STAGE_HEADINGS,
    SOURCE_OF_TRUTH_DIRECTORY,
    SOURCE_OF_TRUTH_FILES,
)

ID_RE = re.compile(IDENTIFIER_PATTERN)

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_required_files(errors: list[str]) -> list[Path]:
    base = ROOT / SOURCE_OF_TRUTH_DIRECTORY
    paths = [base / name for name in SOURCE_OF_TRUTH_FILES]
    for path in paths:
        if not path.is_file():
            errors.append(f"Missing required artefact: {path.relative_to(ROOT)}")
    return paths


def check_headings(errors: list[str]) -> None:
    handoff = read(ROOT / SOURCE_OF_TRUTH_DIRECTORY / "09-Stage-Handoff-Pack.md")
    for heading in REQUIRED_HANDOFF_HEADINGS:
        if heading not in handoff:
            errors.append(f"Missing handoff heading: {heading}")

    stage = read(ROOT / "docs/stages/Stage-0-Playbook-Foundation-and-Architecture-Constitution.md")
    for heading_prefix in REQUIRED_STAGE_HEADINGS:
        if heading_prefix not in stage:
            errors.append(f"Missing Stage 0 section prefix: {heading_prefix}")


def check_identifier_formats(paths: list[Path], errors: list[str]) -> None:
    malformed = re.compile(
        r"\b(?:AP|SG|BSC|US|FR|NFR|CMP|AGT|TOOL|DATA|INT|POL|RSK|CTL|EVAL|ADR|TEST|ASM|ISS)-\d{1,2}(?!\d)"
    )
    for path in paths:
        text = read(path)
        for match in malformed.finditer(text):
            errors.append(f"Malformed identifier {match.group(0)} in {path.relative_to(ROOT)}")


def check_conflicting_definitions(paths: list[Path], errors: list[str]) -> None:
    """Check canonical definition locations rather than every reference table."""
    catalogue = read(ROOT / SOURCE_OF_TRUTH_DIRECTORY / "04-Component-and-Agent-Catalogue.md")
    adr_register = read(ROOT / SOURCE_OF_TRUTH_DIRECTORY / "06-ADR-Register.md")
    data_register = read(ROOT / SOURCE_OF_TRUTH_DIRECTORY / "05-Data-and-Schema-Register.md")

    component_section = catalogue.split("## 1. Component catalogue", 1)[1].split("## 2.", 1)[0]
    interface_section = catalogue.split("## 4. Interface inventory", 1)[1].split("## 5.", 1)[0]
    data_section = data_register.split("## 2. Data object register", 1)[1].split("## 3.", 1)[0]

    definition_sets = {
        "CMP": re.findall(r"^\| (CMP-\d{3}) \| ([^|]+) \|", component_section, re.MULTILINE),
        "ADR": re.findall(r"^## (ADR-\d{3}) - (.+)$", adr_register, re.MULTILINE),
        "DATA": re.findall(r"^\| (DATA-\d{3}) \| ([^|]+) \|", data_section, re.MULTILINE),
        "INT": re.findall(r"^\| (INT-\d{3}) \| ([^|]+) \|", interface_section, re.MULTILINE),
    }

    for kind, pairs in definition_sets.items():
        seen: dict[str, str] = {}
        for identifier, name in pairs:
            normalized = " ".join(name.strip().split())
            previous = seen.get(identifier)
            if previous is not None and previous != normalized:
                errors.append(
                    f"Conflicting canonical definitions for {identifier}: {previous!r} vs {normalized!r}"
                )
            seen[identifier] = normalized


def check_component_references(errors: list[str]) -> None:
    architecture = read(ROOT / SOURCE_OF_TRUTH_DIRECTORY / "03-Architecture-Baseline.md")
    catalogue = read(ROOT / SOURCE_OF_TRUTH_DIRECTORY / "04-Component-and-Agent-Catalogue.md")
    architecture_ids = set(re.findall(r"CMP-\d{3}", architecture))
    catalogue_ids = set(re.findall(r"^\| (CMP-\d{3}) \|", catalogue, re.MULTILINE))
    missing = sorted(architecture_ids - catalogue_ids)
    if missing:
        errors.append(f"Architecture references uncatalogued components: {missing}")


def check_no_implemented_agent(errors: list[str]) -> None:
    catalogue = read(ROOT / SOURCE_OF_TRUTH_DIRECTORY / "04-Component-and-Agent-Catalogue.md")
    agent_section = catalogue.split("## 2. Agent inventory", 1)[1].split("## 3.", 1)[0]
    if re.search(r"\| AGT-\d{3} \|", agent_section):
        errors.append("Stage 0 must not allocate or implement an agent identifier")
    if "No agent is accepted or implemented in Stage 0" not in agent_section:
        errors.append("Agent inventory does not explicitly preserve the Stage 0 no-agent invariant")


def check_manifest_paths(errors: list[str]) -> None:
    required = [
        "README.md",
        "pyproject.toml",
        ".env.example",
        "docs/stages/Stage-0-Playbook-Foundation-and-Architecture-Constitution.md",
        "scripts/validate_source_of_truth.py",
        "src/northstar_agentic_compliance/constitution.py",
        "tests/unit/test_source_of_truth.py",
    ]
    required.extend(str(SOURCE_OF_TRUTH_DIRECTORY / name) for name in SOURCE_OF_TRUTH_FILES)
    for relative in required:
        if not (ROOT / relative).exists():
            errors.append(f"Manifest-required path missing: {relative}")


def check_mermaid_structure(paths: list[Path], errors: list[str]) -> None:
    for path in paths + [ROOT / "docs/stages/Stage-0-Playbook-Foundation-and-Architecture-Constitution.md"]:
        text = read(path)
        starts = [m.start() for m in re.finditer(r"```mermaid\n", text)]
        if not starts:
            continue
        if text.count("```mermaid") > text.count("```"):
            errors.append(f"Unclosed Mermaid fence in {path.relative_to(ROOT)}")
        for block in re.findall(r"```mermaid\n(.*?)```", text, re.DOTALL):
            first = next((line.strip() for line in block.splitlines() if line.strip()), "")
            if not re.match(r"^(flowchart|graph|sequenceDiagram|stateDiagram(?:-v2)?|classDiagram|erDiagram|journey|gantt|pie|mindmap)\b", first):
                errors.append(
                    f"Unrecognized Mermaid declaration '{first}' in {path.relative_to(ROOT)}"
                )


def main() -> int:
    errors: list[str] = []
    paths = check_required_files(errors)
    if not errors:
        check_headings(errors)
        check_identifier_formats(paths, errors)
        check_conflicting_definitions(paths, errors)
        check_component_references(errors)
        check_no_implemented_agent(errors)
        check_manifest_paths(errors)
        check_mermaid_structure(paths, errors)

    if errors:
        print("Stage 0 validation: FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    identifier_count = sum(len(ID_RE.findall(read(path))) for path in paths)
    print("Stage 0 validation: PASSED")
    print(f"- Required artefacts: {len(paths)}")
    print(f"- Identifier references checked: {identifier_count}")
    print("- Component catalogue references: consistent")
    print("- Agent inventory: intentionally empty")
    print("- Repository manifest paths: present")
    print("- Mermaid validation: structural only (renderer not configured)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
