import requests
from utils.logging_config import main_logger as logger

SERVER_URL = "http://127.0.0.1:8000"


def display_results(response: requests.Response) -> None:
    """Handles formatting and printing of the server response."""
    logger.debug("Processing response with status code: %s", response.status_code)
    if response.status_code != 200:
        error_detail = response.json().get("detail", "Unknown error")
        logger.error("Server error %s: %s", response.status_code, error_detail)
        print(f"Server Error ({response.status_code}): {error_detail}")
        return

    results = response.json().get("response", [])
    if not results:
        logger.warning("API returned no tool results")
        print("No tools were executed.")
        return

    logger.info("Displaying %s tool results", len(results))
    for result in results:
        tool_name = result.get("tool")
        tool_output = result.get("result", result.get("error"))
        print(f"\n--- Output from [{tool_name}] ---")
        print(f"{tool_output}")


def process_user_query(user_input: str) -> None:
    """Sends the user's string query to the FastAPI backend."""
    logger.info("Sending query to server: %s", user_input)
    try:
        response = requests.post(f"{SERVER_URL}/query", json={"query": user_input})
        display_results(response)
    except requests.exceptions.ConnectionError:
        logger.error("Failed to connect to server at %s", SERVER_URL)
        print(
            f"\n[!] Connection Error: Could not connect to the server at {SERVER_URL}."
        )
        print("Is your FastAPI backend running? Try: uvicorn app.app:app --reload")
    except Exception as e:
        logger.exception("Unexpected client-side error occurred")
        print(f"\nAn unexpected client-side error occurred: {e}")


def start_client() -> None:
    """Main CLI loop for gathering user input."""
    logger.info("Starting client interactive loop")
    print("Welcome to the AI File Management Client!")
    print("Waiting for your command...")

    while True:
        try:
            user_input = input("\nEnter Query (or type 'exit'): ").strip()

            if user_input.lower() == "exit":
                logger.info("Client session ended by user")
                print("Thanks for using the AI System!")
                break

            if not user_input:
                continue

            process_user_query(user_input)

        except KeyboardInterrupt:
            logger.info("Client interrupted by KeyboardInterrupt")
            print("\nExiting...")
            break


def get_response_server() -> None:
    logger.info("Requesting database health check")
    result = requests.get(f"{SERVER_URL}/database")
    print(result.text)


def add_user(name, email) -> None:
    logger.info("Adding user: %s <%s>", name, email)
    result = requests.post(f"{SERVER_URL}/user", json={"name": name, "email": email})
    print(result.text)


def add_file(filename, user_id) -> None:
    logger.info("Adding file: %s for user %s", filename, user_id)
    response = requests.post(
        f"{SERVER_URL}/files", json={"filename": filename, "user_id": user_id}
    )
    print(response.text)


def specific_data() -> None:
    user_id = 2
    logger.info("Requesting files for user %s", user_id)
    result = requests.post(f"{SERVER_URL}/user/{user_id}/files")
    print(result.text)


if __name__ == "__main__":
    add_user(name="Saloni", email="saloni@gmail.com")
