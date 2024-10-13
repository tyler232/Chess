# Implement later: en passant

def move_piece(board, possible_moves, selected_piece, end_pos):
    start_row, start_col = selected_piece
    end_row, end_col = end_pos

    piece = board[start_row][start_col]
    # Castling
    if is_valid_move(possible_moves, end_pos) and can_castle(board, selected_piece, end_pos) == 1:
        board[start_row][start_col] = ""
        board[end_row][end_col] = piece
        board[7][7] = ""
        board[7][5] = "wr"
    elif is_valid_move(possible_moves, end_pos) and can_castle(board, selected_piece, end_pos) == 2:
        board[start_row][start_col] = ""
        board[end_row][end_col] = piece
        board[7][0] = ""
        board[7][3] = "wr"
    # Queening
    elif is_valid_move(possible_moves, end_pos) and piece == "wp" and end_row == 0:
        board[start_row][start_col] = ""
        board[end_row][end_col] = "wq"
    # Regular move
    elif is_valid_move(possible_moves, end_pos):
        board[start_row][start_col] = ""
        board[end_row][end_col] = piece

# 0: can't castle, 1: can castle kingside, 2: can castle queenside
def can_castle(board, start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    piece = board[start_row][start_col]
    if piece[1] != "k":
        return 0

    if start_row == 7 and start_col == 4 and end_row == 7 and end_col == 6:
        return 1
    elif start_row == 7 and start_col == 4 and end_row == 7 and end_col == 2:
        return 2
    return 0

def is_valid_move(possible_moves, end_pos):
    return end_pos in possible_moves

def get_possible_moves(board, selected_piece):
    piece = board[selected_piece[0]][selected_piece[1]]
    if piece == "wp":
        return possible_moves_pawn(board, selected_piece)
    elif piece == "wn":
        return possible_moves_knight(board, selected_piece)
    elif piece == "wb":
        return possible_moves_bishop(board, selected_piece)
    elif piece == "wr":
        return possible_moves_rook(board, selected_piece)
    elif piece == "wq":
        return possible_moves_bishop(board, selected_piece) + possible_moves_rook(board, selected_piece)
    elif piece == "wk":
        return possible_moves_king(board, selected_piece)
    return []

def possible_moves_pawn(board, start_pos):
    x, y = start_pos
    possible = []
    print(x, y)

    # Moving one square forward
    if x > 0 and board[x - 1][y] == "":
        possible.append((x - 1, y))

    # Moving two squares forward from the starting position
    if x == 6 and board[x - 1][y] == "" and board[x - 2][y] == "":
        possible.append((x - 2, y))

    # Capture moves
    if x > 0 and y > 0 and board[x - 1][y - 1] != "" and board[x - 1][y - 1][0] == "b":
        possible.append((x - 1, y - 1))
    if x > 0 and y < 7 and board[x - 1][y + 1] != "" and board[x - 1][y + 1][0] == "b":
        possible.append((x - 1, y + 1))
    
    return possible

def possible_moves_knight(board, start_pos):
    x, y = start_pos
    possible = []
    print(x, y)

    # Up
    if x > 1:
        if y > 0 and (board[x - 2][y - 1] == "" or board[x - 2][y - 1][0] == "b"):
            possible.append((x - 2, y - 1))
        if y < 7 and (board[x - 2][y + 1] == "" or board[x - 2][y + 1][0] == "b"):
            possible.append((x - 2, y + 1))

    # Down
    if x < 6:
        if y > 0 and (board[x + 2][y - 1] == "" or board[x + 2][y - 1][0] == "b"):
            possible.append((x + 2, y - 1))
        if y < 7 and (board[x + 2][y + 1] == "" or board[x + 2][y + 1][0] == "b"):
            possible.append((x + 2, y + 1))

    # Left
    if y > 1:
        if x > 0 and (board[x - 1][y - 2] == "" or board[x - 1][y - 2][0] == "b"):
            possible.append((x - 1, y - 2))
        if x < 7 and (board[x + 1][y - 2] == "" or board[x + 1][y - 2][0] == "b"):
            possible.append((x + 1, y - 2))

    # Right
    if y < 6:
        if x > 0 and (board[x - 1][y + 2] == "" or board[x - 1][y + 2][0] == "b"):
            possible.append((x - 1, y + 2))
        if x < 7 and (board[x + 1][y + 2] == "" or board[x + 1][y + 2][0] == "b"):
            possible.append((x + 1, y + 2))

    return possible

def possible_moves_bishop(board, start_pos):
    x, y = start_pos
    possible = []
    print(x, y)

    # Up-left
    i, j = x - 1, y - 1
    while i >= 0 and j >= 0:
        if board[i][j] == "":
            possible.append((i, j))
        elif board[i][j][0] == "b":
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
        elif board[i][j][0] == "b":
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
        elif board[i][j][0] == "b":
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
        elif board[i][j][0] == "b":
            possible.append((i, j))
            break
        else:
            break
        i += 1
        j += 1

    return possible

def possible_moves_rook(board, start_pos):
    x, y = start_pos
    possible = []
    print(x, y)

    # Up
    i = x - 1
    while i >= 0:
        if board[i][y] == "":
            possible.append((i, y))
        elif board[i][y][0] == "b":
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
        elif board[i][y][0] == "b":
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
        elif board[x][j][0] == "b":
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
        elif board[x][j][0] == "b":
            possible.append((x, j))
            break
        else:
            break
        j += 1

    return possible

def possible_moves_king(board, selected_piece):
    x, y = selected_piece
    possible = []
    print(x, y)

    # Up
    if x > 0:
        if board[x - 1][y] == "" or board[x - 1][y][0] == "b":
            possible.append((x - 1, y))
        if y > 0 and (board[x - 1][y - 1] == "" or board[x - 1][y - 1][0] == "b"):
            possible.append((x - 1, y - 1))
        if y < 7 and (board[x - 1][y + 1] == "" or board[x - 1][y + 1][0] == "b"):
            possible.append((x - 1, y + 1))

    # Down
    if x < 7:
        if board[x + 1][y] == "" or board[x + 1][y][0] == "b":
            possible.append((x + 1, y))
        if y > 0 and (board[x + 1][y - 1] == "" or board[x + 1][y - 1][0] == "b"):
            possible.append((x + 1, y - 1))
        if y < 7 and (board[x + 1][y + 1] == "" or board[x + 1][y + 1][0] == "b"):
            possible.append((x + 1, y + 1))

    # Left
    if y > 0 and (board[x][y - 1] == "" or board[x][y - 1][0] == "b"):
        possible.append((x, y - 1))

    # Right
    if y < 7 and (board[x][y + 1] == "" or board[x][y + 1][0] == "b"):
        possible.append((x, y + 1))
    
    if x == 7 and y == 4 and board[7][7] == "wr" and board[7][5] == "" and board[7][6] == "":
        possible.append((7, 6))
    elif x == 7 and y == 4 and board[7][0] == "wr" and board[7][1] == "" and board[7][2] == "" and board[7][3] == "":
        possible.append((7, 2))

    return possible
