import os
from dotenv import load_dotenv
from utils.logging_config import main_logger as logger

load_dotenv()


def get_keys():
    gemni_api_key = os.getenv("GEMINI_API_KEY")
    sql_password = os.getenv("PASSWORD")

    if gemni_api_key is None:
        logger.warning("GEMINI_API_KEY is not available in environment variables.")
    else:
        logger.debug("GEMINI_API_KEY loaded from environment variables.")

    if sql_password is None:
        logger.warning("PASSWORD is not available in environment variables.")
    else:
        logger.debug("Database password loaded from environment variables.")

    return {"gemni_api_key": gemni_api_key, "sql_password": sql_password}
