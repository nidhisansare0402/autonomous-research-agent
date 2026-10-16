from rag.vector_store import VectorStore


class ResearchRetriever:
    def __init__(self):
        self.vector_store = VectorStore()

    def retrieve(self, query: str, k: int = 4):
        return self.vector_store.search(
            query=query,
            k=k,
        )