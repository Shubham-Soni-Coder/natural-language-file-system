from typing import List

from fastapi import APIRouter
from schemas import UserCreate, UserResponse
from app import DataBaseDep
from services.user_service import UserService
from utils import main_logger as logger

route = APIRouter()


@route.post("/user", response_model=UserResponse)
def create_user(request: UserCreate, db: DataBaseDep):
    """Create a new user record via UserService."""
    logger.info("Creating user with email: %s", request.email)
    user = UserService.create(db, request)
    logger.debug("Created user id: %s", user.id)
    return user


@route.get("/user", response_model=List[UserResponse])
def get_user(db: DataBaseDep):
    """Retrieve all users from the database via UserService."""
    logger.info("Retrieving user list")
    users = UserService.get_all(db)
    logger.debug("Found %s users", len(users))
    return users
