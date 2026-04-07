from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Task
from schemas import TaskCreate
from utils import main_logger as logger


class QueryService:
    """
    Orchestrates AI query processing with tool execution.
    Moves the tool execution loop and business logic out of routes.
    """

    @staticmethod
    def process_query(query: str, db: Session, ai_handler, mcp_registry):
        """
        Process a user query:
        1. Get available tools from MCP registry
        2. Send query to AI with tools
        3. Execute each tool returned by AI
        4. Collect and return results
        
        Args:
            query: User input string
            db: Database session
            ai_handler: AI handler instance
            mcp_registry: MCP registry instance
            
        Returns:
            Dictionary with results from tool execution
        """
        logger.info("QueryService: Processing query: %s", query)

        # Step 1: Get available tools
        tools = mcp_registry.get_tools()
        logger.debug("QueryService: Retrieved %s available tools", len(tools))

        # Step 2: Get AI decision on which tools to use
        ai_response = ai_handler.run_ai(query, tools)

        if ai_response is None or "tools" not in ai_response:
            logger.warning("QueryService: AI response invalid or missing tools: %s", ai_response)
            raise HTTPException(
                status_code=400, detail="Could not understand query or not tools selected"
            )

        # Step 3: Execute each tool and collect results
        results = []
        for tool_call in ai_response["tools"]:
            tool_name = tool_call.get("tool")
            args = tool_call.get("argument", {})

            if tool_name in mcp_registry.tool_registry:
                logger.info("QueryService: Executing tool: %s", tool_name)
                tool_result = mcp_registry.execute_tool(tool_name, args)
                results.append({"tool": tool_name, "result": tool_result})
            else:
                logger.error("QueryService: Invalid tool requested: %s", tool_name)
                results.append({"tool": tool_name, "error": f"Invalid tool: {tool_name}"})

        logger.info("QueryService: Query processed with %s tool calls", len(results))
        return results
