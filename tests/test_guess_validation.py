import pytest
import requests

BASE_URL = "http://localhost:3000"  # Replace with the actual base URL of the API
VALID_WORDS = ["apple", "grape", "peach", "berry", "melon"]  # Example valid word dictionary


def test_valid_guess():
    """Test that a valid 5-letter word is accepted."""
    guess = "apple"
    response = requests.post(f"{BASE_URL}/submit-guess", json={"guess": guess})
    assert response.status_code == 200

    data = response.json()
    message = data.get("message")

    assert message == "Valid guess.", f"Unexpected message for valid guess: {message}"


def test_invalid_guess_not_in_dictionary():
    """Test that a word not in the dictionary is rejected."""
    guess = "abcde"
    response = requests.post(f"{BASE_URL}/submit-guess", json={"guess": guess})
    assert response.status_code == 400

    data = response.json()
    message = data.get("message")

    assert message == "Invalid word. Please enter a valid 5-letter word.", f"Unexpected message for invalid guess: {message}"


def test_invalid_guess_wrong_length():
    """Test that a word with incorrect length is rejected."""
    guess = "abcd"  # 4 letters
    response = requests.post(f"{BASE_URL}/submit-guess", json={"guess": guess})
    assert response.status_code == 400

    data = response.json()
    message = data.get("message")

    assert message == "Invalid word length. Please enter a 5-letter word.", f"Unexpected message for wrong length: {message}"


def test_invalid_guess_non_alpha():
    """Test that a word with non-alphabetic characters is rejected."""
    guess = "12345"
    response = requests.post(f"{BASE_URL}/submit-guess", json={"guess": guess})
    assert response.status_code == 400

    data = response.json()
    message = data.get("message")

    assert message == "Invalid word. Please enter a valid 5-letter word.", f"Unexpected message for non-alpha guess: {message}"


if __name__ == "__main__":
    pytest.main()