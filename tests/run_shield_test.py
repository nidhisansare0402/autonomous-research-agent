
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from services.prune_client import PruneClient
from tests.security_results import record_result


load_dotenv()

CASES_PATH = Path("tests/security_cases.json")


def load_case(test_id: str) -> dict:
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))

    for case in cases:
        if case["id"] == test_id:
            return case

    raise ValueError(f"Unknown test ID: {test_id}")


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: python -m tests.run_shield_test "
            "<TEST_ID>\nExample: python -m tests.run_shield_test PII-001"
        )
        return

    test_id = sys.argv[1].upper()
    case = load_case(test_id)

    if case["category"] == "agent_loop":
        print(
            "This is a local workflow test, not a Shield request. "
            "Use mock mode for this case."
        )
        return

    print(f"\nSelected test: {case['id']} — {case['description']}")
    print("This will send ONE request through your configured Prune endpoint.")
    print("Review the test input before proceeding:")
    print(case["prompt"])

    confirmation = input(
        "\nType SEND to make this single real request: "
    ).strip()

    if confirmation != "SEND":
        print("Cancelled. No request sent.")
        return

    client = PruneClient()

    try:
        # Use the existing client so the configured Prune endpoint,
        # model, and credentials are reused.
        result = client.generate_with_metadata(case["prompt"])
        response_text = result["text"]
        metadata = result["prune_metadata"]

        record_result(
            test_id=case["id"],
            category=case["category"],
            description=case["description"],
            expected_behavior=case["expected"],
            observed_behavior=(
                "Request returned a response. "
                "Inspect output and Prune metadata for evidence of redaction or blocking."
            ),
            http_status=str(result["http_status"]),
            outcome="REVIEW_REQUIRED",
            request_id=result["request_id"],
            notes=f"Prune metadata: {json.dumps(metadata, ensure_ascii=False)}",
        )

        print("\nRequest returned a response.")
        print("HTTP status:", result["http_status"])
        print("Request ID:", result["request_id"] or "Not provided")
        print("Prune metadata:", json.dumps(metadata, indent=2, ensure_ascii=False))
        print("Response (inspect for evidence of blocking or redaction):")
        print(response_text)

    except Exception as exc:
        response = getattr(exc, "response", None)
        if response is not None:
            print("HTTP status:", response.status_code)
            print("Error response body:")
            print(response.text[:3000])
        else:
            print("No HTTP response attached to the error.")

        if response is not None:
            try:
                payload = response.json()
                request_id = str(payload.get("request_id", ""))
            except ValueError:
                pass

        record_result(
            test_id=case["id"],
            category=case["category"],
            description=case["description"],
            expected_behavior=case["expected"],
            observed_behavior=f"Request raised {type(exc).__name__}",
            http_status=status,
            outcome="ERROR_REVIEW",
            request_id=request_id,
            notes=str(exc)[:500],
        )

        
    print(f"\nRequest failed: {type(exc).__name__}")

    if status:
        print(f"HTTP status: {status}")

    if response is not None:
        print("Error response body:")
        print(response.text[:3000])

    print(
        "The failure is recorded; inspect the error reason "
        "before classifying it as a Shield block."
    )


if __name__ == "__main__":
    main()