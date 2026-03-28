import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import json


class AiHandler:

    def __init__(self):
        # load the env file
        load_dotenv()

        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)

    def build_prompt(self, tools):
        # 1. Configuartion Constructs (Master list)
        ALLOWED_CATEGORIES = ["image", "video", "documents"]
        tools_json = json.dumps(tools, indent=2)

        return f"""
        You are a tool selection system.

        Available tools:
        {tools_json}

        Rules:
        - Always return valid JSON
        - Do NOT explain anything
        - category must be in : {ALLOWED_CATEGORIES}
        - You can return multiple tools if needed 
        - Only output:
        {{
            "tools":[
                {{"tool":"...","argument":{...}}}
            ]
        }}
        """

    def run_ai(self, user_input: str, tools):
        print("Ai is starting ")
        if user_input.strip() == "":
            return None
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_input,
                config=types.GenerateContentConfig(
                    system_instruction=self.build_prompt(tools),
                    response_mime_type="application/json",
                    temperature=0.0,
                ),
            )
            print("Raw Ai response : ", response.text)
            # ----Validation Layer -----
            # 1.  Structured Validation (Is it valid Json)
            try:
                data = json.loads(response.text)
            except json.decoder.JSONDecodeError:
                print("Invalid Json Forment recived from AI")
                return None

            return data

        except Exception as error:
            print(str(error))
            return None


if __name__ == "__main__":
    from mcp_server import MCPServer

    tools = MCPServer().get_tools()
    user_input = input("Enter your query : ")
    ai = AiHandler()
    print(ai.run_ai(user_input, tools))
