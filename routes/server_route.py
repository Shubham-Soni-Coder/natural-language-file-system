from fastapi import APIRouter


route = APIRouter()


@route.get("/database")
def read_db():
    return {"connection": True, "message": "DB connected"}
