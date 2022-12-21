from unittest import TestCase
from app import app, check_session_on_start, add_guess_to_session
from flask import session
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

test_board =   [['P', 'A', 'R','T','Y'],
                ['H', 'I', 'N','D','E'],
                ['O', 'D', 'E','R','T'],
                ['L', 'O', 'N','G','U'],
                ['K', 'G', 'R','A','P'],]

boggle_game = Boggle()

class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    # show_game_page tests
    def test_show_game_page(self):
        '''Testing that show_game_page view function returns correct HTML and
        the proper status code'''
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertIn('<h1>Boggle Game!</h1>', html)
            self.assertEqual(200, resp.status_code)

            self.assertEqual(session['high_score'], 0)
            self.assertEqual(session['games_played'], 0)
            self.assertEqual(session['found_words'], [])
            self.assertIn('<section class="row">', html)


    #check_session_on_start tests
    def test_check_session_on_start(self):
        '''Testing that saved session cookies are not reset with
        check_session_on_start when viewing the "/" route'''
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['high_score'] = 999
                change_session['games_played'] = 999
            
            client.get('/')

            self.assertIsNone(check_session_on_start())
            self.assertEqual(session['high_score'], 999)
            self.assertEqual(session['games_played'], 999)

    #check_guess tests
    def test_check_guess(self):
        '''Testing the "/check" route with a test board'''
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['game_board'] = test_board
                change_session['found_words'] = []

            resp = client.get('/check?guess=part')
            json = resp.get_data(as_text=True)

            self.assertEqual(200, resp.status_code)
            self.assertIsInstance(session['game_board'], list)
            self.assertIn('part', session['found_words'])
            self.assertIn("ok", json)

    def test_check_guess_not_word(self):
        '''Testing the "/check" route with a test board when the user guess
        is not a word'''
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['game_board'] = test_board
                change_session['found_words'] = []

            resp = client.get('/check?guess=askdsk')
            json = resp.get_data(as_text=True)

            self.assertEqual(200, resp.status_code)
            self.assertIn("not-word", json)

    def test_check_guess_not_on_board(self):
        '''Testing the "/check" route with a test board when the user guess
        is not a word'''
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['game_board'] = test_board
                change_session['found_words'] = []

            resp = client.get('/check?guess=route')
            json = resp.get_data(as_text=True)

            self.assertEqual(200, resp.status_code)
            self.assertIn("not-on-board", json)

    def test_check_guess_word_already_found(self):
        '''Testing the "/check" route with a word that the user
        has found already'''
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['found_words'] = ['crocodile']

            resp = client.get('/check?guess=crocodile')
            json = resp.get_data(as_text=True)

            self.assertEqual(200, resp.status_code)
            self.assertIn("result", json)
    

    #add_guess_to_session tests

    def test_add_guess_to_session(self):
        '''Testing function that adds a users guess to the session'''
        with app.test_client() as client:
            client.get('/')
            add_guess_to_session('pizza')

            self.assertIn('pizza', session['found_words'])
            self.assertEqual(len(session['found_words']), 1)


    #end_game tests
    def test_end_first_game(self):
        '''testing route that updates session on game end'''
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['high_score'] = 0
                change_session['games_played'] = 0
            
            resp = client.get('/end-game?score=12')
            json = resp.get_data(as_text=True)

            self.assertEqual(200, resp.status_code)
            self.assertIn("games_played", json)

            self.assertEqual(session['high_score'], 12)
            self.assertEqual(session['games_played'], 1)

    def test_end_game_existing_user(self):
        '''testing route that updates session on game end'''
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['high_score'] = 45
                change_session['games_played'] = 90
            
            resp = client.get('/end-game?score=12')
            json = resp.get_data(as_text=True)

            self.assertEqual(200, resp.status_code)
            self.assertIn("games_played", json)
            
            self.assertEqual(session['high_score'], 45)
            self.assertEqual(session['games_played'], 91)