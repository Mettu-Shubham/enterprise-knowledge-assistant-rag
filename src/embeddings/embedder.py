# create embeddings
from sentence_transformers import SentenceTransformer


class Embedder:

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """
        Initialize embedding model
        """
        self.model = SentenceTransformer(model_name)

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
