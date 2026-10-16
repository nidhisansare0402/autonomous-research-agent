from agents.planner import PlannerAgent


def main():

    planner = PlannerAgent()

    query = """
    Should an enterprise customer support system use
    Retrieval-Augmented Generation (RAG)?
    Analyze the benefits, limitations, alternatives,
    implementation requirements, and risks.
    """

    tasks = planner.run(query)

    print("\n===== PLANNER OUTPUT =====\n")

    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task}")


if __name__ == "__main__":
    main()