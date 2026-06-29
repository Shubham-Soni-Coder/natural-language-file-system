from sqlalchemy.orm import Session
from sqlalchemy import func, select,desc,asc
from models import File,Task
from utils import main_logger as logger
from typing import Optional
from pathlib import Path
from collections import defaultdict

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
    def get_largest_files(db:Session,user_id:int,limit:int)->list[File]:
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
    def get_largest_folders(db:Session,user_id:int,target_path:str,limit:int):
        """
        Get the largest direcrt child folders
        
        Args:
            db:Database session
            user_id : user id
            target_path : Parent directory path.
            limit : Number of folders to return.

        Returns:
            list[tuple]:list of (folder_path,size) tuples.
        """

        logger.debug(
            "Retrieving top %s largest folders for user_id=%s",
            limit,
            user_id
        )
        
        stmt = (
            select(
                File.name,
                File.path,
                File.parent_path,
                File.size
            )
            .where(*DBService.base_filters(user_id,is_folder=False))
        )

        rows = db.execute(stmt).mappings().all()
        folder_data = defaultdict(int)
        target_path = Path(target_path)

        for row in rows:
            current_path = Path(row["parent_path"])
            
            while True:
                if not current_path.is_relative_to(target_path):
                    break
                folder_data[current_path] += row["size"]
                if current_path == target_path:
                    break
                current_path = current_path.parent
            
        clean_data = {
            key:value
            for key,value in folder_data.items()
            if key!= target_path
            }
        sorted_data =  sorted(
            clean_data.items(),
            key=lambda item:item[1],
            reverse=True
        )
        logger.info("Sorted data created : %d",len(sorted_data))
        result = DBService.build_folder_response(db,user_id,sorted_data)

        logger.info("Retrived %d largest folders",limit)
        
        return result[:limit]


    @staticmethod
    def get_largest_folder(db:Session,user_id:int,target_path:str):
        """
            get the largest direct child folder.

            Args:
                db:Database session.
                user_id : User id.
                targest_path : Parent directory path
            
            Returns:
                tuple | None:
            (folder_path,size) or None if no folder exists.
        """
        logger.debug(
            "Retrueving largest folder for user_id=%s , target_path=%s",user_id,target_path
        )
        largest_folder = DBService.get_largest_folders(db,user_id,target_path,1)[0]
        logger.info("Largest folder retrived successfully with largest file:%s",largest_folder)
        return largest_folder

    @staticmethod
    def build_folder_response(
        db:Session,
        user_id:int,
        sorted_data:list[tuple[Path,int]]
    ) -> list[dict]:
        paths = [str(path) for path,_ in sorted_data]
        stmt = (
            select(
                File.name,
                File.path,
                File.parent_path
            ).where(
                *DBService.base_filters(user_id,is_folder=True),
                File.path.in_(paths)
                )
            )
        rows = db.execute(stmt).mappings().all()

        folder_map = {
            row["path"]:row
            for row in rows
        }
        logger.debug("Folder_map created : %d",len(folder_map))
        result = []

        for path,size in sorted_data:
            folder = folder_map.get(str(path))

            if folder is None:
                result.append({
                    "name":path.name,
                    "path":str(path),
                    "parent_path":str(path.parent),
                    "size":size
                })
            
            else:    
                result.append({
                    "name": folder["name"],
                    "path": folder["path"],
                    "parent_path": folder["parent_path"],
                    "size":size
                })
        
        logger.debug("Result generated : %d",len(result))
        return result



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
    def get_newest_file(db:Session,user_id:int) -> str:
        """
            Return the newest file for the given user.
            Args:
                db: Active database session.
                user_id: ID of the user whose files are retrieved.
            Returns:
                File | None: The newest file object if found otherwise None.
        """
        stmt = (
            select(File).where(
            *DBService.base_filters(user_id,is_folder=None))
            .order_by(desc(File.file_created_at))
            .limit(1)
        )

        return db.execute(stmt).scalars().one()

    @staticmethod
    def get_oldest_file(db:Session,user_id:int) -> str:
        """
        Return the oldest file for the given user.
        Args:
            db: Active database session.
            user_id: ID of the user whose files are retrieved.
        Return:
            File | None:
                The oldest file object if fount : otherwise None.
        """
        stmt = (
            select(File)
            .where(*DBService.base_filters(user_id,is_folder=None))
            .order_by(asc(File.file_created_at))
            .limit(1)
        )
        return db.execute(stmt).scalars().one()
        

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
    
    # def get_newest_file()...