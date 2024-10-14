import pygame
import sys
import socket
import pickle
import threading
from movement import *
from board import *

SERVER_IP = "localhost"
SERVER_PORT = 9060
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)

selected_piece = None
running = True
possible_moves = []
move_queue = []
color = None
turn = None

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Multiplayer Chess")

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
    data = sock.recv(4096)
    color = pickle.loads(data)
    display_message("You are " + color)

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
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(SERVER_ADDRESS)

    # Receive the color from the server
    receive_color(sock)

    set_current_player(color)

    if color == "WHITE":
        turn = True

    # Start a thread to receive moves from the server
    threading.Thread(target=receive_moves, args=(sock,), daemon=True).start()

    enemy_king_in_check = False

    while running:
        draw_board()
        king_loc = find_king(board)
        checking = in_check(board, king_loc)
        enemy_king_loc = find_enemy_king(board)
        enemy_in_check_status = enemy_in_check(board, enemy_king_loc)
        
        if enemy_in_check_status:
            enemy_king_in_check = True
        else:
            enemy_king_in_check = False

        if selected_piece:
            draw_select_piece(selected_piece, "WHITE")
            # draw_select_piece(selected_piece, color)
        if possible_moves:
            draw_possible_moves(possible_moves, "WHITE")
            # draw_possible_moves(possible_moves, color)
        if checking:
            draw_in_check(king_loc, "WHITE")
            # draw_in_check(king_loc, color)
        elif enemy_king_in_check:
            draw_in_check(enemy_king_loc, "WHITE")  # Always draw if the enemy king is in check


        draw_pieces("WHITE", board)
        # draw_pieces(color)

        if in_checkmate(board, king_loc):
            print("Displaying Checkmate message (send end)!")
            display_message("YOU LOST")
            # running = False
            send_move("checkmate", sock)
        elif in_stalemate(board, king_loc):
            print("Displaying Stalemate message (send end)!")
            display_message("Stalemate")
            # running = False
            send_move("stalemate", sock)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
                # if color == "WHITE":
                #     row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
                # elif color == "BLACK":
                #     row, col = (ROWS - 1 - pos[1] // SQUARE_SIZE), pos[0] // SQUARE_SIZE
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
            if move and move != "checkmate" and move != "stalemate":
                board = move["board"]
                print("NEW BOARD:", board)
                draw_pieces("WHITE", board)
                update_lastmove((move["piece"], move["from"], move["to"]))
                turn = True
            elif move and move == "checkmate":
                print("Displaying checkmate message (received end)!")
                display_message("Checkmate, YOU WIN!")
                # running = False
                break
            elif move and move == "stalemate":
                print("Displaying stalemate message (received end)!")
                display_message("Stalemate")
                # running = False
                break
            


if __name__ == "__main__":
    main()
