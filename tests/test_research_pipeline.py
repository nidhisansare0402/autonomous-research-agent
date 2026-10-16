from agents.planner import PlannerAgent
from agents.research_pipeline import ResearchPipeline


def main():

    query = """
    Should an enterprise customer support system use
    Retrieval-Augmented Generation (RAG)?
    Analyze the benefits, limitations, alternatives,
    implementation requirements, and risks.
    """

    # 1. Create research plan
    planner = PlannerAgent()
    tasks = planner.run(query)

    print("\n===== RESEARCH PLAN =====\n")

    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task}")

    # 2. Research each task
    pipeline = ResearchPipeline()
    results = pipeline.run(tasks)

    print("\n===== RESEARCH RESULTS =====\n")

    for i, result in enumerate(results, start=1):

        print(f"\n--- Research {i} ---\n")
        print(result)


if __name__ == "__main__":
    main()