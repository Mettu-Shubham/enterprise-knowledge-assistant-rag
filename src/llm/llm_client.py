#llm_
import ollama


class LLMClient:

    def __init__(self, model="llama3"):
        """
        Initialize Ollama model
        """
        self.model = model

    def generate_answer(self, query, context_chunks):
        """
        Generate answer using retrieved context
        """

        # Combine retrieved chunks into context
        context = "\n\n".join([chunk.page_content for chunk in context_chunks])

        prompt = f"""
You are an assistant that answers questions using the provided context.

Context:
{context}

Question:
{query}

Answer clearly and concisely based only on the context.
"""

        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response["message"]["content"]