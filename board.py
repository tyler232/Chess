import pygame

pygame.init()

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
LIGHT_BROWN = (245, 222, 179)


PIECES = {
    "wp": pygame.image.load("wp.png"),  # white pawn
    "bp": pygame.image.load("bp.png"),  # black pawn
    "wr": pygame.image.load("wr.png"),  # white rook
    "br": pygame.image.load("br.png"),  # black rook
    "wn": pygame.image.load("wn.png"),  # white knight
    "bn": pygame.image.load("bn.png"),  # black knight
    "wb": pygame.image.load("wb.png"),  # white bishop
    "bb": pygame.image.load("bb.png"),  # black bishop
    "wq": pygame.image.load("wq.png"),  # white queen
    "bq": pygame.image.load("bq.png"),  # black queen
    "wk": pygame.image.load("wk.png"),  # white king
    "bk": pygame.image.load("bk.png"),  # black king
}

for piece in PIECES:
    PIECES[piece] = pygame.transform.scale(PIECES[piece], (SQUARE_SIZE, SQUARE_SIZE))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')

def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

board = [
    ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]
]

def draw_pieces():
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != "":
                screen.blit(PIECES[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))
