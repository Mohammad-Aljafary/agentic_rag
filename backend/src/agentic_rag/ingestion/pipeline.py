from __future__ import annotations

from pathlib import Path

from sqlalchemy import select as sa_select

from agentic_rag.embeddings.provider import EmbeddingProvider
from agentic_rag.embeddings.vector_store import ChromaVectorStore
from agentic_rag.ingestion.chunking import chunk_document
from agentic_rag.ingestion.files import discover_ingestable_files, read_local_document
from agentic_rag.models.rag import DocumentChunk
from agentic_rag.storage.sqlite import SQLiteMetadataStore, chunks as chunks_table


class IngestionPipeline:
    def __init__(
        self,
        metadata_store: SQLiteMetadataStore,
        vector_store: ChromaVectorStore,
        embedding_provider: EmbeddingProvider,
    ) -> None:
        self._metadata_store = metadata_store
        self._vector_store = vector_store
        self._embedding_provider = embedding_provider

    def ingest_path(self, path: str | Path) -> dict:
        files = discover_ingestable_files(path)
        if not files:
            return {"sources_ingested": 0, "chunks_indexed": 0}

        total_chunks = 0
        for file_path in files:
            source, text = read_local_document(file_path)
            chunks = chunk_document(source, text)
            if not chunks:
                continue

            embeddings = self._embedding_provider.embed([c.text for c in chunks])

            self._metadata_store.upsert_source(source)
            self._metadata_store.replace_chunks(source.source_id, chunks)
            self._vector_store.delete_for_source(source.source_id)
            self._vector_store.add_chunks(chunks, embeddings)
            total_chunks += len(chunks)

        return {"sources_ingested": len(files), "chunks_indexed": total_chunks}

    def reindex(self) -> dict:
        with self._metadata_store.engine.connect() as conn:
            rows = conn.execute(
                sa_select(
                    chunks_table.c.chunk_id,
                    chunks_table.c.source_id,
                    chunks_table.c.text,
                    chunks_table.c.chunk_index,
                )
            ).fetchall()

        if not rows:
            return {"chunks_reindexed": 0}

        chunks = [
            DocumentChunk(
                chunk_id=row[0],
                source_id=row[1],
                text=row[2],
                chunk_index=row[3],
            )
            for row in rows
        ]

        embeddings = self._embedding_provider.embed([c.text for c in chunks])

        self._vector_store.clear()
        self._vector_store.add_chunks(chunks, embeddings)

        return {"chunks_reindexed": len(chunks)}
