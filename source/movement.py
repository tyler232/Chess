import copy
from source.board import promotion_selection, display_temp_message

current_player = "w"
last_move = None
en_passant_location = None
test_mode = False

def move_piece(screen, board, possible_moves, selected_piece, end_pos, ai=False):
    global last_move
    global current_player
    global en_passant_location

    start_row, start_col = selected_piece
    end_row, end_col = end_pos

    piece = board[start_row][start_col]

    # Wrong Turn
    if test_mode and piece != "" and current_player != piece[0]:
        print("Not your Turn")
        en_passant_location = None
        return False

    # Castling
    sucess = False
    copy_board = copy.deepcopy(board)
    if piece == "wk" and is_valid_move(board, possible_moves, end_pos) and can_castle(board, selected_piece, end_pos) == 1:
        copy_board[start_row][start_col] = ""
        copy_board[end_row][end_col] = piece
        copy_board[7][7] = ""
        copy_board[7][5] = "wr"
        checking = in_check(copy_board, find_king(copy_board))
        if not checking:
            board[start_row][start_col] = ""
            board[end_row][end_col] = piece
            board[7][7] = ""
            board[7][5] = "wr"
            last_move = (piece, selected_piece, end_pos)
            if test_mode:
                swap_players()
            sucess = True
        else:
            color = "WHITE" if current_player == "w" else "BLACK"
            display_temp_message(screen, "Check", 1000, color, board)
    elif piece == "wk" and is_valid_move(board, possible_moves, end_pos) and can_castle(board, selected_piece, end_pos) == 2:
        copy_board[start_row][start_col] = ""
        copy_board[end_row][end_col] = piece
        copy_board[7][0] = ""
        copy_board[7][3] = "wr"
        checking = in_check(copy_board, find_king(copy_board))
        if not checking:
            board[start_row][start_col] = ""
            board[end_row][end_col] = piece
            board[7][0] = ""
            board[7][3] = "wr"
            last_move = (piece, selected_piece, end_pos)
            if test_mode:
                swap_players()
            sucess = True
        else:
            color = "WHITE" if current_player == "w" else "BLACK"
            display_temp_message(screen, "Check", 1000, color, board)
    elif piece == "bk" and is_valid_move(board, possible_moves, end_pos) and can_castle(board, selected_piece, end_pos) == 1:
        copy_board[start_row][start_col] = ""
        copy_board[end_row][end_col] = piece
        copy_board[0][7] = ""
        copy_board[0][5] = "br"
        checking = in_check(copy_board, find_king(copy_board))
        if not checking:
            board[start_row][start_col] = ""
            board[end_row][end_col] = piece
            board[0][7] = ""
            board[0][5] = "br"
            last_move = (piece, selected_piece, end_pos)
            if test_mode:
                swap_players()
            sucess = True
        else:
            color = "WHITE" if current_player == "w" else "BLACK"
            display_temp_message(screen, "Check", 1000, color, board)
    elif piece == "bk" and is_valid_move(board, possible_moves, end_pos) and can_castle(board, selected_piece, end_pos) == 2:
        copy_board[start_row][start_col] = ""
        copy_board[end_row][end_col] = piece
        copy_board[0][0] = ""
        copy_board[0][3] = "br"
        checking = in_check(copy_board, find_king(copy_board))
        if not checking:
            board[start_row][start_col] = ""
            board[end_row][end_col] = piece
            board[0][0] = ""
            board[0][3] = "br"
            last_move = (piece, selected_piece, end_pos)
            if test_mode:
                swap_players()
            sucess = True
        else:
            color = "WHITE" if current_player == "w" else "BLACK"
            display_temp_message(screen, "Check", 1000, color, board)
    # Pawn Promotion
    elif is_valid_move(board, possible_moves, end_pos) and piece == "wp" and end_row == 0:
        copy_board[start_row][start_col] = ""
        copy_board[end_row][end_col] = piece
        checking = in_check(copy_board, find_king(copy_board))
        if not checking:
            new_piece = "w" + promotion_selection("WHITE") if not ai else "wq"
            board[start_row][start_col] = ""
            board[end_row][end_col] = new_piece
            last_move = (piece, selected_piece, end_pos)
            if test_mode:
                swap_players()
            sucess = True
        else:
            color = "WHITE" if current_player == "w" else "BLACK"
            display_temp_message(screen, "Check", 1000, color, board)
    elif is_valid_move(board, possible_moves, end_pos) and piece == "bp" and end_row == 7:
        copy_board[start_row][start_col] = ""
        copy_board[end_row][end_col] = piece
        checking = in_check(copy_board, find_king(copy_board))
        if not checking:
            new_piece = "b" + promotion_selection("BLACK") if not ai else "bq"
            board[start_row][start_col] = ""
            board[end_row][end_col] = new_piece
            last_move = (piece, selected_piece, end_pos)
            if test_mode:
                swap_players()
            sucess = True
        else:
            color = "WHITE" if current_player == "w" else "BLACK"
            display_temp_message(screen, "Check", 1000, color, board)
    # En passant
    elif is_valid_move(board, possible_moves, end_pos) and en_passant_location and end_pos == en_passant_location:
        print("Doing En passant")
        copy_board[start_row][start_col] = ""
        copy_board[end_row][end_col] = piece
        if piece == "wp":
            copy_board[end_row + 1][end_col] = ""
        elif piece == "bp":
            copy_board[end_row - 1][end_col] = ""

        checking = in_check(copy_board, find_king(copy_board))
        if not checking:
            board[start_row][start_col] = ""
            board[end_row][end_col] = piece
            if piece == "wp":
                board[end_row + 1][end_col] = ""
            elif piece == "bp":
                board[end_row - 1][end_col] = ""
            last_move = (piece, selected_piece, end_pos)
            if test_mode:
                swap_players()
            sucess = True
        else:
            color = "WHITE" if current_player == "w" else "BLACK"
            display_temp_message(screen, "Check", 1000, color, board)
    # Regular move
    elif is_valid_move(board, possible_moves, end_pos):
        copy_board[start_row][start_col] = ""
        copy_board[end_row][end_col] = piece
        checking = in_check(copy_board, find_king(copy_board))
        if not checking:
            board[start_row][start_col] = ""
            board[end_row][end_col] = piece
            last_move = (piece, selected_piece, end_pos)
            if test_mode:
                swap_players()
            sucess = True
        else:
            color = "WHITE" if current_player == "w" else "BLACK"
            display_temp_message(screen, "Check", 1000, color, board)
    
    print("Last Move: ", last_move)

    en_passant_location = None
    return sucess

# 0: can't castle, 1: can castle kingside, 2: can castle queenside
def can_castle(board, start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    piece = board[start_row][start_col]
    if piece[1] != "k":
        return 0
    
    if piece[0] == "w":
        if start_row == 7 and start_col == 4 and end_row == 7 and end_col == 6:
            return 1
        elif start_row == 7 and start_col == 4 and end_row == 7 and end_col == 2:
            return 2
    elif piece[0] == "b":
        if start_row == 0 and start_col == 4 and end_row == 0 and end_col == 6:
            return 1
        elif start_row == 0 and start_col == 4 and end_row == 0 and end_col == 2:
            return 2
        
    return 0

def is_valid_move(board, possible_moves, end_pos):
    return end_pos in possible_moves

def get_possible_moves_all_players(board, selected_piece):
    piece = board[selected_piece[0]][selected_piece[1]]
    if piece[1] == "p":
        return possible_moves_pawn(board, selected_piece, piece[0])
    elif piece[1] == "n":
        return possible_moves_knight(board, selected_piece, piece[0])
    elif piece[1] == "b":
        return possible_moves_bishop(board, selected_piece, piece[0])
    elif piece[1] == "r":
        return possible_moves_rook(board, selected_piece, piece[0])
    elif piece[1] == "q":
        return possible_moves_bishop(board, selected_piece, piece[0]) + possible_moves_rook(board, selected_piece, piece[0])
    elif piece[1] == "k":
        return possible_moves_king(board, selected_piece, piece[0])
    return []
    

def get_possible_moves(board, selected_piece):
    piece = board[selected_piece[0]][selected_piece[1]]
    if not piece or piece[0] != current_player:
        return []

    return get_possible_moves_all_players(board, selected_piece)


def possible_moves_pawn(board, start_pos, color):
    global en_passant_location
    x, y = start_pos
    possible = []

    # set direction base on player
    direction = -1 if color == "w" else 1
    starting_row = 6 if color == "w" else 1
    opponent_color = "b" if color == "w" else "w"

    # Moving one square forward
    if 0 <= x + direction < 8 and board[x + direction][y] == "":
        possible.append((x + direction, y))

    # Moving two squares forward from the starting position
    if x == starting_row and board[x + direction][y] == "" and board[x + 2 * direction][y] == "":
        possible.append((x + 2 * direction, y))

    # Capture moves
    if 0 <= x + direction < 8 and y > 0 and board[x + direction][y - 1] != "" and board[x + direction][y - 1][0] == opponent_color:
        possible.append((x + direction, y - 1))
    if 0 <= x + direction < 8 and y < 7 and board[x + direction][y + 1] != "" and board[x + direction][y + 1][0] == opponent_color:
        possible.append((x + direction, y + 1))
    
    # En passant
    if last_move:
        last_moved_piece = last_move[0]
        last_moved_start = last_move[1]
        last_moved_end = last_move[2]

        if last_moved_piece[0] == opponent_color and last_moved_piece[1] == "p":
            if abs(last_moved_start[0] - last_moved_end[0]) == 2 and abs(last_moved_end[1] - y) == 1 and last_moved_end[0] == x:
                possible.append((x + direction, last_moved_end[1]))
                en_passant_location = (x + direction, last_moved_end[1])
    return possible

def possible_moves_knight(board, start_pos, color):
    x, y = start_pos
    possible = []

    opponent_color = "b" if color == "w" else "w"

    # Up
    if x > 1:
        if y > 0 and (board[x - 2][y - 1] == "" or board[x - 2][y - 1][0] == opponent_color):
            possible.append((x - 2, y - 1))
        if y < 7 and (board[x - 2][y + 1] == "" or board[x - 2][y + 1][0] == opponent_color):
            possible.append((x - 2, y + 1))

    # Down
    if x < 6:
        if y > 0 and (board[x + 2][y - 1] == "" or board[x + 2][y - 1][0] == opponent_color):
            possible.append((x + 2, y - 1))
        if y < 7 and (board[x + 2][y + 1] == "" or board[x + 2][y + 1][0] == opponent_color):
            possible.append((x + 2, y + 1))

    # Left
    if y > 1:
        if x > 0 and (board[x - 1][y - 2] == "" or board[x - 1][y - 2][0] == opponent_color):
            possible.append((x - 1, y - 2))
        if x < 7 and (board[x + 1][y - 2] == "" or board[x + 1][y - 2][0] == opponent_color):
            possible.append((x + 1, y - 2))

    # Right
    if y < 6:
        if x > 0 and (board[x - 1][y + 2] == "" or board[x - 1][y + 2][0] == opponent_color):
            possible.append((x - 1, y + 2))
        if x < 7 and (board[x + 1][y + 2] == "" or board[x + 1][y + 2][0] == opponent_color):
            possible.append((x + 1, y + 2))

    return possible

def possible_moves_bishop(board, start_pos, color):
    x, y = start_pos
    possible = []

    opponent_color = "b" if color == "w" else "w"

    # Up-left
    i, j = x - 1, y - 1
    while i >= 0 and j >= 0:
        if board[i][j] == "":
            possible.append((i, j))
        elif board[i][j][0] == opponent_color:
            possible.append((i, j))
            break
        else:
            break
        i -= 1
        j -= 1

    # Up-right
    i, j = x - 1, y + 1
    while i >= 0 and j < 8:
        if board[i][j] == "":
            possible.append((i, j))
        elif board[i][j][0] == opponent_color:
            possible.append((i, j))
            break
        else:
            break
        i -= 1
        j += 1

    # Down-left
    i, j = x + 1, y - 1
    while i < 8 and j >= 0:
        if board[i][j] == "":
            possible.append((i, j))
        elif board[i][j][0] == opponent_color:
            possible.append((i, j))
            break
        else:
            break
        i += 1
        j -= 1

    # Down-right
    i, j = x + 1, y + 1
    while i < 8 and j < 8:
        if board[i][j] == "":
            possible.append((i, j))
        elif board[i][j][0] == opponent_color:
            possible.append((i, j))
            break
        else:
            break
        i += 1
        j += 1

    return possible

def possible_moves_rook(board, start_pos, color):
    x, y = start_pos
    possible = []

    opponent_color = "b" if color == "w" else "w"

    # Up
    i = x - 1
    while i >= 0:
        if board[i][y] == "":
            possible.append((i, y))
        elif board[i][y][0] == opponent_color:
            possible.append((i, y))
            break
        else:
            break
        i -= 1

    # Down
    i = x + 1
    while i < 8:
        if board[i][y] == "":
            possible.append((i, y))
        elif board[i][y][0] == opponent_color:
            possible.append((i, y))
            break
        else:
            break
        i += 1

    # Left
    j = y - 1
    while j >= 0:
        if board[x][j] == "":
            possible.append((x, j))
        elif board[x][j][0] == opponent_color:
            possible.append((x, j))
            break
        else:
            break
        j -= 1

    # Right
    j = y + 1
    while j < 8:
        if board[x][j] == "":
            possible.append((x, j))
        elif board[x][j][0] == opponent_color:
            possible.append((x, j))
            break
        else:
            break
        j += 1

    return possible

def possible_moves_king(board, selected_piece, color):
    x, y = selected_piece
    possible = []

    opponent_color = "b" if color == "w" else "w"

    # Up
    if x > 0:
        if board[x - 1][y] == "" or board[x - 1][y][0] == opponent_color:
            possible.append((x - 1, y))
        if y > 0 and (board[x - 1][y - 1] == "" or board[x - 1][y - 1][0] == opponent_color):
            possible.append((x - 1, y - 1))
        if y < 7 and (board[x - 1][y + 1] == "" or board[x - 1][y + 1][0] == opponent_color):
            possible.append((x - 1, y + 1))

    # Down
    if x < 7:
        if board[x + 1][y] == "" or board[x + 1][y][0] == opponent_color:
            possible.append((x + 1, y))
        if y > 0 and (board[x + 1][y - 1] == "" or board[x + 1][y - 1][0] == opponent_color):
            possible.append((x + 1, y - 1))
        if y < 7 and (board[x + 1][y + 1] == "" or board[x + 1][y + 1][0] == opponent_color):
            possible.append((x + 1, y + 1))

    # Left
    if y > 0 and (board[x][y - 1] == "" or board[x][y - 1][0] == opponent_color):
        possible.append((x, y - 1))

    # Right
    if y < 7 and (board[x][y + 1] == "" or board[x][y + 1][0] == opponent_color):
        possible.append((x, y + 1))
    
    # Castling
    if x == 7 and y == 4 and board[7][7] == "wr" and board[7][5] == "" and board[7][6] == "":
        possible.append((7, 6))
    elif x == 7 and y == 4 and board[7][0] == "wr" and board[7][1] == "" and board[7][2] == "" and board[7][3] == "":
        possible.append((7, 2))
    elif x == 0 and y == 4 and board[0][7] == "br" and board[0][5] == "" and board[0][6] == "":
        possible.append((0, 6))
    elif x == 0 and y == 4 and board[0][0] == "br" and board[0][1] == "" and board[0][2] == "" and board[0][3] == "":
        possible.append((0, 2))

    return possible


def find_king(board):
    for row_idx in range(len(board)):
        for col_idx in range(len(board[row_idx])):
            if board[row_idx][col_idx] == f"{current_player}k":
                return (row_idx, col_idx)
    return None

def find_enemy_king(board):
    for row_idx in range(len(board)):
        for col_idx in range(len(board[row_idx])):
            if board[row_idx][col_idx] == f"{'b' if current_player == 'w' else 'w'}k":
                return (row_idx, col_idx)
    return None

def in_check(board, king_location):
    for row_idx in range(len(board)):
        for col_idx in range(len(board[row_idx])):
            piece = board[row_idx][col_idx]
            if piece != "" and piece[0] != current_player:
                possible_moves = get_possible_moves_all_players(board, (row_idx, col_idx))
                if king_location in possible_moves:
                    return True
    return False

def enemy_in_check(board, enemy_king_location):
    for row_idx in range(len(board)):
        for col_idx in range(len(board[row_idx])):
            piece = board[row_idx][col_idx]
            if piece != "" and piece[0] == current_player:
                possible_moves = get_possible_moves_all_players(board, (row_idx, col_idx))
                if enemy_king_location in possible_moves:
                    return True
    return False


def in_checkmate(board, king_location):
    if not in_check(board, king_location):
        return False

    for row_idx in range(len(board)):
        for col_idx in range(len(board[row_idx])):
            piece = board[row_idx][col_idx]
            if piece != "" and piece[0] == current_player:
                possible_moves = get_possible_moves_all_players(board, (row_idx, col_idx))
                for move in possible_moves:
                    copy_board = copy.deepcopy(board)
                    copy_board[row_idx][col_idx] = ""
                    copy_board[move[0]][move[1]] = piece
                    if not in_check(copy_board, find_king(copy_board)):
                        # print("Move: ", (row_idx, col_idx), move)
                        return False
    return True

def enemy_in_checkmate(board, enemy_king_location):
    if not enemy_in_check(board, enemy_king_location):
        return False
    
    for row_idx in range(len(board)):
        for col_idx in range(len(board[row_idx])):
            piece = board[row_idx][col_idx]
            if piece != "" and piece[0] != current_player:
                possible_moves = get_possible_moves_all_players(board, (row_idx, col_idx))
                for move in possible_moves:
                    copy_board = copy.deepcopy(board)
                    copy_board[row_idx][col_idx] = ""
                    copy_board[move[0]][move[1]] = piece
                    if not enemy_in_check(copy_board, find_enemy_king(copy_board)):
                        return False

    return True
    


def in_stalemate(board, king_location):
    if in_check(board, king_location):
        return False

    for row_idx in range(len(board)):
        for col_idx in range(len(board[row_idx])):
            piece = board[row_idx][col_idx]
            if piece != "" and piece[0] == current_player:
                possible_moves = get_possible_moves_all_players(board, (row_idx, col_idx))
                for move in possible_moves:
                    copy_board = copy.deepcopy(board)
                    copy_board[row_idx][col_idx] = ""
                    copy_board[move[0]][move[1]] = piece
                    if not in_check(copy_board, find_king(copy_board)):
                        return False
    return True

def enemy_in_stalemate(board, enemy_king_location):
    if enemy_in_check(board, enemy_king_location):
        return False
    
    for row_idx in range(len(board)):
        for col_idx in range(len(board[row_idx])):
            piece = board[row_idx][col_idx]
            if piece != "" and piece[0] != current_player:
                possible_moves = get_possible_moves_all_players(board, (row_idx, col_idx))
                for move in possible_moves:
                    copy_board = copy.deepcopy(board)
                    copy_board[row_idx][col_idx] = ""
                    copy_board[move[0]][move[1]] = piece
                    if not enemy_in_check(copy_board, find_enemy_king(copy_board)):
                        return False

    return True

def set_test_mode(test):
    global test_mode
    test_mode = test

def set_current_player(player):
    global current_player
    if player == "WHITE":
        current_player = "w"
    elif player == "BLACK":
        current_player = "b"

def get_last_move():
    return last_move

def update_lastmove(move):
    global last_move
    last_move = move

def swap_players():
    global current_player
    current_player = "w" if current_player == "b" else "b"
    return current_player
