from fastapi import APIRouter
from services import MCPServer
from app import McpServerDep
from utils import main_logger as logger


route = APIRouter()


@route.get("/tools")
def get_tools(mcp: McpServerDep):
    logger.info("/tools endpoint invoked")
    tools = mcp.get_tools()
    logger.debug("%s tools available", len(tools))
    return {"status": "success", "tools": tools}
