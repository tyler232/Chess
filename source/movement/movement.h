#ifndef MOVEMENT_H
#define MOVEMENT_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BOARD_SIZE 8

typedef struct {
    int x;
    int y;
} Position;


/**
 * Get all possible moves for a knight
 * @param board The current board
 * @param start_pos The starting position of the knight
 * @param color The color of the knight
 * @param move_count The number of possible moves
 * @return An array of possible moves
*/
Position* possible_moves_knight(char board[BOARD_SIZE][BOARD_SIZE][3], Position start_pos, char color, int* move_count);

/**
 * Get all possible moves for a rook
 * @param board The current board
 * @param start_pos The starting position of the rook
 * @param color The color of the rook
 * @param move_count The number of possible moves
 * @return An array of possible moves
*/
Position* possible_moves_rook(char board[BOARD_SIZE][BOARD_SIZE][3], Position start_pos, char color, int* move_count);

/**
 * Get all possible moves for a bishop
 * @param board The current board
 * @param start_pos The starting position of the bishop
 * @param color The color of the bishop
 * @param move_count The number of possible moves
 * @return An array of possible moves
*/
Position* possible_moves_bishop(char board[BOARD_SIZE][BOARD_SIZE][3], Position start_pos, char color, int* move_count);

#endif
