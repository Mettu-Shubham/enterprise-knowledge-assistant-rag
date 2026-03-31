# LLM RAG Project

Enterprise Knowledge Assistant prototype built with RAG, FastAPI, Chroma, and Ollama.

## Current Phase

Phase 1 focuses on making the local prototype clean, testable, and repeatable.

## Run Locally

From the project root:

```bash
PYTHONPATH=. ./.venv/Scripts/python.exe scripts/test_pipeline.py
```

Start the API:

```bash
PYTHONPATH=. ./.venv/Scripts/python.exe -m uvicorn api.main:app --reload
```

Test the API:

```bash
curl -X POST http://127.0.0.1:8000/query -H "Content-Type: application/json" -d "{\"question\":\"What is the code of ethics?\"}"
```

## Run Repeatable Tests

```bash
PYTHONPATH=. ./.venv/Scripts/python.exe -m unittest discover -s tests -v
```

By default, the embedder prefers a locally cached model first for more repeatable runs.
Set `RAG_EMBEDDING_LOCAL_ONLY=0` if you want it to attempt a network download.
