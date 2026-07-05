# Project Objectives: AI File Management System
## 1. The Goal
The primary objective is to build an **Intelligent Agentic File System**. The goal is to allow users to manage, analyze, and manipulate files using natural language commands. By integrating the **Model Context Protocol (MCP)**, the system acts as a "bridge" between an AI brain (Gemini) and physical storage, allowing for complex, multi-step processes like "keep analyzing this folder" or "clean up my duplicates."

## 2. What We Have To Do
- **Persistent Identity:** Maintain a database of users so that file ownership and process history are preserved across sessions.
- **FileSystem Tools:** Implement a suite of Python functions (Tools) that can count, measure, find, delete, and summarize files.
- **AI Reasoning:** Use Generative AI to map vague user strings (e.g., "What's my biggest file?") into specific function calls.
- **Process Management:** Create a mechanism to track long-running analysis tasks in the database so the AI can "remember" what it is currently doing.
- **Centralized Safety:** Implement global error handling to ensure the system never leaks technical secrets to the user but remains easy for the developer to debug.

## 3. Overview Guide of Every Step
1.  **Initialize Environments:** Load API keys and database credentials.
2.  **Index physical storage:** Scan the target folders to create a baseline of what exists on the disk.
3.  **Sync Database:** Mirror the file metadata into PostgreSQL to allow for high-speed AI queries without re-scanning the disk.
4.  **Register Tools:** Plug the Python logic into the `MCPServer` so the AI knows what "arms" it has to work with.
5.  **Interpret Intent:** Receive a query, send it to Gemini with a "Tool Definition List," and get back a structured instruction.
6.  **Execute & Respond:** Run the Python logic based on the AI's decision and return a JSON result to the user.

## 4. Rules
- **Strict JSON Output:** The `AiHandler` must strictly return JSON. Any conversational filler from the AI will break the execution logic.
- **Owner-File Binding:** Every file record in the database must be linked to a `user_id`. No "orphaned" file records allowed.
- **Technical Isolation:**
    - **Server Terminal:** Full tracebacks and technical metadata.
    - **Client Terminal:** Sanitized, user-friendly messages only.
- **Non-Destructive Defaults:** Tools that delete or move files should ideally log the intent in the database before acting on the physical disk.

## 5. Workflow (Process Logic)

**Input -> AI Brain -> Logic Execution -> Database/FS Sync -> Output**

### Pseudo-code Implementation
```python
def process_query(query: str, db: Session, ai_driver: AiDriver, mcp_registry: MCPRegistry):
    # 1. Fetch available tool metadata schemas from the MCP Registry
    tools = mcp_registry.get_tools() 
    
    # 2. Contextualize the brain (System Instruction + Tools + User Query)
    ai_response = ai_driver.run_ai(query, tools)
    
    # 3. Validation Phase
    if not ai_response or "tools" not in ai_response:
        raise HTTPException(status_code=400, detail="Could not understand query or no tools selected")

    results = []
    for tool_call in ai_response["tools"]:
        tool_name = tool_call.get("tool")
        args = tool_call.get("argument", {})
        
        # 4. Execute the specific Python tool function registered in MCPRegistry
        if tool_name in mcp_registry.tool_registry:
            tool_result = mcp_registry.execute_tool(tool_name, args)
            results.append({"tool": tool_name, "result": tool_result})
        else:
            results.append({"tool": tool_name, "error": f"Invalid tool: {tool_name}"})
            
    # 5. Output response dictionary to the Router
    return results
```

---
*Document Version: 1.0*

### Description of the file:
*   **Goal:** Explicitly states that this is an "Agentic" system, not just a static script.
*   **Tasks:** Focuses on the transition from simple commands to persistent processes ("keep analyzing").
*   **Step-by-Step Guide:** Explains how initialization leads to tool registration and execution.
*   **Rules:** Sets the "Strict JSON" and "Technical Isolation" boundaries we discussed regarding server/client error separation.
*   **Workflow:** Provides a mental model of how a string of text becomes a database update and a user response.

<!--
[PROMPT_SUGGESTION]Can you help me implement the 'Process Management' logic in the database as described in the objectives?[/PROMPT_SUGGESTION]
[PROMPT_SUGGESTION]Should I add a 'deferred_tasks' table to handle the 'keep analyzing' rule in the pseudo-code?[/PROMPT_SUGGESTION]
