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

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Multiplayer Chess")

def send_move(move, sock):
    sock.sendall(pickle.dumps(move))

def receive_moves(sock):
    global move_queue
    while True:
        data = sock.recv(4096)
        if not data:
            break
        move = pickle.loads(data)
        print("Received move from opponent:", move)
        move_queue.append(move)  # Add received move to the queue

def main():
    global running, selected_piece, possible_moves
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(SERVER_ADDRESS)

    # Start a thread to receive moves from the server
    threading.Thread(target=receive_moves, args=(sock,), daemon=True).start()

    while running:
        draw_board()
        king_loc = find_king(board)
        checking = in_check(board, king_loc)

        if selected_piece:
            draw_select_piece(selected_piece)
        if possible_moves:
            draw_possible_moves(possible_moves)
        if checking:
            draw_in_check(king_loc)

        draw_pieces()

        if in_checkmate(board, king_loc):
            display_message("Checkmate!")
            running = False
            send_move("checkmate", sock)
        elif in_stalemate(board, king_loc):
            display_message("Stalemate")
            running = False
            send_move("stalemate", sock)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
                if selected_piece:
                    sucess = move_piece(board, possible_moves, selected_piece, (row, col))
                    if sucess:
                        piece = board[row][col]
                        print("Send Moved piece:", piece)
                        move = {"piece": piece, 
                                "from": selected_piece, 
                                "to": (row, col)}
                        send_move(move, sock)
                    selected_piece = None
                    possible_moves = []
                else:
                    selected_piece = (row, col)
                    possible_moves = get_possible_moves(board, selected_piece)
                    print("Selected piece:", selected_piece)

        # Check if there are any moves in the queue from the server
        while move_queue:
            move = move_queue.pop(0)  # Get the first move from the queue
            if move and move != "checkmate" and move != "stalemate":
                piece = move["piece"]
                from_pos = move["from"]
                to_pos = move["to"]
                board[to_pos[0]][to_pos[1]] = piece
                board[from_pos[0]][from_pos[1]] = ""
                swap_players()

if __name__ == "__main__":
    main()
