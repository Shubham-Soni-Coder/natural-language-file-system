from file_tools import FileTools
from pathlib import Path
from ai_data import AiHandler


class QueryHandler:
    def __init__(self, folder: Path):
        self.tools = FileTools(folder)
        self.ai = AiHandler()
        print("Scanning Folder,Please wait...")
        self.results = self.tools.analyze_folder()

    def process_query(self, user_input):
        ai_response = self.ai.run_ai(user_input)
        if ai_response is None:
            print("Error: ai respone is none")
            return None

        intent = ai_response["intent"].lower()
        argument = ai_response["argument"]

        if intent == "category" and argument is None:
            print("Missing Category")
            return None

        intent_map = {
            "total": self.handle_total,
            "size": self.handle_size,
            "largest": self.handle_largest,
            "summary": self.handle_summary,
            "category": self.handle_category,
        }

        handler = intent_map.get(intent)
        if handler:
            print(handler(argument))
        else:
            print("Unknown Intent: ", intent)

    def handle_total(self, arg=None):
        return f"Total Files: {self.results['total_files']}"

    def handle_size(self, arg=None):
        return f"Total Size: {self.tools.size_converter(self.results['total_size'])}"

    def handle_largest(self, arg=None):
        path_name = Path(self.results["largest_file"]["path"])
        if not path_name:
            return "No files found"
        size = self.tools.size_converter(self.results["largest_file"]["size"])
        return f"""
        Largest File:
        Name: {path_name.name}
        Size: {size}
        Location: {path_name}
        """

    def handle_category(self, category: str):
        if category in self.results["counts"].keys():
            return f"Total {category.title()}: {self.results['counts'][category]}"
        else:
            return f"Invalid category. Available: {self.results['counts'].keys()}"

    def handle_summary(self, arg=None):
        return self.tools.presentation()

    def runner(self):
        while True:
            try:
                user_input = input("\nEnter your query (or 'exit'): ").strip()
                if user_input == "exit":
                    print("Byy..")
                    break
                if not user_input:
                    continue

                self.process_query(user_input)

            except KeyboardInterrupt:
                break
            except Exception as error:
                print(error)


if __name__ == "__main__":
    QueryHandler(Path("test_folder")).runner()
