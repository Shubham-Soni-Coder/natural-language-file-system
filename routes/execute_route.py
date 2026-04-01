from fastapi import APIRouter
from schemas.tool_schema import ToolExecuteRequest
from app.dependencies import McpServerDep
from utils.logging_config import main_logger as logger

route = APIRouter()


@route.post("/execute")
def execute_tools(data: ToolExecuteRequest, mcp: McpServerDep):
    logger.info("/execute endpoint called with tool: %s", data.tool_name)
    result = mcp.execute_tool(data.tool_name, data.arguments)
    logger.debug("Tool execution result: %s", result)
    return {"status": "success", "data": result}
