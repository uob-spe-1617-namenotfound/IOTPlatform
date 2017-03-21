import repositories
import model
import unittest

class TokenTests(unittest.TestCase):
    def setUp(self):
        self.tokens = repositories.TokenRepository(TokenTests.collection, TokenTests.repositories)

    def tearDown(self):
        self.tokens.clear_db()