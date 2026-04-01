from src.config.settings import get_settings
from src.pipeline.rag_pipeline import RAGPipeline


def test_pipeline():
    settings = get_settings()
    pipeline = RAGPipeline(settings)
    domain = "govt_policy"

    print("Loading documents...")
    chunks = pipeline.build_index(rebuild=True)

    print(f"Total chunks created: {len(chunks)}")
    if not chunks:
        print(f"No chunks found in {settings.data_path}.")
        return

    print("\nSample chunk:")
    print(chunks[0])
    print("\nVector DB ready")

    print(f"\nTesting retrieval in domain: {domain}")
    query = "What is the code of ethics?"
    results = pipeline.retriever.retrieve(query, domain=domain)

    print(f"\nRetrieved {len(results)} result(s).")
    if not results:
        print("No matching chunks were returned.")
    else:
        for i, res in enumerate(results, start=1):
            print(f"\nResult {i}:")
            print(res.page_content[:300])
            print(res.metadata)

    result = pipeline.ask(query, domain=domain)

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
