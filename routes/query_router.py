from fastapi import APIRouter
from schemas import QueryRequest
from app import MCPRegistryDep, AiDriverDep, DataBaseDep
from services import QueryService
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
def proces_query(request: QueryRequest, mcp: MCPRegistryDep, ai: AiDriverDep, db: DataBaseDep):
    """
    Process a user query using AI and available tools.
    
    Route delegates to QueryService which handles:
    - Tool selection by AI
    - Tool execution
    - Result collection
    """
    logger.info("/query endpoint called with query: %s", request.query)

    results = QueryService.process_query(request.query, db, ai, mcp)
    
    logger.info("Query processed successfully")
    return {"status": "success", "response": results}
