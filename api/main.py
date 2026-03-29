#fast api 
from fastapi import FastAPI
from pydantic import BaseModel

from src.ingestion.document_loader import DocumentLoader
from src.processing.text_splitter import TextChunker
from src.vectorstore.chroma_store import ChromaStore
from src.retrieval.retriever import Retriever
from src.llm.llm_client import LLMClient


app = FastAPI(title="Enterprise Knowledge Assistant")


class QueryRequest(BaseModel):
    question: str


# ---- Initialize Pipeline ---- #

loader = DocumentLoader("data/raw")
documents = loader.load_documents()

chunker = TextChunker()
chunks = chunker.split_documents(documents)

store = ChromaStore()
vectordb = store.get_vector_store(chunks)

retriever = Retriever(vectordb)

llm = LLMClient()


# ---- API Endpoint ---- #

@app.post("/query")
def query_rag(request: QueryRequest):

    context_chunks = retriever.retrieve(request.question)

    answer = llm.generate_answer(
        request.question,
        context_chunks
    )

    return {
        "question": request.question,
        "answer": answer
    }