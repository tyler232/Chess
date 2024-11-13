import ctypes
from ctypes import Structure, c_int, c_char

# Define constants
BOARD_SIZE = 8
BUF_SIZE = 512

# Define the Position class to match the C struct
class Position(Structure):
    _fields_ = [("x", c_int), ("y", c_int)]

# Load the shared library
lib = ctypes.CDLL('./ai_movement.so')

# Set up the argument and return types for the C function
lib.possible_moves_rook.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), Position, c_char, ctypes.POINTER(Position)]
lib.possible_moves_rook.restype = ctypes.POINTER(Position)

# Create the board with pieces represented by strings like "br" for black rook, "wp" for white pawn, etc.
board = [
    ["wr", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""]
]

# Convert the board into a format suitable for passing to C
def create_board(board):
    ctypes_board = (ctypes.POINTER(ctypes.c_char) * BOARD_SIZE)()

    for i in range(BOARD_SIZE):
        row = (ctypes.c_char * BUF_SIZE)()

        for j in range(BOARD_SIZE):
            piece = board[i][j].encode('utf-8')

            for k in range(len(piece)):
                row[j] = piece[k]

            for k in range(len(piece), BUF_SIZE):
                row[j] = 0

        ctypes_board[i] = ctypes.pointer(row)

    return ctypes_board

# Prepare the board for passing to C
ctypes_board = create_board(board)

# Initialize the starting position of the rook (for example, white rook at (0, 0))
start_pos = Position(0, 0)

# Define the color of the rook ('w' for white, 'b' for black)
color = b'w'

# Prepare the array to store possible moves (64 possible moves max)
possible_moves = (Position * 64)()

# Call the C function to get the possible moves for the rook
moves_ptr = lib.possible_moves_rook(ctypes_board, start_pos, color, possible_moves)

# Print the possible moves
for i in range(64):
    if possible_moves[i].x == 0 and possible_moves[i].y == 0:
        break  # Exit when the first zero move is encountered (indicating no more valid moves)
    print(f"Possible move: ({possible_moves[i].x}, {possible_moves[i].y})")
