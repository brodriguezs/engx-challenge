import pytest
import requests

BASE_URL = "http://localhost:5000"  # Replace with the actual base URL of the API
SECRET_WORD = "apple"  # Example secret word for testing


def test_win_condition():
    """Test that the game ends with a win when the user guesses the word within 6 tries."""
    # Simulate guesses
    guesses = ["grape", "peach", "apple"]  # The correct word is guessed on the third try

    for guess in guesses:
        response = requests.post(f"{BASE_URL}/submit-guess", json={"guess": guess})
        assert response.status_code == 200

    # Check game status
    response = requests.get(f"{BASE_URL}/game-status")
    assert response.status_code == 200

    data = response.json()
    game_over = data.get("game_over")
    result = data.get("result")

    assert game_over is True, "Game should be over after a correct guess."
    assert result == "win", f"Unexpected result for win condition: {result}"


def test_loss_condition():
    """Test that the game ends with a loss when the user does not guess the word after 6 attempts."""
    # Simulate 6 incorrect guesses
    guesses = ["grape", "peach", "melon", "berry", "lemon", "mango"]

    for guess in guesses:
        response = requests.post(f"{BASE_URL}/submit-guess", json={"guess": guess})
        assert response.status_code == 200

    # Check game status
    response = requests.get(f"{BASE_URL}/game-status")
    assert response.status_code == 200

    data = response.json()
    game_over = data.get("game_over")
    result = data.get("result")

    assert game_over is True, "Game should be over after 6 incorrect guesses."
    assert result == "lose", f"Unexpected result for loss condition: {result}"


def test_restart_game():
    """Test that the user can start a new game after a win or loss."""
    # End the current game with a win
    response = requests.post(f"{BASE_URL}/submit-guess", json={"guess": SECRET_WORD})
    assert response.status_code == 200

    # Check game status to confirm win
    response = requests.get(f"{BASE_URL}/game-status")
    assert response.status_code == 200

    data = response.json()
    assert data.get("game_over") is True, "Game should be over after a correct guess."

    # Start a new game
    response = requests.post(f"{BASE_URL}/start-game")
    assert response.status_code == 200

    # Check game status to confirm new game has started
    response = requests.get(f"{BASE_URL}/game-status")
    assert response.status_code == 200

    data = response.json()
    assert data.get("game_over") is False, "New game should not be over immediately."


if __name__ == "__main__":
    pytest.main()