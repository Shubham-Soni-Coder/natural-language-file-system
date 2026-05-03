from utils import SessionLocal
from services import FileService
from core import FileUtils
from fastapi import APIRouter
from pathlib import Path

route = APIRouter()

@route.on_event("startup")
def startup_event():
    db = SessionLocal()
    scanner = FileUtils()
    try:
        generator = scanner.scan()
        FileService.ingest(db,generator,user_id=1)
    finally:
        db.close()    
