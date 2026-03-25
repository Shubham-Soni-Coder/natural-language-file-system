from mcp_server import MCPServer
from ai_data import AiHandler

mcp = MCPServer("test_folder")
ai = AiHandler()


def test_folder():
    while True:
        user_input = input("Enter Query: ")
        if user_input.lower() == "exit":
            print("Thanks for using Ai")
            break

        ai_respone = ai.run_ai(user_input, MCPServer().get_tools())
        if ai_respone is None:
            print("Could not understand query")
            continue

        tool_name = ai_respone["tool"]
        arguments = ai_respone["arguments"]
        if tool_name not in mcp.tool_registry:
            print("Invalid tool from ai")
            continue

        if tool_name == "get_category_count":
            if arguments["category"] not in ["image", "video", "documents"]:
                print("Invalid Category parts")
                continue

        tool_info = mcp.tool_registry[tool_name]
        required_args = tool_info["parameters"]
        has_missing = False

        for param in required_args:
            if param not in arguments:
                print(f"Missing argument: {param}")
                has_missing = True
                break
        if has_missing:
            continue

        result = mcp.execute_tool(tool_name, arguments)

        print("Result: ", result)


if __name__ == "__main__":
    test_folder()
