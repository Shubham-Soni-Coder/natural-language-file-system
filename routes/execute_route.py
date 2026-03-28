from fastapi import APIRouter
from schemas.tool_schema import ToolExecuteRequest
from app.dependencies import McpServerDep

route = APIRouter()


@route.post("/execute")
def execute_tools(data: ToolExecuteRequest, mcp: McpServerDep):
    result = mcp.execute_tool(data.tool_name, data.arguments)
    return {"status": "success", "data": result}
