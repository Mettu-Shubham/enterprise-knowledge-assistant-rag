from src.ingestion.document_loader import DocumentLoader
from src.embeddings.embedder import Embedder
from src.vectorstore.chroma_store import ChromaStore
from src.retrieval.retriever import Retriever
from src.llm.llm_client import LLMClient


def main():
    loader = DocumentLoader("data/raw")
    chunks = loader.load_documents()

    if not chunks:
        print("No documents found in data/raw.")
        return

    embedder = Embedder()
    texts, metadatas = embedder.prepare_chunks(chunks)

    store = ChromaStore()
    store.create_or_load_db(
        texts=texts,
        metadatas=metadatas,
        embedding_function=embedder,
        rebuild=True
    )

    retriever = Retriever(store)

    llm = LLMClient()

    query = "What is the code of ethics?"

    context_chunks = retriever.retrieve(query)

    answer = llm.generate_answer(query, context_chunks)

    print("\nANSWER:\n")
    print(answer)


if __name__ == "__main__":
    main()
