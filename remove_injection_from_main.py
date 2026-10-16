
from rag.vector_store import VectorStore

store = VectorStore()

# Count matching entries before deletion.
matches = store.store.get(
    where={"source": "injection_test.txt"},
    include=["metadatas"],
)

count = len(matches.get("ids", []))
print(f"Matching test entries before cleanup: {count}")

if count:
    confirmation = input(
        "Delete only these entries from research_documents? Type YES: "
    )

    if confirmation == "YES":
        store.store.delete(
            where={"source": "injection_test.txt"}
        )
        print(f"Deleted {count} matching entries.")
    else:
        print("No changes made.")
else:
    print("No matching entries found. Nothing to delete.")