import logging
from fastapi import Depends
from typing import Annotated
from core import MCPRegistry, AiDriver
from utils import get_db, main_logger as logger
from sqlalchemy.orm import Session
from utils import SessionLocal

db = SessionLocal()

# 1. Initialize at once when the server is starting
ai_instance = AiDriver()


# Dependency provider functions
def get_mcp(db:Session=Depends(get_db)) -> MCPRegistry:
    logger.debug("Providing MCPRegistry dependency instance")
    user_id = 1 
    return MCPRegistry(
        db=db,
        user_id=user_id
    )


def get_ai() -> AiDriver:
    logger.debug("Providing AiDriver dependency instance")
    return ai_instance


# Annotated type for super-clean routes!
MCPRegistryDep = Annotated[MCPRegistry, Depends(get_mcp)]
AiDriverDep = Annotated[AiDriver, Depends(get_ai)]
DataBaseDep = Annotated[Session, Depends(get_db)]