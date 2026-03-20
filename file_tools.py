import os
from pathlib import Path
import random
from string import ascii_letters


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
        # cheker
        self.check_folder()

    def check_folder(self):
        if not isinstance(self.folder_name, Path):
            self.folder_name = Path(self.folder_name)
        if not os.path.exists(self.folder_name):
            raise FileNotFoundError("Folder not found")

    def analyze_folder(self):

        for path in self.folder_name.rglob("*"):
            if path.is_file():
                size = path.stat().st_size
                self.results["total_files"] += 1
                self.results["total_size"] += size
                self.category_files(path)
                self.largest_file(path, size)

        return self.results

    def category_files(self, path: Path) -> None:
        """
        Category files by extension
        """
        ext = (
            path.suffix.lower()
        )  # so that we can compare it with the extensions in the dictionary
        found = False
        for cat, ext_set in self.extensions.items():
            if ext in ext_set:
                self.results["counts"][cat] += 1
                found = True
                break
        if not found:
            self.results["counts"]["extra"] += 1

    def largest_file(self, path, size) -> None:
        """
        Find the largest files in a folder and its subfolders.
        """
        current_max_size = self.results["largest_file"]["size"]

        if size > current_max_size:
            self.results["largest_file"]["path"] = str(path)
            self.results["largest_file"]["size"] = size

    def size_converter(self, size=None) -> str:
        if size is None:
            size = self.results["largest_file"]["size"]
        # logic
        for unit in ["bytes", "KB", "MB", "GB", "TB"]:
            if size < 1024:
                return f"{size:.2f} {unit}" if unit != "bytes" else f"{size} {unit}"
            size /= 1024

        return f"{size:.2f} PB"

    def presentation(self):
        res = self.results

        # Values ko variables mein nikalna taaki f-string ganda na dikhe
        total_files = res["total_files"]
        total_size = self.size_converter(res["total_size"])

        # Categories
        img = res["counts"]["image"]
        vid = res["counts"]["video"]
        doc = res["counts"]["documents"]
        oth = res["counts"]["extra"]

        # Largest File Details
        # Path se sirf file ka naam nikalne ke liye .name use karein
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

        return self.report

    def main(self):
        self.analyze_folder()
        print(self.presentation())


if __name__ == "__main__":
    folder_name = Path("test_folder")
    tools = FileTools(folder_name)
    # FileTools(folder_name).find_files_by_extension(".txt")
    tools.main()
