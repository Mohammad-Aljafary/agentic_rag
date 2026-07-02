"""Token-aware document chunking for local ingestion."""

from __future__ import annotations

import hashlib

import tiktoken

from agentic_rag.models.rag import DocumentChunk, DocumentSource

DEFAULT_ENCODING = "cl100k_base"
DEFAULT_CHUNK_SIZE_TOKENS = 400
DEFAULT_OVERLAP_TOKENS = 50


def chunk_document(
    source: DocumentSource,
    text: str,
    chunk_size_tokens: int = DEFAULT_CHUNK_SIZE_TOKENS,
    overlap_tokens: int = DEFAULT_OVERLAP_TOKENS,
    encoding_name: str = DEFAULT_ENCODING,
) -> list[DocumentChunk]:
    """Split document text into stable overlapping token chunks."""
    if chunk_size_tokens <= 0:
        raise ValueError("chunk_size_tokens must be positive")
    if overlap_tokens < 0:
        raise ValueError("overlap_tokens cannot be negative")
    if overlap_tokens >= chunk_size_tokens:
        raise ValueError("overlap_tokens must be smaller than chunk_size_tokens")

    if not text.strip():
        return []

    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(text)
    step = chunk_size_tokens - overlap_tokens
    chunks: list[DocumentChunk] = []

    for chunk_index, token_start in enumerate(range(0, len(tokens), step)):
        token_end = min(token_start + chunk_size_tokens, len(tokens))
        chunk_tokens = tokens[token_start:token_end]
        chunk_text = encoding.decode(chunk_tokens).strip()

        if not chunk_text:
            continue

        chunks.append(
            DocumentChunk(
                chunk_id=_stable_chunk_id(source.source_id, chunk_index, chunk_text),
                source_id=source.source_id,
                text=chunk_text,
                chunk_index=chunk_index,
                metadata={
                    **source.metadata,
                    "title": source.title,
                    "source_type": source.source_type.value,
                    "uri": source.uri,
                    "token_start": token_start,
                    "token_end": token_end,
                    "token_count": len(chunk_tokens),
                    "encoding_name": encoding_name,
                },
            )
        )

        if token_end == len(tokens):
            break

    return chunks


def _stable_chunk_id(source_id: str, chunk_index: int, chunk_text: str) -> str:
    chunk_hash = hashlib.sha256(
        f"{source_id}:{chunk_index}:{chunk_text}".encode("utf-8")
    ).hexdigest()
    return f"chunk_{chunk_hash[:16]}"

def add_to_database(chunks: list[DocumentChunk], db_session) -> None:
    """Add chunks to the database."""
    for chunk in chunks:
        db_session.add(chunk)
    db_session.commit()
