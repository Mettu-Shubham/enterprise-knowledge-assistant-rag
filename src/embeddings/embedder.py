# create embeddings 
from sentence_transformers import SentenceTransformer


class Embedder:

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """
        Initialize embedding model
        """

        self.model = SentenceTransformer(model_name)

    def embed_documents(self, chunks):
        """
        Convert chunks into embeddings
        """

        texts = [chunk.page_content for chunk in chunks]

        embeddings = self.model.encode(
            texts,
            show_progress_bar=True
        )

        return embeddings

    def embed_query(self, query):
        """
        Embed user query
        """

        return self.model.encode(query)