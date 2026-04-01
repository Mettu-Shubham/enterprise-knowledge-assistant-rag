import os
import shutil
from langchain_community.vectorstores import Chroma


class ChromaStore:

    def __init__(self, persist_directory="vectorstore", batch_size=1000):
        self.persist_directory = persist_directory
        self.vectordb = None
        self.batch_size = batch_size

    def create_or_load_db(
        self,
        texts=None,
        metadatas=None,
        embedding_function=None,
        rebuild=False
    ):
        """
        Create a new vector DB or load an existing one.
        Inserts documents in batches to avoid Chroma batch-size errors.
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
            return self.vectordb

        if not texts:
            self.vectordb = Chroma(
                embedding_function=embedding_function,
                persist_directory=self.persist_directory
            )
            return self.vectordb

        first_end = min(self.batch_size, len(texts))
        self.vectordb = Chroma.from_texts(
            texts=texts[:first_end],
            embedding=embedding_function,
            metadatas=metadatas[:first_end] if metadatas else None,
            persist_directory=self.persist_directory
        )

        for start in range(first_end, len(texts), self.batch_size):
            end = start + self.batch_size
            batch_texts = texts[start:end]
            batch_metadatas = metadatas[start:end] if metadatas else None

            self.vectordb.add_texts(
                texts=batch_texts,
                metadatas=batch_metadatas
            )

        return self.vectordb

    def similarity_search(self, query_text, k=5, domain=None):
        """
        Perform similarity search using query text.
        """
        search_filter = None
        if domain:
            search_filter = {"domain": domain}

        return self.vectordb.similarity_search(
            query_text,
            k=k,
            filter=search_filter
        )
