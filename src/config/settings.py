import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    data_path: str = os.getenv("RAG_DATA_PATH", "data/raw")
    vectorstore_path: str = os.getenv("RAG_VECTORSTORE_PATH", "vectorstore")
    embedding_model: str = os.getenv("RAG_EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    embedding_local_only: bool = os.getenv("RAG_EMBEDDING_LOCAL_ONLY", "1") == "1"
    llm_model: str = os.getenv("RAG_LLM_MODEL", "llama3")
    retrieval_k: int = int(os.getenv("RAG_RETRIEVAL_K", "3"))


def get_settings() -> Settings:
    return Settings()
