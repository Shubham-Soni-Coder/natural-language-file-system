import os
from dotenv import load_dotenv

load_dotenv()


def get_keys():
    gemni_api_key = os.getenv("GEMINI_API_KEY")
    sql_password = os.getenv("PASSWORD")

    return {"gemni_api_key": gemni_api_key, "sql_password": sql_password}
