import repositories
import model
import unittest
from bson import ObjectId


class TriggerTests(unittest.TestCase):
    def setUp(self):
        self.triggers = repositories.TriggerRepository(TriggerTests.collection, TriggerTests.repositories)
        self.user1id = ObjectId()
        self.sensor1id = ObjectId()
        self.sensor2id = ObjectId()
        self.actor1id = ObjectId()
        self.actor2id = ObjectId()
        self.trigger1id = self.triggers.add_trigger(self.sensor1id, "motion_detected_start", None,
                                                    self.actor1id, "set_target_temperature", 20,
                                                    self.user1id)
        self.trigger2id = self.triggers.add_trigger(self.sensor2id, "temperature_gets_higher_than", 30,
                                                    self.actor2id, "set_light_switch", True,
                                                    self.user1id)
        self.trigger3id = self.triggers.add_trigger(self.sensor1id, "motion_detected_stop", None,
                                                    self.actor2id, "set_light_switch", False,
                                                    self.user1id)

    def tearDown(self):
        self.triggers.clear_db()

    def test_TriggerAddedCorrectly(self):
        trigger1 = self.triggers.get_trigger_by_id(self.trigger1id)
        attributes = trigger1.get_trigger_attributes()
        self.assertEqual(attributes['sensor_id'], self.sensor1id, "Trigger sensor was not added correctly.")
        self.assertEqual(attributes['event'], "motion_detected_start", "Trigger event type was not added correctly.")
        self.assertIsNone(attributes['event_params'], "Trigger event params were not added correctly.")
        self.assertEqual(attributes['actor_id'], self.actor1id, "Trigger actor was not added correctly.")
        self.assertEqual(attributes['action'], "set_target_temperature", "Trigger action type was not added correctly.")
        self.assertEqual(attributes['action_params'], 20, "Trigger action params were not added correctly.")
        self.assertEqual(attributes['user_id'], self.user1id, "Trigger user was not added correctly.")