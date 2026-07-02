import json
from pathlib import Path

from sqlalchemy import inspect, text

from agentic_rag.models.rag import DocumentChunk, DocumentSource, SourceType
from agentic_rag.storage.sqlite import SQLiteMetadataStore, sources_table


def make_source(source_id: str = "doc_1") -> DocumentSource:
    return DocumentSource(
        source_id=source_id,
        title="RAG Notes",
        source_type=SourceType.markdown,
        uri="file:///tmp/rag-notes.md",
        metadata={
            "content_hash": "abc123",
            "source_path": "/tmp/rag-notes.md",
        },
    )


def make_chunk(
    chunk_id: str = "chunk_1",
    source_id: str = "doc_1",
    chunk_index: int = 0,
) -> DocumentChunk:
    return DocumentChunk(
        chunk_id=chunk_id,
        source_id=source_id,
        text=f"chunk text {chunk_index}",
        chunk_index=chunk_index,
        metadata={"token_start": chunk_index * 10, "token_end": chunk_index * 10 + 10},
    )


def test_initialize_creates_sources_and_chunks_tables(tmp_path: Path):
    db_path = tmp_path / "rag.db"
    store = SQLiteMetadataStore(db_path)

    store.initialize()

    tables = set(inspect(store.engine).get_table_names())

    assert {"sources", "chunks"}.issubset(tables)


def test_store_exposes_sqlalchemy_table_metadata():
    assert sources_table.name == "sources"
    assert sources_table.c.source_id.primary_key


def test_upsert_source_persists_source_metadata(tmp_path: Path):
    db_path = tmp_path / "rag.db"
    store = SQLiteMetadataStore(db_path)
    store.initialize()
    source = make_source()

    store.upsert_source(source)

    with store.engine.connect() as connection:
        row = connection.execute(
            text(
                """
                SELECT source_id, title, source_type, uri, metadata_json
                FROM sources
                WHERE source_id = :source_id
                """
            ),
            {"source_id": source.source_id},
        ).fetchone()

    assert row[:4] == (
        "doc_1",
        "RAG Notes",
        "markdown",
        "file:///tmp/rag-notes.md",
    )
    assert json.loads(row[4]) == source.metadata


def test_upserting_same_source_updates_without_duplicate(tmp_path: Path):
    db_path = tmp_path / "rag.db"
    store = SQLiteMetadataStore(db_path)
    store.initialize()
    store.upsert_source(make_source())

    updated = make_source()
    updated.title = "Updated RAG Notes"
    store.upsert_source(updated)

    with store.engine.connect() as connection:
        rows = connection.execute(text("SELECT title FROM sources")).fetchall()

    assert rows == [("Updated RAG Notes",)]


def test_replace_chunks_persists_chunks_for_source(tmp_path: Path):
    db_path = tmp_path / "rag.db"
    store = SQLiteMetadataStore(db_path)
    store.initialize()
    source = make_source()
    chunks = [make_chunk("chunk_1", chunk_index=0), make_chunk("chunk_2", chunk_index=1)]

    store.upsert_source(source)
    store.replace_chunks(source.source_id, chunks)

    with store.engine.connect() as connection:
        rows = connection.execute(
            text(
                """
                SELECT chunk_id, source_id, chunk_index, text, metadata_json
                FROM chunks
                ORDER BY chunk_index
                """
            )
        ).fetchall()

    assert [(row[0], row[1], row[2], row[3]) for row in rows] == [
        ("chunk_1", "doc_1", 0, "chunk text 0"),
        ("chunk_2", "doc_1", 1, "chunk text 1"),
    ]
    assert json.loads(rows[0][4]) == {"token_start": 0, "token_end": 10}


def test_replace_chunks_removes_old_chunks_for_source_only(tmp_path: Path):
    db_path = tmp_path / "rag.db"
    store = SQLiteMetadataStore(db_path)
    store.initialize()
    store.upsert_source(make_source("doc_1"))
    store.upsert_source(make_source("doc_2"))
    store.replace_chunks("doc_1", [make_chunk("old_chunk", "doc_1", 0)])
    store.replace_chunks("doc_2", [make_chunk("other_chunk", "doc_2", 0)])

    store.replace_chunks("doc_1", [make_chunk("new_chunk", "doc_1", 0)])

    with store.engine.connect() as connection:
        rows = connection.execute(
            text("SELECT chunk_id, source_id FROM chunks ORDER BY source_id")
        ).fetchall()

    assert rows == [("new_chunk", "doc_1"), ("other_chunk", "doc_2")]


def test_counts_returns_document_and_chunk_totals(tmp_path: Path):
    db_path = tmp_path / "rag.db"
    store = SQLiteMetadataStore(db_path)
    store.initialize()
    source = make_source()

    store.upsert_source(source)
    store.replace_chunks(
        source.source_id,
        [make_chunk("chunk_1", chunk_index=0), make_chunk("chunk_2", chunk_index=1)],
    )

    assert store.counts() == {"documents": 1, "chunks": 2}
