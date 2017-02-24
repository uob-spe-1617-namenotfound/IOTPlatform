from api import repositories, model
import unittest
from bson import ObjectId


class HouseGroupTests(unittest.TestCase):
    def __init__(self, testName):
        unittest.TestCase.__init__(self, testName)
        self.houses = repositories.houseRepository(HouseGroupTests.collection)
        self.house_groups = repositories.houseGroupRepository(HouseGroupTests.collection)
        self.house1id = ObjectId()
        self.house1id = self.houses.add_house(self.house1id, "Benny's House")
        self.house2id = self.houses.add_house(self.house1id, "Student House")
        self.house3id = self.houses.add_house(self.house1id, "Third House")
        self.housegroup_id = self.house_groups.add_house_group(self.housegroup_id, "Redland Houses")

    def test_HouseGroupAddedCorrectly(self):
        house_group = self.house_groups.get_house_group_by_id(self.housegroup_id)
        name = house_group.get_house_group_name()
        self.assertEqual(name, "Redland Houses", "House Group name not added correctly.")

    def test_HousesAddedCorrectly(self):
        self.house_groups.add_house_to_group(self.house1id, self.housegroup_id)
        house_group = self.house_groups.get_house_group_by_id(self.housegroup_id)
        self.assertEqual(self.house1id, house_group['house_ids'])

    def test_HouseGroupRemovedCorrectly(self):
        all_house_groups = self.house_groups.get_all_house_groups()
        self.house_groups.remove_house_group(self.housegroup_id)
        all_remaining_house_groups = self.house_groups.get_all_house_groups()
        self.assertEqual(len(all_remaining_house_groups), len(all_house_groups) - 1,
                         "Incorrect number of remaining house groups.")

    def test_GetRoomsForHouse(self):
        houses = self.houses.get_houses_for_house(self.house1id)
        self.assertEqual(len(houses), 3, "Incorrect amount of rooms.")
        name1 = houses[0].get_house_name()
        name2 = houses[1].get_house_name()
        name3 = houses[2].get_house_name()
        self.assertEqual(name1, "Living Room", "First room has incorrect name.")
        self.assertEqual(name2, "Kitchen", "Second room has incorrect name.")
        self.assertEqual(name3, "Bathroom", "Third room has incorrect name.")