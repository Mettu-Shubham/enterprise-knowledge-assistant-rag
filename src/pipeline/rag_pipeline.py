from src.config.settings import Settings
from src.embeddings.embedder import Embedder
from src.ingestion.document_loader import DocumentLoader
from src.llm.llm_client import LLMClient
from src.retrieval.retriever import Retriever
from src.vectorstore.chroma_store import ChromaStore


class RAGPipeline:

    def __init__(
        self,
        settings: Settings,
        loader=None,
        embedder=None,
        store=None,
        retriever=None,
        llm_client=None
    ):
        self.settings = settings
        self.loader = loader or DocumentLoader(
            settings.data_path,
            settings.registry_path
        )        
        self.embedder = embedder or Embedder(
            settings.embedding_model,
            local_files_only=settings.embedding_local_only
        )
        self.store = store or ChromaStore(settings.vectorstore_path)
        self.retriever = retriever
        self.llm_client = llm_client or LLMClient(settings.llm_model)
        self._indexed = False

    def build_index(self, rebuild=False):
        load_result = self.loader.load_documents(changed_only=not rebuild)
        chunks = load_result["chunks"]
        self.last_changes = load_result["changes"]

        if rebuild:
            if not chunks:
                self.retriever = None
                self._indexed = False
                return []

            texts, metadatas = self.embedder.prepare_chunks(chunks)
            self.store.create_or_load_db(
                texts=texts,
                metadatas=metadatas,
                embedding_function=self.embedder,
                rebuild=True
            )
        else:
            if chunks:
                texts, metadatas = self.embedder.prepare_chunks(chunks)
                self.store.create_or_load_db(
                    texts=texts,
                    metadatas=metadatas,
                    embedding_function=self.embedder,
                    rebuild=False
                )

        self.retriever = Retriever(self.store, k=self.settings.retrieval_k)
        self._indexed = True
        return chunks

    def ensure_index(self):
        if self.retriever is None or not self._indexed:
            return self.build_index(rebuild=False)
        return None

    def is_ready(self):
        return self.retriever is not None

    def ask(self, question: str, role: str = "client", domain: str | None = None):
        self.ensure_index()
        if self.retriever is None:
            return {
                "answer": "No documents found in the configured data path.",
                "sources": []
            }

        documents = self.retriever.retrieve(question, role=role, domain=domain)
        return self.llm_client.generate_answer(question, documents)
