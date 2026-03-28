from fastapi import APIRouter, Depends
from services.mcp_server import MCPServer
from app.dependencies import McpServerDep


route = APIRouter()


@route.get("/tools")
def get_tools(mcp: McpServerDep):
    return {"status": "success", "tools": mcp.get_tools()}
