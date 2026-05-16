# Agentic RAG V1 Implementation Plan

## Summary

Build a Python-based, LangGraph-powered agentic RAG system whose first usable version is available through both a CLI and an HTTP API. V1 should ingest mixed knowledge sources, answer questions with citations, and optimize for grounded, traceable responses over advanced autonomy.

## Key Changes

### Product and behavior

- Deliver a single-user local-development system that can ingest local files and web pages into one searchable knowledge base.
- Make grounded Q&A the primary workflow: every final answer should include cited source snippets or source references.
- Keep agent behavior narrow in V1: retrieve context, decide whether more retrieval is needed, synthesize an answer, and abstain when evidence is weak.

### Core architecture

- Use Python as the application language and LangGraph as the orchestration layer.
- Split the system into five subsystems:
  - ingestion for loading local documents and fetched web content
  - indexing for chunking, embedding, and vector-store writes
  - retrieval for semantic search, optional reranking, and citation packaging
  - agent for LangGraph state, tool calls, and answer generation
  - interfaces for CLI commands and HTTP endpoints
- Store document metadata with stable IDs, source type, source location, timestamps, and chunk lineage so citations can point back to originals.
- Start with a local vector store for V1 to reduce operational overhead; keep the indexing interface abstract so a hosted store can be swapped in later.

### Public interfaces

- CLI commands:
  - `ingest` to load or refresh sources
  - `query` to ask a question and print an answer with citations
  - `reindex` to rebuild embeddings/index state when needed
- HTTP API endpoints:
  - `POST /ingest` to submit a local path or URL set for ingestion
  - `POST /query` to return answer text plus citations and retrieval metadata
  - `GET /health` for service readiness
- Define a shared response shape for CLI/API results:
  - `answer`
  - `citations[]` with source identifier, title or path, and relevant excerpt
  - `confidence` or answer status such as `grounded` / `insufficient_evidence`
  - `trace` or debug metadata gated behind a development flag

### Implementation sequence

- Phase 1: bootstrap project structure, dependency management, config loading, logging, and shared data models.
- Phase 2: implement ingestion pipelines for local files and web pages, including normalization and chunking.
- Phase 3: implement embeddings, vector indexing, retrieval, and citation reconstruction.
- Phase 4: build the LangGraph workflow with retrieval tools, answer synthesis, and insufficient-evidence handling.
- Phase 5: expose the workflow through CLI and HTTP API with consistent request/response models.
- Phase 6: add observability, fixtures, sample data, and deployment-oriented documentation.

## Test Plan

- Unit tests for chunking, metadata assignment, citation reconstruction, and retrieval result formatting.
- Integration tests for:
  - ingesting a small mixed-source corpus
  - querying known facts and verifying expected citations are returned
  - handling low-evidence questions by returning an abstaining or insufficient-evidence response
  - reindexing without duplicating records unexpectedly
- API tests for `POST /query`, `POST /ingest`, and `GET /health`.
- CLI smoke tests for the end-to-end flow: ingest corpus, run query, inspect cited output.
- Acceptance scenarios:
  - a user can ingest at least one local document set and one web source set
  - a user can query from CLI and API and receive grounded answers with citations
  - the system avoids confident unsupported answers when retrieval evidence is missing

## Assumptions and Defaults

- V1 is local-first and optimized for developer use rather than multi-tenant production deployment.
- LangGraph + Python is the chosen orchestration stack.
- Mixed-source ingestion means local documents plus web pages in the first release, not cloud drives or SaaS integrations.
- Citation quality and answer grounding take priority over broad tool use, memory, or autonomous task execution.
- Authentication, multi-user support, admin UI, and production-grade deployment automation are out of scope for V1 unless requirements change.
