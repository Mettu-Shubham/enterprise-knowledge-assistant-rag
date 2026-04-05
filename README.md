# Enterprise Knowledge Assistant (Role-Aware RAG)

A local-first enterprise document assistant implementing secure Retrieval-Augmented Generation (RAG) with role-based access control, metadata-aware retrieval, and source-grounded responses.

---

## Overview

This project builds an end-to-end RAG pipeline for querying enterprise documents with strict access control. Documents are organized by domain and sensitivity, enabling secure and realistic enterprise knowledge retrieval.

Key features:

* Recursive document ingestion
* Metadata-aware chunking
* Role-based retrieval filtering (RBAC)
* Persistent vector storage (ChromaDB)
* Local LLM generation (Ollama)
* FastAPI backend + Streamlit frontend
* Source citations with page references

---

## Architecture

```
Documents (data/WorldBank/domain/classification)
        ↓
Ingestion + Metadata Extraction
        ↓
Chunking
        ↓
Embeddings (Sentence Transformers)
        ↓
Vector DB (ChromaDB)
        ↓
User Authentication (FastAPI)
        ↓
Role-Based Retrieval Filtering
        ↓
LLM Generation (Ollama)
        ↓
Answer + Sources
```

---

## Project Structure

```
.
├── api/
│   └── main.py
├── data/
│   ├── users.json
│   └── WorldBank/
│       ├── govt_policy/
│       │   ├── public/
│       │   ├── internal/
│       │   └── confidential/
│       ├── hr1/
│       │   ├── public/
│       │   ├── internal/
│       │   └── confidential/
│       ├── procurement_operations/
│       │   ├── public/
│       │   ├── internal/
│       │   └── confidential/
│       └── finance_budget/
│           ├── public/
│           ├── internal/
│           └── confidential/
├── scripts/
│   ├── scan_documents.py
│   ├── show_registry_changes.py
│   └── test_pipeline.py
├── src/
│   ├── auth/
│   │   └── auth_service.py
│   ├── config/
│   │   └── settings.py
│   ├── embeddings/
│   │   └── embedder.py
│   ├── ingestion/
│   │   ├── document_loader.py
│   │   └── document_registry.py
│   ├── llm/
│   │   └── llm_client.py
│   ├── pipeline/
│   │   └── rag_pipeline.py
│   ├── processing/
│   │   └── text_splitter.py
│   ├── retrieval/
│   │   └── retriever.py
│   └── vectorstore/
│       └── chroma_store.py
├── tests/
│   ├── test_rag_pipeline.py
│   └── test_text_splitter.py
├── streamlit_app.py
├── requirements.txt
└── README.md
```

---

## Dataset Structure

```
data/WorldBank/<domain>/<classification>/<file>
```

Domains:

* govt_policy
* hr1
* procurement_operations
* finance_budget

Classifications:

* public
* internal
* confidential

---

## Access Model

| Role     | Access Scope                        |
| -------- | ----------------------------------- |
| Admin    | All documents                       |
| Employee | Public + internal (own domain only) |
| Client   | Public only                         |

---

## Tech Stack

* Backend: FastAPI
* Frontend: Streamlit
* Embeddings: Sentence Transformers
* Vector DB: ChromaDB
* LLM: Ollama (qwen2.5:7b, llama3)
* PDF: pdfplumber
* DOCX: python-docx

---

## Setup

### Install dependencies

```
pip install -r requirements.txt
```

### Start Ollama

```
ollama serve
ollama pull qwen2.5:7b
```

### Run FastAPI

```
PYTHONPATH=. python -m uvicorn api.main:app --reload
```

### Run Streamlit

```
PYTHONPATH=. streamlit run streamlit_app.py
```

### Open UI

```
http://localhost:8501
```

---

## API Endpoints

### Health

```
GET /health
```

### Login

```
POST /login
```

### Query

```
POST /query
```

Example:

```
{
  "username": "admin1",
  "password": "admin123",
  "question": "What is the code of ethics?"
}
```

---

## Retrieval Flow

```
User → Authentication → Role Check → Metadata Filter
→ Vector Search → Context → LLM → Answer + Sources
```

---

## Testing

```
python -m unittest tests.test_rag_pipeline
python -m unittest tests.test_text_splitter
```

---

## Limitations

* Initial query latency due to warm-up
* Basic authentication (JSON-based)
* Limited vector lifecycle management
* Retrieval noise on ambiguous queries

---

## Future Improvements

* Query rewriting and reranking
* Token-based authentication
* Incremental vector updates
* UI enhancements
* Deployment support
* multimodel implementation

---