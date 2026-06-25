from agentic_rag.models.rag import (
    AnswerStatus,
    Citation,
    DocumentChunk,
    DocumentSource,
    QueryResponse,
    RetrievalTrace,
    SourceType,
)


def test_document_source_serialization_is_stable():
    source = DocumentSource(
        source_id="src_1",
        title="Agentic RAG Paper",
        source_type=SourceType.pdf,
        uri="file://paper.pdf",
        metadata={"author": "test"},
    )

    data = source.model_dump()

    assert data == {
        "source_id": "src_1",
        "title": "Agentic RAG Paper",
        "source_type": "pdf",
        "uri": "file://paper.pdf",
        "metadata": {"author": "test"},
    }


def test_chunk_preserves_lineage():
    chunk = DocumentChunk(
        chunk_id="chunk_1",
        source_id="src_1",
        text="RAG systems retrieve external evidence.",
        chunk_index=0,
    )

    assert chunk.chunk_id == "chunk_1"
    assert chunk.source_id == "src_1"


def test_query_response_grounded():
    citation = Citation(
        source_id="src_1",
        chunk_id="chunk_1",
        title="RAG Notes",
        quoted_text="RAG systems retrieve external evidence.",
    )

    response = QueryResponse(
        status=AnswerStatus.grounded,
        answer="RAG uses retrieved evidence to answer questions.",
        citations=[citation],
        retrieval_trace=RetrievalTrace(
            query="What is RAG?",
            strategy="vector_search",
            results_count=1,
            used_sources=["src_1"],
        ),
    )

    assert response.status == "grounded"
    assert len(response.citations) == 1


def test_query_response_insufficient_evidence():
    response = QueryResponse(
        status=AnswerStatus.insufficient_evidence,
        answer="I do not have enough evidence to answer this.",
        citations=[],
        retrieval_trace=RetrievalTrace(
            query="Unknown question",
            strategy="vector_search",
            results_count=0,
        ),
    )

    assert response.status == "insufficient_evidence"
    assert response.citations == []