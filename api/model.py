import datetime
import logging
import time
from datetime import timedelta

import requests


def get_optional_attribute(attributes, key, default_value=None):
    return attributes[key] if key in attributes else default_value


class User(object):
    def __init__(self, attributes):
        self.user_id = None
        self.name = None
        self.password_hash = None
        self.email_address = None
        self.is_admin = None
        self.faulty = None
        self.set_attributes(attributes)

    def set_attributes(self, attributes):
        self.user_id = attributes['_id']
        self.name = attributes['name']
        self.email_address = attributes['email_address']
        self.password_hash = attributes['password_hash']
        self.is_admin = attributes['is_admin']
        self.faulty = get_optional_attribute(attributes, 'faulty', False)

    def get_user_attributes(self, include_password_hash=False):
        data = {'user_id': self.user_id, 'name': self.name, 'faulty': self.faulty,
                'email_address': self.email_address, 'is_admin': self.is_admin}
        if include_password_hash:
            data['password_hash'] = self.password_hash
        return data

    def get_user_id(self):
        return self.user_id


class House(object):
    def __init__(self, attributes):
        self.house_id = None
        self.user_id = None
        self.name = None
        self.location = None
        self.set_attributes(attributes)

    def set_attributes(self, attributes):
        self.house_id = attributes['_id']
        self.user_id = attributes['user_id']
        self.name = attributes['name']
        self.location = get_optional_attribute(attributes, 'location', None)

    def get_house_attributes(self):
        return {'house_id': self.house_id, 'user_id': self.user_id, 'name': self.name, 'location': self.location}

    def get_house_id(self):
        return self.house_id


class Room(object):
    def __init__(self, attributes):
        self.room_id = None
        self.house_id = None
        self.name = None
        self.set_attributes(attributes)

    def set_attributes(self, attributes):
        self.room_id = attributes['_id']
        self.house_id = attributes['house_id']
        self.name = attributes['name']

    def get_room_attributes(self):
        return {'room_id': self.room_id, 'house_id': self.house_id, 'name': self.name}

    def get_room_id(self):
        return self.room_id


class Device(object):
    def __init__(self, attributes):
        self.device_id = None
        self.house_id = None
        self.room_id = None
        self.user_id = None
        self.name = None
        self.device_type = None
        self.vendor = None
        self.configuration = None
        self.locking_theme_id = None
        self.faulty = None
        self.target = {}
        self.status = {}
        self.set_attributes(attributes)

    def set_attributes(self, attributes):
        self.device_id = attributes['_id']
        self.house_id = attributes['house_id']
        self.user_id = attributes['user_id']
        self.room_id = attributes['room_id']
        self.name = attributes['name']
        self.device_type = attributes['device_type']
        self.locking_theme_id = get_optional_attribute(attributes, 'locking_theme_id', None)
        self.faulty = get_optional_attribute(attributes, 'faulty', False)
        self.target = get_optional_attribute(attributes, 'target', {})
        self.status = get_optional_attribute(attributes, 'status', {})
        self.vendor = get_optional_attribute(attributes, 'vendor', None)
        self.configuration = get_optional_attribute(attributes, 'configuration', None)

    def get_device_attributes(self):
        return {'device_id': self.device_id, 'house_id': self.house_id, 'room_id': self.room_id,
                'user_id': self.user_id, 'name': self.name, 'device_type': self.device_type,
                'locking_theme_id': self.locking_theme_id, 'faulty': self.faulty, 'target': self.target,
                'status': self.status, 'vendor': self.vendor, 'configuration': self.configuration}

    def get_device_id(self):
        return self.device_id

    def read_current_state(self, include_usage_data=0):
        error = None
        data = None
        timestamp = str(time.time())
        if self.vendor == "OWN":
            if "url" in self.configuration:
                url = self.configuration['url']
                try:
                    r = requests.get(url)
                    r_data = r.json()
                    logging.error("Data: {}".format(r_data))
                    if "error" in r_data and r_data["error"] is not None:
                        error = r_data["error"]
                    else:
                        data = {"power_state": r_data['data']['state']}
                except Exception as ex:
                    logging.error("Cannot read data from configuration URL: {}".format(ex))
                    error = "Cannot read data from configuration URL: {}".format(ex)
            else:
                error = "Can't read current state as no url is set in configuration"
        elif self.vendor == "energenie":
            if "username" in self.configuration and "password" in self.configuration and "device_id" in self.configuration:
                try:
                    username = self.configuration['username']
                    password = self.configuration['password']
                    dev_id = int(self.configuration['device_id'])
                    r = requests.get("https://mihome4u.co.uk/api/v1/subdevices/show", auth=(username, password),
                                     json={"id": dev_id, "include_usage_data": include_usage_data})
                    r_data = r.json()
                    if r_data["status"] != "success":
                        error = "External error: {}".format(r_data['status'])
                    else:
                        data = {'power_state': r_data['data']['power_state'], 'voltage': r_data['data']['voltage']}
                except Exception as ex:
                    error = "Cannot read device data from URL: {}".format(ex)
            else:
                error = "Not all required information is set in the configuration"
        else:
            error = "read_current_state not implemented for vendor {}".format(self.vendor)
        if error is not None:
            return {"error": error, "timestamp": timestamp}
        return {"data": data, "timestamp": timestamp}

    def get_energy_readings(self):
        error = None
        data = None
        if self.vendor == "energenie":
            if "username" in self.configuration and "password" in self.configuration and "device_id" in self.configuration:
                try:
                    username = self.configuration['username']
                    password = self.configuration['password']
                    dev_id = int(self.configuration['device_id'])
                    date_format = "%Y-%m-%dT%H:%M:%S.%f%Z"
                    json_data = {"id": dev_id,
                                 "data_type": "watts",
                                 "resolution": "daily",
                                 "start_time": ((datetime.datetime.now() - timedelta(days=7)).strftime(date_format)),
                                 "end_time": (datetime.datetime.now().strftime(date_format)),
                                 "limit": 7}
                    r = requests.get(
                        "https://mihome4u.co.uk/api/v1/subdevices/get_data",
                        auth=(username, password),
                        json=json_data
                    )
                    data = r.json()
                    if data['status'] != "success":
                        error = "External error: {}".format(data['status'])
                except Exception as ex:
                    error = "Cannot get energy reading: {}".format(ex)
            else:
                error = "Not all required information is set in the configuration"
        else:
            error = "get_energy_reading not implemented for vendor {}".format(self.vendor)
        if error is not None:
            return {"error": error}
        return {"data": data}

    def is_faulty(self):
        if "error" in self.status['last_read'] and self.status['last_read']['error'] is not None:
            self.faulty = True
        return self.faulty


class Thermostat(Device):
    def __init__(self, attributes):
        Device.__init__(self, attributes)

    def set_attributes(self, attributes):
        Device.set_attributes(self, attributes=attributes)
        self.temperature_scale = get_optional_attribute(attributes, 'temperature_scale')

    def get_device_attributes(self):
        attributes = Device.get_device_attributes(self)
        attributes.update({'temperature_scale': self.temperature_scale})
        return attributes

    def configure_target_temperature(self, temperature):
        error = None
        data = None
        timestamp = str(time.time())
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
        elif self.vendor == "energenie":
            if "username" in self.configuration and "password" in self.configuration and "device_id" in self.configuration:
                try:
                    username = self.configuration['username']
                    password = self.configuration['password']
                    dev_id = int(self.configuration['device_id'])
                    r = requests.get("https://mihome4u.co.uk/api/v1/subdevices/set_target_temperature",
                                     auth=(username, password),
                                     json={"id": dev_id, "temperature": temperature})
                    r_data = r.json()
                    if r_data["status"] != "success":
                        error = "External error: {}".format(r_data['status'])
                    else:
                        data = {'target_temperature': r_data['data']['target_temperature'],
                                'voltage': r_data['data']['voltage']}
                except Exception as ex:
                    error = "Cannot read device data from URL: {}".format(ex)
            else:
                error = "Not all required information is set in the configuration"
        else:
            error = "configure_target_temperature not implemented for vendor {}".format(self.vendor)
        return {"error": error, "data": data, "timestamp": timestamp}


class MotionSensor(Device):
    def __init__(self, attributes):
        Device.__init__(self, attributes)

    def set_attributes(self, attributes):
        Device.set_attributes(self, attributes=attributes)

    def get_device_attributes(self):
        attributes = Device.get_device_attributes(self)
        return attributes


class LightSwitch(Device):
    def __init__(self, attributes):
        Device.__init__(self, attributes)

    def set_attributes(self, attributes):
        Device.set_attributes(self, attributes=attributes)

    def get_device_attributes(self):
        attributes = Device.get_device_attributes(self)
        return attributes

    def configure_power_state(self, power_state):
        error = None
        if self.vendor == "energenie":
            if "username" in self.configuration and "password" in self.configuration and "device_id" in self.configuration:
                try:
                    username = self.configuration['username']
                    password = self.configuration['password']
                    dev_id = int(self.configuration['device_id'])
                    r = requests.get(
                        "https://mihome4u.co.uk/api/v1/subdevices/power_{}".format("on" if power_state == 1 else "off"),
                        auth=(username, password),
                        json={"id": dev_id})
                    r_data = r.json()
                    if r_data["status"] != "success":
                        error = "External error: {}".format(r_data['status'])
                except Exception as ex:
                    error = "Cannot configure power state: {}".format(ex)
            else:
                error = "Not all required information is set in the configuration"
        elif self.vendor == "OWN":
            if "url" in self.configuration:
                try:
                    r = requests.post(self.configuration["url"] + "/write", json={
                        "power_state": power_state == 1
                    })
                    r_data = r.json()
                    if r_data["error"] is not None:
                        error = "External error: {}".format(r_data["error"])
                except Exception as ex:
                    error = "Cannot configure power state: {}".format(ex)
            else:
                error = "Not all required information is set in the configuration"
        else:
            error = "configure_power_state not implemented for vendor {}".format(self.vendor)
        return error


class OpenSensor(Device):
    def __init__(self, attributes):
        Device.__init__(self, attributes)

    def set_attributes(self, attributes):
        Device.set_attributes(self, attributes=attributes)

    def get_device_attributes(self):
        attributes = Device.get_device_attributes(self)
        return attributes


class Trigger:
    def __init__(self, attributes):
        self.trigger_id = None
        self.sensor_id = None
        self.event = None
        self.event_params = None
        self.actor_id = None
        self.action = None
        self.action_params = None
        self.user_id = None
        self.reading = None
        self.set_attributes(attributes)

    def set_attributes(self, attributes):
        self.trigger_id = attributes['_id']
        self.sensor_id = attributes['sensor_id']
        self.event = attributes['event']
        self.event_params = attributes['event_params']
        self.actor_id = attributes['actor_id']
        self.action = attributes['action']
        self.action_params = attributes['action_params']
        self.user_id = attributes['user_id']
        self.reading = attributes['reading']

    def get_trigger_attributes(self):
        return {'trigger_id': self.trigger_id, 'sensor_id': self.sensor_id,
                'event': self.event, 'event_params': self.event_params, 'actor_id': self.actor_id,
                'action': self.action, 'action_params': self.action_params, 'user_id': self.user_id,
                'reading': self.reading}


class Theme:
    def __init__(self, attributes):
        self.theme_id = None
        self.name = None
        self.user_id = None
        self.settings = []
        self.active = False
        self.set_attributes(attributes)

    def set_attributes(self, attributes):
        self.theme_id = attributes['_id']
        self.name = attributes['name']
        self.user_id = attributes['user_id']
        self.settings = attributes['settings']
        self.active = attributes['active']

    def get_theme_attributes(self):
        return {'theme_id': self.theme_id, 'name': self.name,
                'user_id': self.user_id, 'settings': self.settings, 'active': self.active}


class Token:
    def __init__(self, attributes):
        self.token_id = None
        self.user_id = None
        self.token = None
        self.set_attributes(attributes)

    def set_attributes(self, attributes):
        self.token_id = attributes['_id']
        self.user_id = attributes['user_id']
        self.token = attributes['token']

    def get_token_attributes(self):
        return {'_id': self.token_id, 'user_id': self.user_id, 'key': self.token}
