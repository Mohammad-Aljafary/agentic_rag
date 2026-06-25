# Agentic RAG Backend

Local-first backend for learning Agentic RAG mechanisms step by step.

## Step 1: Foundation

Run the API:

```bash
uv run uvicorn agentic_rag.api:app --reload
```

Run tests:

```bash
uv run pytest -q
```

Health endpoint:

```bash
curl http://127.0.0.1:8000/health
```
