from api import repositories, model
import unittest


class RoomTests(unittest.TestCase):
    def __init__(self, testName):
        unittest.TestCase.__init__(self, testName)
        self.rooms = repositories.RoomRepository(RoomTests.collection)
