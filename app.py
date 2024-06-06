from flask import Flask, request, render_template, jsonify, flash, session
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

boggle_game = Boggle()

@app.route('/')
def show_board():
    """Shows boggle board."""
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    plays = session.get("plays", 0)
    return render_template("index.html", board=board, highscore=highscore, plays=plays)

@app.route('/check-word')
def check_word():
    """Checks if word is valid."""
    word = request.args['word']
    board = session['board']
    validity = boggle_game.check_valid_word(board, word)
    return jsonify({"result": validity})

@app.route('/plays', methods=["POST"])
def update_plays():
    """Updates the server with time played and scores"""
    score = request.json["score"]

    highscore = session.get("highscore", 0)
    plays = session.get("plays", 0)
    
    session["plays"] = plays + 1
    session["highscore"] = max(score, highscore)
    new_highscore = score > highscore
    return jsonify({"highscore": highscore, "plays": plays, "new_highscore": new_highscore})



