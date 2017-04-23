import unittest

from bson import ObjectId


class ThemeTests(unittest.TestCase):
    repository_collection = None

    def setUp(self):
        self.themes = ThemeTests.repository_collection.theme_repository
        self.devices = ThemeTests.repository_collection.device_repository
        self.user1id = ObjectId()
        self.house1id = ObjectId()
        self.device1id = self.devices.add_device(self.house1id, None, "Kitchen Thermostat", "thermostat",
                                                 {'target_temperature': 20}, None, "example")
        self.device2id = self.devices.add_device(self.house1id, None, "Kitchen Light Switch", "light_switch", {}, None, "example")
        self.device3id = self.devices.add_device(self.house1id, None, "Lounge Light Switch", "light_switch", {}, None, "example")
        self.theme1id = self.themes.add_theme(self.user1id, "Test Thermostat",
                                              [{'device_id': self.device1id, 'setting': {'target_temperature': 30}}],
                                              False)
        self.theme2id = self.themes.add_theme(self.user1id, "light_switches",
                                              [{'device_id': self.device2id, 'setting': {'power_state': 0}},
                                               {'device_id': self.device3id, 'setting': {'power_state': 1}}],
                                              False)
        self.theme3id = self.themes.add_theme(self.user1id, "Switch Test",
                                              [{'device_id': self.device3id, 'setting': {'power_state': 1}}],
                                              False)

    def tearDown(self):
        self.themes.clear_db()

    def test_ThemeAddedCorrectly(self):
        theme = self.themes.get_theme_by_id(self.theme1id)
        self.assertEqual(theme.name, 'Test Thermostat', 'name not added correctly')
        self.assertEqual(theme.settings[0]['setting'], {'target_temperature': 30}, 'Setting not added correctly')
        self.assertEqual(theme.active, False, 'Active state not added correctly')

    def test_ChangeThemeState(self):
        updated_theme = self.themes.change_theme_state(self.theme3id, True)
        settings = updated_theme.settings
        device_id = settings[0]['device_id']
        device = self.devices.get_device_by_id(device_id)
        self.assertEqual(updated_theme.active, True, "Active state did not change correctly")
        self.assertEqual(device.status['power_state'], 1, "Theme state did not change correctly")

    def test_RemoveDeviceFromTheme(self):
        theme = self.themes.get_theme_by_id(self.theme2id)
        device_id = theme.settings[0]['device_id']
        self.themes.remove_device_from_theme(self.theme2id, device_id)
        updated_settings = self.themes.get_theme_by_id(self.theme2id).settings
        self.assertEqual(len(updated_settings), 1, "Device not correctly removed from theme")

    def test_ThemeRemovedCorrectly(self):
        self.themes.remove_theme(self.theme3id)
        all_remaining_themes = self.themes.get_all_themes()
        self.assertEqual(len(all_remaining_themes), 2, "A theme was not removed correctly.")

    def test_ThemesLockCorrectly(self):
        theme = self.themes.get_theme_by_id(self.theme3id)
        device = self.devices.get_device_by_id(theme.settings[0]['device_id'])
        self.assertEqual(device.status['power_state'], 0, "Initial device power state is incorrect")
        updated_theme = self.themes.change_theme_state(self.theme3id, True)
        device = self.devices.get_device_by_id(updated_theme.settings[0]['device_id'])
        self.assertEqual(device.status['power_state'], 1, "Theme did not apply settings correctly")
        self.devices.set_power_state(self.device3id, 0)
        device = self.devices.get_device_by_id(updated_theme.settings[0]['device_id'])
        self.assertEqual(device.status['power_state'], 1, "Theme did not lock correctly")
