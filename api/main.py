from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import random

app = FastAPI()

# Models
class Guess(BaseModel):
    word: str

class GuessResponse(BaseModel):
    is_valid: bool
    feedback: Optional[List[str]] = None
    message: Optional[str] = None

class GameState(BaseModel):
    game_id: str
    attempts_left: int
    is_won: bool
    is_over: bool

class NewGameResponse(BaseModel):
    game_id: str
    message: str

# In-memory storage (replace with database in production)
games = {}
word_list = ["apple", "beach", "chair", "dance", "eagle"]  # Example word list
valid_words = set(word_list + ["valid", "words", "added", "here"])  # Add more valid words

@app.post("api/game/new", response_model=NewGameResponse)
async def new_game():
    game_id = str(random.randint(1000, 9999))
    target_word = random.choice(word_list)
    games[game_id] = {
        "target_word": target_word,
        "attempts_left": 6,
        "is_won": False,
        "is_over": False
    }
    return NewGameResponse(game_id=game_id, message="New game started!")

@app.post("api/game/{game_id}/guess", response_model=GuessResponse)
async def make_guess(game_id: str, guess: Guess):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games[game_id]
    
    if game["is_over"]:
        raise HTTPException(status_code=400, detail="Game is already over")
    
    if len(guess.word) != 5 or guess.word.lower() not in valid_words:
        return GuessResponse(is_valid=False, message="Invalid word. Please enter a valid 5-letter word.")
    
    feedback = []
    target_word = game["target_word"]
    
    for i, letter in enumerate(guess.word.lower()):
        if letter == target_word[i]:
            feedback.append("green")
        elif letter in target_word:
            feedback.append("yellow")
        else:
            feedback.append("gray")
    
    game["attempts_left"] -= 1
    
    if guess.word.lower() == target_word:
        game["is_won"] = True
        game["is_over"] = True
        return GuessResponse(is_valid=True, feedback=feedback, message="Congratulations! You've won!")
    
    if game["attempts_left"] == 0:
        game["is_over"] = True
        return GuessResponse(is_valid=True, feedback=feedback, 
                             message=f"Game over. The word was {target_word}.")
    
    return GuessResponse(is_valid=True, feedback=feedback)

@app.get("api/game/{game_id}/state", response_model=GameState)
async def get_game_state(game_id: str):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games[game_id]
    return GameState(
        game_id=game_id,
        attempts_left=game["attempts_left"],
        is_won=game["is_won"],
        is_over=game["is_over"]
    )