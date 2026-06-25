# Agentic RAG Step-by-Step Build

This project is a learning lab for understanding how modern chatbots retrieve fresh and grounded information. We will build it in small working slices. Each slice must run and be testable before moving on.

## Step 1 — Backend foundation

Status: complete.

What it teaches:
- how to structure the backend package
- how to expose an API service
- how to test FastAPI endpoints

Implemented:
- `backend/pyproject.toml`
- `backend/src/agentic_rag/api.py`
- `backend/src/agentic_rag/cli.py`
- `backend/tests/test_health.py`
- `GET /health`

Verify:

```bash
cd backend
uv run pytest -q
uv run uvicorn agentic_rag.api:app --reload
curl http://127.0.0.1:8000/health
```

## Step 2 — Core data models

Goal:
Define the vocabulary of the system before implementing retrieval.

Models to add:
- `DocumentSource`
- `DocumentChunk`
- `Citation`
- `RetrievalResult`
- `RetrievalTrace`
- `QueryRequest`
- `QueryResponse`

What it teaches:
- what metadata a RAG system must preserve for citations
- why chunks need stable IDs and source lineage
- how API response shape controls frontend and tests

Acceptance:
- tests prove model serialization is stable
- query response can represent both `grounded` and `insufficient_evidence`

## Step 3 — Local ingestion for `.txt` and `.md`

Goal:
Load local files into the system and create stable document metadata.

What it teaches:
- how chatbot knowledge bases ingest external data
- how source hashes prevent duplicate ingestion
- how source paths and titles later become citations

Acceptance:
- ingesting a folder discovers `.txt` and `.md` files
- unsupported files are skipped
- document hashes are stable

## Step 4 — Chunking

Goal:
Split documents into searchable chunks with stable chunk IDs.

What it teaches:
- why RAG systems chunk documents
- tradeoff between chunk size and retrieval quality
- preserving source lineage for citations

Acceptance:
- chunks keep document ID, chunk index, text, and source metadata
- tests cover short docs, long docs, and empty docs

## Step 5 — SQLite metadata store

Goal:
Persist sources, chunks, and ingestion state locally.

What it teaches:
- why vector DBs are not enough by themselves
- how metadata DBs support citations and reindexing

Acceptance:
- source and chunk records survive process restart
- re-ingesting unchanged files does not duplicate records

## Step 6 — Embeddings and vector retrieval

Goal:
Turn chunks into vectors and retrieve relevant chunks for a question.

What it teaches:
- semantic search
- query embeddings vs document embeddings
- top-k retrieval and score thresholds

Acceptance:
- a known query retrieves the expected sample chunk
- retrieval results include scores and citation metadata

## Step 7 — Query endpoint and CLI

Goal:
Expose retrieval through `POST /query` and `agentic-rag query`.

What it teaches:
- shared service layer between API and CLI
- stable response schemas for frontend integration

Acceptance:
- API and CLI return the same query response shape
- retrieval trace explains what happened

## Step 8 — Evidence validation

Goal:
Return `insufficient_evidence` when retrieved context is weak.

What it teaches:
- how RAG systems reduce hallucinations
- confidence thresholds and refusal behavior

Acceptance:
- known questions return `grounded`
- unknown questions return `insufficient_evidence`

## Step 9 — Answer generation with citations

Goal:
Use an LLM to generate answers only from retrieved evidence.

What it teaches:
- grounded generation
- citation formatting
- prompt constraints

Acceptance:
- final answer includes citations
- unsupported answers are refused

## Step 10 — Agentic loop

Goal:
Add query rewriting, retrieval planning, and retry/refinement.

What it teaches:
- what makes RAG “agentic”
- how systems recover from weak first retrieval

Acceptance:
- weak first retrieval can trigger a rewritten query
- trace shows original query, rewritten query, and retry result

## Step 11 — Fresh data / web retrieval

Goal:
Add optional web retrieval behind a router.

What it teaches:
- how chatbots get fresh information
- freshness detection
- source reliability and citation issues

Acceptance:
- local questions use local retrieval
- freshness-needed questions route to web retrieval
- web results are cited and validated

## Step 12 — Graph/entity retrieval

Goal:
Extract entities and use them as a second retrieval mechanism.

What it teaches:
- when graph retrieval helps more than vector search
- entity-to-chunk relationships
- hybrid retrieval

Acceptance:
- entity-heavy questions show graph evidence in the trace
- vector + graph retrieval improves at least one demo query
