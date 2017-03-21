import repositories
import model
import main
import unittest


class MgmtTests(unittest.TestCase):
    def __init__(self, testName):
        unittest.TestCase.__init__(self, testName)
        self.users = repositories.UserRepository(MgmtTests.collection)
        self.user1id = self.users.add_user("Benny Clark", "password1", "benny@example.com", False)

    def test_CorrectLogin(self):
        user = self.users.get_user_by_id(self.user1id)
        data = main.login(user['email_address'], user['password'])
        self.assertEqual(data['success'], True, "Login was unsuccessful")
        self.assertEqual(data['error'], None)

    def test_UserRegisteredCorrectly(self):
        user = {'email_address': 'email@example.com', 'password': 'examplepw', 'name': 'Benny Clark', 'location':
            {'lat': 51.529249, 'lng': -0.117973, 'description': 'University of Bristol'}, 'is_admin': False}
        registry_data = main.register(user['email_address'], user['password'], user['name'], user['location'], user['location'])
        user_data = self.users.get_user_by_id(registry_data['user_id'])
        self.assertTrue(registry_data['success'], "Registry was unsuccessful")
        self.assertEqual(registry_data['error'], None)
        self.assertNotEqual(user_data['user_id'], None)
        self.assertEqual(user['email_address'], user_data['email_address'], 'User not registered correctly')
        self.assertEqual(registry_data['user_id'], user_data['user_id'])
