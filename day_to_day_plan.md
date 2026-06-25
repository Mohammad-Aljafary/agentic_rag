# Two-Week Backend Vertical Slice Plan

## Summary

Build a realistic two-week Agentic RAG vertical slice, starting from the current scaffold state. The goal is not the full 6-8 week MVP; it is a working local backend that can ingest files, retrieve relevant chunks, answer through an agent workflow, return citations, expose API/CLI entrypoints, and prove the path with tests.

Assuming work starts today, Tuesday, June 16, 2026, the target demo date is Monday, June 29, 2026.

## Key Decisions

- Scope: backend vertical slice.
- Storage: local-first simple stack.
- Interfaces: FastAPI plus CLI.
- Frontend: keep the existing React UI as a visual shell; only connect it if backend work finishes early.
- Retrieval: prioritize reliable vector retrieval first; add lightweight graph/entity extraction only after the vector path works.
- Web retrieval: out of scope for the two-week slice unless everything else is complete.
- Success definition: local documents can be ingested, queried, cited, and tested repeatably.

## Step-By-Step Plan

### Day 1: Project Foundation

- Add backend package structure: `backend/app`, `backend/tests`, and CLI entrypoint.
- Add Python dependency management and local run commands.
- Define core Pydantic models for documents, chunks, citations, query requests, query responses, and retrieval traces.
- Add `GET /health`.
- Acceptance: backend starts locally and health endpoint passes.

### Day 2: Ingestion Skeleton

- Implement local file ingestion for `.txt` and `.md`.
- Add document metadata: source path, title, hash, timestamps.
- Add chunking with stable chunk IDs.
- Store document and chunk metadata in SQLite.
- Acceptance: CLI can ingest a small folder and show indexed document counts.

### Day 3: Embeddings And Vector Index

- Add embedding provider abstraction.
- Use a local vector store such as Chroma or FAISS.
- Persist chunk embeddings and connect them back to SQLite metadata.
- Add `agentic-rag reindex`.
- Acceptance: reindex can rebuild the vector index without duplicating source records.

### Day 4: Basic Retrieval

- Implement semantic search over indexed chunks.
- Return ranked chunks with scores and source metadata.
- Add citation packaging from retrieved chunks.
- Add unit tests for chunking, metadata, and citation reconstruction.
- Acceptance: a query returns relevant chunks and citation metadata from local files.

### Day 5: Query API And CLI

- Add `POST /query`.
- Add `agentic-rag query "question"`.
- Share the same service layer between API and CLI.
- Return `answer`, `status`, `citations`, `retrieval_trace`, and `confidence`.
- Acceptance: API and CLI produce the same response shape.

### Day 6: Agent Workflow

- Add a minimal LangGraph workflow:
  1. normalize query
  2. retrieve context
  3. validate evidence
  4. generate answer
- Keep planner/router simple for v1: vector retrieval is the default route.
- Acceptance: workflow can answer grounded questions and record trace steps.

### Day 7: Evidence Validation

- Add evidence threshold rules using retrieval score, number of supporting chunks, and source diversity.
- Return `insufficient_evidence` when context is weak.
- Add tests for known-answer and unknown-answer cases.
- Acceptance: the system refuses unsupported answers instead of fabricating.

### Day 8: Lightweight Graph/Entity Pass

- Add simple entity extraction from chunks and queries.
- Store entity-to-source and entity-to-chunk relationships in SQLite.
- Use entity matches as a retrieval boost or trace signal.
- Acceptance: entity-heavy queries show graph/entity evidence in the retrieval trace.

### Day 9: Integration Tests And Demo Corpus

- Add a small sample corpus under test/demo fixtures.
- Add integration tests for ingest -> query -> cited answer.
- Add API tests for health, ingest, and query.
- Add CLI smoke tests.
- Acceptance: one command sequence can run the demo locally.

### Day 10: Polish, Docs, And Final Demo

- Update `README.md` with setup, env vars, run commands, API examples, CLI examples, and known limits.
- Document the two-week scope separately from the full MVP.
- Tighten error handling and logging.
- Optional stretch: connect the existing React input to `POST /query`.
- Acceptance: demo path works from a clean checkout with documented commands.

## Public Interfaces

- `GET /health`
- `POST /ingest`
- `POST /query`
- `agentic-rag ingest <path>`
- `agentic-rag query "<question>"`
- `agentic-rag reindex`

Shared query response:

- `answer`
- `status`: `grounded` or `insufficient_evidence`
- `citations`
- `retrieval_trace`
- `confidence`

## Test Plan

- Unit tests for chunking, hashing, metadata, citations, retrieval scoring, and evidence validation.
- Integration test for ingesting a sample corpus and answering a known question with citations.
- Integration test for an unknown question returning `insufficient_evidence`.
- API tests for `/health`, `/ingest`, and `/query`.
- CLI smoke tests for `ingest`, `query`, and `reindex`.

## Assumptions

- One developer is working full time for two weeks.
- Local development is the priority, not hosted production deployment.
- Authentication, multi-user accounts, admin dashboards, web retrieval, advanced graph reasoning, and production monitoring are out of scope.
- The existing React app remains secondary until the backend vertical slice is reliable.
