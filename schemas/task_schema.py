from pydantic import BaseModel
from typing import Optional, Dict

class TaskCreate(BaseModel):
    user_id: int
    task_type: str
    input_data: Optional[Dict] = None
    parent_task_id: Optional[int] = None


class TaskRespone(BaseModel):
    id: int
    user_id: int
    task_type: str
    status: str
    parent_task_id: Optional[int] = None

    class Config:
        from_attributes = True
    id : int 
    user_id :int 
    task_type:str
    status : str

    class Config:
        from_attributes = True

