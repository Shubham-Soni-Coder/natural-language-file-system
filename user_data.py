from file_tools import FileTools
from pathlib import Path


class QueryHandler:
    def __init__(self, folder: Path):
        self.tools = FileTools(folder)
        print("Scanning Folder,Please wait...")
        self.results = self.tools.analyze_folder()

    def process_query(self, user_input):

        # Mapping
        query_map = {
            "total": self.handle_total,
            "size": self.handle_size,
            "largest": self.handle_largest,
            "image": lambda: self.handle_category("image"),
            "video": lambda: self.handle_category("video"),
            "document": lambda: self.handle_category("documents"),
        }

        user_input = user_input.lower()

        if "summary" in user_input or "all" in user_input:
            print(self.handle_summary())
            return

        # user unput
        found = False
        for key, value in query_map.items():
            if key in user_input:
                result = value()
                print(result)
                found = True
                break

        if not found:
            print("Invalid query")

    def handle_total(self):
        return f"Total Files: {self.results['total_files']}"

    def handle_size(self):
        return f"Total Size: {self.tools.size_converter(self.results['total_size'])}"

    def handle_largest(self):
        path_name = Path(self.results["largest_file"]["path"])
        if path_name == "":
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

    def handle_summary(self):
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
