from __future__ import annotations

import argparse
import sys
from pathlib import Path

from agentic_rag.embeddings.provider import ONNXEmbeddingProvider
from agentic_rag.embeddings.vector_store import ChromaVectorStore
from agentic_rag.ingestion.pipeline import IngestionPipeline
from agentic_rag.storage.sqlite import SQLiteMetadataStore

DEFAULT_DB_PATH = Path.home() / ".agentic_rag" / "metadata.db"
DEFAULT_VECTOR_DIR = Path.home() / ".agentic_rag" / "vectors"


def _get_store() -> SQLiteMetadataStore:
    DEFAULT_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    store = SQLiteMetadataStore(DEFAULT_DB_PATH)
    store.initialize()
    return store


def _get_vector_store() -> ChromaVectorStore:
    DEFAULT_VECTOR_DIR.mkdir(parents=True, exist_ok=True)
    return ChromaVectorStore(DEFAULT_VECTOR_DIR)


def _get_pipeline() -> IngestionPipeline:
    return IngestionPipeline(
        metadata_store=_get_store(),
        vector_store=_get_vector_store(),
        embedding_provider=ONNXEmbeddingProvider(),
    )


def cmd_ingest(args: list[str]) -> None:
    if not args:
        print("Usage: agentic-rag ingest <path>")
        return
    path = Path(args[0])
    if not path.exists():
        print(f"Path does not exist: {path}")
        return
    pipeline = _get_pipeline()
    result = pipeline.ingest_path(path)
    print(f"Ingested {result['sources_ingested']} sources, {result['chunks_indexed']} chunks")


def cmd_reindex() -> None:
    pipeline = _get_pipeline()
    result = pipeline.reindex()
    print(f"Reindexed {result['chunks_reindexed']} chunks")


def cmd_counts() -> None:
    store = _get_store()
    counts = store.counts()
    print(f"Documents: {counts['documents']}, Chunks: {counts['chunks']}")


def main() -> None:
    import sys

    if len(sys.argv) < 2:
        print("Usage: agentic-rag <command> [args]")
        print("Commands: ingest, reindex, counts")
        return

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == "ingest":
        cmd_ingest(args)
    elif command == "reindex":
        cmd_reindex()
    elif command == "counts":
        cmd_counts()
    else:
        print(f"Unknown command: {command}")
        print("Commands: ingest, reindex, counts")
