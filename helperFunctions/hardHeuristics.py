from helperFunctions.positions import *

ROWS = 6
COLUMNS = 7
EMPTY = 0
WINDOW_LENGTH = 4
PLAYER_PIECE = 1
AI_PIECE = 2

# Heuristic for the Hard AI level
def hard_heuristics(board, piece):
    score = 0
    # 1. Block opponent's winning moves
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            window = [board[r][c + i] for i in range(WINDOW_LENGTH)]
            if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
                score += 100  # Block winning move

    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            window = [board[r + i][c] for i in range(WINDOW_LENGTH)]
            if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
                score += 100  # Block winning move

    # 2. Prioritize center columns
    center_column = [board[r][COLUMNS // 2] for r in range(ROWS)]
    if center_column.count(piece) > 0:
        score += 5  # Prioritize controlling the center

    # 3. Prevent future threats (3 in a row)
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
                score -= 3  # Prevent opponent's future threat

    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
                score -= 3  # Prevent opponent's future threat

    return score
