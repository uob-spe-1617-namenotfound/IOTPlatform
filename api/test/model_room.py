import unittest

from bson import ObjectId


class RoomTests(unittest.TestCase):
    repository_collection = None

    def setUp(self):
        self.rooms = RoomTests.repository_collection.room_repository
        self.houses = RoomTests.repository_collection.house_repository
        self.users = RoomTests.repository_collection.user_repository
        self.user1id = self.users.add_user("Benny Clark", "xxxxxxxx", "benny@example.com", False)
        self.house1id = self.houses.add_house(self.user1id, "Benny's House", None)
        self.room1id = self.rooms.add_room(self.house1id, "Living Room")
        self.room2id = self.rooms.add_room(self.house1id, "Kitchen")
        self.room3id = self.rooms.add_room(self.house1id, "Bathroom")

    def tearDown(self):
        self.rooms.clear_db()
        self.houses.clear_db()
        self.users.clear_db()

    def test_RoomAddedCorrectly(self):
        room3 = self.rooms.get_room_by_id(self.room3id)
        attributes = room3.get_room_attributes()
        self.assertEqual(attributes['house_id'], self.house1id, "Room house not added correctly.")
        self.assertEqual(attributes['name'], "Bathroom", "Room name not added correctly.")

    def test_GetRoomsForHouse(self):
        rooms = self.rooms.get_rooms_for_house(self.house1id)
        self.assertEqual(len(rooms), 3, "Incorrect amount of rooms.")
        room1attr = rooms[0].get_room_attributes()
        room2attr = rooms[1].get_room_attributes()
        room3attr = rooms[2].get_room_attributes()
        self.assertEqual(room1attr['name'], "Living Room", "First room has incorrect name.")
        self.assertEqual(room2attr['name'], "Kitchen", "Second room has incorrect name.")
        self.assertEqual(room3attr['name'], "Bathroom", "Third room has incorrect name.")

    def test_GetAllRooms(self):
        all_rooms = self.rooms.get_all_rooms()
        self.assertEqual(len(all_rooms), 3, "Incorrect number of rooms.")

    def test_RoomRemovedCorrectly(self):
        all_rooms = self.rooms.get_all_rooms()
        self.rooms.remove_room(self.room3id)
        all_remaining_rooms = self.rooms.get_all_rooms()
        self.assertEqual(len(all_remaining_rooms), 2, "Incorrect number of remaining rooms.")

    def test_RoomsCannotHaveSameName(self):
        with self.assertRaisesRegex(Exception, "There is already a room with this name."):
            self.rooms.add_room(self.house1id, "Living Room")
