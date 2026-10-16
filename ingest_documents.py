
from rag.document_loader import DocumentLoader
from rag.vector_store import VectorStore

def main():
    loader = DocumentLoader()
    documents = loader.load_documents()
    chunks = loader.split_documents(documents)

    if not chunks:
        print("No documents found to ingest.")
        return

    store = VectorStore()
    ids = store.add_documents(chunks)

    print(f"Documents loaded: {len(documents)}")
    print(f"Chunks processed: {len(chunks)}")
    print(f"Chunk IDs submitted: {len(ids)}")
    print("Ingestion completed.")

if __name__ == "__main__":
    main()