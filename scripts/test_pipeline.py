from src.config.settings import get_settings
from src.pipeline.rag_pipeline import RAGPipeline


def test_pipeline():
    settings = get_settings()
    pipeline = RAGPipeline(settings)

    print("Loading documents...")
    chunks = pipeline.build_index(rebuild=False)

    print(f"Total newly chunks processed: {len(chunks)}")
    if not chunks:
        print(f"No documents found in {settings.data_path}.")
        return

    role = "employee"
    domain = "govt_policy"
    query = "What is the code of ethics?"

    print(f"\nTesting retrieval for role={role}, domain={domain}")
    results = pipeline.retriever.retrieve(query, role=role, domain=domain)

    print(f"\nRetrieved {len(results)} result(s).")
    for i, res in enumerate(results, start=1):
        print(f"\nResult {i}:")
        print(res.page_content[:300])
        print(res.metadata)

    result = pipeline.ask(query, role=role, domain=domain)

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
