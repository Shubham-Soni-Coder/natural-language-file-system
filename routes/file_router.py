from fastapi import APIRouter
from schemas import FileCreate, FileRespone
from app import DataBaseDep
from models import File
from utils import main_logger as logger


route = APIRouter()


@route.get("/files")
def get_files(db: DataBaseDep):
    logger.info("Fetching all files")
    files = db.query(File).all()
    logger.debug("Returned %s files", len(files))
    return files


@route.post("/files", response_model=FileRespone)
def create_files(request: FileCreate, db: DataBaseDep):
    logger.info("Creating file record: %s for user %s", request.filename, request.user_id)
    file = File(filename=request.filename, user_id=request.user_id)
    db.add(file)
    db.commit()
    db.refresh(file)
    logger.debug("Created file id: %s", file.id)
    return file


@route.post("/user/{user_id}/files")
def get_user_files(user_id: int, db: DataBaseDep):
    logger.info("Fetching files for user_id=%s", user_id)
    files = db.query(File).filter(File.user_id == user_id).all()
    logger.debug("Found %s files for user_id=%s", len(files), user_id)
    return files
