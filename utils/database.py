import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .logging_config import main_logger as logger
from .Config import settings


password = settings.DB_PASSWORD

DATABASE_URL = f"postgresql://{settings.DB_USER}:{password}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
logger.debug("Database URL initialized. Password is hidden for security.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()



def init_db():
    from models import File, User, Task  # ensure all model classes are imported before creating tables
    logger.info("Creating database tables if they do not exist")
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    logger.debug("Opening database session")
    try:
        yield db
    finally:
        db.close()
        logger.debug("Database session closed")
