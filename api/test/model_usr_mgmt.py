import unittest

import main
import bcrypt

class MgmtTests(unittest.TestCase):
    repository_collection = None

    def setUp(self):
        self.users = MgmtTests.repository_collection.user_repository
        self.user1id = self.users.add_user("Benny Clark", bcrypt.hashpw("password1".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), "benny@example.com", False)

    def tearDown(self):
        self.users.clear_db()

    def test_CorrectLogin(self):
        user = self.users.get_user_by_id(self.user1id)
        data = self.users.check_password(user.email_address, "password1")
        self.assertEqual(data.user_id, self.user1id, "Login was unsuccessful")

    def test_UserRegisteredCorrectly(self):
        user = {'email_address': 'email@example.com', 'password': 'examplepw', 'name': 'Benny Clark', 'location':
            {'lat': 51.529249, 'lng': -0.117973, 'description': 'University of Bristol'}, 'is_admin': False}
        registered_user_id = self.users.register_new_user(user['email_address'], user['password'], user['name'], user['is_admin'])
        user_data = self.users.get_user_by_id(registered_user_id)
        self.assertNotEqual(user_data.user_id, None)
        self.assertEqual(user_data.email_address, user_data.email_address, 'User not registered correctly')
        self.assertEqual(user_data.user_id, registered_user_id)
