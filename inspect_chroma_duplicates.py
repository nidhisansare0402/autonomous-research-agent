from collections import defaultdict
from rag.vector_store import VectorStore


def main():
    vector_store = VectorStore()
    collection = vector_store.store

    records = collection.get(include=["documents", "metadatas"])
    ids = records.get("ids", [])
    documents = records.get("documents", [])
    metadatas = records.get("metadatas", [])

    exact_groups = defaultdict(list)
    for record_id, document, metadata in zip(ids, documents, metadatas):
        source = (metadata or {}).get("source", "unknown")
        # Exact duplicate means same source and identical text.
        exact_groups[(source, (document or "").strip())].append(record_id)

    duplicate_groups = [
        {
            "source": source,
            "count": len(record_ids),
            "ids": record_ids,
            "preview": text[:180].replace("\n", " "),
        }
        for (source, text), record_ids in exact_groups.items()
        if len(record_ids) > 1
    ]

    print("===== CHROMA DUPLICATE AUDIT (READ-ONLY) =====")
    print("Total records:", len(ids))
    print("Unique source/content pairs:", len(exact_groups))
    print("Exact duplicate groups:", len(duplicate_groups))

    if duplicate_groups:
        for index, group in enumerate(duplicate_groups, start=1):
            print(f"\nDuplicate group {index}")
            print("Source:", group["source"])
            print("Count:", group["count"])
            print("IDs:", group["ids"])
            print("Preview:", group["preview"])
    else:
        print("No exact duplicates found by source + content.")

    print("\nRecords by source:")
    source_counts = defaultdict(int)
    for metadata in metadatas:
        source_counts[(metadata or {}).get("source", "unknown")] += 1
    for source, count in sorted(source_counts.items()):
        print(f"- {source}: {count}")

    print("\nNo records were changed or deleted.")
    print("==============================================")


if __name__ == "__main__":
    main()
