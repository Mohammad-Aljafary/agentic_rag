# Agentic RAG MVP Plan

## Summary

Build a local-first Agentic RAG MVP based on the architecture screenshot. A user submits a query, an agent understands and refines it, a planner selects retrieval strategies, a router queries vector, graph, and optional web sources, results are reranked and validated, and the system generates a final cited answer or returns an insufficient-evidence response.

The MVP target is a working developer-facing system with API and CLI access. The React frontend is deferred until the backend workflow is reliable.

Estimated effort for one developer: **6-8 weeks full time**, or roughly **180-260 engineering hours**.

## Architecture And Behavior

### Core Stack

- Python backend with FastAPI for HTTP endpoints.
- LangGraph for the agent workflow and state transitions.
- Pydantic for request, response, and internal state models.
- Pytest for unit, integration, and API tests.
- Local-first persistence:
  - local vector database for embeddings and semantic chunk search
  - lightweight graph store for entity and source relationships
  - SQLite or another local metadata database for sources, chunks, runs, citations, and traces

### Query Flow

1. A user submits a query through the CLI or API.
2. The query-understanding agent normalizes intent, extracts key entities, and identifies missing context.
3. The agent planner decomposes the request and chooses retrieval needs.
4. The retrieval router selects one or more retrieval paths:
   - vector retrieval for semantic document search
   - graph retrieval for entity and relationship lookup
   - optional web retrieval when local evidence is missing or freshness is required
5. Retrieved results are chunked, reranked, deduplicated, and packaged with citation metadata.
6. The evidence validator checks whether the retrieved context is strong enough to answer.
7. If evidence is weak, the agent can refine the query and retry retrieval.
8. The answer generator returns a grounded answer with citations or an `insufficient_evidence` status.

### Public Interfaces

HTTP API:

- `GET /health` for readiness checks.
- `POST /ingest` to ingest local files, directories, or configured source sets.
- `POST /query` to run the agentic RAG workflow and return an answer with citations and trace metadata.

CLI:

- `agentic-rag ingest <path-or-source>` to ingest documents.
- `agentic-rag query "<question>"` to ask a question and print cited output.
- `agentic-rag reindex` to rebuild embeddings and retrieval indexes.

Shared query response shape:

- `answer`: final answer text.
- `status`: one of `grounded`, `needs_refinement`, or `insufficient_evidence`.
- `citations`: source identifiers, titles or paths, excerpts, and chunk IDs.
- `retrieval_trace`: selected routes, query rewrites, scores, and validation notes.
- `confidence`: evidence-grounding confidence score or label.

## Implementation Phases And Estimate

### 1. Project Foundation: 2-3 Days

- Create the backend package structure.
- Add dependency management, environment configuration, logging, and test setup.
- Define shared models for documents, chunks, retrieval results, citations, agent state, ingest requests, and query responses.
- Add basic developer documentation for local setup.

### 2. Ingestion And Indexing: 5-7 Days

- Support ingestion for local text, Markdown, and PDF files.
- Normalize documents into consistently sized chunks.
- Generate embeddings for chunks.
- Persist source metadata, chunk lineage, timestamps, and indexing state.
- Add `reindex` support that can rebuild embeddings and indexes without duplicating source records.

### 3. Retrieval Layer: 5-7 Days

- Implement semantic vector search.
- Implement graph lookup for entities and source relationships.
- Add optional web search behind a clean adapter interface.
- Build the retrieval router that can select vector, graph, web, or combined retrieval.
- Add reranking, deduplication, score normalization, and citation packaging.

### 4. LangGraph Agent Workflow: 7-10 Days

- Implement the query-understanding node.
- Implement the planner node that chooses retrieval strategies.
- Implement the retrieval-router node.
- Implement the evidence-validation node.
- Implement the query-refinement loop for weak retrieval.
- Implement final answer generation with grounded citations.
- Ensure the workflow can stop safely with `insufficient_evidence` instead of hallucinating.

### 5. API And CLI: 4-6 Days

- Add FastAPI endpoints for health, ingestion, and querying.
- Add CLI commands for ingesting, querying, and reindexing.
- Keep CLI and API behavior consistent by sharing the same service layer.
- Return the same citation and trace schema from both interfaces.

### 6. Testing And Evaluation: 5-7 Days

- Add unit tests for chunking, metadata handling, retrieval routing, citation formatting, and evidence validation.
- Add integration tests for ingest-query-answer workflows.
- Add API tests for `GET /health`, `POST /ingest`, and `POST /query`.
- Add a small golden-answer fixture set for regression testing retrieval quality.

### 7. Documentation And Handoff: 2-3 Days

- Update `README.md` with setup, environment variables, run commands, and test commands.
- Document the architecture, workflow states, response shape, and known limitations.
- Add a demo flow that ingests sample files and asks a grounded question.

### 8. Buffer And Polish: 5-8 Days

- Fix integration issues across ingestion, retrieval, agent workflow, API, and CLI.
- Improve retrieval quality and evidence validation thresholds.
- Tighten error handling and logging.
- Clean retrieval traces so they are useful during development without overwhelming normal output.
- Prepare an MVP demo path.

## Test Plan

### Unit Tests

- Chunk creation preserves source metadata and chunk lineage.
- Citation reconstruction points to the correct source and excerpt.
- Retrieval router chooses vector, graph, web, or combined retrieval correctly.
- Reranking and deduplication produce stable ordered results.
- Evidence validator rejects low-quality or irrelevant context.

### Integration Tests

- Ingest a sample local corpus and answer known questions with citations.
- Query an unknown fact and return `insufficient_evidence`.
- Reindex an existing source set without duplicating records.
- Trigger query refinement when the first retrieval attempt is weak.
- Verify combined vector and graph retrieval improves answers for entity-heavy queries.

### API Tests

- `GET /health` returns service readiness.
- `POST /ingest` accepts a source and reports ingestion status.
- `POST /query` returns `answer`, `status`, `citations`, `retrieval_trace`, and `confidence`.
- `POST /query` returns `insufficient_evidence` when no trustworthy context exists.

### CLI Smoke Tests

- `agentic-rag ingest ./sample_docs`
- `agentic-rag query "What does the sample corpus say about the project architecture?"`
- `agentic-rag reindex`

## Acceptance Criteria

- A developer can install dependencies and run the backend locally.
- A developer can ingest local documents from the CLI.
- A developer can query from the CLI and API.
- Grounded answers include citations.
- Unsupported answers return `insufficient_evidence`.
- Retrieval traces show which routes were used and why.
- Tests cover the core ingestion, retrieval, validation, API, and CLI flows.

## Assumptions And Defaults

- MVP means a working local developer system, not a production beta.
- Primary interface is API plus CLI.
- The existing React frontend is deferred and should not drive the MVP schedule.
- Authentication, multi-user support, hosted deployment, admin dashboards, and production monitoring are out of scope for MVP.
- Web retrieval is optional and should be implemented behind an adapter so the local vector and graph flow remains useful without internet access.
- Citation quality and answer grounding take priority over broad tool use, memory, or autonomous task execution.
