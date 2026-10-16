from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentLoader:
    def __init__(self, documents_dir: str = "data/documents"):
        self.documents_dir = Path(documents_dir)

    def load_documents(self) -> list[Document]:
        documents = []

        for file_path in self.documents_dir.glob("*.txt"):
            text = file_path.read_text(encoding="utf-8")

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": file_path.name
                    }
                )
            )

        return documents

    def split_documents(
        self,
        documents: list[Document]
    ) -> list[Document]:

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
        )

        return splitter.split_documents(documents)