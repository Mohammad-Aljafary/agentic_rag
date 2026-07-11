import chromadb
import pytest

from agentic_rag.embeddings.provider import ONNXEmbeddingProvider
from agentic_rag.embeddings.vector_store import ChromaVectorStore
from agentic_rag.ingestion.pipeline import IngestionPipeline
from agentic_rag.storage.sqlite import SQLiteMetadataStore


@pytest.fixture
def pipeline(tmp_path):
    db_path = tmp_path / "test.db"
    store = SQLiteMetadataStore(db_path)
    store.initialize()

    client = chromadb.EphemeralClient()
    vector_store = ChromaVectorStore(_client=client)

    provider = ONNXEmbeddingProvider()
    return IngestionPipeline(
        metadata_store=store,
        vector_store=vector_store,
        embedding_provider=provider,
    )


def test_ingest_single_file(tmp_path, pipeline):
    doc = tmp_path / "test.txt"
    doc.write_text("RAG retrieves evidence from documents.", encoding="utf-8")

    result = pipeline.ingest_path(tmp_path)

    assert result["sources_ingested"] == 1
    assert result["chunks_indexed"] >= 1
    assert pipeline._metadata_store.counts()["documents"] == 1
    assert pipeline._vector_store.count() >= 1


def test_ingest_empty_directory(pipeline, tmp_path):
    result = pipeline.ingest_path(tmp_path)
    assert result == {"sources_ingested": 0, "chunks_indexed": 0}


def test_reindex_rebuilds_vector_index(pipeline, tmp_path):
    doc = tmp_path / "test.txt"
    doc.write_text("RAG retrieves evidence from documents.", encoding="utf-8")
    pipeline.ingest_path(tmp_path)

    before = pipeline._vector_store.count()
    assert before >= 1

    result = pipeline.reindex()
    assert result["chunks_reindexed"] == before
    assert pipeline._vector_store.count() == before


def test_reindex_empty_returns_zero(pipeline, tmp_path):
    result = pipeline.reindex()
    assert result == {"chunks_reindexed": 0}
