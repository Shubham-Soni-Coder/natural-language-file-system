from fastapi import APIRouter
from utils.logging_config import main_logger as logger

route = APIRouter()


@route.get("/database")
def read_db():
    logger.info("Health check endpoint called")
    return {"connection": True, "message": "DB connected"}
