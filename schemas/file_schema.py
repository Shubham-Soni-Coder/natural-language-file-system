from pydantic import BaseModel


class FileCreate(BaseModel):
    filename: str
    user_id: int


class FileRespone(BaseModel):
    id: int
    filename: str
    user_id: int


class SpecficFileDataRequest(BaseModel):
    user_id: int
