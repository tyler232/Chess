#include "movement.h"

Position* possible_moves_knight(char board[BOARD_SIZE][BOARD_SIZE][3], Position start_pos, char color, int *move_count) {
    int x = start_pos.x;
    int y = start_pos.y;
    Position *possible = (Position *)malloc(8 * sizeof(Position));  // max 8 possible moves
    *move_count = 0;

    char opponent_color = (color == 'w') ? 'b' : 'w';

    // All possible knight moves (2 squares in one direction, 1 in the perpendicular direction)
    int knight_moves[8][2] = {
        {-2, -1}, {-2, 1}, {2, -1}, {2, 1},   // Up-left, Up-right, Down-left, Down-right
        {-1, -2}, {1, -2}, {-1, 2}, {1, 2}     // Left-up, Right-up, Left-down, Right-down
    };

    for (int i = 0; i < 8; i++) {
        int new_x = x + knight_moves[i][0];
        int new_y = y + knight_moves[i][1];

        // Check if the move is within bounds
        if (new_x >= 0 && new_x < BOARD_SIZE && new_y >= 0 && new_y < BOARD_SIZE) {
            // Check if the destination is either empty or occupied by an opponent's piece
            if (strcmp(board[new_x][new_y], "") == 0 || board[new_x][new_y][0] == opponent_color) {
                possible[(*move_count)++] = (Position){new_x, new_y};
            }
        }
    }

    return possible;
}


Position* possible_moves_bishop(char board[BOARD_SIZE][BOARD_SIZE][3], Position start_pos, char color, int *move_count) {
    int x = start_pos.x;
    int y = start_pos.y;
    Position *possible = (Position *)malloc(BOARD_SIZE * BOARD_SIZE * sizeof(Position));
    *move_count = 0;

    char opponent_color = (color == 'w') ? 'b' : 'w';

    // Up-left
    for (int i = x - 1, j = y - 1; i >= 0 && j >= 0; i--, j--) {
        if (strcmp(board[i][j], "") == 0) {
            possible[(*move_count)++] = (Position){i, j};
        } else if (board[i][j][0] == opponent_color) {
            possible[(*move_count)++] = (Position){i, j};
            break;
        } else {
            break;
        }
    }

    // Up-right
    for (int i = x - 1, j = y + 1; i >= 0 && j < BOARD_SIZE; i--, j++) {
        if (strcmp(board[i][j], "") == 0) {
            possible[(*move_count)++] = (Position){i, j};
        } else if (board[i][j][0] == opponent_color) {
            possible[(*move_count)++] = (Position){i, j};
            break;
        } else {
            break;
        }
    }

    // Down-left
    for (int i = x + 1, j = y - 1; i < BOARD_SIZE && j >= 0; i++, j--) {
        if (strcmp(board[i][j], "") == 0) {
            possible[(*move_count)++] = (Position){i, j};
        } else if (board[i][j][0] == opponent_color) {
            possible[(*move_count)++] = (Position){i, j};
            break;
        } else {
            break;
        }
    }

    // Down-right
    for (int i = x + 1, j = y + 1; i < BOARD_SIZE && j < BOARD_SIZE; i++, j++) {
        if (strcmp(board[i][j], "") == 0) {
            possible[(*move_count)++] = (Position){i, j};
        } else if (board[i][j][0] == opponent_color) {
            possible[(*move_count)++] = (Position){i, j};
            break;
        } else {
            break;
        }
    }

    return possible;
}

Position* possible_moves_rook(char board[BOARD_SIZE][BOARD_SIZE][3], Position start_pos, char color, int *move_count) {
    int x = start_pos.x;
    int y = start_pos.y;
    Position *possible = (Position *)malloc(BOARD_SIZE * BOARD_SIZE * sizeof(Position));
    *move_count = 0;

    char opponent_color = (color == 'w') ? 'b' : 'w';

    // Up
    for (int i = x - 1; i >= 0; i--) {
        if (strcmp(board[i][y], "") == 0) {
            possible[(*move_count)++] = (Position){i, y};
        } else if (board[i][y][0] == opponent_color) {
            possible[(*move_count)++] = (Position){i, y};
            break;
        } else {
            break;
        }
    }

    // Down
    for (int i = x + 1; i < BOARD_SIZE; i++) {
        if (strcmp(board[i][y], "") == 0) {
            possible[(*move_count)++] = (Position){i, y};
        } else if (board[i][y][0] == opponent_color) {
            possible[(*move_count)++] = (Position){i, y};
            break;
        } else {
            break;
        }
    }

    // Left
    for (int j = y - 1; j >= 0; j--) {
        if (strcmp(board[x][j], "") == 0) {
            possible[(*move_count)++] = (Position){x, j};
        } else if (board[x][j][0] == opponent_color) {
            possible[(*move_count)++] = (Position){x, j};
            break;
        } else {
            break;
        }
    }

    // Right
    for (int j = y + 1; j < BOARD_SIZE; j++) {
        if (strcmp(board[x][j], "") == 0) {
            possible[(*move_count)++] = (Position){x, j};
        } else if (board[x][j][0] == opponent_color) {
            possible[(*move_count)++] = (Position){x, j};
            break;
        } else {
            break;
        }
    }

    return possible;
}
