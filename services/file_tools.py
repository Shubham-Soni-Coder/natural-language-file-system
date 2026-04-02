import logging
import os
from pathlib import Path
import random
from string import ascii_letters
from utils import main_logger as logger


class FileTools:
    extensions = {
        "image": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"},
        "video": {".mp4", ".avi", ".mkv", ".mov", ".wmv"},
        "documents": {
            ".pdf",
            ".doc",
            ".docx",
            ".txt",
            ".xls",
            ".xlsx",
            ".ppt",
            ".pptx",
        },
    }

    def __init__(self, folder_name: Path):
        self.folder_name = folder_name
        self.results = {
            "counts": {"image": 0, "video": 0, "documents": 0, "extra": 0},
            "total_files": 0,
            "total_size": 0,
            "files": [],
            "largest_file": {"path": "", "size": 0},
        }
        logger.info("Initializing FileTools for folder: %s", folder_name)
        self.check_folder()

    def check_folder(self):
        if not isinstance(self.folder_name, Path):
            self.folder_name = Path(self.folder_name)
        logger.debug("Checking folder path: %s", self.folder_name)
        if not os.path.exists(self.folder_name):
            logger.error("Folder not found: %s", self.folder_name)
            raise FileNotFoundError("Folder not found")

    def analyze_folder(self):
        logger.info("Starting folder analysis: %s", self.folder_name)
        for path in self.folder_name.rglob("*"):
            if path.is_file():
                size = path.stat().st_size
                self.results["total_files"] += 1
                self.results["total_size"] += size
                self.category_files(path)
                self.largest_file(path, size)

        logger.info(
            "Folder analysis complete: %s files, %s bytes total",
            self.results["total_files"],
            self.results["total_size"],
        )
        return self.results

    def category_files(self, path: Path) -> None:
        """
        Category files by extension
        """
        ext = path.suffix.lower()
        logger.debug("Categorizing file %s with extension %s", path, ext)
        found = False
        for cat, ext_set in self.extensions.items():
            if ext in ext_set:
                self.results["counts"][cat] += 1
                found = True
                break
        if not found:
            self.results["counts"]["extra"] += 1
            logger.debug("File categorized as extra: %s", path)

    def largest_file(self, path, size) -> None:
        """
        Find the largest files in a folder and its subfolders.
        """
        current_max_size = self.results["largest_file"]["size"]
        if size > current_max_size:
            self.results["largest_file"]["path"] = str(path)
            self.results["largest_file"]["size"] = size
            logger.debug("New largest file found: %s (%s bytes)", path, size)

    def size_converter(self, size=None) -> str:
        if size is None:
            size = self.results["largest_file"]["size"]
        for unit in ["bytes", "KB", "MB", "GB", "TB"]:
            if size < 1024:
                result = f"{size:.2f} {unit}" if unit != "bytes" else f"{size} {unit}"
                logger.debug("Converted size %s to %s", size, result)
                return result
            size /= 1024

        result = f"{size:.2f} PB"
        logger.debug("Converted size to %s", result)
        return result

    def presentation(self):
        res = self.results
        total_files = res["total_files"]
        total_size = self.size_converter(res["total_size"])

        img = res["counts"]["image"]
        vid = res["counts"]["video"]
        doc = res["counts"]["documents"]
        oth = res["counts"]["extra"]

        path_str = res["largest_file"]["path"]
        l_file_name = Path(path_str) if path_str else "None"
        l_file_size = self.size_converter(res["largest_file"]["size"])

        self.report = f"""
        Folder Report


        Total Files : {total_files}
        Total Size  : {total_size}

        Categories:
        - Images    : {img}
        - Videos    : {vid}
        - Documents : {doc}
        - Others    : {oth}

        Largest File:
        {l_file_name.name} ({l_file_size})
        {"="*30}
        """

        logger.info("Folder report generated")
        return self.report

    def main(self):
        self.analyze_folder()
        report = self.presentation()
        logger.info("FileTools main completed and report generated")
        print(report)


if __name__ == "__main__":
    folder_name = Path("test_folder")
    tools = FileTools(folder_name)
    tools.main()
