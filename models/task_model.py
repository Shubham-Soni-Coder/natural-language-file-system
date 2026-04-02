from sqlalchemy import Column,Integer,String,JSON,Text,TIMESTAMP,ForeignKey,func
from utils.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,nullable=False)

    task_type = Column(String,nullable=False)
    status = Column(String,nullable=False,default="pending")

    input_data = Column(JSON)
    result = Column(JSON)
    error = Column(JSON)

    parent_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)

    created_at = Column(TIMESTAMP,server_default=func.now())
    updated_at = Column(TIMESTAMP,server_default=func.now(),onupdate=func.now())

