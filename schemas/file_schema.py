from pydantic import BaseModel
from datetime import datetime 
from typing import Optional 


class FileCreate(BaseModel):
    name:str
    path:str
    size:int
    mime_type:str
    extension:str
    hash:Optional[str] = None
    user_id:int
    status:Optional[str] = "active"

    @classmethod
    def normalize_extension(cls, v):
        return v.lower().replace(".", "")

class FileResponse(BaseModel):
    id : int
    name:str
    path:str
    size:int
    mime_type:str
    extension:str
    hash:Optional[str] = None
    user_id:int
    created_at:datetime
    updated_at:datetime
    status:str

    class Config:
        from_attributes = True  

class FileUpdate(BaseModel):
    name: Optional[str] = None
    path: Optional[str] = None
    size: Optional[int] = None
    mime_type: Optional[str] = None
    extension: Optional[str] = None
    hash: Optional[str] = None
    status: Optional[str] = None

class FileListRequest(BaseModel):
    user_id :int
    status:Optional[str] = "active"
    limit:int=100
    offset:int = 0 