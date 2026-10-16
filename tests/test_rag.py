from rag.document_loader import DocumentLoader
from rag.vector_store import VectorStore
from rag.retriever import ResearchRetriever


def main():
    loader = DocumentLoader()

    documents = loader.load_documents()

    print(f"\nLoaded documents: {len(documents)}")

    chunks = loader.split_documents(documents)

    print(f"Created chunks: {len(chunks)}")

    vector_store = VectorStore()

    vector_store.add_documents(chunks)

    retriever = ResearchRetriever()

    query = "What are the main benefits of RAG?"

    results = retriever.retrieve(query, k=3)

    print("\n===== RETRIEVED DOCUMENTS =====\n")

    for index, document in enumerate(results, start=1):
        print(f"--- Result {index} ---")
        print(f"Source: {document.metadata.get('source')}")
        print(document.page_content)
        print()


if __name__ == "__main__":
    main()