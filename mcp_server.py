from file_tools import FileTools
from pathlib import Path
import json


class MCPServer:
    def __init__(self, folder_name="test_folder"):
        self.tools = FileTools(folder_name)
        self.results = False

        # cell the server
        self.setup_server()

        # make a registry
        self.tool_registry = {
            "get_total_files": {
                "func": self.get_total_files,
                "description": "Returns the total number of files in the scanned folder.",
                "parameters": {},  # No input needed
            },
            "get_total_size": {
                "func": self.get_total_size,
                "description": "Returns the total size of the folder in a human-readable format (MB/KB).",
                "parameters": {},
            },
            "get_largest_file": {
                "func": self.get_largest_file,
                "description": "Identifies and returns the details of the largest file found.",
                "parameters": {},
            },
            "get_category_count": {
                "func": self.get_category_count,
                "description": "Returns the count of files for a specific category (e.g., 'Images', 'Docs').",
                "parameters": {
                    "category": "string",  # Ai must know that the parameter is string
                },
            },
            "get_summary": {
                "func": self.get_summary,
                "description": "Returns a complete overview of the folder analysis.",
                "parameters": {},
            },
        }

    def setup_server(self):
        print("Indexing Folder, please wait...")
        self.results = self.tools.analyze_folder()
        print("Server is ready..")

    def get_total_files(self) -> int:
        return self.results["total_files"]

    def get_total_size(self) -> str:
        return self.tools.size_converter(self.results["total_size"])

    def get_largest_file(self) -> str:
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

    def get_category_count(self, category):
        if category not in self.results["counts"]:
            return f"Category is not found : {category}"
        return self.results["counts"].get(category)

    def get_summary(self) -> str:
        return self.tools.presentation()

    def get_tools(self):
        return [
            {
                "name": name,
                "description": info["description"],
                "input_schema": info["parameters"],
            }
            for name, info in self.tool_registry.items()
        ]

    def execute_tool(self, tool_name: str, args: dict = None):
        if tool_name not in self.tool_registry:
            return f"Error: Tool '{tool_name}' is not registered."

        handler = self.tool_registry[tool_name]["func"]
        try:
            if args:
                return handler(**args)
            return handler()
        except Exception as e:
            return f"Execution Error: {str(e)}"
