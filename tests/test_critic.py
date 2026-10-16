from agents.planner import PlannerAgent
from agents.research_pipeline import ResearchPipeline
from agents.analyst import AnalystAgent
from agents.critic import CriticAgent


def main():

    query = """
    Should an enterprise customer support system use
    Retrieval-Augmented Generation (RAG)?
    Analyze the benefits, limitations, alternatives,
    implementation requirements, and risks.
    """

    # 1. Planning
    planner = PlannerAgent()
    tasks = planner.run(query)

    # 2. Research
    pipeline = ResearchPipeline()
    research_results = pipeline.run(tasks)

    # 3. Analysis
    analyst = AnalystAgent()
    analysis = analyst.run(
        user_query=query,
        research_results=research_results
    )

    # 4. Criticism
    critic = CriticAgent()
    critique = critic.run(
        user_query=query,
        analysis=analysis
    )

    print("\n===== ANALYSIS =====\n")
    print(analysis)

    print("\n===== CRITIC =====\n")
    print(critique)


if __name__ == "__main__":
    main()