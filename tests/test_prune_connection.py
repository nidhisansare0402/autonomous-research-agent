
import os
from dotenv import load_dotenv

load_dotenv(override=True)


def main():
    test_mode = os.getenv("LLM_TEST_MODE", "false").lower() == "true"
    base_url = os.getenv("PRUNE_BASE_URL", "")
    model = os.getenv("PRUNE_MODEL", "")

    print("\n===== PRUNE CONNECTION CONFIGURATION =====")
    print(f"LLM mock mode: {test_mode}")
    print(f"Prune base URL configured: {bool(base_url)}")
    print(f"Prune model configured: {model or 'NOT SET'}")

    if test_mode:
        print(
            "\nMock mode is enabled. No real Prune request will be made."
        )
        print(
            "This verifies local configuration only, not connectivity."
        )
    elif not base_url or not model:
        print("\nPrune configuration is incomplete.")
    else:
        print(
            "\nLive mode is enabled, but this script intentionally "
            "does not send a request."
        )
        print(
            "Use it to verify configuration before a separately "
            "approved live test."
        )

    print("==========================================\n")


if __name__ == "__main__":
    main()