#dat base to store embed
import os
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings


class ChromaStore:

    def __init__(self, persist_directory="vector_store"):

        self.persist_directory = persist_directory

        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    def get_vector_store(self, chunks=None):
        """
        Load existing DB or create a new one
        """

        if os.path.exists(self.persist_directory):

            vectordb = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embedding_model
            )

        else:

            vectordb = Chroma.from_documents(
                documents=chunks,
                embedding=self.embedding_model,
                persist_directory=self.persist_directory
            )

            vectordb.persist()

        return vectordb