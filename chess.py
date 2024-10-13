import pygame
import sys
import board
from movement import *
from board import *

selected_piece = None
running = True
possible_moves = []

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
    elif in_stalemate(board, king_loc):
        display_message("Stalemate")
        running = False

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
            if selected_piece:
                move_piece(board, possible_moves, selected_piece, (row, col))
                selected_piece = None
                possible_moves = []
            else:
                selected_piece = (row, col)
                possible_moves = get_possible_moves(board, selected_piece)
                print("Selected piece:", selected_piece)
