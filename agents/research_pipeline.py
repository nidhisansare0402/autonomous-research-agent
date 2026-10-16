from agents.researcher import ResearchAgent


class ResearchPipeline:

    def __init__(self):
        self.researcher = ResearchAgent()

    def run(self, tasks: list[str]) -> list[str]:

        results = []

        for index, task in enumerate(tasks, start=1):

            print(f"\nResearching task {index}/{len(tasks)}...")
            print(f"Task: {task}")

            result = self.researcher.run(task)

            results.append(result)

        return results