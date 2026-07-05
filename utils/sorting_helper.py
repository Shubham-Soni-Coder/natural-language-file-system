from .category_helpers import normalize_category
from utils import main_logger as logger
from pathlib import Path
import shutil



def get_category_from_extension(extension: str) -> str:
    if extension is None:
        logger.debug("Sorting helper: get_category_from_extension received None")
        return None

    normalized_extension = normalize_category(extension)
    mapping = {
        "python": ["py", "pyw"],
        "image": ["jpg", "jpeg", "png", "gif", "bmp", "webp", "svg"],
        "video": ["mp4", "mov", "mkv", "avi", "webm", "flv", "wmv"],
        "document": ["pdf", "doc", "docx", "md", "xls", "xlsx", "ppt", "pptx", "odt"],
        "text": ["txt", "md", "rtf"],
        "audio": ["mp3", "wav", "aac", "flac", "ogg", "m4a"],
        "archive": ["zip", "tar", "gz", "rar", "7z", "bz2"],
        "code": ["js", "ts", "java", "cs", "cpp", "c", "rb", "go", "rs", "php", "swift", "kt", "kts"],
    }

    for category, extensions in mapping.items():
        if normalized_extension in extensions:
            logger.debug(
                "category_helpers: get_category_from_extension for '%s' returned '%s'",
                normalized_extension,
                category,
            )
            return category

    logger.debug(
        "category_helpers: get_category_from_extension did not find category for '%s'",
        normalized_extension,
    )
    return "extra"


def move_file(file_path:str,folder:str,report:dict):
    source_path = Path(file_path).expanduser()
    if not source_path.exists():
        logger.warning("Sorting helper: source file does not exist -> %s", source_path)
        report['failed'].append({
            "name": source_path.name,
            "reason": "Source file does not exist"
        })
        return {
            "status":"failed",
            "reason":"Source file does not exist"
        }

    source_path = source_path.resolve()
    folder_path = source_path.parent
    file_name = source_path.name

    if not folder:
        logger.warning("This %s have folder_path :  %s , so change to extra", file_name,folder)
        folder = "extra"

    destination_folder = folder_path / folder
    new_file_path = destination_folder / file_name

    if not destination_folder.exists():
        logger.info("Created destination folder : %s",destination_folder)
        destination_folder.mkdir(parents=True,exist_ok=True)
    
    if new_file_path.exists():
        logger.info("Skipped : %s already exist",str(new_file_path.name))
        report['skipped'].append({
            "name":new_file_path.name,
            "reason":"File already exists"
        })
        return {
            "status":"Skipped",
            "Reason":"File already exists"
        }

    try:
        shutil.move(str(file_path),str(new_file_path))
        logger.info("Moved : %s succesfully moved",new_file_path.name)
        report['moved'].append({"name":new_file_path.name,
            "reason":"File succesfullly moved"
            })
        return {
            "status":"success",
            "old_path":str(source_path),
            "new_path":str(new_file_path),
            "new_parent":str(new_file_path.parent)
        }
    except Exception as e:
        logger.error("Error: %s not moved. Reason: %s",new_file_path.name,str(e))
        report['failed'].append({
            "name":new_file_path.name,
            "reason":str(e)
        })
        return {
            "status":"Error",
            "reason":str(e)
        }
    

def start_sort(result):
    report = {
        "moved": [],
        "skipped": [],
        "failed": [],
    }
    moved_files = []

    for data in result:
        extension = getattr(data, "extension", None)
        if extension is None and isinstance(data, (tuple, list)):
            extension = data[1]

        path = getattr(data, "path", None)
        if path is None and isinstance(data, (tuple, list)):
            path = data[0]

        if path is None:            
            logger.warning("Sorting helper: skipping item with missing path -> %s", data)
            report['failed'].append({
                "name": "unknown",
                "reason": "Missing path"
            })
            continue

        if extension is None:
            logger.warning("Sorting helper: skipping item with missing extension -> %s", path)
            report['failed'].append({
                "name": Path(path).name,
                "reason": "Missing extension"
            })   
            continue    

        folder_type = get_category_from_extension(extension)
        status = move_file(path, folder_type,report)

        if status.get("status") == "success":
            moved_files.append(status)
    return report , moved_files