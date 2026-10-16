
import csv
from pathlib import Path
from datetime import datetime, timezone


RESULTS_PATH = Path("data/security_results.csv")

FIELDS = [
    "timestamp_utc",
    "test_id",
    "category",
    "description",
    "expected_behavior",
    "observed_behavior",
    "http_status",
    "outcome",
    "request_id",
    "notes",
]


def record_result(
    test_id: str,
    category: str,
    description: str,
    expected_behavior: str,
    observed_behavior: str,
    http_status: str = "",
    outcome: str = "NOT_RUN",
    request_id: str = "",
    notes: str = "",
):
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    write_header = not RESULTS_PATH.exists() or RESULTS_PATH.stat().st_size == 0

    with RESULTS_PATH.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)

        if write_header:
            writer.writeheader()

        writer.writerow({
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "test_id": test_id,
            "category": category,
            "description": description,
            "expected_behavior": expected_behavior,
            "observed_behavior": observed_behavior,
            "http_status": http_status,
            "outcome": outcome,
            "request_id": request_id,
            "notes": notes,
        })

    print(f"Recorded {test_id} → {RESULTS_PATH}")


if __name__ == "__main__":
    record_result(
        test_id="LOCAL-001",
        category="test_harness",
        description="Results recorder smoke test",
        expected_behavior="CSV row is written",
        observed_behavior="Local recorder executed",
        outcome="PASS",
        notes="Local-only test; no Prune or Gemini request.",
    )