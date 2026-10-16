from agents.researcher import ResearchAgent


def main():

    researcher = ResearchAgent()

    task = """
    Analyze the main benefits of using Retrieval-Augmented Generation
    for an enterprise customer-support system.
    """

    result = researcher.run(task)

    print("\n===== RESEARCH RESULT =====\n")
    print(result)


if __name__ == "__main__":
    main()