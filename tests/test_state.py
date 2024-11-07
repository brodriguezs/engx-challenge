import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_HOST = os.getenv("HOST")
BASE_URL = f"http://{BASE_HOST}:8000"  # Replace with the actual base URL of your API


def test_game_in_progress():
    """
    Test the game state when the game is in progress.
    """
    game_id = "5678"
    response = requests.get(f"{BASE_URL}/game/{game_id}/state")

    assert response.status_code == 200, "Expected status code 200"

    json_response = response.json()
    assert json_response["game_id"] == game_id, "Game ID should match"
    assert json_response["attempts_left"] == 3, "Expected 3 attempts left"
    assert json_response["is_won"] is False, "Game should not be won"
    assert json_response["is_over"] is False, "Game should not be over"


def test_game_won():
    """
    Test the game state when the game is won.
    """
    game_id = "5678"
    response = requests.get(f"{BASE_URL}/game/{game_id}/state")

    assert response.status_code == 200, "Expected status code 200"

    json_response = response.json()
    assert json_response["game_id"] == game_id, "Game ID should match"
    assert json_response["attempts_left"] == 2, "Expected 2 attempts left"
    assert json_response["is_won"] is True, "Game should be won"
    assert json_response["is_over"] is True, "Game should be over"


def test_game_lost():
    """
    Test the game state when the game is lost.
    """
    game_id = "5678"
    response = requests.get(f"{BASE_URL}/game/{game_id}/state")

    assert response.status_code == 200, "Expected status code 200"

    json_response = response.json()
    assert json_response["game_id"] == game_id, "Game ID should match"
    assert json_response["attempts_left"] == 0, "Expected 0 attempts left"
    assert json_response["is_won"] is False, "Game should not be won"
    assert json_response["is_over"] is True, "Game should be over"


def test_game_not_found():
    """
    Test the response when the game is not found.
    """
    game_id = "9999"
    response = requests.get(f"{BASE_URL}/game/{game_id}/state")

    assert response.status_code == 404, "Expected status code 404 for not found"

    json_response = response.json()
    assert "detail" in json_response, "Response should contain 'detail'"
    assert json_response["detail"] == "Game not found", "Expected 'Game not found' message"