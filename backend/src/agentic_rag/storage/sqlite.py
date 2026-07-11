"""SQLite-backed metadata store for sources, chunks, ingestion runs, and answers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    JSON,
    MetaData,
    String,
    Table,
    Text,
    create_engine,
    func,
    select,
)
from sqlalchemy.dialects.sqlite import insert as sqlite_insert

from agentic_rag.models.rag import DocumentChunk, DocumentSource

metadata = MetaData()

sources = Table(
    "sources",
    metadata,
    Column("source_id", String, primary_key=True),
    Column("title", String),
    Column("source_type", String),
    Column("uri", String),
    Column("metadata_json", JSON),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, server_default=func.now(), onupdate=func.now()),
)

chunks = Table(
    "chunks",
    metadata,
    Column("chunk_id", String, primary_key=True),
    Column("source_id", String, ForeignKey("sources.source_id"), index=True),
    Column("text", Text),
    Column("chunk_index", Integer),
    Column("metadata_json", JSON),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, server_default=func.now(), onupdate=func.now()),
)

Index("ix_chunks_source_chunk", chunks.c.source_id, chunks.c.chunk_index)

ingestion_runs = Table(
    "ingestion_runs",
    metadata,
    Column("run_id", String, primary_key=True),
    Column("source_id", String, ForeignKey("sources.source_id"), index=True),
    Column("status", String),
    Column("chunks_count", Integer),
    Column("error_message", Text, nullable=True),
    Column("started_at", DateTime, server_default=func.now()),
    Column("completed_at", DateTime, nullable=True),
)

answers = Table(
    "answers",
    metadata,
    Column("answer_id", String, primary_key=True),
    Column("query", Text),
    Column("answer_text", Text),
    Column("status", String),
    Column("citations_json", JSON),
    Column("retrieval_trace_json", JSON),
    Column("created_at", DateTime, server_default=func.now()),
)

sources_table = sources


class SQLiteMetadataStore:
    """Metadata store backed by SQLite for sources, chunks, ingestion runs, and answers."""

    def __init__(self, db_path: str | Path) -> None:
        self.engine = create_engine(f"sqlite:///{db_path}")
        self.sources = sources
        self.chunks = chunks
        self.ingestion_runs = ingestion_runs
        self.answers = answers

    def initialize(self) -> None:
        metadata.create_all(self.engine)

    def upsert_source(self, source: DocumentSource) -> None:
        stmt = sqlite_insert(self.sources).values(
            source_id=source.source_id,
            title=source.title,
            source_type=source.source_type.value if source.source_type else None,
            uri=source.uri,
            metadata_json=source.metadata,
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=["source_id"],
            set_={
                "title": stmt.excluded.title,
                "source_type": stmt.excluded.source_type,
                "uri": stmt.excluded.uri,
                "metadata_json": stmt.excluded.metadata_json,
            },
        )
        with self.engine.begin() as conn:
            conn.execute(stmt)

    def replace_chunks(self, source_id: str, chunk_list: list[DocumentChunk]) -> None:
        with self.engine.begin() as conn:
            conn.execute(chunks.delete().where(chunks.c.source_id == source_id))
            for chunk in chunk_list:
                conn.execute(
                    chunks.insert().values(
                        chunk_id=chunk.chunk_id,
                        source_id=chunk.source_id,
                        text=chunk.text,
                        chunk_index=chunk.chunk_index,
                        metadata_json=chunk.metadata,
                    )
                )

    def counts(self) -> dict[str, int]:
        with self.engine.connect() as conn:
            doc_count = conn.execute(select(func.count()).select_from(sources)).scalar()
            chunk_count = conn.execute(select(func.count()).select_from(chunks)).scalar()
        return {"documents": doc_count or 0, "chunks": chunk_count or 0}
