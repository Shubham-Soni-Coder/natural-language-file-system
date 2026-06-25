from services import DBService
from pathlib import Path
import json
from utils import main_logger as logger
from sqlalchemy.orm import Session


class MCPRegistry:
    def __init__(self,db:Session,user_id:int):
        self.tools = DBService()
        self.db = db
        self.user_id=user_id

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
                "description": "Returns the count of files for a specific category or extension. Category can be a file type like python, image, video, document or a raw extension like py, txt, pdf.",
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
        logger.info("Server ready (Db-based mode)")

    def size_converter(self,size:int) -> str:
        logger.debug("size_converter called with size=%s byte s",size)
        if size < 0:
            logger.error("Invalid size : %s (cannot be negative)",size)
            raise ValueError("Size cannot be negative")
        
        units = ["B","KB","MB","GB","TB","PB"]
        index = 0 
        original_size = size # degging 

        try:
            while size>=1024 and index < len(units) -1:
                size /=1024
                index += 1 

            result = f"{size:.2f} {units[index]}"
            logger.debug(
                "Converted size: %s bytes -> %s",
                original_size,
                result
            )
            return result
        except Exception as e:
            logger.exception(
                "Error converting size=%s bytes:%s",
                original_size,
                str(e)
            )
            raise 

    def get_total_files(self) -> int:
        logger.debug("Retrieving total file count")
        return self.tools.get_total_files(self.db,self.user_id)
        

    def get_total_size(self) -> str:
        logger.debug("Retrieving total folder size")
        total_size = self.tools.get_total_size(self.db,self.user_id)
        return self.size_converter(total_size)

    def get_largest_file(self) -> str:
        logger.debug("Retrieving largest file details")
        largest = self.tools.get_largest_file(self.db,self.user_id)

        if not largest:
            logger.warning("No largest file found for user_id=%s",self.user_id)       
            return "No files found"
        
        size = self.size_converter(largest.size)

        logger.debug(
            "Largest file: name=%s , size=%s , path=%s",
            largest.name,
            size,
            largest.path
        )

        return f"""
        Largest File:
        Name: {largest.name}
        Size: {size}
        Location: {largest.path}
        """

    def get_category_count(self, category):
        logger.debug("Retrieving category count: %s",category)

        return self.tools.get_category_count(
            self.db,
            self.user_id,
            category
        )

    def get_summary(self) -> str:
        logger.debug("Generating summary report")
        stats = self.tools.get_summary_stats(self.db,self.user_id)

        total_files = stats["total_file"]
        total_size = self.size_converter(stats["total_size"])
        largest = stats["largest_file"]
        category_counts = stats.get("category_counts",{})

        largest_name = largest.get("name","None")
        largest_size = self.size_converter(largest.get("size",0))
        largest_path = largest.get("path","N/A")

        # forment category section 
        if category_counts:
            category_str = "\n".join(
            [f"  - {ext}: {count}" for ext, count in category_counts.items()]
        )
        else:
            category_str = "  No categories found"

        summary = (
            "\n========== FILE SYSTEM SUMMARY ==========\n"
            f"Total Files   : {total_files}\n"
            f"Total Size    : {total_size}\n"
            "\n--- Largest File ---\n"
            f"Name          : {largest_name}\n"
            f"Size          : {largest_size}\n"
            f"Path          : {largest_path}\n"
            "\n--- Category Breakdown ---\n"
            f"{category_str}\n"
            "========================================="
        )

        logger.debug("Summary generated successfully")

        return summary


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
