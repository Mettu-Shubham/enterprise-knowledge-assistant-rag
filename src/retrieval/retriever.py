#retrival pipeline
class Retriever:

    def __init__(self, vector_store, k=3):
        self.vector_store = vector_store
        self.k = k

    def retrieve(self, query):
        """
        Retrieve top-k relevant chunks for a query
        """
        return self.vector_store.similarity_search(query, k=self.k)
