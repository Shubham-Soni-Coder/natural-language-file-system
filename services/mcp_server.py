from services import FileTools
from pathlib import Path
import json
from utils import main_logger as logger


class MCPServer:
    def __init__(self, folder_name="test_folder"):
        logger.info("Initializing MCPServer with folder: %s", folder_name)
        self.tools = FileTools(folder_name)
        self.results = False

        self.setup_server()

        self.tool_registry = {
            "get_total_files": {
                "func": self.get_total_files,
                "description": "Returns the total number of files in the scanned folder.",
                "parameters": {},
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
                    "category": "string",
                },
            },
            "get_summary": {
                "func": self.get_summary,
                "description": "Returns a complete overview of the folder analysis.",
                "parameters": {},
            },
        }

    def setup_server(self):
        logger.info("Indexing folder, please wait...")
        self.results = self.tools.analyze_folder()
        logger.info(
            "Server is ready with %s files, %s bytes scanned",
            self.results.get("total_files"),
            self.results.get("total_size"),
        )

    def get_total_files(self) -> int:
        logger.debug("Retrieving total file count")
        return self.results["total_files"]

    def get_total_size(self) -> str:
        logger.debug("Retrieving total folder size")
        return self.tools.size_converter(self.results["total_size"])

    def get_largest_file(self) -> str:
        logger.debug("Retrieving largest file details")
        path_name = Path(self.results["largest_file"]["path"])
        if not path_name:
            logger.warning("No largest file found in results")
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
            logger.warning("Requested invalid category: %s", category)
            return f"Category is not found : {category}"
        logger.debug("Retrieving count for category: %s", category)
        return self.results["counts"].get(category)

    def get_summary(self) -> str:
        logger.debug("Generating summary report")
        return self.tools.presentation()

    def get_tools(self):
        logger.debug("Fetching available tool registry")
        return [
            {
                "name": name,
                "description": info["description"],
                "input_schema": info["parameters"],
            }
            for name, info in self.tool_registry.items()
        ]

    def execute_tool(self, tool_name: str, args: dict = None):
        logger.info("Executing tool: %s with args: %s", tool_name, args)
        if tool_name not in self.tool_registry:
            logger.error("Tool not registered: %s", tool_name)
            return f"Error: Tool '{tool_name}' is not registered."

        handler = self.tool_registry[tool_name]["func"]
        try:
            if args:
                return handler(**args)
            return handler()
        except Exception as e:
            logger.exception("Execution failed for tool: %s", tool_name)
            return f"Execution Error: {str(e)}"
