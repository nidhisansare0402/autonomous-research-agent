from collections import defaultdict
from rag.vector_store import VectorStore


def main():
    vector_store = VectorStore()
    collection = vector_store.store

    records = collection.get(include=["documents", "metadatas"])
    ids = records.get("ids", [])
    documents = records.get("documents", [])
    metadatas = records.get("metadatas", [])

    groups = defaultdict(list)
    for record_id, document, metadata in zip(ids, documents, metadatas):
        source = (metadata or {}).get("source", "unknown")
        key = (source, (document or "").strip())
        groups[key].append(record_id)

    duplicate_groups = [
        (key, record_ids)
        for key, record_ids in groups.items()
        if len(record_ids) > 1
    ]

    if not duplicate_groups:
        print("No exact duplicates found. Nothing to delete.")
        return

    print("Exact duplicate groups found:", len(duplicate_groups))
    to_delete = []

    for (source, text), record_ids in duplicate_groups:
        # Keep the first ID and delete only the extra IDs.
        keep_id = record_ids[0]
        delete_ids = record_ids[1:]
        print(f"\nSource: {source}")
        print("Chunk preview:", text[:120].replace("\n", " "))
        print("Keeping ID:", keep_id)
        print("Deleting duplicate ID(s):", delete_ids)
        to_delete.extend(delete_ids)

    confirmation = input(
        f"\nType DELETE {len(to_delete)} to remove only these duplicate records: "
    ).strip()

    if confirmation != f"DELETE {len(to_delete)}":
        print("Cancelled. No records were deleted.")
        return

    collection.delete(ids=to_delete)
    print(f"Deleted {len(to_delete)} duplicate record(s).")
    print("All unique source/content pairs were retained.")


if __name__ == "__main__":
    main()
