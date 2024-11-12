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

class Player(Enum):
    WHITE = "w"
    BLACK = "b"

