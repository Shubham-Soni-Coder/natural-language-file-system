from core import AiDriver,MCPRegistry

tools = MCPRegistry().get_tools()
user_input = input("Enter your query : ")
ai = AiDriver()
result = ai.run_ai(user_input, tools)