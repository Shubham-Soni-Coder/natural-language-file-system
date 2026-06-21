from fastapi import APIRouter
from utils import main_logger as logger
from app import DataBaseDep

route = APIRouter()


@route.get("/database")
def read_db(db:DataBaseDep):
    logger.info("Health check endpoint called")
    is_connection = db.execute("SELECT 1")

    return {
        "connection":True,
        "message":"DB connected"
    }
