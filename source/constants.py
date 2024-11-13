from enum import Enum

class Color(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BROWN = (139, 69, 19)
    LIGHT_BROWN = (245, 222, 179)
    GREEN = (0, 255, 0)
    GRAY = (200, 200, 200)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    BLUE = (0, 0, 255)
    PURPLE = (255, 0, 255)
    ROYAL_PURPLE = (142, 81, 169)
    

class Player(Enum):
    WHITE = "w"
    BLACK = "b"

class Difficulty(Enum):
    NOVICE = "Novice"
    EASY = "Easy"
    STANDARD = "Standard"
    HARD = "Hard"
    EXPERT = "Expert"