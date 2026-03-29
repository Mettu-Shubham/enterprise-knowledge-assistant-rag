from src.ingestion.document_loader import DocumentLoader
from src.embeddings.embedder import Embedder
from src.vectorstore.chroma_store import ChromaStore


def test_pipeline():
    print("🔹 Loading documents...")
    loader = DocumentLoader("data/raw")
    chunks = loader.load_documents()

    print(f"✅ Total chunks created: {len(chunks)}")

    print("\n🔹 Sample chunk:")
    print(chunks[0])

    print("\n🔹 Generating embeddings...")
    embedder = Embedder()
    embeddings, texts, metadatas = embedder.embed_documents(chunks)

    print(f"✅ Embeddings created: {len(embeddings)}")

    print("\n🔹 Creating vector DB...")
    store = ChromaStore()

    vectordb = store.create_or_load_db(
        texts=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print("✅ Vector DB ready")

    print("\n🔹 Testing retrieval...")
    query = "What is the document about?"
    query_embedding = embedder.embed_query(query)

    results = store.similarity_search(query_embedding, k=3)

    print("\n✅ Retrieval Results:")
    for i, res in enumerate(results):
        print(f"\nResult {i+1}:")
        print(res.page_content[:200])
        print(res.metadata)


if __name__ == "__main__":
    test_pipeline()