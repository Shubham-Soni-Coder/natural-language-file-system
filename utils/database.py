import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from utils.logging_config import main_logger as logger
from utils.utilas import get_keys

password = get_keys()["sql_password"]

if password is None:
    logger.warning("Database password is not set in environment variables.")

DATABASE_URL = f"postgresql://postgres:{password}@localhost:5432/database"
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
