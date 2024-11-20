import numpy as np

ROWS = 6
COLUMNS = 7

def create_board():
    return np.zeros((ROWS, COLUMNS), dtype=int)

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def get_next_open_row(board, col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r

def is_valid_location(board, col):
    return board[ROWS - 1][col] == 0

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMNS):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations
