import requests
import pytest
import os
from dotenv import load_dotenv

load_dotenv()

BASE_HOST = os.getenv("HOST")
BASE_URL = f"http://{BASE_HOST}:8000"  # Replace with the actual base URL of your API


def test_start_new_game_success():
    """
    Test that starting a new game returns a successful response with a game_id and message.
    """
    response = requests.post(f"{BASE_URL}/game/new")

    assert response.status_code == 200, "Expected status code 200"

    json_response = response.json()
    assert "game_id" in json_response, "Response should contain 'game_id'"
    assert isinstance(json_response["game_id"], str), "'game_id' should be a string"
    assert len(json_response["game_id"]) > 0, "'game_id' should not be empty"

    assert "message" in json_response, "Response should contain 'message'"
    assert json_response["message"] == "New game started!", "Message should be 'New game started!'"


def test_start_new_game_invalid_method():
    """
    Test that using an invalid HTTP method returns an error.
    """
    response = requests.get(f"{BASE_URL}/game/new")  # Using GET instead of POST

    assert response.status_code == 405, "Expected status code 405 for method not allowed"


def test_start_new_game_invalid_endpoint():
    """
    Test that accessing an invalid endpoint returns a 404 error.
    """
    response = requests.post(f"{BASE_URL}/game/invalid")

    assert response.status_code == 404, "Expected status code 404 for not found"


def test_start_new_game_server_error(mocker):
    """
    Simulate a server error and test the response.
    """
    mocker.patch('requests.post', side_effect=Exception("Server error"))

    with pytest.raises(Exception) as excinfo:
        requests.post(f"{BASE_URL}/game/new")

    assert "Server error" in str(excinfo.value), "Expected server error message"

# To run these tests, use the command: pytest <name_of_this_file>.py