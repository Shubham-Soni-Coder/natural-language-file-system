from fastapi import APIRouter
from schemas.user_schema import UserCreate, UserResponse
from app.dependencies import DataBaseDep
from models.user_model import User

route = APIRouter()


@route.post("/user", response_model=UserResponse)
def create_user(request: UserCreate, db: DataBaseDep):
    name = request.name
    email = request.email
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@route.get("/user")
def get_user(db: DataBaseDep):
    return db.query(User).all()
