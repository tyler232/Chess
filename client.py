import pygame
import sys
import socket
import errno
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
running = True
possible_moves = []
move_queue = []
color = None
turn = None

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT + 2 * BAR_HEIGHT))
pygame.display.set_caption("Multiplayer Chess")

def read_until_nl(sock):
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
    global SERVER_IP, SERVER_PORT, SERVER_ADDRESS, PLAYER_ID

    ip_input = input(f"Enter server IP (default: {SERVER_IP}): ") or SERVER_IP
    port_input = input(f"Enter server port (default: {SERVER_PORT}): ") or str(SERVER_PORT)
    id_input = input("Enter your player ID (default: RANDOM ): ") or ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))

    SERVER_IP = ip_input
    SERVER_PORT = int(port_input)
    SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)
    PLAYER_ID = id_input

    print(f"Connecting to server at {SERVER_IP}:{SERVER_PORT}...")


def send_move(move, sock):
    sock.sendall(pickle.dumps(move))

def receive_moves(sock):
    global move_queue, running
    while True:
        data = sock.recv(4096)
        if not data:
            break
        move = pickle.loads(data)
        print("Received move from opponent:", move)
        move_queue.append(move)  # Add received move to the queue

def receive_color(sock):
    global color
    color = read_until_nl(sock)
    print(f"Received color from server: {color} (length: {len(color)})")

def main():
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
    global running, selected_piece, possible_moves, color, turn

    # get the server IP and port from the user
    display_message("Connecting to server...")
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
        screen.fill((0, 0, 0))
        display_message("Waiting for another player to connect...")
    elif connection_status == "FULL":
        screen.fill((0, 0, 0))
        display_message("Game is full")
        running = False
        return
    connection_status = read_until_nl(sock)
    print("Connection status:", connection_status)
    if connection_status == "STRT":
        screen.fill((0, 0, 0))
        display_message("Game Starts!")
    elif connection_status == "RSRT":
        screen.fill((0, 0, 0))
        display_message("Game Resumes!")

    # Receive the color from the server
    receive_color(sock)
    screen.fill((0, 0, 0))
    display_message("You are " + color)
    set_current_player(color)

    # Receive the opponent's name from the server
    opponent_name = read_until_nl(sock)
    player_name = PLAYER_ID
    
    if color == "WHITE":
        turn = True

    # Start a thread to receive moves from the server
    threading.Thread(target=receive_moves, args=(sock,), daemon=True).start()

    enemy_king_in_check = False
    
    while running:
        draw_top_bar(opponent_name)
        draw_board()
        draw_bottom_bar(player_name)

        king_loc = find_king(board)
        checking = in_check(board, king_loc)
        enemy_king_loc = find_enemy_king(board)
        enemy_in_check_status = enemy_in_check(board, enemy_king_loc)
        
        if enemy_in_check_status:
            enemy_king_in_check = True
        else:
            enemy_king_in_check = False

        if selected_piece:
            # draw_select_piece(selected_piece, "WHITE")
            draw_select_piece(selected_piece, color)
        if possible_moves:
            # draw_possible_moves(possible_moves, "WHITE")
            draw_possible_moves(possible_moves, color)
        if checking:
            # draw_in_check(king_loc, "WHITE")
            draw_in_check(king_loc, color)
        elif enemy_king_in_check:
            # draw_in_check(enemy_king_loc, "WHITE")  # Always draw if the enemy king is in check
            draw_in_check(enemy_king_loc, color)


        # draw_pieces("WHITE", board)
        draw_pieces(color, board)

        if in_checkmate(board, king_loc):
            print("Displaying Checkmate message (send end)!")
            display_message("YOU LOST")
            # running = False
        elif in_stalemate(board, king_loc):
            print("Displaying Stalemate message (send end)!")
            display_message("Stalemate")
            # running = False
        elif enemy_in_checkmate(board, enemy_king_loc):
            print("Displaying Checkmate message (send end)!")
            display_message("YOU WIN")
            # running = False
        elif enemy_in_stalemate(board, enemy_king_loc):
            print("Displaying Stalemate message (send end)!")
            display_message("Stalemate")
            # running = False

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = pos[0] // SQUARE_SIZE
                row = (pos[1] - BAR_HEIGHT) // SQUARE_SIZE
                if row < 0 or row >= ROWS:
                    continue
                if color == "BLACK":
                    row = ROWS - 1 - row
                if selected_piece:
                    sucess = move_piece(board, possible_moves, selected_piece, (row, col))
                    if sucess:
                        piece = board[row][col]
                        print("Send Moved piece:", piece)
                        move = {"piece": piece, 
                                "from": selected_piece, 
                                "to": (row, col),
                                "possible_moves": possible_moves,
                                "board": board}
                        send_move(move, sock)
                        turn = False
                    selected_piece = None
                    possible_moves = []
                    
                else:
                    piece = board[row][col]
                    print("Selecting piece at:", (row, col))
                    if turn and piece and ((piece[0] == "w" and color == "WHITE") or (piece[0] == "b" and color == "BLACK")):
                        selected_piece = (row, col)
                        possible_moves = get_possible_moves(board, selected_piece)

        # Check if there are any moves in the queue from the server
        while move_queue:
            move = move_queue.pop(0)  # Get the first move from the queue
            if move:
                board = move["board"]
                print("NEW BOARD:", board)
                draw_pieces(color, board)
                update_lastmove((move["piece"], move["from"], move["to"]))
                turn = True
            

if __name__ == "__main__":
    main()
