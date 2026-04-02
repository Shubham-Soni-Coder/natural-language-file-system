from fastapi import APIRouter, HTTPException
from schemas import QueryRequest
from app import McpServerDep, AiHandlerDep
from utils import main_logger as logger

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
    logger.info("/query endpoint called with query: %s", request.query)

    tools = mcp.get_tools()
    ai_response = ai.run_ai(request.query, tools)

    if ai_response is None or "tools" not in ai_response:
        logger.warning("AI response invalid or missing tools: %s", ai_response)
        raise HTTPException(
            status_code=400, detail="Could not understand query or not tools selected"
        )

    results = []
    for tool_call in ai_response["tools"]:
        tool_name = tool_call.get("tool")
        args = tool_call.get("argument", {})

        if tool_name in mcp.tool_registry:
            tool_result = mcp.execute_tool(tool_name, args)
            results.append({"tool": tool_name, "result": tool_result})
        else:
            logger.error("Invalid tool requested: %s", tool_name)
            results.append({"tool": tool_name, "error": f"Invalid tool: {tool_name}"})

    logger.info("Query processed with %s tool calls", len(results))
    return {"status": "success", "response": results}
