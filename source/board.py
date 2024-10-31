import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 900, 900
BOARD_WIDTH, BOARD_HEIGHT = int(SCREEN_WIDTH * 0.84), int(SCREEN_HEIGHT * 0.84)
BAR_HEIGHT = (SCREEN_HEIGHT - BOARD_HEIGHT) // 2
ROWS, COLS = 8, 8
SQUARE_SIZE = BOARD_WIDTH // COLS
BOARD_START_X = (SCREEN_WIDTH - BOARD_WIDTH) // 2
BOARD_START_Y = (SCREEN_HEIGHT - BOARD_HEIGHT) // 2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
LIGHT_BROWN = (245, 222, 179)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

PIECES = {
    "wp": pygame.image.load("assets/wp.png"),  # white pawn
    "bp": pygame.image.load("assets/bp.png"),  # black pawn
    "wr": pygame.image.load("assets/wr.png"),  # white rook
    "br": pygame.image.load("assets/br.png"),  # black rook
    "wn": pygame.image.load("assets/wn.png"),  # white knight
    "bn": pygame.image.load("assets/bn.png"),  # black knight
    "wb": pygame.image.load("assets/wb.png"),  # white bishop
    "bb": pygame.image.load("assets/bb.png"),  # black bishop
    "wq": pygame.image.load("assets/wq.png"),  # white queen
    "bq": pygame.image.load("assets/bq.png"),  # black queen
    "wk": pygame.image.load("assets/wk.png"),  # white king
    "bk": pygame.image.load("assets/bk.png"),  # black king
}

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
for piece in PIECES:
    PIECES[piece] = pygame.transform.scale(PIECES[piece], (SQUARE_SIZE, SQUARE_SIZE))

def draw_top_bar(screen, opponent_name, score):
    font_size = int(BAR_HEIGHT * 0.4)
    font = pygame.font.Font(None, font_size)
    text = font.render(f"Opponent: {opponent_name}", True, WHITE)
    screen.blit(text, (10, 10))
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10 + font_size))

def delete_top_bar(screen):
    pygame.draw.rect(screen, BLACK, (0, 0, BOARD_WIDTH, BAR_HEIGHT))

def draw_bottom_bar(screen, player_name, score):
    font_size = int(BAR_HEIGHT * 0.4)
    font = pygame.font.Font(None, font_size)
    text = font.render(f"Player: {player_name}", True, WHITE)
    screen.blit(text, (10, BOARD_HEIGHT + BAR_HEIGHT))
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, BOARD_HEIGHT + BAR_HEIGHT + 36))

def delete_bottom_bar(screen):
    pygame.draw.rect(screen, BLACK, (0, BOARD_HEIGHT + BAR_HEIGHT, BOARD_WIDTH, BAR_HEIGHT))
    
def draw_board(screen):
    # Calculate the starting position of the board
    board_start_x = (SCREEN_WIDTH - BOARD_WIDTH) // 2
    board_start_y = (SCREEN_HEIGHT - BOARD_HEIGHT) // 2
    for row in range(ROWS):
        for col in range(COLS):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(screen, color, (board_start_x + col * SQUARE_SIZE, board_start_y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_select_piece(screen, selected_piece, player_color):
    if player_color == "BLACK":
        row = ROWS - 1 - selected_piece[0]  # Reverse the row for Black
        col = selected_piece[1]
    else:
        row, col = selected_piece

    pygame.draw.rect(screen, GREEN, (BOARD_START_X + col * SQUARE_SIZE, BOARD_START_Y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_possible_moves(screen, possible_moves, player_color):
    for move in possible_moves:
        if player_color == "BLACK":
            row = ROWS - 1 - move[0]  # Reverse the row for Black
            col = move[1]
        else:
            row, col = move
        pygame.draw.rect(screen, GREEN, (BOARD_START_X + col * SQUARE_SIZE, BOARD_START_Y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(screen, player_color, board):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != "":
                if player_color == "WHITE":
                    screen.blit(PIECES[piece], (BOARD_START_X + col * SQUARE_SIZE, BOARD_START_Y + row * SQUARE_SIZE))
                elif player_color == "BLACK":
                    screen.blit(PIECES[piece], (BOARD_START_X + col * SQUARE_SIZE, BOARD_START_Y + (ROWS - 1 - row) * SQUARE_SIZE))

def draw_in_check(screen, king_loc, player_color):
    if player_color == "BLACK":
        row = ROWS - 1 - king_loc[0]
        col = king_loc[1]
    else:
        row, col = king_loc

    pygame.draw.rect(screen, RED, (BOARD_START_X + col * SQUARE_SIZE, BOARD_START_Y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def promotion_selection(player_color):
    font = pygame.font.Font(None, 36)
    options = ["q", "r", "b", "n"]  # The promotion options (Queen, Rook, Bishop, Knight)
    piece_images = {
        "q": pygame.image.load("assets/wq.png" if player_color == "WHITE" else "assets/bq.png"),
        "r": pygame.image.load("assets/wr.png" if player_color == "WHITE" else "assets/br.png"),
        "b": pygame.image.load("assets/wb.png" if player_color == "WHITE" else "assets/bb.png"),
        "n": pygame.image.load("assets/wn.png" if player_color == "WHITE" else "assets/bn.png"),
    }

    selected_piece = None

    # Set the dimensions and position for the selection box
    box_width = 300
    box_height = 120
    box_x = (BOARD_WIDTH - box_width) // 2
    box_y = (BOARD_HEIGHT - box_height) // 2

    # Draw the selection box
    pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height))
    pygame.draw.rect(screen, BROWN, (box_x + 5, box_y + 5, box_width - 10, box_height - 10))  # Inner white box

    title_text = font.render("Promote to:", True, (255, 0, 0))
    screen.blit(title_text, (box_x + 10, box_y + 10))
    spacing = (box_width - 20) // len(options)

    # Draw options (images)
    for i, option in enumerate(options):
        piece_image = piece_images[option]
        piece_image = pygame.transform.scale(piece_image, (60, 60))  # Resize the image if needed
        image_rect = piece_image.get_rect(center=(box_x + 10 + i * spacing + spacing // 2, box_y + box_height // 2))
        screen.blit(piece_image, image_rect)

    pygame.display.flip()

    # Wait for user selection
    while selected_piece is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Check if the click is within the selection box
                if box_x < pos[0] < box_x + box_width and box_y < pos[1] < box_y + box_height:
                    # Calculate which piece was clicked based on the position
                    for i in range(len(options)):
                        piece_rect = piece_images[options[i]].get_rect(center=(box_x + 10 + i * spacing + spacing // 2, box_y + box_height // 2))
                        if piece_rect.collidepoint(pos):  # Check if click is on this piece
                            selected_piece = options[i]  # Get the letter for the selected piece
                            break
    return selected_piece

def resize_screen(width, height):
    global SCREEN_WIDTH, SCREEN_HEIGHT, BOARD_WIDTH, BOARD_HEIGHT, SQUARE_SIZE, BOARD_START_X, BOARD_START_Y, BAR_HEIGHT
    SCREEN_WIDTH, SCREEN_HEIGHT = width, height
    BOARD_WIDTH, BOARD_HEIGHT = int(SCREEN_WIDTH * 0.84), int(SCREEN_HEIGHT * 0.84)
    BOARD_WIDTH = BOARD_HEIGHT = min(BOARD_WIDTH, BOARD_HEIGHT)
    SQUARE_SIZE = BOARD_WIDTH // COLS
    BOARD_START_X = (SCREEN_WIDTH - BOARD_WIDTH) // 2
    BOARD_START_Y = (SCREEN_HEIGHT - BOARD_HEIGHT) // 2
    BAR_HEIGHT = (SCREEN_HEIGHT - BOARD_HEIGHT) // 2
    for piece in PIECES:
        PIECES[piece] = pygame.transform.scale(PIECES[piece], (SQUARE_SIZE, SQUARE_SIZE))
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    return screen

def display_message(screen, message):
    font = pygame.font.Font(None, 74)
    text = font.render(message, True, (255, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)
