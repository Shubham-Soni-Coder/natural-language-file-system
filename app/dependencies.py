from fastapi import Depends
from typing import Annotated
from services.mcp_server import MCPServer
from services.ai_data import AiHandler
from utilas.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# 1. Initalize at once when the server is starting
mcp_instance = MCPServer()
ai_instance = AiHandler()


# Dependency Privider functions
def get_mcp() -> MCPServer:
    return mcp_instance


def get_ai() -> AiHandler:
    return ai_instance


# Annotated type for super-clean routes!
McpServerDep = Annotated[MCPServer, Depends(get_mcp)]
AiHandlerDep = Annotated[AiHandler, Depends(get_ai)]
DataBaseDep = Annotated[Session, Depends(get_db)]
