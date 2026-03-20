import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import json
import logging


# config the logging
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")


class AiHandler:

    # 1. Configuartion Constructs (Master list)
    ALLOWED_INTENTS = ["total", "size", "largest", "category", "summary"]
    ALLOWED_CATEGORIES = ["image", "video", "documents", "all"]

    Prompt = """You are an intent detection system.

        Your task is to extract structured intent from user queries.

        Available intents:
        - total
        - size
        - largest
        - category (requires one of: image, video, documents)
        - summary

        Rules:
        - Return ONLY valid JSON.
        - Do NOT add any explanation.
        - Do NOT add text before or after JSON.
        - "intent" must be one of the allowed intents.
        - "argument" must be:
            - null for intents: total, size, largest, summary
            - one of: image, video, documents (ONLY if intent = category)

        Normalization rules:
        - Convert plural to singular:
            - images → image
            - videos → video
            - documents/docs/files → documents
        - Map similar words:
            - pics/photos → image
            - vids/movies → video

        Output format:
        {
        "intent": "...",
        "argument": ...
        }

        Examples:

        User input: "how many files are there?"
        Output:
        {"intent": "total", "argument": null}

        User input: "what is the total size?"
        Output:
        {"intent": "size", "argument": null}

        User input: "show largest file"
        Output:
        {"intent": "largest", "argument": null}

        User input: "show all images"
        Output:
        {"intent": "category", "argument": "image"}

        User input: "list videos"
        Output:
        {"intent": "category", "argument": "video"}

        User input: "give me full summary"
        Output:
        {"intent": "summary", "argument": null}
    """

    def __init__(self):
        # load the env file
        load_dotenv()

        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)

    def run_ai(self, user_input: str):

        if user_input == "":
            return "No query"
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_input,
                config=types.GenerateContentConfig(
                    system_instruction=self.Prompt,
                    response_mime_type="application/json",
                    temperature=0.0,
                ),
            )

            # ----Validation Layer -----
            # 1.  Structured Validation (Is it valid Json)
            try:
                data = json.loads(response.text)
            except json.decoder.JSONDecodeError:
                print("Invalid Json Forment recived from AI")
                return None

            # 2. Schems Validation (Do the keys exists)
            if "intent" not in data or "argument" not in data:
                print("Missing required keys in Ai resoned")
                return None

            # 3. Value Validation (Do the value allowed)
            if data["intent"] not in self.ALLOWED_INTENTS:
                print(f"Unsupported intent: {data['intent']}")
                return None

            # Special check for category arguments
            if (
                data["intent"] == "category"
                and data["argument"] not in self.ALLOWED_CATEGORIES
            ):
                print("Invaild category arguments")
                return None

            return data

        except Exception as error:
            print(str(error))
            return None


if __name__ == "__main__":
    user_input = input("Enter your query : ")
    ai = AiHandler()
    print(ai.run_ai(user_input))
