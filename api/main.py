#fast api 
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

from src.ingestion.document_loader import DocumentLoader
from src.embeddings.embedder import Embedder
from src.vectorstore.chroma_store import ChromaStore
from src.retrieval.retriever import Retriever
from src.llm.llm_client import LLMClient


app = FastAPI(title="Enterprise Knowledge Assistant")
DATA_PATH = "data/raw"


class QueryRequest(BaseModel):
    question: str


# ---- Initialize Pipeline ---- #
retriever = None
llm = LLMClient()


def get_retriever():
    global retriever

    if retriever is not None:
        return retriever

    loader = DocumentLoader(DATA_PATH)
    chunks = loader.load_documents()

    if not chunks:
        return None

    embedder = Embedder()
    texts, metadatas = embedder.prepare_chunks(chunks)

    store = ChromaStore()
    store.create_or_load_db(
        texts=texts,
        metadatas=metadatas,
        embedding_function=embedder,
        rebuild=True
    )

    retriever = Retriever(store)
    return retriever


# ---- API Endpoint ---- #

@app.post("/query")
def query_rag(request: QueryRequest):
    active_retriever = get_retriever()

    if active_retriever is None:
        raise HTTPException(
            status_code=400,
            detail="No documents found in data/raw."
        )

    query = request.question

    documents = active_retriever.retrieve(query)

    result = llm.generate_answer(query, documents)

    return {
        "answer": result["answer"],
        "sources": result["sources"]
    }
