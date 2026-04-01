from fastapi import APIRouter
from services.mcp_server import MCPServer
from app.dependencies import McpServerDep
from utils.logging_config import main_logger as logger


route = APIRouter()


@route.get("/tools")
def get_tools(mcp: McpServerDep):
    logger.info("/tools endpoint invoked")
    tools = mcp.get_tools()
    logger.debug("%s tools available", len(tools))
    return {"status": "success", "tools": tools}
