import pygame
import sys
import socket
import errno
import time
import random
import string
import pickle
import threading
from source.movement import *
from source.board import *

SERVER_IP = "localhost"
SERVER_PORT = 9060
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)
PLAYER_ID = None

selected_piece = None
client_running = True
game_running = False
possible_moves = []
move_queue = []
color = None
turn = None
player_score = 0
opponent_score = 0

music_button = None
sound_on = True

# Initialize Pygame
pygame.init()
pygame.mixer.init()
icon = pygame.image.load('assets/icon.png')
sound = pygame.mixer.Sound("assets/chess_move.wav")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Multiplayer Chess")

def read_until_nl(sock):
    '''
    read data from the socket until a newline character is encountered
    @param sock: the socket to read from
    @return: the data read from the socket
    '''
    buffer = ""
    recv_bit = 0
    while True:
        recv_bit += 1
        curr_char = sock.recv(1)
        if curr_char == b'\n':
            break
        buffer += curr_char.decode('utf-8')

    print(f"{recv_bit} bits received")
    return buffer

def get_server_info():
    '''
    get the server IP and port from the user, also set up user id
    '''
    global SERVER_IP, SERVER_PORT, SERVER_ADDRESS, PLAYER_ID

    ip_input = input(f"Enter server IP (default: {SERVER_IP}): ") or SERVER_IP
    port_input = input(f"Enter server port (default: {SERVER_PORT}): ") or str(SERVER_PORT)
    id_input = input("Enter your player ID (default: RANDOM ): ") or ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))

    SERVER_IP = ip_input
    SERVER_PORT = int(port_input)
    SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)
    PLAYER_ID = id_input

    print(f"Connecting to server at {SERVER_IP}:{SERVER_PORT}...")

def send_restart_request(sock):
    '''
    send a request to the server to restart the game
    @param sock: the server socket to send data to
    '''
    sock.sendall(b"RSTG\n")

def send_move(move, sock):
    '''
    send a move to the server
    @param move: the move to send
    @param sock: the server socket to send data to
    '''
    sock.sendall(pickle.dumps(move))

def receive_moves(sock):
    '''
    Thread function to receive moves from the server
    @param sock: the server socket to receive data from
    @return: None
    '''
    global move_queue, game_running
    print("Starting receive_moves thread...")
    while game_running:
        print("loop in thread")
        print("running: ", game_running)
        data = None
        try: 
            data = sock.recv(4096)
            if not data:
                break
            move = pickle.loads(data)
            print("Received move from opponent:", move)
            move_queue.append(move)  # Add received move to the queue
        except (EOFError, ConnectionResetError) as e:
            print(f"Connection error: {e}. Exiting thread...")
            break
        except Exception as e:
            print(f"Error in receive_moves: {e}. (invalid load key '\x00' is normal behavior to quit thread) Exiting thread...")
            data = sock.recv(1)
            break
    print("Exiting receive_moves thread...")

def receive_color(sock):
    '''
    receive the color from the server
    @param sock: the server socket to receive data from
    @return: None
    '''
    global color
    color = read_until_nl(sock)
    print(f"Received color from server: {color} (length: {len(color)})")

def prepare_new_game(sock, player_name, opponent_name):
    '''
    prepare for a new game by resetting the board and sending a restart request to the server
    @param sock: the server socket to send data to
    @param player_name: the name of the player
    @param opponent_name: the name of the opponent
    @return: None
    '''
    global player_score, opponent_score, music_button, sound_on
    delete_top_bar(screen)
    delete_bottom_bar(screen)
    clear_screen(screen)
    music_button = draw_top_bar(screen, opponent_name, opponent_score, sound_on)
    draw_bottom_bar(screen, player_name, player_score)
    display_message(screen, "New Game Starting")
    pygame.display.flip()
    send_restart_request(sock)

def main():
    global screen
    global client_running, game_running
    global selected_piece, possible_moves, color, turn
    global player_score, opponent_score
    global music_button, sound_on
    clear_screen(screen)
    
    # get the server IP and port from the user
    display_message(screen, "Connecting to server...")
    get_server_info()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(SERVER_ADDRESS)

    # Send the player ID to the server
    id_header = str(PLAYER_ID + "\n")
    sock.sendall(id_header.encode('utf-8'))
    
    # Recieve connection status
    connection_status = read_until_nl(sock)
    print("Connection status:", connection_status)
    if connection_status == "WAIT":
        clear_screen(screen)
        display_message(screen, "Waiting for opponent...")
    elif connection_status == "FULL":
        clear_screen(screen)
        display_message(screen, "Game is full")
        client_running = False
        return
    connection_status = read_until_nl(sock)
    print("Connection status:", connection_status)
    if connection_status == "STRT":
        clear_screen(screen)
        display_message(screen, "Game Starts!")
    elif connection_status == "RSRT":
        clear_screen(screen)
        display_message(screen, "Game Resumes!")

    # Receive the color from the server
    receive_color(sock)
    clear_screen(screen)
    display_message(screen, "You are " + color)
    set_current_player(color)

    # Receive the opponent's name from the server
    opponent_name = read_until_nl(sock)
    player_name = PLAYER_ID
    
    # set up first hand
    if color == "WHITE":
        turn = True

    while client_running:
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

        game_running = True
        # Start a thread to receive moves from the server
        receive_thread = threading.Thread(target=receive_moves, args=(sock,), daemon=True)
        receive_thread.start()

        enemy_king_in_check = False
        
        button_info = None

        while game_running:
            # Draw the screen
            music_button = draw_top_bar(screen, opponent_name, opponent_score, sound_on)
            draw_board(screen)
            button_info = draw_bottom_bar(screen, player_name, player_score)

            # check if the player is in check
            king_loc = find_king(board)
            last_move = get_last_move()
            checking = in_check(board, king_loc)
            enemy_king_loc = find_enemy_king(board)
            enemy_in_check_status = enemy_in_check(board, enemy_king_loc)
            
            if enemy_in_check_status:
                enemy_king_in_check = True
            else:
                enemy_king_in_check = False

            if selected_piece:
                draw_select_piece(screen, selected_piece, color)
            if possible_moves:
                draw_possible_moves(screen, possible_moves, color)
            if checking:
                draw_in_check(screen, king_loc, color)
            elif enemy_king_in_check:
                draw_in_check(screen, enemy_king_loc, color)
            
            if last_move and ((last_move[0][0] == "w" and color == "BLACK") or (last_move and last_move[0][0] == "b" and color == "WHITE")):
                draw_last_move(last_move, screen, color)

            draw_pieces(screen, color, board)

            if in_checkmate(board, king_loc):
                print(screen, "Displaying Checkmate message (send end)!")
                display_message(screen, "YOU LOST")
                opponent_score += 1
                prepare_new_game(sock, player_name, opponent_name)
                game_running = False
                break
            elif in_stalemate(board, king_loc):
                print(screen, "Displaying Stalemate message (send end)!")
                display_message(screen, "Stalemate")
                player_score += 1
                opponent_score += 1
                prepare_new_game(sock, player_name, opponent_name)
                game_running = False
                break
            elif enemy_in_checkmate(board, enemy_king_loc):
                print(screen, "Displaying Checkmate message (send end)!")
                display_message(screen, "YOU WIN")
                player_score += 1
                prepare_new_game(sock, player_name, opponent_name)
                game_running = False
                break
            elif enemy_in_stalemate(board, enemy_king_loc):
                print(screen, "Displaying Stalemate message (send end)!")
                display_message(screen, "Stalemate")
                player_score += 1
                opponent_score += 1
                prepare_new_game(sock, player_name, opponent_name)
                game_running = False
                break

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    screen = resize_screen(event.w, event.h)
                    global SCREEN_WIDTH, SCREEN_HEIGHT, BOARD_WIDTH, BOARD_HEIGHT, SQUARE_SIZE, BOARD_START_X, BOARD_START_Y, BAR_HEIGHT
                    SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
                    BOARD_WIDTH, BOARD_HEIGHT = int(SCREEN_WIDTH * 0.84), int(SCREEN_HEIGHT * 0.84)
                    BOARD_WIDTH = BOARD_HEIGHT = min(BOARD_WIDTH, BOARD_HEIGHT)
                    SQUARE_SIZE = BOARD_WIDTH // COLS
                    BOARD_START_X = (SCREEN_WIDTH - BOARD_WIDTH) // 2
                    BOARD_START_Y = (SCREEN_HEIGHT - BOARD_HEIGHT) // 2
                    BAR_HEIGHT = (SCREEN_HEIGHT - BOARD_HEIGHT) // 2
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    # check if the button is clicked
                    # music button clicked
                    if music_button.collidepoint(pos):
                        print("Music Button clicked")
                        # clear the cross
                        if not sound_on:
                            clear_screen(screen)
                        sound_on = not sound_on
                        continue
                    if button_info:
                        # resign button clicked
                        if button_clicked(pos[0], pos[1], button_info[0], button_info[1], button_info[4], button_info[5]):
                            print("Resign Button clicked")
                            if not turn:
                                display_temp_message(screen, "Not your turn", 1000, color, board)
                                continue
                            else:
                                if not draw_confirm_window(screen, "Are you sure you want to resign?"):
                                    continue
                                move = {"piece": None,
                                        "from": None,
                                        "to": None,
                                        "possible_moves": [],
                                        "board": board,
                                        "end_seeking": "resign"}
                                send_move(move, sock)
                                turn = False
                                display_message(screen, "YOU RESIGNED")
                                opponent_score += 1
                                prepare_new_game(sock, player_name, opponent_name)
                                game_running = False
                                break
                        # draw button clicked
                        elif button_clicked(pos[0], pos[1], button_info[2], button_info[3], button_info[4], button_info[5]):
                            print("Draw Button clicked")
                            if not turn:
                                display_temp_message(screen, "Not your turn", 1000, color, board)
                                continue
                            else:
                                if not draw_confirm_window(screen, "Are you sure you want to offer a draw?"):
                                    continue
                                move = {"piece": None,
                                        "from": None,
                                        "to": None,
                                        "possible_moves": [],
                                        "board": board,
                                        "end_seeking": "draw_req"}
                                send_move(move, sock)
                                continue
                    # Check if the click is within the board
                    if (pos[0] < BOARD_START_X or pos[0] > BOARD_START_X + BOARD_WIDTH) or (pos[1] < BOARD_START_Y or pos[1] > BOARD_START_Y + BOARD_HEIGHT):
                        continue
                    col = (pos[0] - BOARD_START_X) // SQUARE_SIZE
                    row = (pos[1] - BOARD_START_Y) // SQUARE_SIZE

                    if row < 0 or row >= ROWS:
                        continue
                    if color == "BLACK":
                        row = ROWS - 1 - row
                    if selected_piece:
                        sucess = move_piece(screen, board, possible_moves, selected_piece, (row, col))
                        if sucess:
                            piece = board[row][col]
                            print("Send Moved piece:", piece)
                            move = {"piece": piece, 
                                    "from": selected_piece, 
                                    "to": (row, col),
                                    "possible_moves": possible_moves,
                                    "board": board,
                                    "end_seeking": None}
                            send_move(move, sock)
                            if sound_on:
                                sound.play()
                            turn = False
                        selected_piece = None
                        possible_moves = []
                        
                    else:
                        piece = board[row][col]
                        print("Selecting piece at:", (row, col))
                        if turn and piece and ((piece[0] == "w" and color == "WHITE") or (piece[0] == "b" and color == "BLACK")):
                            selected_piece = (row, col)
                            possible_moves = get_possible_moves(board, selected_piece)
                        elif not turn and piece and ((piece[0] == "w" and color == "WHITE") or (piece[0] == "b" and color == "BLACK")):
                            print("Not your turn")
                            request_temp_message(screen, "Not your turn", 1000, color, board)

            # Check if there are any moves in the queue from the server
            while move_queue:
                move = move_queue.pop(0)  # Get the first move from the queue
                if move:
                    if move["end_seeking"] == "resign":
                        display_message(screen, "OPPONENT RESIGNED")
                        player_score += 1
                        prepare_new_game(sock, player_name, opponent_name)
                        game_running = False
                        update_lastmove(None)
                        break
                    elif move["end_seeking"] == "draw_req":
                        if draw_confirm_window(screen, "Opponent offered a draw. Do you accept?"):
                            display_message(screen, "DRAW")
                            move = {"piece": None,
                                    "from": None,
                                    "to": None,
                                    "possible_moves": [],
                                    "board": board,
                                    "end_seeking": "draw_conf"}
                            send_move(move, sock)
                            player_score += 1
                            opponent_score += 1
                            prepare_new_game(sock, player_name, opponent_name)
                            game_running = False
                            update_lastmove(None)
                        break
                    elif move["end_seeking"] == "draw_conf":
                        display_message(screen, "DRAW")
                        player_score += 1
                        opponent_score += 1
                        prepare_new_game(sock, player_name, opponent_name)
                        game_running = False
                        update_lastmove(None)
                        break
                    board = move["board"]
                    print("NEW BOARD:", board)
                    draw_pieces(screen, color, board)
                    update_lastmove((move["piece"], move["from"], move["to"]))
                    if sound_on:
                        sound.play()
                    turn = True
                

        print("out of game loop")
        print(game_running)    
        receive_thread.join()
        print("Game ended, New game starting...")

        # reset color and priority for next game
        new_color = "WHITE" if color == "BLACK" else "BLACK"
        color = new_color
        set_current_player(color)
        turn = True if color == "WHITE" else False

        # wait 5 seconds until start next game
        time.sleep(5)

if __name__ == "__main__":
    main()
