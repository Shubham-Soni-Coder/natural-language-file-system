from sqlalchemy.orm import Session
from models import File
from schemas import FileCreate, FileResponse
from utils import main_logger as logger
from sqlalchemy.dialects.postgresql import insert

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

    @staticmethod
    def validate_File_Data(data:dict)->bool:
        # ------------------Basic Validation-------
        if not data.get("name"):
            logger.warning("Skipping File: missing name | data=%s",data)
            return False
        if not data.get("path"):
            logger.warning("Skipping file: missing path | nam=%s",data.get("name"))
            return False
        if data.get("size",0) < 0:
            logger.warning("Skipping file :invalid size | path=%s size=%s",
            data.get("path"),data.get("size"))
            return False
        return True
    
    @staticmethod
    def prepare_file_data(data:dict,user_id:int) -> dict:
        return {
            "name":data["name"],
            "path":data["path"],
            "parent_path":data["parent_path"],
            "is_folder":data["is_folder"],
            "size":data["size"],
            "mime_type":data.get("mime_type"),
            "extension":data.get("extension"),
            "hash":data.get("hash"),
            "user_id":user_id,
            "status":data.get("status","active")
        }

    @staticmethod
    def insert_batch(db:Session,batch:int):
        if not batch:
            return

        stmt = insert(File).values(batch)

        stmt = stmt.on_conflict_do_nothing(
            index_elements=["path"]
        )
        try:
            db.execute(stmt)
            db.commit()
            logger.info("Inserted batch of %s files (duplicates ignored)",len(batch))
        except Exception as e:
            logger.exception("Batch insert falied | error=%s",str(e))
            db.rollback()

    @staticmethod
    def ingest(db:Session,generator, user_id: int, batch_size: int = 100):
        batch = []

        for data in generator:
            # validation 
            if not FileService.validate_File_Data(data):
                filename = data.get("name","UnknownFile")
                logger.warning(f"validation falied for '{filename}'. Skipping this file")
                continue

            prepared = FileService.prepare_file_data(data,user_id)
            batch.append(prepared)

            if len(batch) >= batch_size:
                FileService.insert_batch(db,batch)
                batch.clear()
        if batch:
            FileService.insert_batch(db,batch)
        
        logger.info("File ingestion completed")
        