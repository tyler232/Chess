#include <stdio.h>
#include <assert.h>
#include "movement.h"

void test_possible_moves_king() {
    // Initialize an empty board with all cells set to ""
    char board[BOARD_SIZE][BOARD_SIZE][3] = {{{""}}};

    // Place a white king at (4, 4)
    board[4][4][0] = 'w';
    board[4][4][1] = 'k';

    Position start_pos = {4, 4};
    int move_count = 0;

    Position* moves = possible_moves_king(board, start_pos, 'w', &move_count);
    Position expected_moves[] = {
        {3, 4}, {3, 3}, {3, 5},
        {5, 4}, {5, 3}, {5, 5},
        {4, 3}, {4, 5}
    };

    int expected_count = 8;
    assert(move_count == expected_count);
    for (int i = 0; i < move_count; i++) {
        assert(moves[i].x == expected_moves[i].x);
        assert(moves[i].y == expected_moves[i].y);
    }

    printf("test_possible_moves_king passed (1/5).\n");
    free(moves);

    // Refresh the board
    for (int i = 0; i < BOARD_SIZE; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            board[i][j][0] = '\0';
            board[i][j][1] = '\0';
        }
    }

    // Place a black king at (4, 4)
    board[4][4][0] = 'b';
    board[4][4][1] = 'k';

    // Place a white pawn at (3, 3) and a black queen at (5, 4)
    board[3][3][0] = 'w';
    board[3][3][1] = 'p';
    board[5][4][0] = 'b';
    board[5][4][1] = 'q';

    start_pos.x = 4;
    start_pos.y = 4;
    move_count = 0;
    moves = possible_moves_king(board, start_pos, 'b', &move_count);
    Position expected_moves2[] = {
        {3, 4}, {3, 3}, {3, 5},
        {5, 3}, {5, 5},
        {4, 3}, {4, 5}
    };
    expected_count = 7;
    assert(move_count == expected_count);

    for (int i = 0; i < move_count; i++) {
        assert(moves[i].x == expected_moves2[i].x);
        assert(moves[i].y == expected_moves2[i].y);
    }

    printf("test_possible_moves_king passed (2/5).\n");
    free(moves);

    // Refresh the board
    for (int i = 0; i < BOARD_SIZE; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            board[i][j][0] = '\0';
            board[i][j][1] = '\0';
        }
    }

    // Place a white king at (7, 4)
    board[7][4][0] = 'w';
    board[7][4][1] = 'k';

    // Place white rooks at (7, 7) and (7, 0)
    board[7][7][0] = 'w';
    board[7][7][1] = 'r';
    board[7][0][0] = 'w';
    board[7][0][1] = 'r';

    start_pos.x = 7;
    start_pos.y = 4;
    move_count = 0;
    moves = possible_moves_king(board, start_pos, 'w', &move_count);

    Position expected_moves3[] = {
        {6, 4}, {6, 3}, {6, 5},
        {7, 3}, {7, 5},
        {7, 6}, {7, 2}
    };
    expected_count = 7;
    assert(move_count == expected_count);

    for (int i = 0; i < move_count; i++) {
        assert(moves[i].x == expected_moves3[i].x);
        assert(moves[i].y == expected_moves3[i].y);
    }

    printf("test_possible_moves_king passed (3/5).\n");
    free(moves);

    // Refresh the board
    for (int i = 0; i < BOARD_SIZE; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            board[i][j][0] = '\0';
            board[i][j][1] = '\0';
        }
    }

    // Place a black king at (0, 4)
    board[0][4][0] = 'b';
    board[0][4][1] = 'k';

    // Place black rooks at (0, 7) and (0, 0)
    board[0][7][0] = 'b';
    board[0][7][1] = 'r';
    board[0][0][0] = 'b';
    board[0][0][1] = 'r';

    start_pos.x = 0;
    start_pos.y = 4;
    move_count = 0;
    moves = possible_moves_king(board, start_pos, 'b', &move_count);
    Position expected_moves4[] = {
        {1, 4}, {1, 3}, {1, 5},
        {0, 3}, {0, 5},
        {0, 6}, {0, 2}
    };

    expected_count = 7;
    assert(move_count == expected_count);
    for (int i = 0; i < move_count; i++) {
        assert(moves[i].x == expected_moves4[i].x);
        assert(moves[i].y == expected_moves4[i].y);
    }

    printf("test_possible_moves_king passed (4/5).\n");

    free(moves);

    // Refresh the board
    for (int i = 0; i < BOARD_SIZE; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            board[i][j][0] = '\0';
            board[i][j][1] = '\0';
        }
    }

    // Place a black king at (0, 4)
    board[0][4][0] = 'b';
    board[0][4][1] = 'k';

    // Place black rooks at (0, 7) and (0, 0)
    board[0][7][0] = 'b';
    board[0][7][1] = 'r';
    board[0][0][0] = 'b';
    board[0][0][1] = 'r';

    // Place a black bishop at (0, 3)
    board[0][3][0] = 'b';
    board[0][3][1] = 'b';

    start_pos.x = 0;
    start_pos.y = 4;
    move_count = 0;
    moves = possible_moves_king(board, start_pos, 'b', &move_count);
    Position expected_moves5[] = {
        {1, 4}, {1, 3}, {1, 5},
        {0, 5}, {0, 6}
    };

    expected_count = 5;
    assert(move_count == expected_count);
    for (int i = 0; i < move_count; i++) {
        assert(moves[i].x == expected_moves5[i].x);
        assert(moves[i].y == expected_moves5[i].y);
    }

    printf("test_possible_moves_king passed (5/5).\n");

    free(moves);
}


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
    test_possible_moves_king();
    printf("All tests passed.\n");
    return 0;
}