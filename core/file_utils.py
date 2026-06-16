from pathlib import Path
import hashlib
import mimetypes
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
        return path.suffix.lower().replace(".","")
    
    def get_mine_type(self,path:Path)->str:
        mime_type,_ = mimetypes.guess_type(str(path))
        return mime_type or "applcation/octet_stream"
    
    def get_file_size(self,path:Path)->str:
        return path.stat().st_size

    def get_file_hash(self,path:Path,enable:bool=True)->Optional[str]:
        """Generate SHA256 hjashth hash of a file to check for uniquencess."""
        if not enable:
            return None

        sha256_hash = hashlib.sha256()
        try:
            with open(file_path,"rb") as f:
                while chunk := f.read(8192):
                    sha256_hash.update(chunk)
            file_hash = sha256_hash.hexdigest()
            return file_hash
        except Exception as e:
            logger.error("Error generating hash for %s:%s", file_path,e)
            return None
    
    def build_file_metadata(
        self, path: Path, include_hash: bool = False
    ) -> Dict:

        try:
            return {
                "name": path.name,
                "path": str(path.resolve()),
                "size": self.get_file_size(path),
                "mime_type": self.get_mine_type(path),
                "extension": self.get_extension(path),
                "hash": self.get_file_hash(path, include_hash),
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
            ".env"
        }

        for path in self.folder.rglob("*"):

            if any(folder in path.parts for folder in SKIP_FOLDERS):
                # logger.debug(f"Skipped '{path}' (reason: system/generated folder)")
                continue


            if path.is_file():
                metadata = self.build_file_metadata(path, include_hash)

                if metadata:  # skip broken files
                    yield metadata
                else:
                    # logger.warning(f"Skipped '{path}' (reason: metadata extraction failed)") 
                    continue

        logger.info("Scanning completed")

if __name__ == "__main__":
    folder_path = "E:/File_mangement_system"
    scanner = FileUtils(folder_path)
    result = scanner.scan(include_hash=False)
    for metadata in result:
        print(metadata)
