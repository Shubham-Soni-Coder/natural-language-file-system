import requests
import json
from ai_data import AiHandler
from mcp_server import MCPServer

# get responed
tools = requests.get("http://127.0.0.1:8000/tools").json()

ai = AiHandler()
mcp = MCPServer()


# ai rspone
def get_respone(user_input, tools):
    ai_respone = ai.run_ai(user_input, tools)
    return ai_respone


def respone_checker(ai_respone):
    if ai_respone is None:
        print("Could not understand query")
        return None
    if ai_respone.get("tools") is None:
        print("tools not found")
        return None
    return ai_respone.get("tools")


def text_checker(tools):
    # 1.Strcuture check
    if "tool" not in tools or "argument" not in tools:
        return {"status": "error", "message": "Missing required Keys in Ai responed"}
    tool_name = tools["tool"]
    args = tools["argument"]
    # 2. tool validation
    if tool_name not in mcp.tool_registry:
        return {"status": "error", "message": f"Invalid tool : {tool_name}"}
    # 3. valdation arguments
    required = mcp.tool_registry[tool_name]["parameters"]

    for param in required:
        if param not in args:
            return {"status": "error", "message": f"missing argument {param}"}
    return tools


def result_showner(tools_list):
    result = []

    for tools in tools_list:
        tools = text_checker(tools)
        tool_name = tools["tool"]
        arguments = tools["argument"]

        respone = requests.post(
            "http://127.0.0.1:8000/execute",
            json={"tool_name": tool_name, "arguments": arguments},
        )

        result.append(respone.json())

    return result


while True:
    user_input = input("Enter Query: ")
    if user_input.lower() == "exit":
        print("Thanks for using Ai")
        break

    ai_respone = get_respone(user_input, tools)
    tools_list = respone_checker(ai_respone)
    result = result_showner(tools_list)

    print(result)
