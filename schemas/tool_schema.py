from pydantic import BaseModel
from typing import Optional


class ToolExecuteRequest(BaseModel):
    tool_name: str
    arguments: Optional[dict] = {}
