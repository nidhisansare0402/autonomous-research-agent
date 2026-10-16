
from langgraph.graph import StateGraph, START, END

from graph.state import ResearchState
from graph.nodes import (
    planner_node,
    researcher_node,
    analyst_node,
    critic_node,
    synthesizer_node,
)



def should_revise(state):
    print("[DEBUG] Routing after Critic")
    print("[DEBUG] revision_needed:", state.get("revision_needed"))
    print("[DEBUG] revision_count:", state.get("revision_count", 0))

    if (
        state.get("revision_needed", False)
        and state.get("revision_count", 0) <= 1
    ):
        print("[DEBUG] Routing to revision_researcher")
        return "revision_researcher"

    print("[DEBUG] Routing to synthesizer")
    return "synthesizer"


def build_workflow():
    graph = StateGraph(ResearchState)

    graph.add_node("planner", planner_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("analyst", analyst_node)
    graph.add_node("critic", critic_node)
    graph.add_node("revision_researcher", researcher_node)
    graph.add_node("synthesizer", synthesizer_node)

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "researcher")
    graph.add_edge("researcher", "analyst")
    graph.add_edge("analyst", "critic")

    graph.add_conditional_edges(
        "critic",
        should_revise,
        {
            "revision_researcher": "revision_researcher",
            "synthesizer": "synthesizer",
        },
    )

    graph.add_edge("revision_researcher", "analyst")
    graph.add_edge("synthesizer", END)

    print("[DEBUG] Workflow compiled with revision_researcher → analyst")
    return graph.compile()