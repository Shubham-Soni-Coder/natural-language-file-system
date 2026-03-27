from fastapi import FastAPI
from mcp_server import MCPServer

# init
app = FastAPI()

mcp = MCPServer()


@app.get("/tools")
def get_tools():
    return {"status": "success", "tools": mcp.get_tools()}


@app.post("/execute")
def execute_tools(data: dict):
    tool = data.get("tool")
    args = data.get("arguments", {})

    # validation tool
    if tool not in mcp.tool_registry:
        return {"status": "error", "message": "Invalid tool"}

    # valdation arguments
    required = mcp.tool_registry[tool]["parameters"]

    for param in required:
        if param not in args:
            return {"error": f"missing argument {param}"}

    result = mcp.execute_tool(tool, args)

    return {"status": "success", "data": result}
