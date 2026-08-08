import json
from pathlib import Path

from northstar_compliance.knowledge.service import KnowledgePreparationService
from northstar_compliance.knowledge.validation import validate_prepared_corpus


def _write_fixture(root: Path, *, text: str = "# Policy\nRequired evidence.\n") -> Path:
    (root / "documents").mkdir(parents=True)
    (root / "documents" / "policy.md").write_text(text, encoding="utf-8")
    manifest = {
        "sources": [
            {
                "source_id": "POL-001",
                "title": "Policy",
                "source_type": "POLICY",
                "owner": "Owner",
                "relative_path": "documents/policy.md",
                "version_label": "1",
                "effective_from": "2026-01-01",
                "effective_to": None,
                "jurisdictions": ["CA"],
                "business_domains": ["LENDING"],
                "access": {
                    "classification": "INTERNAL",
                    "allowed_groups": ["COMPLIANCE_ANALYST"],
                    "residency": "CA",
                    "purpose": "REGULATORY_CHANGE_ANALYSIS",
                },
                "retention_class": "ACTIVE",
                "authoritative": True,
            }
        ]
    }
    path = root / "manifest.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    return path


def test_ingestion_is_idempotent(tmp_path: Path) -> None:
    input_root = tmp_path / "input"
    output = tmp_path / "output"
    manifest = _write_fixture(input_root)
    service = KnowledgePreparationService(input_root=input_root, output_root=output)
    first = service.prepare(manifest)
    second = service.prepare(manifest)
    assert first.items[0].action == "CREATED"
    assert second.items[0].action == "REUSED"
    assert first.items[0].source_version_id == second.items[0].source_version_id
    assert validate_prepared_corpus(output)["sources"] == 1


def test_content_change_creates_new_version(tmp_path: Path) -> None:
    input_root = tmp_path / "input"
    output = tmp_path / "output"
    manifest = _write_fixture(input_root)
    service = KnowledgePreparationService(input_root=input_root, output_root=output)
    first = service.prepare(manifest)
    (input_root / "documents" / "policy.md").write_text("# Policy\nChanged evidence.\n", encoding="utf-8")
    second = service.prepare(manifest)
    assert first.items[0].source_version_id != second.items[0].source_version_id
    corpus_manifest = json.loads((output / "corpus-manifest.json").read_text(encoding="utf-8"))
    assert corpus_manifest["version_count"] == 2
