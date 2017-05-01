import unittest


class ThemeTests(unittest.TestCase):
    repository_collection = None

    def setUp(self):
        self.themes = ThemeTests.repository_collection.theme_repository
        self.devices = ThemeTests.repository_collection.device_repository
        self.houses = ThemeTests.repository_collection.house_repository
        self.users = ThemeTests.repository_collection.user_repository
        self.themes.clear_db()
        self.devices.clear_db()
        self.houses.clear_db()
        self.users.clear_db()

        self.user1id = self.users.add_user("Benny Clark", "xxxxxxxx", "benny@example.com", False)
        self.house1id = self.houses.add_house(self.user1id, "Benny's House", None)
        self.device1id = self.devices.add_device(
            house_id=self.house1id,
            room_id=None,
            name="Kitchen Thermostat",
            device_type="thermostat",
            target={'target_temperature': 20},
            configuration={"url": "http://dummy-sensor:5000/thermostat/1"},
            vendor="OWN")
        self.device2id = self.devices.add_device(house_id=self.house1id,
                                                 room_id=None, name="Kitchen Light Switch",
                                                 device_type="light_switch",
                                                 target={},
                                                 configuration={"url": "http://dummy-sensor:5000/light_switch/1"},
                                                 vendor="OWN")
        self.device3id = self.devices.add_device(house_id=self.house1id,
                                                 room_id=None,
                                                 name="Lounge Light Switch",
                                                 device_type="light_switch",
                                                 target={},
                                                 configuration={"url": "http://dummy-sensor:5000/light_switch/2"},
                                                 vendor="OWN")
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
        pass

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
        self.assertEqual(device.target['power_state'], 1, "Theme state did not change correctly")

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
        self.assertEqual(device.target['power_state'], 0, "Initial device power state is incorrect")
        updated_theme = self.themes.change_theme_state(self.theme3id, True)
        device = self.devices.get_device_by_id(updated_theme.settings[0]['device_id'])
        self.assertEqual(device.target['power_state'], 1, "Theme did not apply settings correctly")
        self.devices.set_power_state(self.device3id, 0)
        device = self.devices.get_device_by_id(updated_theme.settings[0]['device_id'])
        self.assertEqual(device.target['power_state'], 1, "Theme did not lock correctly")
