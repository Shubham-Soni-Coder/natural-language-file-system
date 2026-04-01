import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import json
from utils.logging_config import main_logger as logger


class AiHandler:

    def __init__(self):
        load_dotenv()

        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning("GEMINI_API_KEY is not configured.")
        self.client = genai.Client(api_key=self.api_key)
        logger.info("AiHandler initialized")

    def build_prompt(self, tools):
        ALLOWED_CATEGORIES = ["image", "video", "documents"]
        tools_json = json.dumps(tools, indent=2)
        logger.debug("Building AI prompt for tools: %s", tools_json)

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
                {{"tool":"...","argument":{{...}}}}
            ]
        }}
        """

    def run_ai(self, user_input: str, tools):
        logger.info("AI processing query")
        if user_input.strip() == "":
            logger.warning("Empty user input received for AI processing")
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
            logger.debug("Raw AI response: %s", response.text)
            try:
                data = json.loads(response.text)
            except json.decoder.JSONDecodeError:
                logger.warning("Invalid JSON format received from AI")
                return None

            return data

        except Exception as error:
            logger.exception("AI execution failed")
            return None


if __name__ == "__main__":
    from services.mcp_server import MCPServer

    tools = MCPServer().get_tools()
    user_input = input("Enter your query : ")
    ai = AiHandler()
    result = ai.run_ai(user_input, tools)
    logger.info("AI runner produced result: %s", result)
