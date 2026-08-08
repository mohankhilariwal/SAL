import json
from pathlib import Path

from northstar_compliance.knowledge.service import KnowledgePreparationService


def test_fixture_corpus_has_exact_coordinates_and_access_propagation(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    input_root = project_root / "datasets" / "stage2a" / "input"
    output = tmp_path / "prepared"
    service = KnowledgePreparationService(input_root=input_root, output_root=output)
    run = service.prepare(input_root / "manifest.json")
    assert len(run.items) == 5
    assert sum(item.chunk_count for item in run.items) >= 5

    manifest = json.loads((output / "corpus-manifest.json").read_text(encoding="utf-8"))
    for source_id, version_id in manifest["active_versions"].items():
        root = output / "corpus" / source_id / version_id
        descriptor = json.loads((root / "descriptor.json").read_text(encoding="utf-8"))
        normalized_lines = (root / "normalized.txt").read_text(encoding="utf-8").splitlines()
        with (root / "chunks.jsonl").open(encoding="utf-8") as handle:
            chunks = [json.loads(line) for line in handle]
        covered = set()
        for chunk in chunks:
            covered.update(range(chunk["line_start"], chunk["line_end"] + 1))
            expected = "\n".join(normalized_lines[chunk["line_start"] - 1 : chunk["line_end"]])
            assert expected == chunk["text"]
            assert chunk["access"] == descriptor["access"]
        assert covered == set(range(1, len(normalized_lines) + 1))
