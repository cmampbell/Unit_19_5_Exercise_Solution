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
    '''Will generate a game board, save it to the session, check session cookies for
    users high score, number of games played, and set values in the session if they
    do not exist.'''
    session['game_board'] = boggle_game.make_board()
    session['found_words'] = []

    check_session_on_start()

    return render_template('game_page.html', game_board = session['game_board'], games_played=session['games_played'], high_score=session['high_score'], found_words=session['found_words'])

def check_session_on_start():
    '''Check session to see if high score and games played values exist. If not, make them'''
    if session.get('high_score') is None:
        session['high_score'] = 0

    if session.get('games_played') is None:
        session['games_played'] = 0

@app.route('/check')
def check_guess():
    '''Route that will take the user input from site and check against database of words'''
    # get the users guess
    user_guess = request.args.get('guess')

    if user_guess in session['found_words']:
        return jsonify({'result': 'already found'})
    else:
        add_guess_to_session(user_guess)
        return jsonify({'result': boggle_game.check_valid_word(session['game_board'], user_guess), 'found_words': session['found_words']})

def add_guess_to_session(user_guess):
        found_words = session['found_words']
        found_words.append(user_guess)
        session['found_words'] = found_words

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

