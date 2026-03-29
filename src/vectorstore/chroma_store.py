# database to store embeddings
import os
from langchain_community.vectorstores import Chroma


class ChromaStore:

    def __init__(self, persist_directory="vectorstore"):
        self.persist_directory = persist_directory
        self.vectordb = None

    def create_or_load_db(self, texts=None, embeddings=None, metadatas=None):
        """
        Create a new vector DB or load existing one
        """

        # Load existing DB
        if os.path.exists(self.persist_directory):
            self.vectordb = Chroma(
                persist_directory=self.persist_directory
            )

        # Create new DB
        else:
            self.vectordb = Chroma.from_embeddings(
                texts=texts,
                embeddings=embeddings,
                metadatas=metadatas,
                persist_directory=self.persist_directory
            )

            self.vectordb.persist()

        return self.vectordb

    def similarity_search(self, query_embedding, k=5):
        """
        Perform similarity search using query embedding
        """
        results = self.vectordb.similarity_search_by_vector(
            query_embedding,
            k=k
        )
        return results