from sqlalchemy import Integer, String,Boolean , Column, ForeignKey,func , TIMESTAMP
from utils import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("files.id"))
    name = Column(String,nullable=False)
    path = Column(String,nullable=False,unique=True)
    parent_path = Column(String,nullable=True)
    is_folder = Column(Boolean,nullable=False,default=False)
    size = Column(Integer,nullable=False)
    mime_type = Column(String,nullable=True)
    extension = Column(String,nullable=True)
    hash = Column(String,nullable=True,index=True)

    created_at = Column(TIMESTAMP,server_default=func.now())
    updated_at = Column(TIMESTAMP,server_default=func.now(),onupdate=func.now())
    
    status = Column(String,default="active")

