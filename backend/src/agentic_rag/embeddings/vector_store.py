from __future__ import annotations

from pathlib import Path
from typing import Any

import chromadb
from chromadb import PersistentClient

from agentic_rag.models.rag import DocumentChunk


class ChromaVectorStore:
    def __init__(
        self,
        persist_dir: str | Path | None = None,
        _client: Any | None = None,
        _collection_name: str = "chunks",
    ) -> None:
        if _client is not None:
            self._client = _client
        else:
            self._client = chromadb.PersistentClient(path=str(persist_dir))
        self._collection_name = _collection_name
        self._collection = self._client.get_or_create_collection(
            name=_collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(self, chunks: list[DocumentChunk], embeddings: list[list[float]]) -> None:
        ids = [c.chunk_id for c in chunks]
        texts = [c.text for c in chunks]
        metadatas = [
            {"source_id": c.source_id, "chunk_index": c.chunk_index} for c in chunks
        ]
        self._collection.add(ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)

    def search(self, query_embedding: list[float], top_k: int) -> list[tuple[str, float]]:
        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )
        ids = results["ids"][0] if results["ids"] else []
        distances = results["distances"][0] if results["distances"] else []
        return list(zip(ids, distances))

    def delete_for_source(self, source_id: str) -> None:
        self._collection.delete(where={"source_id": source_id})

    def count(self) -> int:
        return self._collection.count()

    def clear(self) -> None:
        self._client.delete_collection(self._collection.name)
        self._collection = self._client.create_collection(
            name=self._collection.name,
            metadata={"hnsw:space": "cosine"},
        )
