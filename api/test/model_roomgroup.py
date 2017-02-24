from api import repositories, model
import unittest
from bson import ObjectId


class RoomGroupTests(unittest.TestCase):
    def __init__(self, testName):
        unittest.TestCase.__init__(self, testName)
        self.rooms = repositories.RoomRepository(RoomGroupTests.collection)
        self.room_groups = repositories.RoomGroupRepository(RoomGroupTests.collection)
        self.house1id = ObjectId()
        self.room1id = self.rooms.add_room(self.house1id, "Living Room")
        self.room2id = self.rooms.add_room(self.house1id, "Kitchen")
        self.room3id = self.rooms.add_room(self.house1id, "Bathroom")
        self.roomgroup_id = self.room_groups.add_room_group(self.roomgroup_id, "Upstairs")

    def test_RoomGroupAddedCorrectly(self):
        room_group = self.room_groups.get_room_group_by_id(self.roomgroup_id)
        name = room_group.get_room_group_name()
        self.assertEqual(name, "Upstairs", "Room Group name not added correctly.")

    def test_GetRoomsForHouse(self):
        rooms = self.rooms.get_rooms_for_house(self.house1id)
        self.assertEqual(len(rooms), 3, "Incorrect amount of rooms.")
        name1 = rooms[0].get_room_name()
        name2 = rooms[1].get_room_name()
        name3 = rooms[2].get_room_name()
        self.assertEqual(name1, "Living Room", "First room has incorrect name.")
        self.assertEqual(name2, "Kitchen", "Second room has incorrect name.")
        self.assertEqual(name3, "Bathroom", "Third room has incorrect name.")

    def test_RoomsAddedCorrectly(self):
        self.room_groups.add_room_to_group(self.room1id, self.roomgroup_id)
        room_group = self.room_groups.get_room_group_by_id(self.roomgroup_id)
        self.assertEqual(self.room1id, room_group['room_ids'])

    def test_RoomGroupRemovedCorrectly(self):
        all_room_groups = self.room_groups.get_all_room_groups()
        self.room_groups.remove_room_group(self.roomgroup_id)
        all_remaining_room_groups = self.room_groups.get_all_room_groups()
        self.assertEqual(len(all_remaining_room_groups), len(all_room_groups) - 1,
                         "Incorrect number of remaining room groups.")