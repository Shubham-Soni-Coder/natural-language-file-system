from sqlalchemy.orm import Session
from sqlalchemy import func, select,desc
from models import File,Task
from utils import main_logger as logger
from typing import Optional

class DBService:
    """
    Service layer for database-wide aggregation and complex queries.
    Used by MCP Registry to provide real-time stats from the database.
    """

    @staticmethod
    def file_filters(user_id: int):
        """Return common filters used for file-only queries."""
        filters = [
            File.user_id == user_id,
            File.is_folder == False,
        ]
        logger.debug("DBService: Using file-only filters for user_id=%s", user_id)
        return filters

    @staticmethod
    def get_total_files(db: Session, user_id: int) -> int:
        logger.debug("DBService: Counting total files for user_id=%s", user_id)
        stmt = select(func.count()).select_from(File).where(*DBService.file_filters(user_id))
        return db.execute(stmt).scalar_one()

    @staticmethod
    def get_total_size(db: Session, user_id: int) -> int:
        logger.debug("DBService: Calculating total size for user_id=%s", user_id)
        stmt = select(func.sum(File.size)).where(*DBService.file_filters(user_id))
        return db.execute(stmt).scalar_one() or 0


    @staticmethod
    def get_largest_file(db: Session, user_id: int) -> Optional[File]:
        logger.debug("DBService: Fetching largest file for user_id=%s", user_id)
        stmt = select(File).where(*DBService.file_filters(user_id)).order_by(desc(File.size)).limit(1)
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def normalize_category(category: str) -> str:
        if category is None:
            logger.debug("DBService: normalize_category received None")
            return ""

        normalized = category.strip().lower().lstrip(".")
        logger.debug(
            "DBService: normalize_category transformed '%s' to '%s'",
            category,
            normalized,
        )
        return normalized

    @staticmethod
    def get_extensions_for_category(category: str) -> list[str] | None:
        mapping = {
            "python": ["py", "pyw"],
            "image": ["jpg", "jpeg", "png", "gif", "bmp", "webp", "svg"],
            "video": ["mp4", "mov", "mkv", "avi", "webm", "flv", "wmv"],
            "documents": ["pdf", "doc", "docx", "txt", "md", "xls", "xlsx", "ppt", "pptx", "odt"],
            "document": ["pdf", "doc", "docx", "txt", "md", "odt"],
            "text": ["txt", "md", "rtf"],
            "audio": ["mp3", "wav", "aac", "flac", "ogg", "m4a"],
            "archive": ["zip", "tar", "gz", "rar", "7z", "bz2"],
            "code": ["py", "js", "ts", "java", "cs", "cpp", "c", "rb", "go", "rs", "php", "swift", "kt", "kts"],
        }
        extensions = mapping.get(category)
        logger.debug(
            "DBService: get_extensions_for_category for '%s' returned %s",
            category,
            extensions,
        )
        return extensions

    @staticmethod
    def get_category_count(db: Session, user_id: int, category_ext: str) -> int:
        normalized = DBService.normalize_category(category_ext)
        logger.debug("DBService: Fetching count for category input: %s, normalized: %s", category_ext, normalized)

        if not normalized:
            logger.warning("DBService: Empty category provided for count query")
            return 0

        extensions = DBService.get_extensions_for_category(normalized)
        if extensions:
            logger.info(
                "DBService: Counting files for category '%s' using extensions %s",
                normalized,
                extensions,
            )
            stmt = select(func.count()).where(
                *DBService.file_filters(user_id),
                File.extension.in_(extensions),
            )
        else:
            logger.info(
                "DBService: Counting files for raw extension '%s'",
                normalized,
            )
            stmt = select(func.count()).where(
                *DBService.file_filters(user_id),
                File.extension == normalized,
            )

        count = db.execute(stmt).scalar_one()
        logger.debug("DBService: get_category_count result=%s for user_id=%s", count, user_id)
        return count

    @staticmethod 
    def get_all_category_count(db:Session,user_id:int)->dict:
        """"""
        stmt = select(
            File.extension,
            func.count().label("count")
        ).where(
            *DBService.file_filters(user_id)
        ).group_by(File.extension)

        result = db.execute(stmt).all()
        
        return {ext:count for ext,count in result}

    @staticmethod
    def get_summary_stats(db: Session, user_id: int) -> dict:
        """
        Returns a combined dictionary of stats, similar to what FileUtils.analyze_folder did.
        """ 
        total_file = DBService.get_total_files(db,user_id)
        total_size = DBService.get_total_size(db,user_id)
        largest = DBService.get_largest_file(db,user_id)
        category_count = DBService.get_all_category_count(db,user_id)

        return {
            "total_file":total_file,
            "total_size":total_size,
            "largest_file":{
                "name": largest.name if largest else "None",
                "size":largest.size if largest else 0 ,
                "path":largest.path if largest else "N/A"
            },
            "category_counts":category_count
        }