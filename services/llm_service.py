
import os
import uuid

from services.prune_client import PruneClient


class LLMService:
    # Shared across instances for mock Critic revision testing.
    _mock_critic_calls = 0

    def __init__(self):
        self.test_mode = (
            os.getenv("LLM_TEST_MODE", "false").lower() == "true"
        )
        self.unique_requests = (
            os.getenv("PRUNE_UNIQUE_REQUESTS", "false").lower() == "true"
        )

        if not self.test_mode:
            self.prune = PruneClient()

    def generate(self, prompt: str) -> str:
        if self.test_mode:
            return self._mock_response(prompt)

        # Optional cache-key variation for live requests.
        # This does not guarantee a cache bypass.
        if self.unique_requests:
            request_ref = uuid.uuid4().hex
            prompt = (
                f"{prompt}\n\n"
                f"Internal request reference: {request_ref}. "
                "Do not mention this reference in your answer."
            )

        return self.prune.generate(prompt)

    def _mock_response(self, prompt: str) -> str:
        prompt_lower = prompt.lower()

        if "planning agent" in prompt_lower:
            return '["Identify the main benefits and limitations of RAG."]'

        if "critic agent" in prompt_lower:
            type(self)._mock_critic_calls += 1

            if type(self)._mock_critic_calls == 1:
                return (
                    '{"decision":"REVISE",'
                    '"issues":["Needs more detail on benefits."],'
                    '"feedback":"Include specific benefits supported by the retrieved evidence."}'
                )

            return (
                '{"decision":"PASS","issues":[],'
                '"feedback":"The revised answer addresses the question sufficiently."}'
            )

        if "final synthesis agent" in prompt_lower:
            return (
                "Retrieval-Augmented Generation (RAG) retrieves relevant "
                "information from a knowledge base and supplies it to an LLM "
                "to help produce a grounded answer. Its usefulness depends on "
                "retrieval quality and the quality of the source documents."
            )

        if (
            "analysis agent" in prompt_lower
            or "final-answer agent" in prompt_lower
        ):
            return (
                "RAG can improve answers by giving an LLM relevant external "
                "information, helping it use domain-specific or updated knowledge. "
                "Its effectiveness depends on retrieval quality and the reliability "
                "of the documents."
            )

        if "research agent" in prompt_lower:
            marker = "Retrieved knowledge:"
            retrieved = ""

            if marker in prompt:
                retrieved = prompt.split(marker, 1)[1]
                retrieved = retrieved.split(
                    "\nInstructions:", 1
                )[0].strip()

            if not retrieved or retrieved.startswith(
                "No relevant documents were found"
            ):
                return (
                    "No relevant documents were found in the local knowledge base. "
                    "This is a mock-mode result; live research was not performed."
                )

            return (
                "Research findings from the local knowledge base:\n\n"
                + retrieved
            )

        return "Mock response: no matching agent prompt was detected."