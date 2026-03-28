from fastapi import APIRouter, HTTPException
from schemas.query_schema import QueryRequest
from app.dependencies import McpServerDep, AiHandlerDep

route = APIRouter()


@route.post(
    "/query",
    responses={
        400: {
            "description": "Could not understand query or no tools selected",
            "content": {
                "application/json": {
                    "example": {"detail": "Could not understand query or not tools selected"}
                }
            },
        }
    },
)
def proces_query(request: QueryRequest, mcp: McpServerDep, ai: AiHandlerDep):

    # 1. Get avilable local tools
    tools = mcp.get_tools()

    # 2. Get ai respone
    ai_response = ai.run_ai(request.query, tools)

    if ai_response is None or "tools" not in ai_response:
        raise HTTPException(
            status_code=400, detail="Could not understand query or not tools selected"
        )

    # 3. Execite tools
    results = []
    for tool_call in ai_response["tools"]:
        tool_name = tool_call.get("tool")
        args = tool_call.get("argument", {})

        # Verify and execute
        if tool_name in mcp.tool_registry:
            tool_result = mcp.execute_tool(tool_name, args)
            results.append({"tool": tool_name, "result": tool_result})
        else:
            results.append({"tool": tool_name, "error": f"Invalid tool: {tool_name}"})

    return {"status": "success", "response": results}
