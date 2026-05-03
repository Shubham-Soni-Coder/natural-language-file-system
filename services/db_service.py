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
    def get_total_files(db: Session, user_id: int) -> int:
        logger.debug("DBService: Counting total files for user_id=%s", user_id)
        stmt = select(func.count()).select_from(File)
        return db.execute(stmt).scalar_one()

    @staticmethod
    def get_total_size(db: Session, user_id: int) -> int:
        logger.debug("DBService: Calculating total size for user_id=%s", user_id)
        stmt = select(func.sum(File.size))
        return db.execute(stmt).scalar_one() or 0


    @staticmethod
    def get_largest_file(db: Session, user_id: int) -> Optional[File]:
        logger.debug("DBService: Fetching largest file for user_id=%s", user_id)
        stmt = select(File).order_by(desc(File.size)).limit(1)
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_category_count(db: Session, user_id: int, category_ext: str) -> int:
        logger.debug("DBService: Fetching count for category (ext): %s", category_ext)
        stmt = select(func.count()).where(
            File.extension == category_ext.lower(),
            File.user_id == user_id
        )
        return db.execute(stmt).scalar_one()

    @staticmethod 
    def get_all_category_count(db:Session,user_id:int)->dict:
        """"""
        stmt = select(
            File.extension,
            func.count().label("count")
        ).where(
            File.user_id == user_id
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
            }
        }