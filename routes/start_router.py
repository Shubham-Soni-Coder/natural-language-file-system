from utils import SessionLocal
from services import FileService
from core import FileUtils
from fastapi import APIRouter
from pathlib import Path
from utils import main_logger as logger

route = APIRouter()

@route.on_event("startup")
def startup_event():
    db = SessionLocal()
    foldername = "E:/File_mangement_system"
    scanner = FileUtils(foldername)
    try:
        generator = scanner.scan()
        FileService.ingest(db,generator,user_id=1)

        logger.info("Startup File Ingestion complete suceesfully")

    except Exception as errror:
        logger.error(f"Critical error during startup file scan : {errror}")
    finally:
        db.close()    
