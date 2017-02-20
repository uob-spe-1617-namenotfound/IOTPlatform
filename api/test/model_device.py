from api import repositories, model
import unittest
from bson import ObjectId


class DeviceTests(unittest.TestCase):
    def __init__(self, testName):
        unittest.TestCase.__init__(self, testName)
        self.devices = repositories.DeviceRepository(DeviceTests.collection)
        self.house1id = ObjectId()
        self.room1id = ObjectId()
        self.device1id = self.devices.add_device(self.house1id, None, "Kitchen Thermostat", "thermostat", 1, None, "example")
        self.device2id = self.devices.add_device(self.house1id, None, "Kitchen Motion Sensor", "motion_sensor", 1, None, "example")
        self.device3id = self.devices.add_device(self.house1id, None, "Kitchen Light Switch", "light_switch", 1, None, "example")

    def test_DeviceAddedCorrectly(self):
        device3 = self.devices.get_device_by_id(self.device3id)
        house_id = device3.get_device_house()
        self.assertEqual(house_id, self.house1id, "Device house not added correctly.")
        room_id = device3.get_device_room()
        self.assertEqual(room_id, None, "Device room not added correctly.")
        name = device3.get_device_name()
        self.assertEqual(name, "Kitchen Light Switch", "Device name not added correctly.")
        device_type = device3.get_device_type()
        self.assertEqual(device_type, "light_switch", "Device type not added correctly.")
        power_state = device3.get_device_power_state()
        self.assertEqual(power_state, 1, "Device power state not added correctly.")
        configuration = device3.get_device_configuration()
        self.assertEqual(configuration, None, "Device configuration not added correctly.")
        vendor = device3.get_device_vendor()
        self.assertEqual(vendor, "example", "Device vendor not added correctly.")

    def test_DeviceAddedToRoom(self):
        self.devices.link_device_to_room(self.room1id, self.device1id)
        device1 = self.devices.get_device_by_id(self.device1id)
        room_id = device1.get_device_room()
        self.assertEqual(room_id, self.room1id, "Device 1 not added to room correctly.")
        self.devices.link_device_to_room(self.room1id, self.device2id)
        device2 = self.devices.get_device_by_id(self.device2id)
        room_id = device2.get_device_room()
        self.assertEqual(room_id, self.room1id, "Device 2 not added to room correctly.")
        self.devices.link_device_to_room(self.room1id, self.device3id)
        device3 = self.devices.get_device_by_id(self.device3id)
        room_id = device3.get_device_room()
        self.assertEqual(room_id, self.room1id, "Device 3 not added to room correctly.")