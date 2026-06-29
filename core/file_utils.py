from pathlib import Path
import hashlib
import mimetypes
from datetime import datetime
from typing import Generator,Dict,Optional
from utils import main_logger as logger

class FileUtils:
    
    def __init__(self, folder:str):
        self.folder = Path(folder)
        self.result = {}
        logger.info("Initializing FileUtils for folder: %s", folder)
        self.check_folder()

    def check_folder(self):
        if not self.folder.exists() or not self.folder.is_dir():
            logger.error(f"Invalid Folder : {self.folder}")
            raise FileNotFoundError(f"Folder Not Found : {self.folder}")

    def get_extension(self,path:Path)->str:
        if path.suffix:
            return path.suffix[1:].lower()
        elif path.name.startswith(".") or path.name.count(".") == 1:
            return path.name[1:].lower()
        return ""

    def get_mime_type(self,path:Path)->str:
        mime_type,_ = mimetypes.guess_type(str(path))
        return mime_type or "application/octet_stream"
    
    def get_file_size(self,path:Path)->int:
        return path.stat().st_size 

    def get_file_hash(self,path:Path,enable:bool=True)->Optional[str]:
        """Generate SHA256 hjashth hash of a file to check for uniquencess."""
        if not enable:
            return None

        sha256_hash = hashlib.sha256()
        try:
            with open(path,"rb") as f:
                while chunk := f.read(8192):
                    sha256_hash.update(chunk)
            file_hash = sha256_hash.hexdigest()
            return file_hash
        except Exception as e:
            logger.error("Error generating hash for %s:%s", path,e)
            return None
    
    def build_file_metadata(
        self, path: Path, include_hash: bool = False
    ) -> Dict: 
        try:
            resolved_path = path.resolve()
            parent = resolved_path.parent
            stat = path.stat()
            
            return {
                "name": path.name,
                "path": str(resolved_path),
                "parent_path": str(parent) if parent != resolved_path else None,
                "is_folder": path.is_dir(),
                "size": self.get_file_size(path) if path.is_file() else 0,
                "mime_type": self.get_mime_type(path) if path.is_file() else None,
                "extension": self.get_extension(path) if path.is_file() else None,
                "hash": self.get_file_hash(path, include_hash) if path.is_file() else None,
                "file_created_at":datetime.fromtimestamp(stat.st_ctime),
                "file_modified_at":datetime.fromtimestamp(stat.st_mtime)
            }
        except Exception as e:
            logger.error(f"Metadata error for {path}: {e}")
            return {}



    def scan(self, include_hash: bool = False) -> Generator[Dict, None, None]:
        logger.info(f"Scanning folder: {self.folder}")
        SKIP_FOLDERS = {
            "__pycache__",
            ".git",
            "venv",
            ".venv",
            "node_modules",
            ".env",
            ".gitignore",
            "logs",
        }

        for path in self.folder.rglob("*"):

            if any(folder in path.parts for folder in SKIP_FOLDERS):
                # logger.debug(f"Skipped '{path}' (reason: system/generated folder)")
                continue



            metadata = self.build_file_metadata(path, include_hash if path.is_file() else False)

            if metadata:  # skip broken files
                yield metadata
            else:
                # logger.warning(f"Skipped '{path}' (reason: metadata extraction failed)") 
                continue

        logger.info("Scanning completed")

if __name__ == "__main__":
    import csv 
    folder_path = "E:/File_mangement_system"
    output_csv = "File_metadata.csv"

    scanner = FileUtils(folder_path)
    result = scanner.scan(include_hash=False)
    
    headers = ["name","path","parent_path","is_folder","size","mime_type","extension","hash"]

    try:
        with open(output_csv,mode="w",newline="",encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file,fieldnames=headers)

            writer.writeheader()

            for metadata in result:
                filtered_metadata = {k: v for k,v in metadata.items() if k in headers}
                writer.writerow(filtered_metadata)
        print(f"Success!")
    except Exception as e:
        print(f"An error occurred while writing to csv : {e}")
