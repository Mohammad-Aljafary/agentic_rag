from pathlib import Path

from agentic_rag.ingestion.files import (
    discover_ingestable_files,
    read_local_document,
)
from agentic_rag.models.rag import SourceType


def test_discovers_txt_and_markdown_files_in_stable_path_order(tmp_path: Path):
    docs = tmp_path / "docs"
    nested = docs / "nested"
    nested.mkdir(parents=True)
    zebra = docs / "zebra.md"
    alpha = docs / "alpha.txt"
    beta = nested / "beta.md"
    ignored = docs / "ignore.pdf"

    zebra.write_text("zebra", encoding="utf-8")
    alpha.write_text("alpha", encoding="utf-8")
    beta.write_text("beta", encoding="utf-8")
    ignored.write_text("ignore", encoding="utf-8")

    assert discover_ingestable_files(docs) == [
        alpha,
        beta,
        zebra,
    ]


def test_discovers_supported_single_file(tmp_path: Path):
    document = tmp_path / "README.MD"
    document.write_text("# Read me", encoding="utf-8")

    assert discover_ingestable_files(document) == [document]


def test_skips_unsupported_single_file(tmp_path: Path):
    document = tmp_path / "data.csv"
    document.write_text("not supported yet", encoding="utf-8")

    assert discover_ingestable_files(document) == []


def test_read_local_document_builds_stable_source_metadata(tmp_path: Path):
    document = tmp_path / "rag-notes.md"
    document.write_text("# RAG Notes\n\nRAG retrieves evidence.", encoding="utf-8")

    source, text = read_local_document(document)

    assert text == "# RAG Notes\n\nRAG retrieves evidence."
    assert source.source_id.startswith("doc_")
    assert source.title == "rag-notes"
    assert source.source_type == SourceType.markdown
    assert source.uri == str(document.resolve())
    assert source.metadata["source_path"] == str(document.resolve())
    assert len(source.metadata["content_hash"]) == 64
    assert source.metadata["file_size"] == document.stat().st_size
    assert "modified_at" in source.metadata


def test_read_local_document_hash_is_stable_for_same_content(tmp_path: Path):
    first = tmp_path / "first.txt"
    second = tmp_path / "second.txt"
    first.write_text("same content", encoding="utf-8")
    second.write_text("same content", encoding="utf-8")

    first_source, _ = read_local_document(first)
    second_source, _ = read_local_document(second)

    assert first_source.metadata["content_hash"] == second_source.metadata["content_hash"]
    assert first_source.source_id == second_source.source_id
    assert first_source.source_type == SourceType.text
