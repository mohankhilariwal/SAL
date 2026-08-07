"""Executable Stage 0 tests."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from northstar_agentic_compliance.constitution import (  # noqa: E402
    REQUIRED_HANDOFF_HEADINGS,
    SOURCE_OF_TRUTH_DIRECTORY,
    SOURCE_OF_TRUTH_FILES,
)


class SourceOfTruthTests(unittest.TestCase):
    def test_001_all_ten_artefacts_exist(self) -> None:
        base = ROOT / SOURCE_OF_TRUTH_DIRECTORY
        self.assertEqual(10, len(SOURCE_OF_TRUTH_FILES))
        for name in SOURCE_OF_TRUTH_FILES:
            self.assertTrue((base / name).is_file(), name)

    def test_002_handoff_sections_exist(self) -> None:
        handoff = (ROOT / SOURCE_OF_TRUTH_DIRECTORY / "09-Stage-Handoff-Pack.md").read_text(
            encoding="utf-8"
        )
        for heading in REQUIRED_HANDOFF_HEADINGS:
            self.assertIn(heading, handoff)

    def test_003_validator_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_source_of_truth.py")],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("Stage 0 validation: PASSED", result.stdout)

    def test_004_stage_one_is_blocked_pending_acceptance(self) -> None:
        constitution = (ROOT / SOURCE_OF_TRUTH_DIRECTORY / "00-Project-Constitution.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Stage 1 must not begin", constitution)

    def test_005_no_agent_identifier_is_allocated(self) -> None:
        catalogue = (ROOT / SOURCE_OF_TRUTH_DIRECTORY / "04-Component-and-Agent-Catalogue.md").read_text(
            encoding="utf-8"
        )
        agent_section = catalogue.split("## 2. Agent inventory", 1)[1].split("## 3.", 1)[0]
        self.assertNotRegex(agent_section, r"\| AGT-\d{3} \|")


if __name__ == "__main__":
    unittest.main()
