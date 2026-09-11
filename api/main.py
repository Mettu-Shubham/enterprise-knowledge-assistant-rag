from contextlib import asynccontextmanager

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from src.auth.auth_service import AuthService
from src.config.settings import get_settings
from src.pipeline.rag_pipeline import RAGPipeline


settings = get_settings()
pipeline = RAGPipeline(settings)
auth_service = AuthService(
    users_path=settings.users_path,
    jwt_secret_key=settings.jwt_secret_key,
    jwt_algorithm=settings.jwt_algorithm,
    jwt_expiration_minutes=settings.jwt_expiration_minutes
)
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    payload = auth_service.decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return {
        "username": payload["sub"],
        "role": payload.get("role", "client"),
        "domain": payload.get("domain")
    }


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Warm the vector index at startup so the first frontend query is faster.
    """
    try:
        pipeline.ensure_index()
    except Exception as exc:
        print(f"Startup index warmup failed: {exc}")
    yield


app = FastAPI(
    title="Enterprise Knowledge Assistant",
    lifespan=lifespan
)


class LoginRequest(BaseModel):
    username: str
    password: str


class QueryRequest(BaseModel):
    question: str


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "data_path": settings.data_path,
        "vectorstore_path": settings.vectorstore_path,
        "users_path": settings.users_path,
        "index_ready": pipeline.is_ready()
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

    access_token = auth_service.create_access_token(
        data={
            "sub": user["username"],
            "role": user["role"],
            "domain": user.get("domain")
        }
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@app.post("/query")
def query_rag(request: QueryRequest, current_user: dict = Depends(get_current_user)):
    if not pipeline.is_ready():
        pipeline.ensure_index()

    if not pipeline.is_ready():
        raise HTTPException(
            status_code=400,
            detail=f"No documents found in {settings.data_path}."
        )

    result = pipeline.ask(
        request.question,
        role=current_user["role"],
        domain=current_user.get("domain")
    )

    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "user": {
            "username": current_user["username"],
            "role": current_user["role"],
            "domain": current_user.get("domain")
        }
    }