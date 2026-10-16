from dotenv import load_dotenv

load_dotenv()

from graph.workflow import build_workflow


def main():

    workflow = build_workflow()

    initial_state = {
        "user_query": "What are the main benefits and limitations of RAG?"
    }

    result = workflow.invoke(initial_state)

    print("\n==============================")
    print("       FINAL WORKFLOW STATE")
    print("==============================\n")

    print("Research Tasks:")
    for task in result.get("research_tasks", []):
        print("-", task)

    print("\nAnalysis:")
    print(result.get("analysis"))

    print("\nCritique:")
    print(result.get("critique"))

    print("\nRevision Count:")
    print(result.get("revision_count"))

    print("\n===== FINAL ANSWER =====\n")
    print(result.get("final_answer"))

    

if __name__ == "__main__":
    main()