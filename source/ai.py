from source.movement import *
from source.constants import *
from source.board import *
import random

board_score_cache = {}
board_move_cache = {}

def evaluate_board(board):
    piece_values = {
        'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 1000  # Piece values
    }
    
    score = 0
    
    for row in board:
        for piece in row:
            if piece != "":
                color = piece[0]  # 'w' or 'b'
                value = piece_values.get(piece[1], 0)
                if color == "b":
                    score += value
                else:
                    score -= value
                    
    return score

def minimax(board, depth, alpha, beta, is_maximizing_player):
    board_hash = hash(str(board))
    if depth == 0 or game_over(board):
        # cache hit
        if board_hash in board_score_cache:
            return board_score_cache[board_hash]
        else:
            evaluation = evaluate_board(board)
            board_score_cache[board_hash] = evaluation
            return evaluation

    if is_maximizing_player:  # AI's turn (maximize score)
        max_eval = float('-inf')
        for move in generate_ai_moves(board):
            new_board = apply_move(board, move)
            eval = minimax(new_board, depth-1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:  # Opponent's turn (minimize score)
        min_eval = float('inf')
        for move in generate_enemy_moves(board):
            new_board = apply_move(board, move)
            eval = minimax(new_board, depth-1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def generate_ai_moves(board):
    board_hash = hash(str(board))
    if board_hash in board_move_cache:
        return board_move_cache[board_hash]
    
    moves = []
    priorities = []
    for r in range(8):
        for c in range(8):
            if board[r][c] != "" and board[r][c][0] == "b":
                set_current_player(Player.BLACK)
                possible_moves = get_possible_moves(board, (r, c))
                for move in possible_moves:
                    new_board = apply_move(board, ((r, c), move))
                    king_loc = find_king(new_board)
                    if not in_check(new_board, king_loc):
                        priorities.append(evaluate_board(new_board))
                        moves.append(((r, c), move))
    # Create a list of tuples (move, priority) and sort by priority
    moves_with_priority = list(zip(moves, priorities))
    moves_with_priority.sort(key=lambda x: x[1], reverse=True)  # Sort by priority

    # Return the sorted moves based on highest priority
    sorted_moves = [move for move, priority in moves_with_priority]

    board_move_cache[board_hash] = sorted_moves
    return sorted_moves

def generate_enemy_moves(board):
    board_hash = hash(str(board))
    if board_hash in board_move_cache:
        return board_move_cache[board_hash]
    
    moves = []
    priorities = []
    for r in range(8):
        for c in range(8):
            if board[r][c] != "" and board[r][c][0] == "w":
                set_current_player(Player.WHITE)
                possible_moves = get_possible_moves(board, (r, c))
                set_current_player(Player.BLACK)
                for move in possible_moves:
                    new_board = apply_move(board, ((r, c), move))
                    enemy_king_loc = find_enemy_king(new_board)
                    if not enemy_in_check(new_board, enemy_king_loc):
                        priorities.append(evaluate_board(new_board))
                        moves.append(((r, c), move))
    # Create a list of tuples (move, priority) and sort by priority
    moves_with_priority = list(zip(moves, priorities))
    moves_with_priority.sort(key=lambda x: x[1], reverse=True)  # Sort by priority

    # Return the sorted moves based on highest priority
    sorted_moves = [move for move, priority in moves_with_priority]

    board_move_cache[board_hash] = sorted_moves
    return sorted_moves


def apply_move(board, move):
    start_pos, end_pos = move
    new_board = [row[:] for row in board]  # Create a deep copy of the board
    piece = new_board[start_pos[0]][start_pos[1]]
    if piece == "wp" and end_pos[0] == 0:  # Promote white pawn
        piece = "wq"
    elif piece == "bp" and end_pos[0] == 7:  # Promote black pawn
        piece = "bq"
    new_board[start_pos[0]][start_pos[1]] = ""
    new_board[end_pos[0]][end_pos[1]] = piece
    return new_board

def ai_move(board, depth=3):
    best_moves = []
    max_eval = float('-inf')

    for move in generate_ai_moves(board):
        new_board = apply_move(board, move)
        eval = minimax(new_board, depth-1, float('-inf'), float('inf'), False)
        
        if eval > max_eval:
            max_eval = eval
            best_moves = [move]  # Start a new list with the current move
        elif eval == max_eval:
            best_moves.append(move)  # Add move to the list of best moves with the same score

    # Randomly choose from moves with the highest evaluation
    best_move = random.choice(best_moves) if best_moves else None
    return best_move

# Example Usage
def make_ai_move(board, screen, miss_rate=0.0, depth=3):
    best_move = ai_move(board, depth)
    print("AI's best move:", best_move)
    if best_move:
        # Introduce a miss rate to simulate human error
        if random.random() < miss_rate:
            print("AI missed the best move!")
            possible_moves = generate_ai_moves(board)
            best_move = random.choice(possible_moves)
        start_pos, end_pos = best_move
        return move_piece(screen, board, get_possible_moves(board, start_pos), start_pos, end_pos, ai=True)
    return False
    

def game_over(board):
    king_loc = find_king(board)
    if in_checkmate(board, king_loc) or in_stalemate(board, king_loc):
        return True

    enemy_king_loc = find_enemy_king(board)
    if enemy_in_checkmate(board, enemy_king_loc) or enemy_in_stalemate(board, enemy_king_loc):
        return True
    return False

