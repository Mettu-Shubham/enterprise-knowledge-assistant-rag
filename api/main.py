from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

from src.config.settings import get_settings
from src.pipeline.rag_pipeline import RAGPipeline


app = FastAPI(title="Enterprise Knowledge Assistant")
settings = get_settings()
pipeline = RAGPipeline(settings)


class QueryRequest(BaseModel):
    question: str
    domain: str | None = None

@app.post("/query")
def query_rag(request: QueryRequest):
    pipeline.ensure_index()

    if not pipeline.is_ready():
        raise HTTPException(
            status_code=400,
            detail=f"No documents found in {settings.data_path}."
        )

    result = pipeline.ask(request.question, domain=request.domain)

    return {
        "answer": result["answer"],
        "sources": result["sources"]
    }
