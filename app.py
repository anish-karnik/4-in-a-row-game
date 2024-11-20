from flask import Flask, render_template, request, jsonify
from helperFunctions.minmax import *
app = Flask(__name__)

PLAYER_PIECE = 1
AI_PIECE = 2
board = create_board()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/player_move', methods=['POST'])
def player_move():
    data = request.get_json()
    col = data.get("column")

    if is_valid_location(board, col):
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, PLAYER_PIECE)
        
        if winning_move(board, PLAYER_PIECE):
            return jsonify(board=board.tolist(), winner='Player')
        
        elif not get_valid_locations(board):
            return jsonify(board=board.tolist(), draw=True)

    return jsonify(board=board.tolist())

@app.route('/ai_move', methods=['POST'])
def ai_move():
    # Calculate the AI move with minimax
    # col, _ = minimax(board, 4, -math.inf, math.inf, True)
    try:
        level = current_difficulty
    except:
        level = "easy"

    if level == "easy":
        col = mixed_easy_ai_move(board)
    elif level == "medium":
        col = medium_ai_move(board)
    else:
        col = hard_ai_move(board)
    
    if is_valid_location(board, col):
        # Drop the piece on the board for AI
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, AI_PIECE)
        
        response = {"board": board.tolist(), "aiMoveMade": True}

        # Check for winning condition after sending the board state
        if winning_move(board, AI_PIECE):
            response["winner"] = 'AI'
        elif not get_valid_locations(board):
            response["draw"] = True

        return jsonify(response)
    else:
        return jsonify(board=board.tolist())

@app.route('/set_difficulty', methods=['POST'])
def set_difficulty():
    global current_difficulty
    data = request.get_json()
    current_difficulty = data.get('difficulty', 'easy')
    return jsonify(success=True)

@app.route('/restart', methods=['POST'])
def restart():
    global board
    board = create_board()
    return jsonify(board=board.tolist())

if __name__ == '__main__':
    app.run(debug=True)
