import logging
import time

import requests


def get_optional_attribute(attributes, key):
    return attributes[key] if key in attributes else None


class User(object):
    def __init__(self, user_id, name, password_hash, email_address, is_admin):
        self.user_id = user_id
        self.name = name
        self.password_hash = password_hash
        self.email_address = email_address
        self.is_admin = is_admin

    def get_user_attributes(self):
        return {'user_id': self.user_id, 'name': self.name, 'password_hash': self.password_hash,
                'email_address': self.email_address, 'is_admin': self.is_admin}

    def get_user_id(self):
        return self.user_id


class House(object):
    def __init__(self, house_id, user_id, name):
        self.house_id = house_id
        self.user_id = user_id
        self.name = name

    def get_house_attributes(self):
        return {'house_id': self.house_id, 'user_id': self.user_id, 'name': self.name}

    @classmethod
    def from_dict(cls, d):
        h = House(user_id=d['user_id'] if 'user_id' in d else None,
                  house_id=d['_id'] if '_id' in d else None,
                  name=d['name'] if 'name' in d else "")
        return h


# House groups could be used for fleet management or for people with multiple houses
class HouseGroup(object):
    def __init__(self, house_group_id, house_ids, name):
        self.house_group_id = house_group_id
        self.house_ids = house_ids
        self.name = name

    def get_house_group_attributes(self):
        return {'house_group_id': self.house_group_id, 'house_ids': self.house_ids, 'name': self.name}


class Room(object):
    def __init__(self, room_id, house_id, name):
        self.room_id = room_id
        self.house_id = house_id
        self.name = name

    def get_room_attributes(self):
        return {'room_id': self.room_id, 'house_id': self.house_id, 'name': self.name}


# Room groups could be things like 'Upstairs', or to be used for templates
class RoomGroup(object):
    def __init__(self, room_group_id, room_ids, name):
        self.room_group_id = room_group_id
        self.room_ids = room_ids
        self.name = name

    def get_room_group_attributes(self):
        return {'room_group_id': self.room_group_id, 'room_ids': self.room_ids, 'name': self.name}


class Device(object):
    def __init__(self, attributes):
        self.device_id = None
        self.house_id = None
        self.room_id = None
        self.name = None
        self.device_type = None
        self.power_state = None
        self.last_read = None
        self.vendor = None
        self.configuration = None
        self.set_attributes(attributes)

    def set_attributes(self, attributes):
        self.device_id = attributes['_id']
        self.house_id = attributes['house_id']
        self.room_id = attributes['room_id']
        self.name = attributes['name']
        self.device_type = attributes['device_type']
        self.power_state = attributes['power_state']
        self.last_read = attributes['last_read']
        self.vendor = attributes['vendor'] if "vendor" in attributes else None
        self.configuration = attributes['configuration'] if "configuration" in attributes else None

    def get_device_attributes(self):
        return {'_id': str(self.device_id), 'device_id': str(self.device_id), 'house_id': self.house_id,
                'room_id': self.room_id, 'name': self.name,
                'device_type': self.device_type, 'power_state': self.power_state,
                'last_read': self.last_read, 'vendor': self.vendor, 'configuration': self.configuration}

    def get_device_id(self):
        return self.device_id

    def get_device_type(self):
        return self.device_type

    def read_current_state(self):

        error = None
        data = None
        timestamp = str(time.time())
        if self.vendor == "OWN":
            if "url" in self.configuration:
                url = self.configuration['url']
                try:
                    r = requests.get(url)
                    r_data = r.json()
                    if "error" in r_data and r_data["error"] is not None:
                        error = r_data["error"]
                    else:
                        data = r_data['data']
                except Exception as ex:
                    error = "Cannot read data from configuration URL: {}".format(ex)
            else:
                error = "Can't read current state as no url is set in configuration"
        elif self.vendor == "energenie":
            if "username" in self.configuration and "password" in self.configuration and "device_id" in self.configuration:
                try:
                    username = self.configuration['username']
                    password = self.configuration['password']
                    dev_id = int(self.configuration['device_id'])
                    logging.debug(
                        "Retrieving mihome4u data. Auth = {}, json = {}".format((username, password), {"id": dev_id}))
                    r = requests.get("https://mihome4u.co.uk/api/v1/subdevices/show", auth=(username, password),
                                     json={"id": dev_id})
                    r_data = r.json()
                    logging.debug("Got: {}".format(r_data))
                    if r_data["status"] != "success":
                        error = "External error: {}".format(r_data['status'])
                    else:
                        data = {'power_state': r_data['data']['power_state'], 'voltage': r_data['data']['voltage']}
                except Exception as ex:
                    error = "Cannot read device data from URL: {}".format(ex)
            else:
                error = "Not all required information is set in the configuration"
            logging.debug("Read current data for the device: {}".format(data))
        else:
            error = "read_current_state not implemented for vendor {}".format(self.vendor)
        if error is not None:
            return {"error": error, "timestamp": timestamp}
        return {"data": data, "timestamp": timestamp}

    def is_faulty(self):
        if "error" in self.last_read and self.last_read['error'] is not None:
            return True
        return False


class Thermostat(Device):
    def __init__(self, attributes):
        self.last_temperature = None
        self.target_temperature = None
        self.locked_max_temp = None
        self.locked_min_temp = None
        self.temperature_scale = None
        Device.__init__(self, attributes)

    def set_attributes(self, attributes):
        attributes['device_type'] = "thermostat"
        Device.set_attributes(self, attributes=attributes)
        self.last_temperature = get_optional_attribute(attributes, 'last_temperature')
        self.target_temperature = get_optional_attribute(attributes, 'target_temperature')
        self.locked_max_temp = get_optional_attribute(attributes, 'locked_max_temperature')
        self.locked_min_temp = get_optional_attribute(attributes, 'locked_min_temperature')
        self.temperature_scale = get_optional_attribute(attributes, 'temperature_scale')

    def get_device_attributes(self):
        attributes = Device.get_device_attributes(self)
        attributes.update({
            'last_temperature': self.last_temperature, 'target_temperature': self.target_temperature,
            'locked_max_temp': self.locked_max_temp, 'locked_min_temp': self.locked_min_temp,
            'temperature_scale': self.temperature_scale
        })
        return attributes

    def configure_target_temperature(self, temperature):
        error = None
        if self.vendor == "OWN":
            if "url" in self.configuration:
                url = self.configuration['url'] + "/write"
                try:
                    r = requests.post(url, json={"target_temperature": temperature})
                    r_data = r.json()
                    if "error" in r_data and r_data["error"] is not None:
                        error = r_data["error"]
                except Exception as ex:
                    error = "Cannot configure target temperature from configuration URL: {}".format(ex)
            else:
                error = "Can't configure target temperature as no url is set in configuration"
        else:
            error = "configure_target_temperature not implemented for vendor {}".format(self.vendor)
        return error


class MotionSensor(Device):
    def __init__(self, attributes):
        self.sensor_data = None
        Device.__init__(self, attributes)

    def set_attributes(self, attributes):
        Device.set_attributes(self, attributes=attributes)
        self.sensor_data = get_optional_attribute(attributes, 'sensor_data')

    def get_device_attributes(self):
        attributes = Device.get_device_attributes(self)
        attributes.update({'sensor_data': self.sensor_data})
        return attributes


class LightSwitch(Device):
    def __init__(self, attributes):
        Device.__init__(self, attributes)

    def get_device_attributes(self):
        return Device.get_device_attributes(self)

    def configure_power_state(self, power_state):
        error = None
        if self.vendor == "energenie":
            if "username" in self.configuration and "password" in self.configuration and "device_id" in self.configuration:
                try:
                    username = self.configuration['username']
                    password = self.configuration['password']
                    dev_id = int(self.configuration['device_id'])
                    logging.debug(
                        "Setting power state mihome4u data. Auth = {}, json = {}".format((username, password),
                                                                                         {"id": dev_id}))
                    r = requests.get(
                        "https://mihome4u.co.uk/api/v1/subdevices/power_{}".format("on" if power_state == 1 else "off"),
                        auth=(username, password),
                        json={"id": dev_id})
                    r_data = r.json()
                    logging.debug("Got: {}".format(r_data))
                    if r_data["status"] != "success":
                        error = "External error: {}".format(r_data['status'])
                except Exception as ex:
                    error = "Cannot configure power state: {}".format(ex)
            else:
                error = "Not all required information is set in the configuration"
        else:
            error = "configure_power_state not implemented for vendor {}".format(self.vendor)
        return error


class OpenSensor(Device):
    def __init__(self, attributes):
        self.sensor_data = None
        Device.__init__(self, attributes)

    def set_attributes(self, attributes):
        Device.set_attributes(self, attributes=attributes)
        self.sensor_data = attributes["sensor_data"]

    def get_device_attributes(self):
        attributes = Device.get_device_attributes(self)
        attributes.update({'sensor_data': self.sensor_data})
        return attributes


class DeviceGroup(object):
    def __init__(self, device_group_id, device_ids, name):
        self.device_group_id = device_group_id
        self.device_ids = device_ids
        self.name = name

    def get_device_group_attributes(self):
        return {'device_group_id': self.device_group_id, 'device_ids': self.device_ids, 'name': self.name}


class Trigger:
    def __init__(self, trigger, action):
        self.trigger_id = None
        self.trigger_sensor_id = None
        self.trigger = trigger
        self.actor_id = None
        self.action = action

    def get_trigger_attributes(self):
        return {'trigger_id': self.trigger_id, 'trigger_sensor_id': self.trigger_sensor_id,
                'trigger': self.trigger, 'actor_id': self.actor_id, 'action': self.action}
