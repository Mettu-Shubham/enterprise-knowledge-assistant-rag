class Retriever:

    def __init__(self, vector_store, k=3):
        self.vector_store = vector_store
        self.k = k

    def retrieve(self, query, role="client", domain=None):
        filters = self._build_access_filter(role, domain)
        return self.vector_store.similarity_search(
            query,
            k=self.k,
            filters=filters
        )

    def _build_access_filter(self, role, domain):
        if role == "admin":
            return None

        if role == "client":
            return {"classification": "public"}

        if role == "employee":
            if domain:
                return {
                    "$or": [
                        {"classification": "public"},
                        {
                            "$and": [
                                {"classification": "internal"},
                                {"domain": domain}
                            ]
                        }
                    ]
                }
            return {"classification": "public"}

        return {"classification": "public"}
