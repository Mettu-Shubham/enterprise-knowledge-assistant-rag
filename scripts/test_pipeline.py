from src.ingestion.document_loader import DocumentLoader
from src.embeddings.embedder import Embedder
from src.llm.llm_client import LLMClient
from src.retrieval.retriever import Retriever
from src.vectorstore.chroma_store import ChromaStore


def test_pipeline():
    print("Loading documents...")
    loader = DocumentLoader("data/raw")
    chunks = loader.load_documents()

    print(f"Total chunks created: {len(chunks)}")
    if not chunks:
        print("No chunks found in data/raw.")
        return

    print("\nSample chunk:")
    print(chunks[0])

    print("\nGenerating embeddings...")
    embedder = Embedder()
    texts, metadatas = embedder.prepare_chunks(chunks)
    embeddings = embedder.embed_documents(texts)
    print(f"Embeddings created: {len(embeddings)}")

    print("\nCreating vector DB...")
    store = ChromaStore()
    store.create_or_load_db(
        texts=texts,
        metadatas=metadatas,
        embedding_function=embedder,
        rebuild=True
    )
    print("Vector DB ready")

    print("\nTesting retrieval...")
    query = "What is the code of ethics?"
    retriever = Retriever(store, k=3)
    results = retriever.retrieve(query)
    llm = LLMClient()

    print(f"\nRetrieved {len(results)} result(s).")
    if not results:
        print("No matching chunks were returned.")
    else:
        for i, res in enumerate(results, start=1):
            print(f"\nResult {i}:")
            print(res.page_content[:300])
            print(res.metadata)

    result = llm.generate_answer(query, results)

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")
    if result["sources"]:
        for source in result["sources"]:
            print(source)
    else:
        print("No sources found.")


if __name__ == "__main__":
    test_pipeline()
