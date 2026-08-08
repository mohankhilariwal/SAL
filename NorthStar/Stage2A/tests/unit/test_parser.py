from pathlib import Path

import pytest

from northstar_compliance.knowledge.parser import parse_text_document, resolve_bounded_path
from northstar_compliance.knowledge.schemas import KnowledgeError


def test_parser_preserves_line_coordinates_and_hashes(tmp_path: Path) -> None:
    path = tmp_path / "sample.md"
    path.write_bytes(b"# Heading\r\nLine two\r\n")
    parsed = parse_text_document(path)
    assert parsed.lines == ("# Heading", "Line two")
    assert parsed.normalized_text == "# Heading\nLine two\n"
    assert len(parsed.raw_sha256) == 64
    assert len(parsed.normalized_sha256) == 64


def test_parser_rejects_binary_nul_and_non_utf8(tmp_path: Path) -> None:
    nul = tmp_path / "nul.txt"
    nul.write_bytes(b"abc\x00def")
    with pytest.raises(KnowledgeError, match="NUL"):
        parse_text_document(nul)

    bad = tmp_path / "bad.md"
    bad.write_bytes(b"\xff\xfe")
    with pytest.raises(KnowledgeError, match="UTF-8"):
        parse_text_document(bad)


def test_parser_rejects_unsupported_and_oversized(tmp_path: Path) -> None:
    pdf = tmp_path / "file.pdf"
    pdf.write_bytes(b"not a pdf")
    with pytest.raises(KnowledgeError, match="unsupported"):
        parse_text_document(pdf)

    huge = tmp_path / "huge.txt"
    huge.write_text("x" * 20, encoding="utf-8")
    with pytest.raises(KnowledgeError, match="max_bytes"):
        parse_text_document(huge, max_bytes=10)


def test_resolve_bounded_path_rejects_escape(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    with pytest.raises(KnowledgeError, match="escapes"):
        resolve_bounded_path(root, "../outside.txt")
