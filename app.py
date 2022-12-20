from boggle import Boggle
from flask import Flask, render_template, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = 'poopybutthole'
debug = DebugToolbarExtension(app)

boggle_game = Boggle()

# add home page that will ask user to start the game
    #contains button with get action to the game page
@app.route('/')
def show_game_page():
    '''View function that will render the template for the Boggle game,
    and set the game board in the session'''
    session['game_board'] = boggle_game.make_board()

    if session.get('high_score') is None:
        session['high_score'] = 0

    if session.get('games_played') is None:
        session['games_played'] = 0

    return render_template('game_page.html', game_board = session['game_board'], games_played=session['games_played'], high_score=session['high_score'])

@app.route('/check')
def check_guess():
    '''Route that will take the user input from site and check against database of words'''
    # get the users guess
    user_guess = request.args.get('guess')
    return jsonify({'result': boggle_game.check_valid_word(session['game_board'], user_guess)})

@app.route('/end-game')
def end_game():
    '''Route that accepts a get request sent at the end of the game, recording the high score
    and how many times the user has played the game'''

    #check for high score
    user_score = int(request.args.get('score'))
    print(session.get('high_score'))
    print(session.get('games_played'))

    #increment games played
    session['games_played'] += 1

    #if the user has a new high score
    if user_score > session.get('high_score'):
        session['high_score'] = user_score
    
    
    return jsonify({'games_played': session['games_played'], 'high_score': user_score})