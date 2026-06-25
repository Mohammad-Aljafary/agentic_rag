"""Pydantic models for retrieval-augmented generation workflows."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class SourceType(str, Enum):
    """Supported source document types."""

    pdf = "pdf"
    webpage = "webpage"
    markdown = "markdown"
    text = "text"
    unknown = "unknown"


class AnswerStatus(str, Enum):
    """Grounding status for a generated answer."""

    grounded = "grounded"
    insufficient_evidence = "insufficient_evidence"


class DocumentSource(BaseModel):
    """Metadata describing a source document available for retrieval."""

    source_id: str
    title: str | None = None
    source_type: SourceType = SourceType.unknown
    uri: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class DocumentChunk(BaseModel):
    """A retrievable chunk of text with source lineage."""

    chunk_id: str
    source_id: str
    text: str
    chunk_index: int
    metadata: dict[str, Any] = Field(default_factory=dict)


class Citation(BaseModel):
    """Evidence cited in a generated answer."""

    source_id: str
    chunk_id: str
    title: str
    uri: str | None = None
    quoted_text: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class RetrievalResult(BaseModel):
    """A retrieved chunk and its ranking score."""

    chunk: DocumentChunk
    score: float
    citations: list[Citation] = Field(default_factory=list)


class RetrievalTrace(BaseModel):
    """Trace data describing how retrieval was performed."""

    query: str
    strategy: str
    results_count: int
    used_sources: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class QueryRequest(BaseModel):
    """Request payload for a RAG query."""

    query: str
    top_k: int = 5
    session_id: str | None = None
    retrieval_strategy: str = "default"
    filters: dict[str, Any] | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class QueryResponse(BaseModel):
    """Response payload for a RAG query."""

    status: AnswerStatus
    answer: str
    citations: list[Citation] = Field(default_factory=list)
    retrieval_trace: RetrievalTrace
    metadata: dict[str, Any] = Field(default_factory=dict)
