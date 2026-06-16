from utils import SessionLocal
from services import FileService
from core import FileUtils
from fastapi import APIRouter
from pathlib import Path

route = APIRouter()

@route.on_event("startup")
def startup_event():
    db = SessionLocal()
    foldername = "E:/File_mangement_system"
    scanner = FileUtils(foldername)
    try:
        generator = scanner.scan()
        FileService.ingest(db,generator,user_id=1)
    finally:
        db.close()    
