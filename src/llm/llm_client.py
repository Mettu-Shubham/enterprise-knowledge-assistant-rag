import os
import re


class LLMClient:

    def __init__(self, model_name=None):
        self.model_name = model_name or os.getenv("RAG_LLM_MODEL", "qwen2.5:7b")

    def generate_answer(self, query, documents):
        """
        Generate answer with sources.
        """
        normalized_documents = [self._normalize_document(doc) for doc in documents]
        fallback_answer = (
            "I could not find enough relevant information in the authorized documents for that question."
        )

        if not normalized_documents:
            return {
                "answer": fallback_answer,
                "sources": []
            }

        context = "\n\n".join([doc["content"] for doc in normalized_documents])

        prompt = f"""
You are an enterprise knowledge assistant.

Answer the user's question using only the provided context.
If the question has multiple parts, identify each part and answer each part separately.
Write a clear and helpful answer in 2 to 5 short paragraphs or numbered points.
Do not simply repeat the document title or the question.
If the context is not enough for one part of the question, clearly say so.
Do not invent facts outside the context.

Context:
{context}

Question:
{query}

Answer:
"""

        response = self._generate_response(prompt, query, normalized_documents)
        if self._is_insufficient_response(response):
            return {
                "answer": fallback_answer,
                "sources": []
            }

        sources = []
        for doc in normalized_documents:
            meta = doc["metadata"]

            source_str = f"{meta.get('source', 'unknown')}"

            if "page" in meta:
                source_str += f" (Page {meta['page']})"
            sources.append(source_str)

        return {
            "answer": response,
            "sources": list(dict.fromkeys(sources))
        }

    def _normalize_document(self, doc):
        if isinstance(doc, dict):
            return doc

        return {
            "content": getattr(doc, "page_content", str(doc)),
            "metadata": getattr(doc, "metadata", {}) or {}
        }

    def _generate_response(self, prompt, query, documents):
        ollama_response = self._generate_with_ollama(prompt)
        if ollama_response:
            return ollama_response

        return self._extractive_fallback(query, documents)

    def _is_insufficient_response(self, response):
        if not response:
            return True

        normalized = response.strip().lower()
        fallback_markers = [
            "i'm sorry",
            "i am sorry",
            "does not align with the provided context",
            "doesn't align with the provided context",
            "does not align with the context",
            "doesn't align with the context",
            "doesn't seem to be related",
            "does not seem to be related",
            "not appropriate to answer",
            "based solely on the given information",
            "provided context does not",
            "context does not contain",
            "based on the provided context",
            "could not find relevant information",
            "could not find enough relevant information",
            "do not have enough information",
            "not enough information",
            "insufficient information",
        ]
        return any(marker in normalized for marker in fallback_markers)

    def _generate_with_ollama(self, prompt):
        try:
            from ollama import Client

            client = Client(host=os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434"))
            response = client.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    "temperature": 0.2
                }
            )
            return response.get("response", "").strip() or None
        except Exception:
            return None

    def _extractive_fallback(self, query, documents):
        query_terms = {
            term for term in re.findall(r"\w+", query.lower())
            if len(term) > 2
        }

        ranked_sentences = []
        for doc in documents:
            sentences = re.split(r"(?<=[.!?])\s+", doc["content"])
            for sentence in sentences:
                words = set(re.findall(r"\w+", sentence.lower()))
                score = len(query_terms & words)
                if score > 0:
                    ranked_sentences.append((score, sentence.strip()))

        ranked_sentences.sort(key=lambda item: item[0], reverse=True)
        best_sentences = [sentence for _, sentence in ranked_sentences[:3] if sentence]

        if best_sentences:
            return " ".join(best_sentences)

        return documents[0]["content"][:500].strip()
