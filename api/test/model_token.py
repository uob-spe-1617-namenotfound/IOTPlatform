import unittest

from bson import ObjectId


class TokenTests(unittest.TestCase):
    repository_collection = None

    def setUp(self):
        self.tokens = TokenTests.repository_collection.token_repository
        self.users = TokenTests.repository_collection.user_repository
        self.tokens.clear_db()
        self.users.clear_db()

        self.user1id = self.users.add_user("Benny Clark", "xxxxxxxx", "benny@example.com", False)
        self.user2id = self.users.add_user("Floris Kint", "xxxxxxxx", "floris@example.com", True)
        self.user3id = self.users.add_user("Ben Fossett", "xxxxxxxx", "ben@example.com", True)
        self.token1 = self.tokens.generate_token(self.user1id)
        self.token2 = self.tokens.generate_token(self.user2id)
        self.token3 = self.tokens.generate_token(self.user3id)

    def tearDown(self):
        pass

    def test_TokenAddedCorrectly(self):
        token = self.tokens.find_by_token(self.token1)
        self.assertEqual(token['user_id'], self.user1id, "Token user was not added correctly.")

    def test_TokenRemovedCorrectly(self):
        self.tokens.invalidate_token(self.token3)
        all_remaining_tokens = self.tokens.get_all_tokens()
        self.assertEqual(len(all_remaining_tokens), 2, "A token was not removed.")

    def test_TokensAreUnique(self):
        unique = self.tokens.check_token_is_new(self.token1)
        self.assertFalse(unique, "The existing token was not recognised.")
