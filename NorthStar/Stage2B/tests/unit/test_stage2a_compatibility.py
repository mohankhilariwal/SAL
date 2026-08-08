from hashlib import sha256
from pathlib import Path
import json
import pytest

from northstar_compliance.knowledge.parser import parse_document, resolve_bounded
from northstar_compliance.knowledge.validation import validate_prepared_corpus


def test_020_hashes_and_lines_preserved(stage):
    _,corpus,_,_,_,_=stage
    report=validate_prepared_corpus(corpus)
    assert report["passed"]
    for chunk in corpus.chunks:
        assert sha256(chunk.text.encode()).hexdigest()==chunk.text_sha256


def test_021_rejects_unsupported_and_nul(tmp_path):
    (tmp_path/"bad.bin").write_bytes(b"x")
    with pytest.raises(ValueError): parse_document(tmp_path,"bad.bin")
    (tmp_path/"bad.txt").write_bytes(b"a\x00b")
    with pytest.raises(ValueError): parse_document(tmp_path,"bad.txt")


def test_022_path_traversal_rejected(tmp_path):
    with pytest.raises(ValueError): resolve_bounded(tmp_path,"../escape.txt")


def test_023_deterministic_chunk_ids(stage,tmp_path):
    root,corpus,_,_,_,_=stage
    from northstar_compliance.knowledge.service import KnowledgePreparationService
    from northstar_compliance.knowledge.corpus import load_prepared_corpus
    out=tmp_path/"again"
    KnowledgePreparationService().prepare(root/"datasets/stage2a/input/manifest.json",root/"datasets/stage2a/input",out)
    again=load_prepared_corpus(out)
    assert [c.chunk_id for c in corpus.chunks]==[c.chunk_id for c in again.chunks]


def test_024_chunks_do_not_cross_sections(stage):
    _,corpus,_,_,_,_=stage
    assert all(c.heading_path for c in corpus.chunks)


def test_025_access_propagated(stage):
    _,corpus,_,_,_,_=stage
    assert all(c.access.allowed_groups for c in corpus.chunks)
