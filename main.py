import requests

SERVER_URL = "http://127.0.0.1:8000"


def display_results(response: requests.Response) -> None:
    """Handles formatting and printing of the server response."""
    if response.status_code != 200:
        error_detail = response.json().get("detail", "Unknown error")
        print(f"Server Error ({response.status_code}): {error_detail}")
        return

    results = response.json().get("response", [])
    if not results:
        print("No tools were executed.")
        return

    for result in results:
        tool_name = result.get("tool")
        tool_output = result.get("result", result.get("error"))
        print(f"\n--- Output from [{tool_name}] ---")
        print(f"{tool_output}")


def process_user_query(user_input: str) -> None:
    """Sends the user's string query to the FastAPI backend."""
    try:
        response = requests.post(f"{SERVER_URL}/query", json={"query": user_input})
        display_results(response)
    except requests.exceptions.ConnectionError:
        print(
            f"\n[!] Connection Error: Could not connect to the server at {SERVER_URL}."
        )
        print("Is your FastAPI backend running? Try: uvicorn app.app:app --reload")
    except Exception as e:
        print(f"\nAn unexpected client-side error occurred: {e}")


def start_client() -> None:
    """Main CLI loop for gathering user input."""
    print("Welcome to the AI File Management Client!")
    print("Waiting for your command...")

    while True:
        try:
            user_input = input("\nEnter Query (or type 'exit'): ").strip()

            if user_input.lower() == "exit":
                print("Thanks for using the AI System!")
                break

            if not user_input:
                continue

            process_user_query(user_input)

        except KeyboardInterrupt:
            print("\nExiting...")
            break


def get_response_server() -> None:
    result = requests.get(f"{SERVER_URL}/database")
    print(result.text)


if __name__ == "__main__":
    get_response_server()
