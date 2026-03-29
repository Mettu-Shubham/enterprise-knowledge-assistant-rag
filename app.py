from src.ingestion.document_loader import DocumentLoader
from src.processing.text_splitter import TextChunker
from src.vectorstore.chroma_store import ChromaStore
from src.retrieval.retriever import Retriever
from src.llm.llm_client import LLMClient


def main():

    loader = DocumentLoader("data/raw")
    documents = loader.load_documents()

    chunker = TextChunker()
    chunks = chunker.split_documents(documents)

    store = ChromaStore()
    vectordb = store.create_vector_store(chunks)

    retriever = Retriever(vectordb)

    llm = LLMClient()

    query = "What is the code of ethics?"

    context_chunks = retriever.retrieve(query)

    answer = llm.generate_answer(query, context_chunks)

    print("\nANSWER:\n")
    print(answer)


if __name__ == "__main__":
    main()