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

    def test_GetDevicesForHouse(self):
        devices = self.devices.get_devices_for_house(self.house1id)
        self.assertEqual(len(devices), 3, "Incorrect amount of devices.")
        name1 = devices[0].get_device_name()
        name2 = devices[1].get_device_name()
        name3 = devices[2].get_device_name()
        self.assertEqual(name1, "Kitchen Thermostat", "First device has incorrect name.")
        self.assertEqual(name2, "Kitchen Motion Sensor", "First device has incorrect name.")
        self.assertEqual(name3, "Kitchen Light Switch", "First device has incorrect name.")

    def test_GetDevicesForRoom(self):
        self.devices.link_device_to_room(self.room1id, self.device1id)
        self.devices.link_device_to_room(self.room1id, self.device2id)
        self.devices.link_device_to_room(self.room1id, self.device3id)
        devices = self.devices.get_devices_for_room(self.room1id)
        self.assertEqual(len(devices), 3, "Incorrect amount of devices.")
        name1 = devices[0].get_device_name()
        name2 = devices[1].get_device_name()
        name3 = devices[2].get_device_name()
        self.assertEqual(name1, "Kitchen Thermostat", "First device has incorrect name.")
        self.assertEqual(name2, "Kitchen Motion Sensor", "First device has incorrect name.")
        self.assertEqual(name3, "Kitchen Light Switch", "First device has incorrect name.")

    def test_SetPowerState(self):
        self.devices.set_power_state(self.device3id, 0)
        device3 = self.devices.get_device_by_id(self.device3id)
        power_state = device3.get_device_power_state()
        self.assertEqual(power_state, 0, "Device power state not configured correctly.")

    def test_DeviceRemovedCorrectly(self):
        all_devices = self.devices.get_all_devices()
        self.devices.remove_device(self.device3id)
        all_remaining_devices = self.devices.get_all_devices()
        self.assertEqual(len(all_remaining_devices), len(all_devices) - 1, "Incorrect number of remaining devices.")