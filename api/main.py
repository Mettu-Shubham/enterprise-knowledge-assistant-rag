from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

from src.auth.auth_service import AuthService
from src.config.settings import get_settings
from src.pipeline.rag_pipeline import RAGPipeline


app = FastAPI(title="Enterprise Knowledge Assistant")
settings = get_settings()
pipeline = RAGPipeline(settings)
auth_service = AuthService(settings.users_path)


class LoginRequest(BaseModel):
    username: str
    password: str


class QueryRequest(BaseModel):
    username: str
    password: str
    question: str


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "data_path": settings.data_path,
        "vectorstore_path": settings.vectorstore_path,
        "users_path": settings.users_path
    }


@app.get("/domains")
def list_domains():
    domains = pipeline.get_available_domains()
    return {
        "domains": domains
    }


@app.post("/login")
def login(request: LoginRequest):
    user = auth_service.authenticate(request.username, request.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    return {
        "message": "Login successful",
        "user": user
    }


@app.post("/query")
def query_rag(request: QueryRequest):
    user = auth_service.authenticate(request.username, request.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    pipeline.ensure_index()

    if not pipeline.is_ready():
        raise HTTPException(
            status_code=400,
            detail=f"No documents found in {settings.data_path}."
        )

    result = pipeline.ask(
        request.question,
        role=user["role"],
        domain=user.get("domain")
    )

    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "user": {
            "username": user["username"],
            "role": user["role"],
            "domain": user.get("domain")
        }
    }