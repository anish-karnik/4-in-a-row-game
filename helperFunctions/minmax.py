import math
import random
from helperFunctions.positions import *
from helperFunctions.hardHeuristics import hard_heuristics

ROWS = 6
COLUMNS = 7
EMPTY = 0
WINDOW_LENGTH = 4
PLAYER_PIECE = 1
AI_PIECE = 2

def winning_move(board, piece):
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

    return False

def score_position(board, piece):
    score = 0

    center_array = [int(board[i][COLUMNS // 2]) for i in range(ROWS)]
    center_count = center_array.count(piece)
    score += center_count * 3  


    for r in range(ROWS):
        row_array = [int(board[r][c]) for c in range(COLUMNS)]
        for c in range(COLUMNS - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    for c in range(COLUMNS):
        col_array = [int(board[r][c]) for r in range(ROWS)]
        for r in range(ROWS - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def minimax(board, depth, alpha, beta, maximizingPlayer,level):
    valid_locations = get_valid_locations(board)
    is_terminal = winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(valid_locations) == 0

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 1000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -1000000)
            else:
                return (None, 0)
        else:
            if level== "hard":
                return (None, hard_heuristics(board, AI_PIECE)) 
            else:
                return (None, score_position(board, AI_PIECE))

    if maximizingPlayer:
        value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, AI_PIECE)
            new_score = minimax(temp_board, depth - 1, alpha, beta, False,level)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value

    else:
        value = math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, PLAYER_PIECE)
            new_score = minimax(temp_board, depth - 1, alpha, beta, True, level)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value
    
def easy_ai_move(board):
    valid_locations = get_valid_locations(board)
    return random.choice(valid_locations)

def medium_ai_move(board):
    return minimax(board, 3, -math.inf, math.inf, True, "medium")[0]  # Depth 3

def hard_ai_move(board):
    return minimax(board, 5, -math.inf, math.inf, True, "hard")[0]  # Depth 5

def mixed_easy_ai_move(board):
    if random.random() < 0.5:  # 50% chance for random move
        return easy_ai_move(board)
    else:
        return minimax(board, 2, -math.inf, math.inf, True, "easy")[0]  # Depth 2
