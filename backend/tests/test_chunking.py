import pytest
import tiktoken

from agentic_rag.ingestion.chunking import chunk_document
from agentic_rag.models.rag import DocumentSource, SourceType


def make_source(source_type: SourceType = SourceType.text) -> DocumentSource:
    return DocumentSource(
        source_id="doc_test",
        title="Test Doc",
        source_type=source_type,
        uri="file:///tmp/test.txt",
        metadata={"content_hash": "abc123", "source_path": "/tmp/test.txt"},
    )


def token_count(text: str) -> int:
    return len(tiktoken.get_encoding("cl100k_base").encode(text))


def test_empty_document_produces_no_chunks():
    assert chunk_document(make_source(), "   \n\t") == []


def test_short_document_produces_one_chunk_with_lineage():
    source = make_source()

    chunks = chunk_document(
        source,
        "RAG retrieves evidence.",
        chunk_size_tokens=20,
        overlap_tokens=0,
    )

    assert len(chunks) == 1
    assert chunks[0].source_id == source.source_id
    assert chunks[0].chunk_index == 0
    assert chunks[0].text == "RAG retrieves evidence."
    assert chunks[0].metadata["title"] == "Test Doc"
    assert chunks[0].metadata["source_path"] == "/tmp/test.txt"
    assert chunks[0].metadata["token_start"] == 0
    assert chunks[0].metadata["token_count"] == token_count(chunks[0].text)


def test_long_document_produces_token_limited_overlapping_chunks():
    text = " ".join(f"word{i}" for i in range(80))

    chunks = chunk_document(
        make_source(),
        text,
        chunk_size_tokens=20,
        overlap_tokens=5,
    )

    assert len(chunks) > 1
    assert all(token_count(chunk.text) <= 20 for chunk in chunks)
    assert chunks[1].metadata["token_start"] == 15
    assert chunks[1].metadata["token_start"] < chunks[0].metadata["token_end"]


def test_chunk_ids_are_stable_for_same_source_and_text():
    source = make_source()
    text = " ".join(f"stable{i}" for i in range(50))

    first = chunk_document(source, text, chunk_size_tokens=20, overlap_tokens=5)
    second = chunk_document(source, text, chunk_size_tokens=20, overlap_tokens=5)

    assert [chunk.chunk_id for chunk in first] == [chunk.chunk_id for chunk in second]


def test_invalid_overlap_must_be_smaller_than_chunk_size():
    with pytest.raises(ValueError, match="overlap_tokens must be smaller"):
        chunk_document(
            make_source(),
            "RAG retrieves evidence.",
            chunk_size_tokens=20,
            overlap_tokens=20,
        )


def test_markdown_source_preserves_source_type_in_metadata():
    chunks = chunk_document(
        make_source(SourceType.markdown),
        "# Heading\n\nMarkdown content.",
        chunk_size_tokens=20,
        overlap_tokens=0,
    )

    assert chunks[0].metadata["source_type"] == "markdown"
