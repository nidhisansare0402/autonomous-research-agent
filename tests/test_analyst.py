from agents.planner import PlannerAgent
from agents.research_pipeline import ResearchPipeline
from agents.analyst import AnalystAgent


def main():

    query = """
    Should an enterprise customer support system use
    Retrieval-Augmented Generation (RAG)?
    Analyze the benefits, limitations, alternatives,
    implementation requirements, and risks.
    """

    # Planner
    planner = PlannerAgent()
    tasks = planner.run(query)

    # Research
    pipeline = ResearchPipeline()
    research_results = pipeline.run(tasks)

    # Analysis
    analyst = AnalystAgent()
    analysis = analyst.run(
        user_query=query,
        research_results=research_results
    )

    print("\n===== ANALYSIS =====\n")
    print(analysis)


if __name__ == "__main__":
    main()