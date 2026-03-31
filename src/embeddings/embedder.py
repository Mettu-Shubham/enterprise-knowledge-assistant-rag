# create embeddings
from sentence_transformers import SentenceTransformer


class Embedder:

    def __init__(self, model_name="all-MiniLM-L6-v2", local_files_only=True):
        """
        Initialize embedding model
        """
        self.model_name = model_name
        self.local_files_only = local_files_only
        self.model = self._load_model()

    def embed_documents(self, texts):
        """
        Convert plain texts into embeddings.

        Args:
            texts (list[str]): Plain text chunks

        Returns:
            list[list[float]]
        """
        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            show_progress_bar=True
        )

        if hasattr(embeddings, "tolist"):
            embeddings = embeddings.tolist()
        return embeddings

    def prepare_chunks(self, chunks):
        """
        Split structured chunks into texts and metadatas for vector storage.
        """
        if not chunks:
            return [], []

        texts = [chunk["content"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]
        return texts, metadatas

    def embed_query(self, query):
        """
        Embed user query
        """
        embedding = self.model.encode(query)
        if hasattr(embedding, "tolist"):
            embedding = embedding.tolist()
        return embedding

    def _load_model(self):
        try:
            return SentenceTransformer(
                self.model_name,
                local_files_only=self.local_files_only
            )
        except Exception:
            if self.local_files_only:
                return SentenceTransformer(
                    self.model_name,
                    local_files_only=False
                )
            raise
