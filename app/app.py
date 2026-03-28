from fastapi import FastAPI
from services.mcp_server import MCPServer

# init
app = FastAPI()

mcp = MCPServer()


@app.get("/tools")
def get_tools():
    return {"status": "success", "tools": mcp.get_tools()}


@app.post("/execute")
def execute_tools(data: dict):
    tool = data["tool_name"]
    args = data.get("arguments")

    result = mcp.execute_tool(tool, args)

    return {"status": "success", "data": result}
