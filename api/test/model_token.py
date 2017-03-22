import repositories
import model
import unittest
from bson import ObjectId

class TokenTests(unittest.TestCase):
    def setUp(self):
        self.tokens = repositories.TokenRepository(TokenTests.collection, TokenTests.repositories)
        self.user1id = ObjectId()
        self.token1 = self.collection.generate_token(self.user1id)

    def tearDown(self):
        self.tokens.clear_db()

    def test_TokenAddedCorrectly(self):
        token = self.collection.find_one({'token': self.token1})
        self.assertEqual(token['user_id'], self.user1id, "Token user was not added correctly.")