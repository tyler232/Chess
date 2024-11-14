#include <stdio.h>
#include <assert.h>
#include "movement.h"

void test_possible_moves_knight() {
    // Initialize an empty board with all cells set to ""
    char board[BOARD_SIZE][BOARD_SIZE][3] = {{{""}}};

    // Place a white knight at (4, 4)
    board[4][4][0] = 'w';
    board[4][4][1] = 'n';

    Position start_pos = {4, 4};
    int move_count = 0;

    Position* moves = possible_moves_knight(board, start_pos, 'w', &move_count);

    Position expected_moves[] = {
        {2, 3}, {2, 5}, {6, 3}, {6, 5},
        {3, 2}, {5, 2}, {3, 6}, {5, 6}
    };

    int expected_count = 8;
    assert(move_count == expected_count);
    for (int i = 0; i < move_count; i++) {
        assert(moves[i].x == expected_moves[i].x);
        assert(moves[i].y == expected_moves[i].y);
    }

    printf("test_possible_moves_knight passed (1/2).\n");
    free(moves);

    // Refresh the board
    for (int i = 0; i < BOARD_SIZE; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            board[i][j][0] = '\0';
            board[i][j][1] = '\0';
        }
    }

    // Place a black knight at (4, 4)
    board[4][4][0] = 'b';
    board[4][4][1] = 'n';

    // Place a white pawn at (2, 3) and a black queen at (5, 6)
    board[2][3][0] = 'w';
    board[2][3][1] = 'p';
    board[5][6][0] = 'b';
    board[5][6][1] = 'q';

    start_pos.x = 4;
    start_pos.y = 4;
    move_count = 0;
    moves = possible_moves_knight(board, start_pos, 'b', &move_count);
    Position expected_moves2[] = {
        {2, 3}, {2, 5}, {6, 3}, {6, 5},
        {3, 2}, {5, 2}, {3, 6}
    };
    expected_count = 7;
    assert(move_count == expected_count);

    for (int i = 0; i < move_count; i++) {
        assert(moves[i].x == expected_moves2[i].x);
        assert(moves[i].y == expected_moves2[i].y);
    }

    printf("test_possible_moves_knight passed (2/2).\n");
    free(moves);
}


void test_possible_moves_bishop() {
    // Initialize an empty board with all cells set to ""
    char board[BOARD_SIZE][BOARD_SIZE][3] = {{{""}}};

    // Place a white bishop at (4, 4)
    board[4][4][0] = 'w';
    board[4][4][1] = 'b';

    Position start_pos = {4, 4};
    int move_count = 0;

    Position* moves = possible_moves_bishop(board, start_pos, 'w', &move_count);
    Position expected_moves[] = {
        {3, 3}, {2, 2}, {1, 1}, {0, 0}, // Up-left
        {3, 5}, {2, 6}, {1, 7}, // Up-right
        {5, 3}, {6, 2}, {7, 1}, // Down-left
        {5, 5}, {6, 6}, {7, 7} // Down-right
    };

    int expected_count = 13;
    assert(move_count == expected_count);
    for (int i = 0; i < move_count; i++) {
        assert(moves[i].x == expected_moves[i].x);
        assert(moves[i].y == expected_moves[i].y);
    }

    printf("test_possible_moves_bishop passed (1/2).\n");
    free(moves);

    // refresh board
    for (int i = 0; i < BOARD_SIZE; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            board[i][j][0] = '\0';
            board[i][j][1] = '\0';
        }
    }

    // Place a black bishop at (4, 4)
    board[4][4][0] = 'b';
    board[4][4][1] = 'b';

    // Place a white pawn at (2, 2) and a black queen at (6, 6)
    board[2][2][0] = 'w';
    board[2][2][1] = 'p';
    board[6][6][0] = 'b';
    board[6][6][1] = 'q';

    start_pos.x = 4;
    start_pos.y = 4;
    move_count = 0;
    moves = possible_moves_bishop(board, start_pos, 'b', &move_count);
    Position expected_moves2[] = {
        {3, 3}, {2, 2}, // Up-left
        {3, 5}, {2, 6}, {1, 7}, // Up-right
        {5, 3}, {6, 2}, {7, 1}, // Down-left
        {5, 5} // Down-right
    };
    expected_count = 9;
    assert(move_count == expected_count);

    for (int i = 0; i < move_count; i++) {
        assert(moves[i].x == expected_moves2[i].x);
        assert(moves[i].y == expected_moves2[i].y);
    }

    printf("test_possible_moves_bishop passed (2/2).\n");
    free(moves);
}

void test_possible_moves_rook() {
    // Initialize an empty board with all cells set to ""
    char board[BOARD_SIZE][BOARD_SIZE][3] = {{{""}}};

    // Place a white rook at (4, 4)
    board[4][4][0] = 'w';
    board[4][4][1] = 'r';

    Position start_pos = {4, 4};
    int move_count = 0;

    Position* moves = possible_moves_rook(board, start_pos, 'w', &move_count);
    Position expected_moves[] = {
        {3, 4}, {2, 4}, {1, 4}, {0, 4}, // Up
        {5, 4}, {6, 4}, {7, 4}, // Down
        {4, 3}, {4, 2}, {4, 1}, {4, 0}, // Left
        {4, 5}, {4, 6}, {4, 7} // Right
    };

    int expected_count = 14;
    assert(move_count == expected_count);
    for (int i = 0; i < move_count; i++) {
        assert(moves[i].x == expected_moves[i].x);
        assert(moves[i].y == expected_moves[i].y);
    }

    printf("test_possible_moves_rook passed (1/2).\n");
    free(moves);

    // refresh board
    for (int i = 0; i < BOARD_SIZE; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            board[i][j][0] = '\0';
            board[i][j][1] = '\0';
        }
    }

    // Place a black rook at (4, 4)
    board[4][4][0] = 'b';
    board[4][4][1] = 'r';

    // Place a white pawn at (2, 4) and a black queen at (4, 6)
    board[2][4][0] = 'w';
    board[2][4][1] = 'p';
    board[4][6][0] = 'b';
    board[4][6][1] = 'q';

    start_pos.x = 4;
    start_pos.y = 4;
    move_count = 0;
    moves = possible_moves_rook(board, start_pos, 'b', &move_count);
    Position expected_moves2[] = {
        {3, 4}, {2, 4}, // Up
        {5, 4}, {6, 4}, {7, 4}, // Down
        {4, 3}, {4, 2}, {4, 1}, {4, 0}, // Left
        {4, 5} // Right
    };
    expected_count = 10;
    assert(move_count == expected_count);

    for (int i = 0; i < move_count; i++) {
        assert(moves[i].x == expected_moves2[i].x);
        assert(moves[i].y == expected_moves2[i].y);
    }

    printf("test_possible_moves_rook passed (2/2).\n");
    free(moves);
}

int main() {
    test_possible_moves_knight();
    test_possible_moves_bishop();
    test_possible_moves_rook();
    printf("All tests passed.\n");
    return 0;
}