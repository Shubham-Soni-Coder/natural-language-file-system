from fastapi import APIRouter
from app import MCPRegistryDep
from utils import main_logger as logger


route = APIRouter()


@route.get("/tools")
def get_tools(mcp: MCPRegistryDep):
    logger.info("/tools endpoint invoked")
    tools = mcp.get_tools()
    logger.debug("%s tools available", len(tools))
    return {"status": "success", "tools": tools}
