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
    def base_filters(user_id: int,is_folder:bool |None = None ):
        """
        Return the common database filters for a user's records.

        Args:
            user_id: ID of the user whose records are filtered.

        Returns:
            A list of SQLAlchemy filter expressions.
        """
        filters = [
            File.user_id == user_id,
        ]
        logger.debug("Creating base filters for user_id=%s", user_id)

        if is_folder is not None:
            filters.append(File.is_folder.is_(is_folder))

        return filters

    @staticmethod
    def get_total_files(db: Session, user_id: int) -> int:
        logger.debug("DBService: Counting total files for user_id=%s", user_id)
        stmt = select(func.count()).select_from(File).where(*DBService.base_filters(user_id,is_folder=False))
        return db.execute(stmt).scalar_one()

    @staticmethod
    def get_total_size(db: Session, user_id: int) -> int:
        logger.debug("DBService: Calculating total size for user_id=%s", user_id)
        stmt = select(func.sum(File.size)).where(*DBService.base_filters(user_id,is_folder=None))
        return db.execute(stmt).scalar_one() or 0

    @staticmethod
    def get_largest_files(db:Session,user_id:int,limit:int=5)->list[File]:
        """
        Return the largest files for a user.

        Args:
            db: Active database session.
            user_id: ID of the user whose files are retrieved.
            limit: Maximum number of files to return.

        Returns:
            list[File]: Files ordered by size in descending order.
        """
        logger.debug(
            "DBService: Fetching %d largest files for user_id=%s",
            limit,
            user_id,
        )

        stmt = (
        select(File)
        .where(*DBService.base_filters(user_id, is_folder=False))
        .order_by(desc(File.size))
        .limit(limit)
        )

        return db.execute(stmt).scalars().all()


    @staticmethod
    def get_largest_file(db: Session, user_id: int) -> Optional[File]:
        """
        Return the largest file for a user.

        Args:
            db: Active database session.
            user_id: ID of the user whose largest file is retrieved.

        Returns:
            Optional[File]: The largest file, or None if no files exist.
        """
        logger.debug("DBService: Fetching largest file for user_id=%s", user_id)

        files = DBService.get_largest_files(db, user_id, limit=1)
        return files[0] if files else None

    @staticmethod
    def get_folder_count(db:Session,user_id:int) -> int:
        logger.debug("Counting folders for user_id=%s", user_id)
        """
        Return the total number of folders for a user.

        Args:
            db: Active database session.
            user_id: ID of the user whose folders are counted.

        Returns:
            Total number of folders.
        """
        stmt = (
            select(func.count())
            .where(
                File.is_folder.is_(True),
                *DBService.base_filters(user_id)
            )
        )

        return db.execute(stmt).scalar_one()


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
                *DBService.base_filters(user_id),
                File.extension.in_(extensions),
            )
        else:
            logger.info(
                "DBService: Counting files for raw extension '%s'",
                normalized,
            )
            stmt = select(func.count()).where(
                *DBService.base_filters(user_id,is_folder=None),
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
            *DBService.base_filters(user_id)
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