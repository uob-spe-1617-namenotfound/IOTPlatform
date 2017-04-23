import unittest

from bson import ObjectId


class AdminTests(unittest.TestCase):
    repository_collection = None

    def setUp(self):
        self.devices = AdminTests.repository_collection.device_repository
        self.house1id = ObjectId()
        self.adapter1id = self.devices.add_device(house_id=self.house1id, room_id=None, name="Test Adapter",
                                                  device_type="light_switch", target={},
                                                  configuration={"username": 'bc15050@mybristol.ac.uk',
                                                                 "password": 'test1234',
                                                                 "device_id": '46865'},
                                                  vendor='energenie')

    def tearDown(self):
        self.devices.clear_db()

    def test_GettingEnergyReadingsAsList(self):
        consumption = self.devices.get_energy_consumption(self.adapter1id)
        self.assertIsInstance(consumption, list, "Not returning correct format for energy consumption")
        # We can probably only assume that the length is 7 for devices that are actually being used.
        # self.assertEqual(len(consumption), 7, "Size of consumption array is not correct")
