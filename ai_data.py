import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import json


class AiHandler:

    # 1. Configuartion Constructs (Master list)
    ALLOWED_INTENTS = ["total", "size", "largest", "category", "summary"]
    ALLOWED_CATEGORIES = ["image", "video", "documents", "all"]

    PROMPT = """
    You are a tool selection system.

    Available tools:
    - get_total_files
    - get_total_size
    - get_largest_file
    - get_category_count (requires: category = image/video/documents)
    - get_summary

    Rules:
    - Always return valid JSON
    - Do NOT explain anything
    - Only output:
    {
    "tool": "...",
    "arguments": {...}
    }
    """

    def __init__(self):
        # load the env file
        load_dotenv()

        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)

    def run_ai(self, user_input: str):
        print("Ai is starting ")
        if user_input.strip() == "" or user_input.lower() == "exit":
            return "No query"
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_input,
                config=types.GenerateContentConfig(
                    system_instruction=self.PROMPT,
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

            # 2. Schems Validation (Do the keys exists)
            if "tool" not in data or "arguments" not in data:
                print("Missing required keys in Ai resoned")
                return None

            # 3. Check for category as dict
            if not isinstance(data["tool"], str) or not isinstance(
                data["arguments"], dict
            ):
                print("Invalid data type in Ai resoned")
                return None

            return data

        except Exception as error:
            print(str(error))
            return None


if __name__ == "__main__":
    user_input = input("Enter your query : ")
    ai = AiHandler()
    print(ai.run_ai(user_input))
