from data_model import model
import unittest


class UserTests(unittest.TestCase):
    user_repository = model.UserRepository()
    user1 = model.User("user_id_1", "Benny Clark", "xxxxxxxx", "benny1152@gmail.com", False)
    user2 = model.User("user_id_2", "Floris Kint", "xxxxxxxx", "nobody@gmail.com", True)

    def testIs_AdminIsABool(self):
        admin = UserTests.user1.is_admin
        self.assertEqual(admin, False)
        admin = UserTests.user2.is_admin
        self.assertEqual(admin, True)

    def testAddToRepoIsCorrect(self):
        user = UserTests.user1
        repo = UserTests.user_repository
        self.assertEqual(repo.users, {})
        repo.add_user(user)
        users_dict = {'user_id_1': {'is_admin': False, 'user_id': 'user_id_1', 'password_hash': 'xxxxxxxx',
                                    'email_address': 'benny1152@gmail.com', 'name': 'Benny Clark'}}
        self.assertEqual(repo.users, users_dict)

    def testRemoveFromRepoIsCorrect(self):
        user = UserTests.user1
        repo = UserTests.user_repository
        repo.add_user(user)
        repo.remove_user(user.user_id)
        self.assertEqual(repo.users, {})

    def getUserIsCorrect(self):
        first_user = UserTests.user1
        second_user = UserTests.user2
        repo = UserTests.user_repository
        repo.add_user(first_user)
        repo.add_user(second_user)
        x = repo.get_user_by_id(second_user.user_id)
        self.assertEqual(x, second_user.user_id)


class HouseTests(unittest.TestCase):

    house1 = model.House("user_id", "1", "Benny's Home")

    def testGetAttributesIsCorrect(self):
        house = HouseTests.house1
        attributes = {'name': "Benny's Home", 'house_id': '1', 'user_id': 'user_id'}
        self.assertEquals(model.House.get_house_attributes(house), attributes)

def main():
    unittest.main()


if __name__ == '__main__':
    main()
