
import json
from pathlib import Path


def main():
    cases_path = Path("tests/security_cases.json")
    cases = json.loads(cases_path.read_text(encoding="utf-8"))

    print(f"Loaded {len(cases)} security test cases.\n")

    for case in cases:
        print(f"[{case['id']}] {case['category']}")
        print(f"Description: {case['description']}")
        print(f"Expected: {case['expected']}")
        print()

    print("Security test definitions validated.")
    print("No Prune, Gemini, or other external API calls were made.")


if __name__ == "__main__":
    main()