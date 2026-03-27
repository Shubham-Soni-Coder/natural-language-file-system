import requests
import json
from ai_data import AiHandler

# get responed
tools = requests.get("http://127.0.0.1:8000/tools").json()

ai = AiHandler()


# ai rspone
def get_respone(user_input, tools):
    ai_respone = ai.run_ai(user_input, tools)
    return ai_respone


def respone_checker(ai_respone):
    if ai_respone is None:
        print("Could not understand query")
        return None
    tool_name = ai_respone["tool"]
    arguments = ai_respone["arguments"]

    return tool_name, arguments


while True:
    user_input = input("Enter Query: ")
    if user_input.lower() == "exit":
        print("Thanks for using Ai")
        break

    ai_respone = get_respone(user_input, tools)
    tool_name, arguments = respone_checker(ai_respone)
    respone = requests.post(
        "http://127.0.0.1:8000/execute",
        json={"tool": tool_name, "arguments": arguments},
    )

    print(respone.json())
