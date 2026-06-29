from sqlalchemy import (
     Integer, String,Boolean , Column,
      ForeignKey,func , TIMESTAMP , DateTime
)
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

    file_created_at = Column(DateTime,nullable=True)
    file_modified_at = Column(DateTime,nullable=True)


    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at = Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)
    
    status = Column(String,default="active")

