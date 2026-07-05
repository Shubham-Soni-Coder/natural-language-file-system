from utils import main_logger as logger


def normalize_category(category: str) -> str:
    if category is None:
        logger.debug("category_helpers: normalize_category received None")
        return ""

    normalized = category.strip().lower().lstrip(".")
    logger.debug(
        "category_helpers: normalize_category transformed '%s' to '%s'",
        category,
        normalized,
    )
    return normalized


def get_extensions_for_category(category: str) -> list[str] | None:
    mapping = {
        "python": ["py", "pyw"],
        "image": ["jpg", "jpeg", "png", "gif", "bmp", "webp", "svg"],
        "video": ["mp4", "mov", "mkv", "avi", "webm", "flv", "wmv"],
        "document": ["pdf", "doc", "docx", "txt", "md", "xls", "xlsx", "ppt", "pptx", "odt"],
        "text": ["txt", "md", "rtf"],
        "audio": ["mp3", "wav", "aac", "flac", "ogg", "m4a"],
        "archive": ["zip", "tar", "gz", "rar", "7z", "bz2"],
        "code": ["py", "js", "ts", "java", "cs", "cpp", "c", "rb", "go", "rs", "php", "swift", "kt", "kts"],
    }
    extensions = mapping.get(category)
    logger.debug(
        "category_helpers: get_extensions_for_category for '%s' returned %s",
        category,
        extensions,
    )
    return extensions
