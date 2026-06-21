import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import json
from utils import main_logger as logger, settings

class AiDriver:

    def __init__(self):

        self.api_key = settings.GEMINI_API_KEY
        self.client = genai.Client(api_key=self.api_key)
        logger.info("AiDriver initialized")

    def build_prompt(self, tools):
        logger.debug("Building AI prompt for tools: %s", tools_json)
        tools_json = json.dumps(tools, indent=2)

        return f"""
        You are a tool selection system.

        Available tools:
        {tools_json}

        Rules:
        - Always return valid JSON
        - Do NOT explain anything
        - Select the most appropriate tool
        - You may return multiple tools if required
        - When the user refers to a file type, use a generic file_type value
        - Examples of file_type:
        - python
        - image
        - video
        - pdf
        - document
        - audio
        - archive
        - Do not generate SQL
        - Do not generate file paths unless explicitly requested

        Only output:

        {{
        "tools": [
            {{
            "tool": "...",
            "argument": {{
                ...
                }}
            }}
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
    from mcp_registry import MCPRegistry

    tools = MCPRegistry().get_tools()
    user_input = input("Enter your query : ")
    ai = AiDriver()
    result = ai.run_ai(user_input, tools)