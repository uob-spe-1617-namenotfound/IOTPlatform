import unittest

from bson import ObjectId

import repositories


class HouseTests(unittest.TestCase):
    repository_collection = None

    def setUp(self):
        self.houses = HouseTests.repository_collection.house_repository
        self.user1id = ObjectId()
        self.user2id = ObjectId()
        self.house1id = self.houses.add_house(self.user1id, "Benny's House", None)
        self.house2id = self.houses.add_house(self.user2id, "Floris' House", None)
        self.house3id = self.houses.add_house(self.user2id, "Floris' Other House", None)

    def tearDown(self):
        self.houses.clear_db()

    def test_HouseAddedCorrectly(self):
        house3 = self.houses.get_house_by_id(self.house3id)
        attributes = house3.get_house_attributes()
        self.assertEqual(attributes['user_id'], self.user2id, "House user not added correctly.")
        self.assertEqual(attributes['name'], "Floris' Other House", "House name not added correctly.")

    def test_GetHousesForUser(self):
        houses = self.houses.get_houses_for_user(self.user2id)
        self.assertEqual(len(houses), 2, "Incorrect amount of houses.")
        house1attr = houses[0].get_house_attributes()
        house2attr = houses[1].get_house_attributes()
        self.assertEqual(house1attr['name'], "Floris' House", "First house has incorrect name.")
        self.assertEqual(house2attr['name'], "Floris' Other House", "Second house has incorrect name.")

    def test_GetAllHouses(self):
        all_houses = self.houses.get_all_houses()
        self.assertEqual(len(all_houses), 3, "Incorrect number of houses.")

    def test_HouseRemovedCorrectly(self):
        all_houses = self.houses.get_all_houses()
        self.houses.remove_house(self.house3id)
        all_remaining_houses = self.houses.get_all_houses()
        self.assertEqual(len(all_remaining_houses), 2, "Incorrect number of remaining houses.")

    def test_HousesCannotHaveSameName(self):
        with self.assertRaisesRegex(Exception, "There is already a house with this name."):
            self.houses.add_house(self.user1id, "Benny's House", None)
