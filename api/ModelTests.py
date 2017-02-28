from api import model
import unittest


class UserTests(unittest.TestCase):
    user_repository = model.UserRepository()
    user1 = model.User("Benny Clark", "xxxxxxxx", "benny1152@gmail.com", False)
    user2 = model.User("Floris Kint", "xxxxxxxx", "nobody@gmail.com", True)

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
    house1 = model.House("Benny's Home")
    house2 = model.House("Example Home")
    house3 = model.House("John's Home")

    house_repository = model.HouseRepository()
    user1 = model.User("user_id_1", "Benny Clark", "xxxxxxxx", "benny1152@gmail.com", False)
    user2 = model.User("user_id_2", "Floris Kint", "xxxxxxxx", "nobody@gmail.com", True)


    def testGetAttributesIsCorrect(self):
        house = HouseTests.house1
        attributes = {'name': "Benny's Home", 'house_id': '1', 'user_id': 'user_id_1'}
        self.assertEquals(model.House.get_house_attributes(house), attributes)

    def testAddHouseToUser(self):
        house = HouseTests.house2
        user = HouseTests.user2
        repo = HouseTests.house_repository
        self.assertEquals(house.user_id, 'user_id_2')
        repo.add_house_to_user(user, house)
        self.assertEquals(house.user_id, user.user_id)

    # def testGetHousesForUser(self):
    #     first_house = HouseTests.house1
    #     second_house = HouseTests.house2
    #     third_house = HouseTests.house3
    #
    #     repo = HouseTests.house_repository
    #     repo.add_house(first_house)
    #     repo.add_house(second_house)
    #     repo.add_house(third_house)
    #     lst = repo.get_houses_for_user("user_id_1")
    #     self.assertEquals(lst, repo.houses)


class DeviceTests(unittest.TestCase):
    device_repository = model.DeviceRepository()
    device1 = model.Device("1", "room_id", "device_id", "Benny's Thermostat", "thermostat", 1, 24.7, 25.0, "no sensor")

    def testChangePowerState(self):
        device = DeviceTests.device1
        model.Device.change_power_state(device)
        self.assertEquals(device.power_state, 0)

    def testSetTargetTemp(self):
        device = DeviceTests.device1
        model.Device.set_target_temp(device, 30.0)
        self.assertEquals(device.target_temp, 30.0)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
