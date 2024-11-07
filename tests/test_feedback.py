import pytest
import requests

BASE_URL = "http://localhost:3000"  # Replace with the actual base URL of the API
SECRET_WORD = "apple"  # Example secret word for testing


def test_correct_guess():
    """Test that a correct guess returns all letters as correct."""
    guess = "apple"
    response = requests.post(f"{BASE_URL}/submit-guess", json={"guess": guess})
    assert response.status_code == 200

    data = response.json()
    feedback = data.get("feedback")

    expected_feedback = [{"letter": "a", "status": "correct"},
                         {"letter": "p", "status": "correct"},
                         {"letter": "p", "status": "correct"},
                         {"letter": "l", "status": "correct"},
                         {"letter": "e", "status": "correct"}]

    assert feedback == expected_feedback, f"Unexpected feedback for correct guess: {feedback}"


def test_partial_correct_guess():
    """Test that a partially correct guess returns appropriate feedback."""
    guess = "apric"
    response = requests.post(f"{BASE_URL}/submit-guess", json={"guess": guess})
    assert response.status_code == 200

    data = response.json()
    feedback = data.get("feedback")

    expected_feedback = [{"letter": "a", "status": "correct"},
                         {"letter": "p", "status": "correct"},
                         {"letter": "r", "status": "absent"},
                         {"letter": "i", "status": "absent"},
                         {"letter": "c", "status": "absent"}]

    assert feedback == expected_feedback, f"Unexpected feedback for partially correct guess: {feedback}"


def test_wrong_position_guess():
    """Test that a guess with correct letters in the wrong position returns appropriate feedback."""
    guess = "pleap"
    response = requests.post(f"{BASE_URL}/submit-guess", json={"guess": guess})
    assert response.status_code == 200

    data = response.json()
    feedback = data.get("feedback")

    expected_feedback = [{"letter": "p", "status": "present"},
                         {"letter": "l", "status": "present"},
                         {"letter": "e", "status": "present"},
                         {"letter": "a", "status": "present"},
                         {"letter": "p", "status": "absent"}]

    assert feedback == expected_feedback, f"Unexpected feedback for wrong position guess: {feedback}"


def test_incorrect_guess():
    """Test that an incorrect guess returns all letters as absent."""
    guess = "wrong"
    response = requests.post(f"{BASE_URL}/submit-guess", json={"guess": guess})
    assert response.status_code == 200

    data = response.json()
    feedback = data.get("feedback")

    expected_feedback = [{"letter": "w", "status": "absent"},
                         {"letter": "r", "status": "absent"},
                         {"letter": "o", "status": "absent"},
                         {"letter": "n", "status": "absent"},
                         {"letter": "g", "status": "absent"}]

    assert feedback == expected_feedback, f"Unexpected feedback for incorrect guess: {feedback}"


if __name__ == "__main__":
    pytest.main()