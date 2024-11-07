import pytest
import requests


BASE_URL = "http://localhost:3000"  # Replace with the actual base URL of the API
WORD_LIST = ["apple", "grape", "peach", "berry", "melon"]  # Example predefined word list


def test_word_selection_success():
    """Test that a 5-letter word is selected from the predefined list."""
    response = requests.post(f"{BASE_URL}/start-game")
    assert response.status_code == 200

    data = response.json()
    selected_word = data.get("selected_word")

    assert selected_word is not None, "No word was selected."
    assert selected_word in WORD_LIST, "Selected word is not in the predefined list."
    assert len(selected_word) == 5, "Selected word is not 5 letters long."


def test_randomness_of_word_selection():
    """Test that the word selection is random by checking for variability over multiple requests."""
    selected_words = set()
    num_trials = 100

    for _ in range(num_trials):
        response = requests.post(f"{BASE_URL}/start-game")
        assert response.status_code == 200

        data = response.json()
        selected_word = data.get("selected_word")
        assert selected_word in WORD_LIST, "Selected word is not in the predefined list."
        selected_words.add(selected_word)

    # Check that more than one unique word was selected over multiple trials
    assert len(selected_words) > 1, "Word selection does not appear to be random."


def test_invalid_endpoint():
    """Test the behavior when an invalid endpoint is accessed."""
    response = requests.post(f"{BASE_URL}/invalid-endpoint")
    assert response.status_code == 404, "Expected 404 Not Found for invalid endpoint."


def test_method_not_allowed():
    """Test the behavior when an incorrect HTTP method is used."""
    response = requests.get(f"{BASE_URL}/start-game")
    assert response.status_code == 405, "Expected 405 Method Not Allowed for GET request."


if __name__ == "__main__":
    pytest.main()