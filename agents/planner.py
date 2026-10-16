import json

from services.llm_service import LLMService


class PlannerAgent:

    def __init__(self):
        self.llm = LLMService()

    def run(self, user_query: str) -> list[str]:

        prompt = f"""
You are a planning agent.

Break the user's research question into exactly 1 short research tasks.

Rules:
- Each task must be one short sentence.
- Each task must be less than 15 words.
- Return ONLY a JSON array.
- Do not use markdown.
- Do not add explanations.
- Do not use newline characters inside task strings.

User question:
{user_query}

Example:
["Analyze the main benefits and limitations"]
"""

        response = self.llm.generate(prompt).strip()

        print("\n===== RAW PLANNER RESPONSE =====")
        print(response)
        print("================================\n")

        try:
            tasks = json.loads(response)

        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Planner returned invalid JSON:\n{response}"
            ) from exc

        if not isinstance(tasks, list):
            raise RuntimeError(
                "Planner response must be a JSON array."
            )

        if len(tasks) != 1:
            raise RuntimeError(
                f"Planner returned {len(tasks)} tasks instead of 1:\n{tasks}"
            )

        if not all(isinstance(task, str) for task in tasks):
            raise RuntimeError(
                "Every planner task must be a string."
            )

        return tasks