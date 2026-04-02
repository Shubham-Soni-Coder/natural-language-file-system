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


def get_db():
    db = SessionLocal()
    logger.debug("Opening database session")
    try:
        yield db
    finally:
        db.close()
        logger.debug("Database session closed")
