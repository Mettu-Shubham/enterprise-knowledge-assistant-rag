import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    data_path: str = os.getenv("RAG_DATA_PATH", "data/WorldBank")
    vectorstore_path: str = os.getenv("RAG_VECTORSTORE_PATH", "vectorstore")
    registry_path: str = os.getenv("RAG_REGISTRY_PATH", "data/document_registry.json")
    users_path: str = os.getenv("RAG_USERS_PATH", "data/users.json")
    embedding_model: str = os.getenv("RAG_EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    embedding_local_only: bool = os.getenv("RAG_EMBEDDING_LOCAL_ONLY", "1") == "1"
    llm_model: str = os.getenv("RAG_LLM_MODEL", "qwen2.5:7b")
    retrieval_k: int = int(os.getenv("RAG_RETRIEVAL_K", "8"))
    jwt_secret_key: str = os.getenv("RAG_JWT_SECRET_KEY", "dev-secret-key-change-in-prod-1234567890")
    jwt_algorithm: str = os.getenv("RAG_JWT_ALGORITHM", "HS256")
    jwt_expiration_minutes: int = int(os.getenv("RAG_JWT_EXPIRATION_MINUTES", "60"))


def get_settings() -> Settings:
    return Settings()