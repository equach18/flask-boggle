from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    """Testing for app.py"""
    # TODO -- write tests for every view function / feature!
    def setUp(self):
        """Set up before each test"""
        app.config['TESTING']= True

    def test_homepage(self):
        """Checks that the server went through with the correct sessions and html displayed"""
        with app.test_client() as client:
           res = client.get('/')
           html = res.get_data(as_text=True)

           self.assertEqual(res.status_code, 200)
           self.assertIn('<h1>Boggle!</h1>', html)
           self.assertIn('board', session)
           self.assertIn('<p>Total Times Played: 0</p>', html)
           self.assertIn('<p>Highscore: 0</p>', html)
           self.assertIsNone(session.get('highscore'))
           self.assertIsNone(session.get('plays'))

    def test_invalid_word(self):
        """Tests if the word is not in the dictionary."""
        with app.test_client() as client:
            client.get('/')
            res = client.get('/check-word?word=dfgdfgfdd')
            self.assertEqual(res.json['result'], "not-word")

    def test_valid_word(self):
        """Tests if the word is valid."""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [['T', 'T', 'O', 'P', 'T'],
                                           ['T', 'T', 'O', 'T', 'T'],
                                           ['T', 'T', 'O', 'T', 'T'],
                                           ['T', 'T', 'O', 'T', 'T'],
                                           ['T', 'T', 'O', 'T', 'T']]
        
        res = client.get('/check-word?word=pot')
        self.assertEqual(res.status_code,200)
        self.assertEqual(res.json['result'], 'ok')
        
    def test_unfindable_word(self):
        """Tests if the word is in the dictionary, but not found on the board."""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [['T', 'T', 'O', 'P', 'T'],
                                           ['T', 'T', 'O', 'T', 'T'],
                                           ['T', 'T', 'O', 'T', 'T'],
                                           ['T', 'T', 'O', 'T', 'T'],
                                           ['T', 'T', 'O', 'T', 'T']]
        
            res = client.get('/check-word?word=abdominothoracic')
            self.assertEqual(res.status_code,200)
            self.assertEqual(res.json['result'], 'not-on-board')

    def test_highscore(self):
        """Tests if new high score has been recorded and data is accurate."""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['highscore'] = 10
                change_session['plays'] = 10

            res = client.post('/plays', json={'score': 11})
            data = res.get_json()

            self.assertEqual(res.status_code,200)
            self.assertEqual(data['plays'], 10)
            self.assertEqual(data['new_highscore'], True)

