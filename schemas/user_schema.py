from pydantic import BaseModel


class UserDataRequest(BaseModel):
    name: str
    email: str
