import os
import shutil
from langchain_community.vectorstores import Chroma


class ChromaStore:

    def __init__(self, persist_directory="vectorstore", batch_size=1000):
        self.persist_directory = persist_directory
        self.vectordb = None
        self.batch_size = batch_size

    def has_existing_db(self):
        db_file = os.path.join(self.persist_directory, "chroma.sqlite3")
        return os.path.exists(db_file)

    def load_existing_db(self, embedding_function=None):
        if not self.has_existing_db():
            return None

        self.vectordb = Chroma(
            embedding_function=embedding_function,
            persist_directory=self.persist_directory
        )
        return self.vectordb

    def create_or_load_db(
        self,
        texts=None,
        metadatas=None,
        embedding_function=None,
        rebuild=False
    ):
        db_file = os.path.join(self.persist_directory, "chroma.sqlite3")

        if rebuild and os.path.isdir(self.persist_directory):
            shutil.rmtree(self.persist_directory)
            db_file = os.path.join(self.persist_directory, "chroma.sqlite3")

        if os.path.exists(db_file):
            self.vectordb = Chroma(
                embedding_function=embedding_function,
                persist_directory=self.persist_directory
            )

            # Add only newly processed chunks, if any
            if texts:
                self._add_in_batches(texts, metadatas)

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

        self._add_in_batches(
            texts[first_end:],
            metadatas[first_end:] if metadatas else None
        )

        return self.vectordb

    def _add_in_batches(self, texts, metadatas=None):
        if not texts:
            return

        for start in range(0, len(texts), self.batch_size):
            end = start + self.batch_size
            batch_texts = texts[start:end]
            batch_metadatas = metadatas[start:end] if metadatas else None

            self.vectordb.add_texts(
                texts=batch_texts,
                metadatas=batch_metadatas
            )

    def similarity_search(self, query_text, k=5, filters=None):
        return self.vectordb.similarity_search(
            query_text,
            k=k,
            filter=filters
        )