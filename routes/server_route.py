from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utilas.database import get_db
from models.user_model import User

route = APIRouter()


@route.get("/database")
def read_db():
    return {"connection": True, "message": "DB connected"}
