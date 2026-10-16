
from typing import TypedDict


class ResearchState(TypedDict, total=False):
    # Original user request
    user_query: str

    # Planner output
    research_tasks: list[str]

    # Researcher output
    research_results: list[str]

    # Analyst output
    analysis: str

    # Critic output
    critique: dict

    # Critic decision
    revision_needed: bool

    # Prevent endless revision loops
    revision_count: int

    # Final Synthesizer output
    final_answer: str