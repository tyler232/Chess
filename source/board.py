import pygame
import time
from source.constants import *

SCREEN_WIDTH, SCREEN_HEIGHT = 900, 900
BOARD_WIDTH, BOARD_HEIGHT = int(SCREEN_WIDTH * 0.84), int(SCREEN_HEIGHT * 0.84)
BAR_HEIGHT = (SCREEN_HEIGHT - BOARD_HEIGHT) // 2
ROWS, COLS = 8, 8
SQUARE_SIZE = BOARD_WIDTH // COLS
BOARD_START_X = (SCREEN_WIDTH - BOARD_WIDTH) // 2
BOARD_START_Y = (SCREEN_HEIGHT - BOARD_HEIGHT) // 2

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

msg_interrupt_flag = False

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
for piece in PIECES:
    PIECES[piece] = pygame.transform.scale(PIECES[piece], (SQUARE_SIZE, SQUARE_SIZE))

def draw_mode_selection(screen):
    '''
    Draw the mode selection screen
    '''
    font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.05))
    
    # Draw the title
    title_text = font.render("Select Game Mode", True, Color.WHITE.value)
    title_text_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(title_text, title_text_rect)

    # Draw the buttons
    button_width = int(SCREEN_WIDTH * 0.3)
    button_height = int(SCREEN_HEIGHT * 0.1)
    single_mode_button_x = (SCREEN_WIDTH - button_width) // 2
    single_mode_button_y = SCREEN_HEIGHT // 2
    multi_mode_button_x = single_mode_button_x
    multi_mode_button_y = single_mode_button_y + button_height + int(SCREEN_HEIGHT * 0.1)
    single_mode_button = pygame.Rect(single_mode_button_x, single_mode_button_y, button_width, button_height)
    multi_mode_button = pygame.Rect(multi_mode_button_x, multi_mode_button_y, button_width, button_height)

    pygame.draw.rect(screen, Color.LIGHT_BROWN.value, single_mode_button)
    pygame.draw.rect(screen, Color.BROWN.value, multi_mode_button)

    # Button text
    button_font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.04))
    single_text = button_font.render("Single Player", True, Color.WHITE.value)
    multi_text = button_font.render("Multiplayer", True, Color.WHITE.value)

    # Position text at the center of each button
    single_text_rect = single_text.get_rect(center=single_mode_button.center)
    multi_text_rect = multi_text.get_rect(center=multi_mode_button.center)

    # Blit text onto the screen
    screen.blit(single_text, single_text_rect)
    screen.blit(multi_text, multi_text_rect)

    # Selection
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if single_mode_button.collidepoint(pos):
                    clear_screen(screen)
                    return "single"
                elif multi_mode_button.collidepoint(pos):
                    clear_screen(screen)
                    return "multi"
        pygame.display.flip()

    return None

def draw_difficulty_selection(screen):
    '''
    Draw the difficulty selection screen
    '''
    font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.05))
    
    title_text = font.render("Select Difficulty", True, Color.WHITE.value)
    title_text_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 10))
    screen.blit(title_text, title_text_rect)

    # Difficulty levels and their positions
    difficulty_levels = [Difficulty.NOVICE, Difficulty.EASY, Difficulty.STANDARD, Difficulty.HARD, Difficulty.EXPERT]
    text_color = [Color.BLACK, Color.GREEN, Color.BLUE, Color.ROYAL_PURPLE, Color.RED]
    button_width = int(SCREEN_WIDTH * 0.3)
    button_height = int(SCREEN_HEIGHT * 0.08)
    button_x = (SCREEN_WIDTH - button_width) // 2
    spacing = int(SCREEN_HEIGHT * 0.07)

    # Draw each button
    buttons = []
    for i, level in enumerate(difficulty_levels):
        button_y = (SCREEN_HEIGHT // 6) + i * (button_height + spacing)  # Move up the starting y-position
        button = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, Color.LIGHT_BROWN.value if i % 2 != 0 else Color.BROWN.value, button)
        
        # Button text
        button_font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.04))
        level_text = button_font.render(level.value, True, text_color[i].value)
        level_text_rect = level_text.get_rect(center=button.center)
        
        # Blit text onto the screen
        screen.blit(level_text, level_text_rect)
        
        # Store button and level
        buttons.append((button, level))

    # Selection
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button, level in buttons:
                    if button.collidepoint(pos):
                        clear_screen(screen)
                        return level
        
        pygame.display.flip()


    

def draw_top_bar(screen, opponent_name, score, sound_on, oppo_name_coloring=Color.WHITE.value):
    '''
    Draw the top bar with the opponent's name and score
    '''
    font_size = int(BAR_HEIGHT * 0.4)
    font = pygame.font.Font(None, font_size)
    text = font.render(f"Opponent: {opponent_name}", True, oppo_name_coloring)
    screen.blit(text, (10, 10))
    score_text = font.render(f"Score: {score}", True, Color.WHITE.value)
    screen.blit(score_text, (10, 10 + font_size))

    music_icon = pygame.image.load("assets/music_icon.png").convert_alpha()
    icon_size = int(BAR_HEIGHT * 0.8)  # Scale icon to 80% of bar height
    music_icon = pygame.transform.scale(music_icon, (icon_size, icon_size))
    
    # Calculate icon position as a percentage of the screen width
    icon_x = screen.get_width() * 0.9  # 90% of screen width
    icon_y = (BAR_HEIGHT - icon_size) / 2
    music_icon_rect = pygame.Rect(icon_x, icon_y, icon_size, icon_size)
    screen.blit(music_icon, (icon_x, icon_y))

    if not sound_on:
        line_thickness = 3
        pygame.draw.line(screen, Color.RED.value, (icon_x, icon_y), (icon_x + icon_size, icon_y + icon_size), line_thickness)
        pygame.draw.line(screen, Color.RED.value, (icon_x + icon_size, icon_y), (icon_x, icon_y + icon_size), line_thickness)
    
    return music_icon_rect


def delete_top_bar(screen):
    '''
    Delete the top bar
    '''
    pygame.draw.rect(screen, Color.BLACK.value, (0, 0, BOARD_WIDTH, BAR_HEIGHT))

def draw_bottom_bar(screen, player_name, score):
    '''
    Draw the bottom bar with the player's name, score, and resign button.
    '''
    # Draw the info text
    font_size = int(BAR_HEIGHT * 0.4)
    font = pygame.font.Font(None, font_size)
    text = font.render(f"Player: {player_name}", True, Color.WHITE.value)
    screen.blit(text, (10, BOARD_HEIGHT + BAR_HEIGHT))
    score_text = font.render(f"Score: {score}", True, Color.WHITE.value)
    screen.blit(score_text, (10, BOARD_HEIGHT + BAR_HEIGHT + 36))

    # Draw resign button
    button_width = int(SCREEN_WIDTH * 0.15)
    button_height = int(BAR_HEIGHT * 0.6)
    resign_button_x = int(SCREEN_WIDTH * 0.85) - button_width
    resign_button_y = BOARD_HEIGHT + BAR_HEIGHT + int(BAR_HEIGHT * 0.2)
    pygame.draw.rect(screen, Color.RED.value, (resign_button_x, resign_button_y, button_width, button_height))

    # Draw Draw button
    draw_button_x = int(SCREEN_WIDTH * 0.80) - (2 * button_width)
    draw_button_y = resign_button_y
    pygame.draw.rect(screen, Color.YELLOW.value, (draw_button_x, draw_button_y, button_width, button_height))
    
    # Draw resign button text
    button_text = font.render("Resign", True, Color.WHITE.value)
    text_rect = button_text.get_rect(center=(resign_button_x + button_width / 2, resign_button_y + button_height / 2))
    screen.blit(button_text, text_rect)

    # Draw stalemate button text
    button_text = font.render("Draw", True, Color.BLACK.value)
    text_rect = button_text.get_rect(center=(draw_button_x + button_width / 2, draw_button_y + button_height / 2)) 
    screen.blit(button_text, text_rect)

    return [resign_button_x, resign_button_y, draw_button_x, draw_button_y, button_width, button_height]

def button_clicked(mouse_x, mouse_y, button_x, button_y, button_width, button_height):
    '''
    Checks if the mouse click is inside resign button
    '''
    return button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height

def delete_bottom_bar(screen):
    '''
    Delete the bottom bar
    '''
    pygame.draw.rect(screen, Color.BLACK.value, (0, BOARD_HEIGHT + BAR_HEIGHT, BOARD_WIDTH, BAR_HEIGHT))
    
def draw_board(screen):
    '''
    Draw the chess board
    '''
    # Calculate the starting position of the board
    board_start_x = (SCREEN_WIDTH - BOARD_WIDTH) // 2
    board_start_y = (SCREEN_HEIGHT - BOARD_HEIGHT) // 2
    for row in range(ROWS):
        for col in range(COLS):
            color = Color.LIGHT_BROWN.value if (row + col) % 2 == 0 else Color.BROWN.value
            pygame.draw.rect(screen, color, (board_start_x + col * SQUARE_SIZE, board_start_y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_select_piece(screen, selected_piece, player):
    '''
    draw a green square around the selected piece
    '''
    if player == Player.BLACK:
        row = ROWS - 1 - selected_piece[0]  # Reverse the row for Black
        col = selected_piece[1]
    else:
        row, col = selected_piece

    pygame.draw.rect(screen, Color.GREEN.value, (BOARD_START_X + col * SQUARE_SIZE, BOARD_START_Y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_possible_moves(screen, possible_moves, player):
    '''
    Draw green squares around the possible moves
    '''
    for move in possible_moves:
        if player == Player.BLACK:
            row = ROWS - 1 - move[0]  # Reverse the row for Black
            col = move[1]
        else:
            row, col = move
        pygame.draw.rect(screen, Color.GREEN.value, (BOARD_START_X + col * SQUARE_SIZE, BOARD_START_Y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(screen, player, board):
    '''
    draw pieces on board
    '''
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != "":
                if player == Player.WHITE:
                    screen.blit(PIECES[piece], (BOARD_START_X + col * SQUARE_SIZE, BOARD_START_Y + row * SQUARE_SIZE))
                elif player == Player.BLACK:
                    screen.blit(PIECES[piece], (BOARD_START_X + col * SQUARE_SIZE, BOARD_START_Y + (ROWS - 1 - row) * SQUARE_SIZE))

def draw_in_check(screen, king_loc, player):
    '''
    draw a red square around the king if in check
    '''
    if player == Player.BLACK:
        row = ROWS - 1 - king_loc[0]
        col = king_loc[1]
    else:
        row, col = king_loc

    pygame.draw.rect(screen, Color.RED.value, (BOARD_START_X + col * SQUARE_SIZE, BOARD_START_Y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_last_move(last_move, screen, player):
    '''
    draw a yellow outer layer around the last move
    '''
    if not last_move:
        return  # If there’s no last move, simply return
    
    last_move_from = last_move[1]  # Starting position of the move (row, col)
    last_move_to = last_move[2]    # Ending position of the move (row, col)

    # Yellow border for the 'from' square
    from_x = BOARD_START_X + last_move_from[1] * SQUARE_SIZE
    from_y = BOARD_START_Y + last_move_from[0] * SQUARE_SIZE

    # Yellow border for the 'to' square
    to_x = BOARD_START_X + last_move_to[1] * SQUARE_SIZE
    to_y = BOARD_START_Y + last_move_to[0] * SQUARE_SIZE

    if player == Player.BLACK:
        from_y = BOARD_START_Y + (ROWS - 1 - last_move_from[0]) * SQUARE_SIZE
        to_y = BOARD_START_Y + (ROWS - 1 - last_move_to[0]) * SQUARE_SIZE

    pygame.draw.rect(screen, Color.YELLOW.value, (to_x, to_y, SQUARE_SIZE, SQUARE_SIZE), 5)
    pygame.draw.rect(screen, Color.YELLOW.value, (from_x, from_y, SQUARE_SIZE, SQUARE_SIZE), 5)


def promotion_selection(screen, player):
    '''
    promotion selection screen and return the selected piece of which the pawn will be promoted to
    '''
    font = pygame.font.Font(None, 36)
    options = ["q", "r", "b", "n"]  # The promotion options (Queen, Rook, Bishop, Knight)
    piece_images = {
        "q": pygame.image.load("assets/wq.png" if player == Player.WHITE else "assets/bq.png"),
        "r": pygame.image.load("assets/wr.png" if player == Player.WHITE else "assets/br.png"),
        "b": pygame.image.load("assets/wb.png" if player == Player.WHITE else "assets/bb.png"),
        "n": pygame.image.load("assets/wn.png" if player == Player.WHITE else "assets/bn.png"),
    }

    selected_piece = None

    # Set the dimensions and position for the selection box
    box_width = 300
    box_height = 120
    box_x = (BOARD_WIDTH - box_width) // 2
    box_y = (BOARD_HEIGHT - box_height) // 2

    # Draw the selection box
    pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height))
    pygame.draw.rect(screen, Color.BROWN.value, (box_x + 5, box_y + 5, box_width - 10, box_height - 10))  # Inner white box

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
    clear_screen(screen)
    return selected_piece

def resize_screen(width, height):
    '''
    resize the screen and return the new screen
    '''
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
    clear_screen(screen)
    return screen

def draw_confirm_window(screen, text):
    '''
    Draw a confirmation window
    '''
    window_width = int(SCREEN_WIDTH * 0.5)
    window_height = int(SCREEN_HEIGHT * 0.3)
    window_x = (SCREEN_WIDTH - window_width) // 2
    window_y = (SCREEN_HEIGHT - window_height) // 2
    pygame.draw.rect(screen, Color.GRAY.value, (window_x, window_y, window_width, window_height))
    pygame.draw.rect(screen, Color.BLACK.value, (window_x, window_y, window_width, window_height), 2)

    # Confirmation text
    font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.03))
    text = font.render(text, True, Color.BLACK.value)
    screen.blit(text, (window_x + int(SCREEN_HEIGHT * 0.05), window_y + int(SCREEN_HEIGHT * 0.08)))

    # Draw "Yes" button
    confirm_button_width = int(window_width * 0.25)
    confirm_button_height = int(window_height * 0.15)

    yes_button_x = window_x + int(window_width * 0.1)
    yes_button_y = window_y + int(window_height * 0.55)
    yes_button = pygame.Rect(yes_button_x, yes_button_y, confirm_button_width, confirm_button_height)
    pygame.draw.rect(screen, Color.RED.value, yes_button)
    yes_text = font.render("Yes", True, Color.WHITE.value)
    screen.blit(yes_text, (yes_button_x + confirm_button_width // 3, yes_button_y + confirm_button_height // 6))

    # Draw "No" button
    no_button_x = window_x + int(window_width * 0.65)
    no_button_y = yes_button_y
    no_button = pygame.Rect(no_button_x, no_button_y, confirm_button_width, confirm_button_height)
    pygame.draw.rect(screen, Color.RED.value, no_button)
    no_text = font.render("No", True, Color.WHITE.value)
    screen.blit(no_text, (no_button_x + confirm_button_width // 3, no_button_y + confirm_button_height // 6))


    pygame.display.flip()

    # Wait for user confirmation
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return handle_confirmation(event, yes_button, no_button)
            else:
                break
    return None

def handle_confirmation(event, yes_button, no_button):
    '''
    Handle clicks on the "Yes" or "No" buttons in the confirm window.
    '''
    if event.type == pygame.MOUSEBUTTONDOWN:
        if yes_button.collidepoint(event.pos):
            print("Resignation confirmed")
            return True
        elif no_button.collidepoint(event.pos):
            print("Resignation canceled")
            return False
    return None

def display_message(screen, message):
    '''
    display a message on the screen
    '''
    font = pygame.font.Font(None, 74)
    text = font.render(message, True, (255, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

def display_message_with_serverip(screen, message, server_ip):
    font = pygame.font.Font(None, 74)
    text = font.render(message, True, (255, 0, 0))
    server_text = font.render("SERVER IP: " + server_ip, True, (255, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    server_text_rect = server_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + (SCREEN_HEIGHT * 0.15)))
    screen.blit(server_text, server_text_rect)
    pygame.display.flip()



def display_temp_message(screen, message, duration, player, board):
    '''
    Display a temporary message centered on the board, interruptible by new messages.
    '''
    global interrupt_flag
    interrupt_flag = True  # Set flag to indicate a new message is being displayed

    font = pygame.font.Font(None, 36)
    msg_surface = font.render(message, True, (255, 255, 255))
    msg_rec = msg_surface.get_rect(center=(
        BOARD_START_X + BOARD_WIDTH // 2,
        BOARD_START_Y + BOARD_HEIGHT // 2
    ))

    # Draw the message and update the display
    screen.blit(msg_surface, msg_rec)
    pygame.display.flip()
    
    # Track the start time to manage duration
    start_time = time.time()
    
    while time.time() - start_time < duration / 1000.0:
        # Check if an interrupt request has come in
        if not interrupt_flag:
            break

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                interrupt_flag = False  # Interrupt the message immediately
                break
        pygame.event.pump()  # Handle events to avoid freezing

    # Reset the interrupt flag and clear the message by redrawing
    interrupt_flag = False
    draw_board(screen)
    draw_pieces(screen, player, board)
    pygame.display.flip()

def draw_start_or_join_server(screen):
    font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.05))

    # Draw the title
    title_text = font.render("Start or Join Server", True, Color.WHITE.value)

    title_text_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(title_text, title_text_rect)

    # Draw the buttons
    button_width = int(SCREEN_WIDTH * 0.3)
    button_height = int(SCREEN_HEIGHT * 0.1)
    button_x = (SCREEN_WIDTH - button_width) // 2
    spacing = int(SCREEN_HEIGHT * 0.07)
    button_texts = ["Start Server", "Join Server"]
    for i, button_text in enumerate(button_texts):
        button_y = SCREEN_HEIGHT // 2 + i * (button_height + spacing)
        button = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, Color.LIGHT_BROWN.value if i % 2 != 0 else Color.BROWN.value, button)
        
        # Button text
        button_font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.04))
        text = button_font.render(button_text, True, Color.WHITE.value)
        text_rect = text.get_rect(center=button.center)
        
        # Blit text onto the screen
        screen.blit(text, text_rect)
    
    # Selection
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, button_text in enumerate(button_texts):
                    button_y = SCREEN_HEIGHT // 2 + i * (button_height + spacing)
                    button = pygame.Rect(button_x, button_y, button_width, button_height)
                    if button.collidepoint(pos):
                        clear_screen(screen)
                        return button_text
                
        pygame.display.flip()

def draw_server_selection(screen, servers :list):
    '''
    Draw the server selection screen
    '''
    font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.05))
    
    # Draw the title
    title_text = font.render("Select Server", True, Color.WHITE.value)
    title_text_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(title_text, title_text_rect)

    # Draw the buttons
    button_width = int(SCREEN_WIDTH * 0.3)
    button_height = int(SCREEN_HEIGHT * 0.1)
    button_x = (SCREEN_WIDTH - button_width) // 2
    spacing = int(SCREEN_HEIGHT * 0.07)
    for i, server in enumerate(servers):
        button_y = SCREEN_HEIGHT // 2 + i * (button_height + spacing)
        server_button = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, Color.LIGHT_BROWN.value if i % 2 != 0 else Color.BROWN.value, server_button)
        
        # Button text
        button_font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.04))
        server_text = button_font.render(server, True, Color.WHITE.value)
        server_text_rect = server_text.get_rect(center=server_button.center)
        
        # Blit text onto the screen
        screen.blit(server_text, server_text_rect)
    
    # Selection
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, server in enumerate(servers):
                    button_y = SCREEN_HEIGHT // 2 + i * (button_height + spacing)
                    server_button = pygame.Rect(button_x, button_y, button_width, button_height)
                    if server_button.collidepoint(pos):
                        clear_screen(screen)
                        return server
                
        pygame.display.flip()

    return None
    

def request_temp_message(screen, message, duration, player, board):
    '''
    Request a new temporary message, interrupting any current message.
    '''
    global interrupt_flag
    # Set the flag to immediately stop any current message
    interrupt_flag = False
    display_temp_message(screen, message, duration, player, board)

def clear_screen(screen):
    '''
    clear the screen to the default background image
    '''
    background = pygame.image.load('assets/background.png')
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(background, (0, 0))
    pygame.display.flip()

