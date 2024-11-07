import requests
import pytest
import os
from dotenv import load_dotenv

load_dotenv()

BASE_HOST = os.getenv("HOST")
BASE_URL = f"http://{BASE_HOST}:8000"  # Replace with the actual base URL of your API


@pytest.mark.parametrize("word, expected_status, expected_response", [
    # Scenario 1: Valid guess, not correct
    ("beach", 200, {
        "is_valid": True,
        "feedback": ["gray", "green", "yellow", "gray", "gray"],
        "message": None
    }),
    # Scenario 2: Invalid word
    ("zzzzz", 200, {
        "is_valid": False,
        "feedback": None,
        "message": "Invalid word. Please enter a valid 5-letter word."
    }),
    # Scenario 3: Correct guess (win condition)
    ("eagle", 200, {
        "is_valid": True,
        "feedback": ["green", "green", "green", "green", "green"],
        "message": "Congratulations! You've won!"
    }),
    # Scenario 4: Last attempt, incorrect (lose condition)
    ("chair", 200, {
        "is_valid": True,
        "feedback": ["gray", "gray", "green", "gray", "gray"],
        "message": "Game over. The word was eagle."
    }),
])
def test_guess_word(word, expected_status, expected_response):
    response = requests.post(f"{BASE_URL}/game/5678/guess", json={"word": word})

    assert response.status_code == expected_status
    assert response.json() == expected_response


if __name__ == "__main__":
    pytest.main()