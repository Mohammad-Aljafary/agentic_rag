import uuid

import chromadb

from agentic_rag.embeddings.vector_store import ChromaVectorStore
from agentic_rag.models.rag import DocumentChunk


def _make_chunk(
    chunk_id: str = "c1",
    source_id: str = "doc_1",
    chunk_index: int = 0,
    text: str = "some text",
) -> DocumentChunk:
    return DocumentChunk(
        chunk_id=chunk_id,
        source_id=source_id,
        text=text,
        chunk_index=chunk_index,
    )


def _store() -> ChromaVectorStore:
    return ChromaVectorStore(
        _client=chromadb.EphemeralClient(),
        _collection_name=f"test_{uuid.uuid4().hex[:8]}",
    )


def test_add_and_count():
    store = _store()
    chunks = [_make_chunk("c1", chunk_index=0), _make_chunk("c2", chunk_index=1)]
    embeddings = [[0.1] * 384, [0.2] * 384]

    store.add_chunks(chunks, embeddings)
    assert store.count() == 2


def test_search_returns_results():
    store = _store()
    chunks = [_make_chunk("c1", chunk_index=0, text="hello world")]
    store.add_chunks(chunks, [[0.1] * 384])

    results = store.search([0.1] * 384, top_k=1)
    assert len(results) == 1
    assert results[0][0] == "c1"


def test_delete_for_source():
    store = _store()
    store.add_chunks(
        [_make_chunk("c1", source_id="doc_1")],
        [[0.1] * 384],
    )
    store.add_chunks(
        [_make_chunk("c2", source_id="doc_2")],
        [[0.2] * 384],
    )

    store.delete_for_source("doc_1")
    assert store.count() == 1


def test_count():
    store = _store()
    assert store.count() == 0
    store.add_chunks([_make_chunk("c1")], [[0.1] * 384])
    assert store.count() == 1
