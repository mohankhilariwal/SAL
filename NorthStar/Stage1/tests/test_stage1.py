from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from northstar_compliance.artifact_store import LocalArtifactStore
from northstar_compliance.intake import IntakeError, ingest_publication
from northstar_compliance.mock_model import DeterministicMockSummaryModel
from northstar_compliance.model_gateway import ModelResult
from northstar_compliance.service import run_summary
from northstar_compliance.validation import SummaryValidationError, build_validated_summary

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "datasets/stage1/sample-publication.txt"
ADVERSARIAL = ROOT / "datasets/stage1/adversarial-publication.txt"


def ingest(path: Path):
    return ingest_publication(
        path,
        title="Synthetic Notice",
        source_uri="synthetic://notice",
        jurisdiction="CA",
    )


class Stage1Tests(unittest.TestCase):
    def test_008_intake_preserves_hash_and_lines(self):
        pub = ingest(SAMPLE)
        self.assertEqual(pub.metadata.sha256, hashlib.sha256(SAMPLE.read_bytes()).hexdigest())
        self.assertEqual(pub.metadata.line_count, len(SAMPLE.read_text().splitlines()))

    def test_009_rejects_unsupported_extension(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "notice.pdf"
            path.write_bytes(b"not-a-pdf")
            with self.assertRaises(IntakeError):
                ingest(path)

    def test_010_rejects_empty_input(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "notice.txt"
            path.write_text("")
            with self.assertRaises(IntakeError):
                ingest(path)

    def test_011_rejects_size_excess(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "notice.txt"
            path.write_text("x" * 20)
            with self.assertRaises(IntakeError):
                ingest_publication(path, title="x", source_uri="x", jurisdiction="CA", max_bytes=10)

    def test_012_mock_pipeline_is_preliminary_and_human_reviewed(self):
        pub = ingest(SAMPLE)
        with tempfile.TemporaryDirectory() as td:
            result = run_summary(pub, model=DeterministicMockSummaryModel(), store=LocalArtifactStore(Path(td)))
            self.assertEqual(result.summary.disposition, "preliminary_unapproved")
            self.assertTrue(result.summary.human_review_required)
            self.assertEqual(result.summary.approval_status, "not_requested")
            self.assertEqual(result.summary.legal_conclusion, "not_provided")

    def test_013_every_fact_has_exact_valid_evidence(self):
        pub = ingest(SAMPLE)
        payload = DeterministicMockSummaryModel().summarize(pub).payload
        summary = build_validated_summary(pub, payload)
        self.assertGreaterEqual(len(summary.source_facts), 4)
        for claim in summary.source_facts:
            self.assertEqual(claim.evidence[0].source_sha256, pub.metadata.sha256)
            self.assertIn(claim.evidence[0].excerpt, pub.lines[claim.evidence[0].line_start - 1])

    def test_014_fabricated_line_is_rejected(self):
        pub = ingest(SAMPLE)
        payload = DeterministicMockSummaryModel().summarize(pub).payload
        payload["source_facts"][0]["line_start"] = 999
        payload["source_facts"][0]["line_end"] = 999
        with self.assertRaises(SummaryValidationError):
            build_validated_summary(pub, payload)

    def test_015_artifacts_are_persisted(self):
        pub = ingest(SAMPLE)
        with tempfile.TemporaryDirectory() as td:
            result = run_summary(pub, model=DeterministicMockSummaryModel(), store=LocalArtifactStore(Path(td)))
            self.assertEqual({p.name for p in result.artifact_path.iterdir()}, {"source.txt", "metadata.json", "summary.json", "model-invocation.json"})
            saved = json.loads((result.artifact_path / "summary.json").read_text())
            self.assertEqual(saved["disposition"], "preliminary_unapproved")

    def test_016_injected_document_cannot_set_approval(self):
        pub = ingest(ADVERSARIAL)
        with tempfile.TemporaryDirectory() as td:
            result = run_summary(pub, model=DeterministicMockSummaryModel(), store=LocalArtifactStore(Path(td)))
            self.assertEqual(result.summary.disposition, "preliminary_unapproved")
            self.assertEqual(result.summary.approval_status, "not_requested")
            self.assertTrue(result.summary.human_review_required)

    def test_017_model_cannot_override_application_status(self):
        pub = ingest(SAMPLE)
        payload = DeterministicMockSummaryModel().summarize(pub).payload
        payload.update({"disposition": "approved", "human_review_required": False})
        summary = build_validated_summary(pub, payload)
        self.assertEqual(summary.disposition, "preliminary_unapproved")
        self.assertTrue(summary.human_review_required)

    def test_018_no_agent_or_tool_identifier_allocated(self):
        pattern_hits = []
        import re
        pattern = re.compile(r"\b(?:AGT|TOOL)-\d{3}\b")
        for path in ROOT.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".py", ".mmd", ".txt"}:
                pattern_hits.extend(pattern.findall(path.read_text(errors="ignore")))
        self.assertEqual(pattern_hits, [])

    def test_019_no_retrieval_or_action_method_in_model_protocol(self):
        text = (ROOT / "src/northstar_compliance/model_gateway.py").read_text()
        self.assertNotIn("retrieve(", text)
        self.assertNotIn("execute_tool", text)


if __name__ == "__main__":
    unittest.main()
