from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate
from utils import main_logger as logger

class UserService:
    """
    Handles User database operations.
    Keeps route logic thin by moving all DB work into the service layer.
    """

    @staticmethod
    def create(db: Session, data: UserCreate) -> User:
        """
        Create a new user record in the database.

        Args:
            db: Database session.
            data: UserCreate schema containing name and email.

        Returns:
            Created User ORM instance.
        """
        logger.info("UserService: Creating new user with email=%s", data.email)
        user = User(name=data.name, email=data.email)
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.debug("UserService: Created user id=%s", user.id)
        return user

    @staticmethod
    def get_all(db: Session) -> list[User]:
        """
        Fetch all users from the database.

        Args:
            db: Database session.

        Returns:
            List of User ORM instances.
        """
        logger.info("UserService: Retrieving all users")
        users = db.query(User).all()
        logger.debug("UserService: Found %s users", len(users))
        return users
