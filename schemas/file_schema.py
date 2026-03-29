from pydantic import BaseModel


class FileDataRequest(BaseModel):
    filename: str
    user_id: int
