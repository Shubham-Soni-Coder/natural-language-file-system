from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from utilas.utilas import get_keys

password = get_keys()["sql_password"]

DATABASE_URL = f"postgresql://postgres:{password}@localhost:5432/database"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
