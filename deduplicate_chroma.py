
from collections import defaultdict
from rag.vector_store import VectorStore


def main():
    store = VectorStore()

    records = store.store.get(
        where={"source": "rag_basics.txt"},
        include=["documents", "metadatas"],
    )

    # Group entries by their exact document content.
    groups = defaultdict(list)

    for index, document_id in enumerate(records["ids"]):
        content = records["documents"][index]
        groups[content].append(document_id)

    duplicate_ids = []

    print("\n===== CHROMA DUPLICATE INSPECTION =====")
    print("Total rag_basics.txt entries:", len(records["ids"]))
    print("Unique content chunks:", len(groups))

    for chunk_number, (content, ids) in enumerate(groups.items(), start=1):
        print(f"\nChunk group {chunk_number}")
        print("Matching entries:", len(ids))
        print("Content preview:", content[:120].replace("\n", " "))

        # Keep one copy of each exact chunk.
        if len(ids) > 1:
            duplicate_ids.extend(ids[1:])
            print("Proposed duplicate IDs:", ids[1:])

    print("\nEntries proposed for deletion:", len(duplicate_ids))

    if not duplicate_ids:
        print("No exact duplicate chunks found. Nothing changed.")
        return

    confirmation = input(
        "\nDelete only the extra exact duplicate chunks? Type YES: "
    )

    if confirmation == "YES":
        store.store.delete(ids=duplicate_ids)
        print("Removed", len(duplicate_ids), "duplicate entries.")
    else:
        print("Cancelled. No changes made.")


if __name__ == "__main__":
    main()