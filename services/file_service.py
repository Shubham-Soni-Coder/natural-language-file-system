from sqlalchemy.orm import Session
from models import File
from schemas import FileCreate, FileResponse
from utils import main_logger as logger


class FileService:
    """
    Handles File database operations.
    Abstracts database queries from routes for clean separation of concerns.
    """

    @staticmethod
    def get_all(db: Session):
        """
        Fetch all files from database.
        
        Args:
            db: Database session
            
        Returns:
            List of all File records
        """
        logger.info("FileService: Fetching all files")
        files = db.query(File).all()
        logger.debug("FileService: Retrieved %s files", len(files))
        return files

    @staticmethod
    def get_by_user(db: Session, user_id: int):
        """
        Fetch all files belonging to a specific user.
        
        Args:
            db: Database session
            user_id: User ID to filter by
            
        Returns:
            List of File records for the user
        """
        logger.info("FileService: Fetching files for user_id=%s", user_id)
        files = db.query(File).filter(File.user_id == user_id).all()
        logger.debug("FileService: Found %s files for user_id=%s", len(files), user_id)
        return files

    @staticmethod
    def create(db: Session, data: FileCreate):
        """
        Create a new file record in the database.
        
        Args:
            db: Database session
            data: FileCreate schema with filename and user_id
            
        Returns:
            Created File record
        """
        logger.info("FileService: Creating file record: %s for user %s", data.name, data.user_id)
        file = File(name=data.name,
                    path=data.path,
                    size=data.size,
                    mime_type=data.mime_type,
                    extension=data.extension,
                    hash=data.hash,
                    user_id=data.user_id,
                    status=data.status)
        db.add(file)
        db.commit()
        db.refresh(file)
        logger.debug("FileService: Created file id: %s", file.id)
        return file

    @staticmethod
    def delete(db: Session, file_id: int):
        """
        Delete a file record from the database.
        
        Args:
            db: Database session
            file_id: ID of file to delete
            
        Returns:
            Boolean indicating success
        """
        logger.info("FileService: Deleting file id=%s", file_id)
        file = db.query(File).filter(File.id == file_id).first()
        
        if not file:
            logger.warning("FileService: File not found for deletion: id=%s", file_id)
            return False
        
        db.delete(file)
        db.commit()
        logger.debug("FileService: File deleted successfully: id=%s", file_id)
        return True

    @staticmethod
    def update(db: Session, file_id: int, data: dict):
        """
        Update a file record.
        
        Args:
            db: Database session
            file_id: ID of file to update
            data: Dictionary of fields to update
            
        Returns:
            Updated File record or None if not found
        """
        logger.info("FileService: Updating file id=%s with data: %s", file_id, data)
        file = db.query(File).filter(File.id == file_id).first()
        
        if not file:
            logger.warning("FileService: File not found for update: id=%s", file_id)
            return None
        
        for key, value in data.items():
            if hasattr(file, key):
                setattr(file, key, value)
        
        db.commit()
        db.refresh(file)
        logger.debug("FileService: File updated successfully: id=%s", file_id)
        return file
