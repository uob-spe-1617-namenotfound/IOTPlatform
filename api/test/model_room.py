from api import repositories, model
import unittest
from bson import ObjectId


class RoomTests(unittest.TestCase):
    def __init__(self, testName):
        unittest.TestCase.__init__(self, testName)
        self.rooms = repositories.RoomRepository(RoomTests.collection)
        self.house1id = ObjectId()
        self.room1id = self.rooms.add_room(self.house1id, "Living Room")
        self.room2id = self.rooms.add_room(self.house1id, "Kitchen")
        self.room3id = self.rooms.add_room(self.house1id, "Bathroom")

    def test_RoomAddedCorrectly(self):
        room3 = self.rooms.get_room_by_id(self.room3id)
        house_id = room3.get_room_house()
        self.assertEqual(house_id, self.house1id, "Room house not added correctly.")
        name = room3.get_room_name()
        self.assertEqual(name, "Bathroom", "Room name not added correctly.")

    def test_GetRoomsForHouse(self):
        rooms = self.rooms.get_rooms_for_house(self.house1id)
        self.assertEqual(len(rooms), 3, "Incorrect amount of rooms.")
        name1 = rooms[0].get_room_name()
        name2 = rooms[1].get_room_name()
        name3 = rooms[2].get_room_name()
        self.assertEqual(name1, "Living Room", "First room has incorrect name.")
        self.assertEqual(name2, "Kitchen", "Second room has incorrect name.")
        self.assertEqual(name3, "Bathroom", "Third room has incorrect name.")

    def test_RoomRemovedCorrectly(self):
        all_rooms = self.rooms.get_all_rooms()
        self.rooms.remove_room(self.room3id)
        all_remaining_rooms = self.rooms.get_all_rooms()
        self.assertEqual(len(all_remaining_rooms), len(all_rooms) - 1, "Incorrect number of remaining rooms.")