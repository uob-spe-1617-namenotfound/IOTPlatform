from api import repositories, model
import unittest
from bson import ObjectId


class HouseTests(unittest.TestCase):
    def __init__(self, testName):
        unittest.TestCase.__init__(self, testName)
        self.houses = repositories.HouseRepository(HouseTests.collection)
        self.user1id = ObjectId()
        self.user2id = ObjectId()
        self.house1id = self.houses.add_house(self.user1id, "Benny's House")
        self.house2id = self.houses.add_house(self.user2id, "Floris' House")
        self.house3id = self.houses.add_house(self.user2id, "Floris' Other House")

    def test_HouseAddedCorrectly(self):
        house3 = self.houses.get_house_by_id(self.house3id)
        user_id = house3.get_house_user()
        self.assertEqual(user_id, self.user2id, "House user not added correctly.")
        name = house3.get_house_name()
        self.assertEqual(name, "Floris' Other House", "House name not added correctly.")

    def test_GetHousesForUser(self):
        houses = self.houses.get_houses_for_user(self.user2id)
        self.assertEqual(len(houses), 2, "Incorrect amount of houses.")
        name1 = houses[0].get_house_name()
        name2 = houses[1].get_house_name()
        self.assertEqual(name1, "Floris' House", "First house has incorrect name.")
        self.assertEqual(name2, "Floris' Other House", "Second house has incorrect name.")

    def test_HouseRemovedCorrectly(self):
        all_houses = self.houses.get_all_houses()
        self.houses.remove_house(self.house3id)
        all_remaining_houses = self.houses.get_all_houses()
        self.assertEqual(len(all_remaining_houses), len(all_houses) - 1, "Incorrect number of remaining houses.")
