import os
import shutil
from langchain_community.vectorstores import Chroma


class ChromaStore:

    def __init__(self, persist_directory="vectorstore"):
        self.persist_directory = persist_directory
        self.vectordb = None

    def create_or_load_db(
        self,
        texts=None,
        metadatas=None,
        embedding_function=None,
        rebuild=False
    ):
        """
        Create a new vector DB or load existing one.
        """
        db_file = os.path.join(self.persist_directory, "chroma.sqlite3")

        if rebuild and os.path.isdir(self.persist_directory):
            shutil.rmtree(self.persist_directory)
            db_file = os.path.join(self.persist_directory, "chroma.sqlite3")

        if os.path.exists(db_file):
            self.vectordb = Chroma(
                embedding_function=embedding_function,
                persist_directory=self.persist_directory
            )
        else:
            self.vectordb = Chroma.from_texts(
                texts=texts,
                embedding=embedding_function,
                metadatas=metadatas,
                persist_directory=self.persist_directory
            )

        return self.vectordb

    def similarity_search(self, query_text, k=5):
        """
        Perform similarity search using query text.
        """
        return self.vectordb.similarity_search(
            query_text,
            k=k
        )
