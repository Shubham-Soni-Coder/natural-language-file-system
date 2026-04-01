from fastapi import APIRouter
from schemas.user_schema import UserCreate, UserResponse
from app.dependencies import DataBaseDep
from models.user_model import User
from utils.logging_config import main_logger as logger

route = APIRouter()


@route.post("/user", response_model=UserResponse)
def create_user(request: UserCreate, db: DataBaseDep):
    logger.info("Creating user with email: %s", request.email)
    user = User(name=request.name, email=request.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.debug("Created user id: %s", user.id)
    return user


@route.get("/user")
def get_user(db: DataBaseDep):
    logger.info("Retrieving user list")
    users = db.query(User).all()
    logger.debug("Found %s users", len(users))
    return users
