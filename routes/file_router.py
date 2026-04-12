from fastapi import APIRouter
from schemas import FileCreate, FileResponse
from app import DataBaseDep
from services import FileService
from utils import main_logger as logger


route = APIRouter()


@route.get("/files")
def get_files(db: DataBaseDep):
    """Fetch all files from database via FileService"""
    logger.info("Fetching all files")
    files = FileService.get_all(db)
    logger.debug("Returned %s files", len(files))
    return files


@route.post("/files", response_model=FileResponse)
def create_files(request: FileCreate, db: DataBaseDep):
    """Create a new file record via FileService"""
    logger.info("Creating file record: %s for user %s", request.name, request.user_id)
    return FileService.create(db, request)


@route.post("/user/{user_id}/files")
def get_user_files(user_id: int, db: DataBaseDep):
    """Fetch files for a specific user via FileService"""
    logger.info("Fetching files for user_id=%s", user_id)
    files = FileService.get_by_user(db, user_id)
    logger.debug("Found %s files for user_id=%s", len(files), user_id)
    return files
