class LLMClient:

    def __init__(self, model_name="llama3"):
        self.model_name = model_name

    def generate_answer(self, query, documents):
        """
        Generate answer with sources
        """

        context = "\n\n".join([doc["content"] for doc in documents])

        prompt = f"""
Answer the question using the context below.

Context:
{context}

Question:
{query}

Answer:
"""

        # Replace this with your actual LLM call
        response = f"(Mock Answer) Based on context: {query}"

        # Extract sources
        sources = []
        for doc in documents:
            meta = doc["metadata"]

            source_str = f"{meta.get('source', 'unknown')}"

            if "page" in meta:
                source_str += f" (Page {meta['page']})"

            source_str += f" [Chunk {meta.get('chunk_id', '-')}]"

            sources.append(source_str)

        return {
            "answer": response,
            "sources": list(set(sources))  # remove duplicates
        }