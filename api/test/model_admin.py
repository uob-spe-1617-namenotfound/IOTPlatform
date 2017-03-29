import repositories
import model
import unittest
from bson import ObjectId


class AdminTests(unittest.TestCase):
    def setUp(self):
        self.devices = repositories.DeviceRepository(AdminTests.collection, AdminTests.repositories)
        self.house1id = ObjectId()
        self.adapter1id = self.devices.add_device(self.house1id, None, "Test Adapter", "light_switch", 1,
                                                {"username": 'bc15050@mybristol.ac.uk',
                                                 "password": 'test1234',
                                                 "device_id": '46865'}, 'energenie')

    def tearDown(self):
        self.devices.clear_db()

    def test_GettingEnergyReadingsAsList(self):
        consumption = self.devices.get_energy_consumption(self.adapter1id)
        self.assertIsInstance(consumption, list, "Not returning correct format for energy consumption")
        self.assertEqual(len(consumption), 7, "Size of consumption array is not correct")
