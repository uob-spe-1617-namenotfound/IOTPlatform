import unittest


class UserTests(unittest.TestCase):
    repository_collection = None

    def setUp(self):
        self.users = UserTests.repository_collection.user_repository
        self.user1id = self.users.add_user("Benny Clark", "xxxxxxxx", "benny@example.com", False)
        self.user2id = self.users.add_user("Floris Kint", "xxxxxxxx", "floris@example.com", True)
        self.user3id = self.users.add_user("Ben Fossett", "xxxxxxxx", "ben@example.com", True)

    def tearDown(self):
        self.users.clear_db()

    def test_UserAddedCorrectly(self):
        user3 = self.users.get_user_by_id(self.user3id)
        attributes = user3.get_user_attributes()
        self.assertEqual(user3.name, "Ben Fossett", "User name not added correctly.")
        self.assertEqual(user3.password_hash, "xxxxxxxx", "User password not added correctly.")
        self.assertEqual(user3.email_address, "ben@example.com", "User email not added correctly.")
        self.assertTrue(user3.is_admin, "User admin status not added correctly.")

    def test_GetAllUsers(self):
        all_users = self.users.get_all_users()
        self.assertEqual(len(all_users), 3, "Incorrect number of users.")

    def test_UserRemovedCorrectly(self):
        all_users = self.users.get_all_users()
        self.users.remove_user(self.user3id)
        all_remaining_users = self.users.get_all_users()
        self.assertEqual(len(all_remaining_users), 2, "A user has not been removed.")

    def test_UsersCannotHaveSameEmail(self):
        with self.assertRaisesRegex(Exception, "There is already an account with this email."):
            self.users.add_user("Benny Smith", "xxxxxxxx", "benny@example.com", False)

    def test_GetAttributesIncludingPassword(self):
        user3 = self.users.get_user_by_id(self.user3id)
        attributes = user3.get_user_attributes(1)
        password_hash = attributes['password_hash']
        self.assertEqual(password_hash, "xxxxxxxx", "get attributes not correctly including pw hash")
