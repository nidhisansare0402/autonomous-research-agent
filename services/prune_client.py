import os
import requests
from dotenv import load_dotenv

load_dotenv()

class PruneAPIError(RuntimeError):
    def __init__(self, status_code: int, details: dict, raw_body: str = ""):
        self.status_code = status_code
        self.code = details.get("code", "unknown_error")
        self.message = details.get("error", "Prune request failed")
        self.docs_url = details.get("docs_url", "")
        self.raw_body = raw_body

        super().__init__(self.message)

class PruneClient:
    def __init__(self):
        self.base_url = os.getenv(
            "PRUNE_BASE_URL",
            "https://api.withprune.com/v1"
        ).rstrip("/")

        self.api_key = os.getenv("PRUNE_API_KEY")
        self.model = os.getenv("PRUNE_MODEL", "gemini-2.5-flash")

        if not self.api_key:
            raise ValueError("PRUNE_API_KEY is not set")

    
    def generate(self, prompt: str) -> str:
        url = f"{self.base_url}/chat/completions"

        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 2000,
            },
            timeout=120,
        )

        if not response.ok:
            try:
                details = response.json()
            except ValueError:
                details = {}

            if not isinstance(details, dict):
                details = {}

            error = PruneAPIError(
                status_code=response.status_code,
                details=details,
                raw_body=response.text,
            )

            print("\n===== PRUNE ERROR =====")
            print("Status:", error.status_code)
            print("Code:", error.code)
            print("Reason:", error.message)
            if error.docs_url:
                print("Docs:", error.docs_url)
            print("=======================\n")

            raise error

        data = response.json()

        if "candidates" in data:
            try:
                return data["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError, TypeError) as exc:
                raise RuntimeError(
                    "Unexpected Gemini response format"
                ) from exc

        if "choices" in data:
            try:
                return data["choices"][0]["message"]["content"]
            except (KeyError, IndexError, TypeError) as exc:
                raise RuntimeError(
                    "Unexpected OpenAI-compatible response format"
                ) from exc

        raise RuntimeError(
            f"Unknown Prune response format. "
            f"Returned keys: {list(data.keys())}"
        )

    
    def generate_with_metadata(self, prompt: str) -> dict:
        """Return the response text and Prune metadata for security testing."""
        url = f"{self.base_url}/chat/completions"

        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 2000,
            },
            timeout=120,
        )

        response.raise_for_status()
        data = response.json()

        if "candidates" in data:
            try:
                text = data["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError, TypeError) as exc:
                raise RuntimeError("Unexpected Gemini response format") from exc
        elif "choices" in data:
            try:
                text = data["choices"][0]["message"]["content"]
            except (KeyError, IndexError, TypeError) as exc:
                raise RuntimeError("Unexpected OpenAI-compatible response format") from exc
        else:
            raise RuntimeError(
                f"Unknown Prune response format. Keys: {list(data.keys())}"
            )

        return {
            "text": text,
            "http_status": response.status_code,
            "request_id": (
                response.headers.get("x-request-id")
                or data.get("request_id", "")
            ),
            "prune_metadata": data.get("prune_metadata", {}),
        }