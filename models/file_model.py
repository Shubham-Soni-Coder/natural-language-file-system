from sqlalchemy import Integer, String, Column, ForeignKey
from utils import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
