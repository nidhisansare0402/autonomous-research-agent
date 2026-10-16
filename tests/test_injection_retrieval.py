
from pathlib import Path

from langchain_core.documents import Document
from rag.vector_store import VectorStore


def main():
    test_file = Path("data/documents/injection_test.txt")
    text = test_file.read_text(encoding="utf-8")

    # Use a separate collection so the main RAG data stays untouched.
    from langchain_chroma import Chroma
    from langchain_huggingface import HuggingFaceEmbeddings

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    store = Chroma(
        collection_name="injection_security_test",
        embedding_function=embeddings,
        persist_directory="data/chroma",
    )

    store.add_documents([
        Document(
            page_content=text,
            metadata={"source": test_file.name},
        )
    ])

    results = store.similarity_search(
        "What security risks can malicious instructions in RAG documents cause?",
        k=1,
    )

    print("\n===== INJECTION TEST RETRIEVAL =====")

    for result in results:
        print("Source:", result.metadata.get("source"))
        print(result.page_content)

    print("\nRetrieval test complete. No LLM API calls were made.")


if __name__ == "__main__":
    main()