import logging
from fastapi import Depends
from typing import Annotated
from services import MCPServer, AiHandler
from utils import get_db, main_logger as logger
from sqlalchemy.orm import Session

# 1. Initialize at once when the server is starting
mcp_instance = MCPServer()
ai_instance = AiHandler()


# Dependency provider functions
def get_mcp() -> MCPServer:
    logger.debug("Providing MCPServer dependency instance")
    return mcp_instance


def get_ai() -> AiHandler:
    logger.debug("Providing AiHandler dependency instance")
    return ai_instance


# Annotated type for super-clean routes!
McpServerDep = Annotated[MCPServer, Depends(get_mcp)]
AiHandlerDep = Annotated[AiHandler, Depends(get_ai)]
DataBaseDep = Annotated[Session, Depends(get_db)]