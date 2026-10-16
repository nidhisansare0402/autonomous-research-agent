import hashlib
from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


class VectorStore:
    def __init__(self, persist_directory: str = "data/chroma"):
        self.persist_directory = Path(persist_directory)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.store = Chroma(
            collection_name="research_documents",
            embedding_function=self.embeddings,
            persist_directory=str(self.persist_directory),
        )

    @staticmethod
    def _document_id(document) -> str:
        source = str(document.metadata.get("source", "unknown"))
        content = document.page_content.strip()
        digest = hashlib.sha256(
            f"{source}\0{content}".encode("utf-8")
        ).hexdigest()
        return digest

    def add_documents(self, documents):
        """Idempotently add chunks: the same source/content gets the same ID."""
        if not documents:
            return []

        # Deduplicate identical source/content chunks within this input batch.
        unique_documents = {}
        for document in documents:
            unique_documents[self._document_id(document)] = document

        ids = list(unique_documents.keys())
        docs = list(unique_documents.values())

        # Chroma upserts by ID; re-ingesting the same chunk won't create a new row.
        self.store.add_documents(documents=docs, ids=ids)
        return ids

    def search(self, query: str, k: int = 4):
        return self.store.similarity_search(query, k=k)
