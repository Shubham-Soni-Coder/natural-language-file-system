from fastapi import APIRouter
from schemas.file_schema import FileCreate, FileRespone
from app.dependencies import DataBaseDep
from models.file_model import File


route = APIRouter()


@route.get("/files")
def get_files(db: DataBaseDep):
    return db.query(File).all()


@route.post("/files", response_model=FileRespone)
def create_files(request: FileCreate, db: DataBaseDep):
    filename = request.filename
    user_id = request.user_id
    file = File(filename=filename, user_id=user_id)
    db.add(file)
    db.commit()
    db.refresh(file)
    return file


@route.post("/user/{user_id}/files")
def get_user_files(user_id: int, db: DataBaseDep):
    return db.query(File).filter(File.user_id == user_id).all()
