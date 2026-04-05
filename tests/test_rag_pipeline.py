import unittest

from src.config.settings import Settings
from src.pipeline.rag_pipeline import RAGPipeline


class FakeLoader:

    def __init__(self, chunks):
        self.chunks = chunks

    def load_documents(self, changed_only=False):
        return {
            "chunks": self.chunks,
            "changes": {
                "new": [],
                "modified": [],
                "deleted": [],
                "unchanged": [],
            },
            "documents": [],
        }


class FakeEmbedder:

    def prepare_chunks(self, chunks):
        texts = [chunk["content"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]
        return texts, metadatas


class FakeStore:

    def __init__(self, existing_db=True):
        self.calls = []
        self.existing_db = existing_db

    def create_or_load_db(self, texts=None, metadatas=None, embedding_function=None, rebuild=False):
        self.calls.append(
            {
                "texts": texts,
                "metadatas": metadatas,
                "embedding_function": embedding_function,
                "rebuild": rebuild,
            }
        )

    def load_existing_db(self, embedding_function=None):
        return self if self.existing_db else None

    def similarity_search(self, query, k=5, filters=None):
        return [
            {
                "content": "The code of ethics explains expected ethical behavior.",
                "metadata": {"source": "policy.pdf", "chunk_id": 0, "page": 1},
            }
        ]


class FakeLLMClient:

    def generate_answer(self, question, documents):
        return {
            "answer": f"Answer for: {question}",
            "sources": ["policy.pdf (Page 1)"],
        }


class RAGPipelineTests(unittest.TestCase):

    def test_build_index_creates_retriever_when_chunks_exist(self):
        chunks = [
            {
                "content": "Ethics policy chunk",
                "metadata": {"source": "policy.pdf", "chunk_id": 0},
            }
        ]
        store = FakeStore()
        pipeline = RAGPipeline(
            settings=Settings(),
            loader=FakeLoader(chunks),
            embedder=FakeEmbedder(),
            store=store,
            llm_client=FakeLLMClient(),
        )

        result = pipeline.build_index(rebuild=True)

        self.assertEqual(result, chunks)
        self.assertTrue(pipeline.is_ready())
        self.assertEqual(len(store.calls), 1)
        self.assertTrue(store.calls[0]["rebuild"])

    def test_ask_returns_graceful_response_when_no_documents_exist(self):
        pipeline = RAGPipeline(
            settings=Settings(),
            loader=FakeLoader([]),
            embedder=FakeEmbedder(),
            store=FakeStore(existing_db=False),
            llm_client=FakeLLMClient(),
        )

        result = pipeline.ask("What is the code of ethics?")

        self.assertEqual(result["sources"], [])
        self.assertIn("No documents found", result["answer"])

    def test_ask_uses_retrieved_documents(self):
        chunks = [
            {
                "content": "Ethics policy chunk",
                "metadata": {"source": "policy.pdf", "chunk_id": 0},
            }
        ]
        pipeline = RAGPipeline(
            settings=Settings(),
            loader=FakeLoader(chunks),
            embedder=FakeEmbedder(),
            store=FakeStore(),
            llm_client=FakeLLMClient(),
        )

        result = pipeline.ask("What is the code of ethics?")

        self.assertEqual(result["answer"], "Answer for: What is the code of ethics?")
        self.assertEqual(result["sources"], ["policy.pdf (Page 1)"])


if __name__ == "__main__":
    unittest.main()
