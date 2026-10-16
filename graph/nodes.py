from agents.planner import PlannerAgent
from agents.research_pipeline import ResearchPipeline
from agents.analyst import AnalystAgent
from agents.critic import CriticAgent
from agents.synthesizer import SynthesizerAgent


def planner_node(state):
    tasks = PlannerAgent().run(state["user_query"])
    return {
        "research_tasks": tasks,
        "revision_count": 0,
        "revision_needed": False,
    }



def researcher_node(state):
    print("[DEBUG] Researcher node entered; revision_needed =", state.get("revision_needed", False))
    print("[DEBUG] Entering researcher_node")
    print(f"[DEBUG] Revision needed: {state.get('revision_needed', False)}")

    pipeline = ResearchPipeline()

    if state.get("revision_needed"):
        feedback = state.get("critique", {}).get("feedback", "")
        revision_task = (
            f"Find evidence directly relevant to the user's original question "
            f"that addresses this specific review feedback: {feedback}"
        )
        results = pipeline.run([revision_task])
        return {
            "research_results": state.get("research_results", []) + results
        }

    return {"research_results": pipeline.run(state["research_tasks"])}


def analyst_node(state):
    analysis = AnalystAgent().run(
        user_query=state["user_query"],
        research_results=state["research_results"],
    )
    return {"analysis": analysis}



def critic_node(state):
    print("\n[DEBUG] Entering critic_node")

    critique = CriticAgent().run(
        user_query=state["user_query"],
        analysis=state["analysis"],
    )

    revision_needed = critique["decision"] == "REVISE"
    revision_count = state.get("revision_count", 0) + int(revision_needed)

    print(f"[DEBUG] Critic decision: {critique['decision']}")
    print(f"[DEBUG] Revision needed: {revision_needed}")
    print(f"[DEBUG] Revision count: {revision_count}")

    return {
        "critique": critique,
        "revision_needed": revision_needed,
        "revision_count": revision_count,
    }


def synthesizer_node(state):
    final_answer = SynthesizerAgent().run(
        user_query=state["user_query"],
        research_results=state.get("research_results", []),
        analysis=state.get("analysis", ""),
        critique=state.get("critique", {}),
    )
    return {"final_answer": final_answer}
