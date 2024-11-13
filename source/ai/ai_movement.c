#include <stdio.h>
#include <string.h>

#define BOARD_SIZE 8
#define BUF_SIZE 512

typedef struct {
    int x;
    int y;
} Position;

// Function to get possible moves for a rook
Position *possible_moves_rook(char *board[BOARD_SIZE][BOARD_SIZE], Position start_pos, char color, Position possible_moves[64]) {
    int count = 0;
    int opponent_color = (color == 'w') ? 'b' : 'w';
    int x = start_pos.x;
    int y = start_pos.y;

    printf("Checking for rook at (%d, %d)\n", x, y);

    for (int i = x - 1; i >= 0; i--) {
        if (board[i][y][0] == '\0') {  // Empty space
            possible_moves[count++] = (Position){i, y};
        } else if (board[i][y][0] == opponent_color) {  // Opponent piece
            possible_moves[count++] = (Position){i, y};
            break;
        } else {  // Friendly piece
            break;
        }
    }

    // Down
    printf("Checking for rook at (%d, %d)\n", x, y);
    for (int i = x + 1; i < BOARD_SIZE; i++) {
        printf("Checking (%d, %d)\n", i, y);
        if (board[i][y][0] == opponent_color) {  // Opponent piece
            possible_moves[count++] = (Position){i, y};
            break;
        } else if (board[i][y][0] == color) {  // Friendly piece
            printf("reach here\n");
            break;
        }
        possible_moves[count++] = (Position){i, y};
    }

    // Left
    for (int j = y - 1; j >= 0; j--) {
        if (board[x][j][0] == '\0') {  // Empty space
            possible_moves[count++] = (Position){x, j};
        } else if (board[x][j][0] == opponent_color) {  // Opponent piece
            possible_moves[count++] = (Position){x, j};
            break;
        } else {  // Friendly piece
            break;
        }
    }

    // Right
    for (int j = y + 1; j < BOARD_SIZE; j++) {
        printf("Checking (%d, %d)\n", x, j);
        if (board[x][j][0] == '\0') {  // Empty space
            possible_moves[count++] = (Position){x, j};
        } else if (board[x][j][0] == opponent_color) {  // Opponent piece
            possible_moves[count++] = (Position){x, j};
            break;
        } else {  // Friendly piece
            break;
        }
    }

    for (int i = 0; i < count; i++) {
        printf("(%d, %d)\n", possible_moves[i].x, possible_moves[i].y);
    }
    return possible_moves;
}