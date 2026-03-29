from fastapi import APIRouter
from schemas.file_schema import FileDataRequest
from app.dependencies import DataBaseDep
from models.file_model import File


route = APIRouter()


@route.get("/files")
def get_files(db: DataBaseDep):
    return db.query(File).all()


@route.post("/files")
def create_files(request: FileDataRequest, db: DataBaseDep):
    filename = request.filename
    user_id = request.user_id
    file = File(filename=filename, user_id=user_id)
    db.add(file)
    db.commit()
    db.refresh(file)
    return file
